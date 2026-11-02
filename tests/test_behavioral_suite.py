"""Integrity tests for the behavioral suite (tests/behavioral).

These do NOT execute any skill. They check that the suite is complete and honest:
every skill has the four scenario kinds, fixtures are synthetic, saved runs are graded,
and a PASS never records a failed criterion. They also unit-test the harness's screening logic.
"""
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "behavioral"))
import validate_skills as v  # noqa: E402
import harness as h  # noqa: E402

BEH = Path(__file__).resolve().parent / "behavioral"
REQUIRED_KEYS = {"id", "skill", "category", "title", "fixtures", "prompt", "expect", "critical",
                 "noncritical", "must_match", "must_not_match", "trap_tokens", "failure_modes"}


class SuiteIntegrity(unittest.TestCase):
    def setUp(self) -> None:
        self.scns = h.load_scenarios()

    def test_every_skill_has_four_kinds(self) -> None:
        by: dict[str, set[str]] = {}
        for s in self.scns:
            by.setdefault(s["skill"], set()).add(s["category"])
        self.assertEqual(set(by), v.EXPECTED)
        for skill, cats in by.items():
            self.assertEqual(cats, set(h.CATEGORIES), skill)

    def test_ids_unique_and_well_formed(self) -> None:
        ids = [s["id"] for s in self.scns]
        self.assertEqual(len(ids), len(set(ids)))
        for s in self.scns:
            self.assertRegex(s["id"], r"^[A-Z]{2}-[NMEX][0-9]+$")
            self.assertEqual(s["id"].split("-")[1][0], {"normal": "N", "missing": "M", "evidence": "E", "edge": "X"}[s["category"]])

    def test_fields_and_references(self) -> None:
        for s in self.scns:
            self.assertTrue(REQUIRED_KEYS <= set(s), s["id"])
            self.assertIn(s["expect"], h.EXPECTS, s["id"])
            self.assertTrue(s["prompt"].strip() and s["critical"], s["id"])
            for rx in s["must_match"] + s["must_not_match"]:
                re.compile(rx)
            for d in s["fixtures"]:
                self.assertTrue((h.FIXTURES / d).is_dir(), f"{s['id']}: fixture {d}")

    def test_generated_docs_list_every_scenario(self) -> None:
        matrix = (BEH / "MATRIX.md").read_text(encoding="utf-8")
        for s in self.scns:
            self.assertIn(s["id"], matrix)
            doc = (BEH / "scenarios" / f"{s['skill']}.md").read_text(encoding="utf-8")
            self.assertIn(f"## {s['id']}:", doc)
            for crit in s["critical"]:
                self.assertIn(crit, doc, f"{s['id']} docs stale: run harness.py docs")

    def test_fixtures_are_synthetic(self) -> None:
        self.assertIn("SYNTHETIC", (h.FIXTURES / "_base" / "README.md").read_text(encoding="utf-8"))
        for p in h.FIXTURES.rglob("*"):
            if p.is_file() and h.is_text(p):
                for email in re.findall(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", p.read_text(encoding="utf-8")):
                    self.assertTrue(email.endswith("@example.test"), f"{p}: non-synthetic email {email}")

    def test_saved_runs_are_graded_and_consistent(self) -> None:
        for d in sorted(h.RUNS.glob("*/attempt-*")):
            ev = d / "EVAL.md"
            self.assertTrue(ev.is_file(), f"{d} has no EVAL.md (ungraded run)")
            text = ev.read_text(encoding="utf-8")
            m = re.search(r"^Status:\s*(PASS|FAIL|BLOCKED)\s*$", text, re.M)
            self.assertIsNotNone(m, f"{ev}: missing Status line")
            if m.group(1) == "PASS":
                self.assertNotIn("- [F]", text, f"{ev}: PASS with a failed criterion")
            if m.group(1) == "FAIL":
                self.assertIn("- [F]", text, f"{ev}: FAIL without a failed criterion")
            self.assertTrue((d / "RESPONSE.md").is_file() or m.group(1) == "BLOCKED", f"{d}: no RESPONSE.md")


class RunIntegrity(unittest.TestCase):
    """Duplicate or unlabeled attempts must not be able to distort the counts."""

    def test_collect_never_overwrites_a_stored_attempt(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            saved_runs = h.RUNS
            h.RUNS = tmp_path / "runs"
            try:
                sandbox, manifest = tmp_path / "sb", tmp_path / "man.json"
                h.prepare("UA-M1", sandbox, manifest)
                (sandbox / "RESPONSE.md").write_text("reply\n", encoding="utf-8")
                (sandbox / "HARNESS.md").write_text("harness\n", encoding="utf-8")
                stored = h.RUNS / "UA-M1" / "attempt-1"
                stored.mkdir(parents=True)
                (stored / "EVAL.md").write_text("Status: PASS\n", encoding="utf-8")
                self.assertIsNone(h.collect("UA-M1", sandbox, manifest, 1, "2000-01-01"))
                self.assertEqual((stored / "EVAL.md").read_text(encoding="utf-8"), "Status: PASS\n")
            finally:
                h.RUNS = saved_runs

    def test_every_attempt_has_metadata_and_a_unique_fingerprint(self) -> None:
        import json as _json
        for sid_dir in sorted(h.RUNS.glob("*")):
            seen: dict[str, str] = {}
            for d in sorted(sid_dir.glob("attempt-*")):
                mp = d / "META.json"
                self.assertTrue(mp.is_file(), f"{d} has no META.json")
                meta = _json.loads(mp.read_text(encoding="utf-8"))
                for key in ("scenario", "attempt", "fingerprint", "standard_sha", "skill_sha", "source"):
                    self.assertIn(key, meta, f"{mp}: missing {key}")
                self.assertNotIn(meta["fingerprint"], seen, f"{d} duplicates {seen.get(meta['fingerprint'])}")
                seen[meta["fingerprint"]] = d.name

    def test_fingerprint_depends_on_content(self) -> None:
        self.assertEqual(h.fingerprint({"a": "1", "b": "2"}), h.fingerprint({"b": "2", "a": "1"}))
        self.assertNotEqual(h.fingerprint({"a": "1"}), h.fingerprint({"a": "2"}))


class HarnessScreening(unittest.TestCase):
    def check(self, scn_id: str, texts: dict, response: str = "ok", violations=None, run_date: str = "2026-01-01"):
        return {r["id"]: r["status"] for r in
                h.run_checks(h.get(scn_id), texts, violations or [], response, run_date)}

    def test_stop_scenario_fails_when_a_deliverable_is_written(self) -> None:
        res = self.check("PD-M1", {"design/discovery/product-discovery-x-2026-01-01.md": "> skill: product-discovery \n"})
        self.assertEqual(res["A1"], "FAIL")

    def test_stop_scenario_passes_without_deliverable(self) -> None:
        res = self.check("PD-M1", {})
        self.assertEqual(res["A1"], "PASS")

    def test_planted_identifier_is_flagged(self) -> None:
        res = self.check("PB-N1", {}, response="Persona based on Marisol Quenby")
        self.assertEqual(res["A9"], "FAIL")

    # Regression screens for the open failures. They detect the defect in saved output;
    # they cannot make a model avoid it.
    def test_age_descriptor_is_flagged(self) -> None:
        # PF-N1 attempt 7: "older" sat beside P3, whose note records an age.
        res = self.check("PF-N1", {}, response="whether older or less app-confident users are affected is [assumption]")
        self.assertEqual(res.get("A17"), "REVIEW")
        self.assertNotIn("A17", self.check("PF-N1", {}, response="whether less app-confident users are affected"))

    def test_evidence_age_must_match_its_date(self) -> None:
        # RP-M1 attempt 4: 642 days given where the dates give 643.
        bad = self.check("RP-M1", {}, response="last week 2025-01-27 (642 days old)", run_date="2026-11-01")
        self.assertEqual(bad["A18"], "FAIL")
        ok = self.check("RP-M1", {}, response="last week 2025-01-27 (643 days old)", run_date="2026-11-01")
        self.assertEqual(ok["A18"], "PASS")
        # the a4 table form: range of dates beside a range of ages
        table = self.check("RP-M1", {}, response="| export | weeks 2025-01-06 to 2025-01-27 | 664 to 642 |", run_date="2026-11-01")
        self.assertEqual(table["A18"], "FAIL")
        # PF-N1 attempt 8 form: age before its date, all correct; must not pair across clauses
        order = self.check("PF-N1", {}, response="against 2026-11-02): tickets 665 days (2025-01-06) to 637 days (2025-02-03) old",
                           run_date="2026-11-02")
        self.assertEqual(order["A18"], "PASS")

    def test_could_not_find_count_with_weaker_ticket_is_flagged(self) -> None:
        # CS-E1 attempt 5 and PF-N1 attempt 6: T-04 says "Looking for the code", not that it could not be found.
        bad = self.check("CS-E1", {}, response="4 tickets (T-01, T-04, T-09, T-12) say the code could not be found or seen")
        self.assertEqual(bad["A19"], "REVIEW")
        ok = self.check("CS-E1", {}, response="Could not find the code: T-01, T-12. Weaker: T-04, T-09.")
        self.assertEqual(ok["A19"], "PASS")

    def test_attributed_quote_must_be_verbatim_in_its_source(self) -> None:
        # PF-N1 attempt 9 merged ticket subjects; JM-N1 attempt 5 gave P4's words to P1.
        merged = self.check("PF-N1", {}, response='Tickets "where is my/the code" (T-01, T-04)')
        self.assertEqual(merged["A20"], "FAIL")
        wrong_person = self.check("JM-N1", {}, response='P1 "felt silly" about asking support')
        self.assertEqual(wrong_person["A20"], "FAIL")
        # UF-N1 attempt 5: one quote credited to two tickets, only one of which has those words
        shared = self.check("UF-N1", {}, response='T2 cites T-01, T-12 "Cannot find pickup code"')
        self.assertEqual(shared["A20"], "FAIL")
        ok = self.check("JM-N1", {}, response='P4 said "I felt silly" | T-05 "Arrived and the point was closed"')
        self.assertEqual(ok["A20"], "PASS")
        self.assertNotIn("A20", self.check("JM-N1", {}, response='Task: "Find your pickup code"'))

    def test_near_verbatim_unattributed_quote_is_flagged(self) -> None:
        # PF-N1 attempts 2 to 6: "where is my parcel" / "where is my stuff" for "where their stuff is".
        res = self.check("PF-N1", {}, response='Stakeholder framing: "people keep asking where my stuff is"')
        self.assertEqual(res.get("A21"), "REVIEW")

    def test_count_line_matches_its_members(self) -> None:
        # CS-E1 attempt 7: "3 more people" where P1 was already in the strict count.
        ok = self.check("CS-E1", {}, response="- Could not find the code: 3 people — P1, P3, T-12\n"
                                              "- Weaker statements, not counted above: 2 people — T-04, P4")
        self.assertEqual(ok["A22"], "PASS")
        repeat = self.check("CS-E1", {}, response="- Could not find the code: 3 people — P1, P3, T-12\n"
                                                  "- Weaker statements: 3 more people — T-04, P4, P1")
        self.assertEqual(repeat["A22"], "FAIL")
        same_person = self.check("CS-E1", {}, response="- Could not find the code: 3 people — P1, T-01, P3")
        self.assertEqual(same_person["A22"], "FAIL")
        weak_member = self.check("CS-E1", {}, response="- Could not find the code: 4 people — P1, P3, T-12, T-04")
        self.assertEqual(weak_member["A22"], "FAIL")
        # CS-E1 attempt 10: the same slip with trailing evidence tags, which the first pattern missed
        tagged = self.check("CS-E1", {}, response="Could not find the pickup code: 3 people — P3, T-01, T-12 [observed]\n"
                                                  "Weaker statements (looking for, lost it): 3 people — T-04, P1, P4 [observed]")
        self.assertEqual(tagged["A22"], "FAIL")

    def test_unexpected_date_is_flagged_and_run_date_allowed(self) -> None:
        bad = self.check("PB-N1", {}, response="Interviewed on 2031-05-05")
        self.assertEqual(bad["A8"], "FAIL")
        ok = self.check("PB-N1", {}, response="Written on 2026-01-01")
        self.assertEqual(ok["A8"], "PASS")

    def test_unsupported_figure_is_flagged_for_review(self) -> None:
        res = self.check("PB-N1", {}, response="Conversion rose 37% last month")
        self.assertEqual(res["A10"], "REVIEW")

    def test_input_modification_fails_write_discipline(self) -> None:
        res = self.check("PB-N1", {}, violations=["modified README.md"])
        self.assertEqual(res["A2"], "FAIL")

    def test_mermaid_balance(self) -> None:
        self.assertTrue(h.mermaid_balanced("```mermaid\nA[x] --> B{y}\n```"))
        self.assertFalse(h.mermaid_balanced("```mermaid\nA[x --> B{y}\n```"))
        self.assertIsNone(h.mermaid_balanced("no diagram"))


if __name__ == "__main__":
    unittest.main()
