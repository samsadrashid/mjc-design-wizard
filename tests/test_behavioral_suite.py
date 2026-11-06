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

    def test_adapter_manifest_update_is_allowed_but_other_input_edits_are_not(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            saved_runs = h.RUNS
            h.RUNS = tmp_path / "runs"
            try:
                sandbox, manifest = tmp_path / "sb", tmp_path / "man.json"
                h.prepare("UA-M1", sandbox, manifest)
                (sandbox / "design").mkdir(exist_ok=True)
                (sandbox / "design" / "figma.json").write_text('{"schema_version": 1, "artifacts": {}}', encoding="utf-8")
                manifest.write_text(json.dumps(h.file_hashes(sandbox)), encoding="utf-8")
                (sandbox / "design" / "figma.json").write_text('{"schema_version": 1, "artifacts": {"a/b": {}}}', encoding="utf-8")
                (sandbox / "RESPONSE.md").write_text("reply\n", encoding="utf-8")
                (sandbox / "HARNESS.md").write_text("harness\n", encoding="utf-8")
                dest = h.collect("UA-M1", sandbox, manifest, 1, "2000-01-01")
                auto = json.loads((dest / "AUTO.json").read_text(encoding="utf-8"))["checks"]
                self.assertEqual({c["id"]: c["status"] for c in auto}["A2"], "PASS")
                self.assertTrue((dest / "output" / "design" / "figma.json").is_file())
                # a broken manifest, or any other modified input, is still a violation
                (sandbox / "design" / "figma.json").write_text("{not json", encoding="utf-8")
                (sandbox / "RESPONSE.md").write_text("another reply\n", encoding="utf-8")  # a different fingerprint
                dest2 = h.collect("UA-M1", sandbox, manifest, 2, "2000-01-01")
                auto2 = json.loads((dest2 / "AUTO.json").read_text(encoding="utf-8"))["checks"]
                self.assertEqual({c["id"]: c["status"] for c in auto2}["A2"], "FAIL")
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


class QualityMatrix(unittest.TestCase):
    STATUSES = {"PASS", "FAIL", "PARTIAL", "NOT TESTED", "BLOCKED"}

    def rows(self) -> dict[str, list[str]]:
        text = (BEH / "QUALITY.md").read_text(encoding="utf-8")
        out = {}
        for ln in text.splitlines():
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) == 8 and cells[0] not in ("Skill", "---") and not cells[0].startswith("-"):
                out[cells[0]] = cells[1:]
        return out

    def test_every_skill_has_seven_dimensions_with_valid_statuses(self) -> None:
        rows = self.rows()
        self.assertEqual(len(rows), 19)
        for skill, cells in rows.items():
            self.assertTrue(set(cells) <= self.STATUSES, f"{skill}: {cells}")

    def test_not_tested_is_never_reported_as_pass(self) -> None:
        figma = json.loads((BEH / "figma_results.json").read_text(encoding="utf-8"))
        for skill, cells in self.rows().items():
            structural, behavioral, evidence, completeness, deliverable, fig, regression = cells
            if fig == "PASS":
                self.assertEqual(figma.get(skill, {}).get("status"), "PASS", skill)
            if skill not in figma:
                self.assertEqual((deliverable, fig), ("NOT TESTED", "NOT TESTED"), skill)
            if behavioral == "PASS":
                self.assertTrue(evidence == completeness == "PASS", f"{skill}: behavioral PASS needs evidence and completeness PASS")


class HarnessScreening(unittest.TestCase):
    def check(self, scn_id: str, texts: dict, response: str = "ok", violations=None, run_date: str = "2026-01-01"):
        return {r["id"]: r["status"] for r in
                h.run_checks(h.get(scn_id), texts, violations or [], response, run_date)}

    def check_h(self, scn_id: str, harness_text: str):
        return {r["id"]: r["status"] for r in
                h.run_checks(h.get(scn_id), {}, [], "ok", "2026-01-01", harness_text)}

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

    def test_stakeholder_quote_once_and_reading_line_unquoted(self) -> None:
        # PF-N1 attempt 14: the sentence repeated in Open questions and a quoted word in `Our reading:`; attempt 15: repeated in two sections.
        q = "People keep asking where their stuff is."
        once = "> skill: problem-framing\nStakeholder said: \"%s\" (docs/stakeholder-request.md)\nOur reading: they want parcel status.\n" % q
        ok = self.check("PF-N1", {"design/discovery/pf-x.md": once}, response="done")
        self.assertEqual(ok["A23"], "PASS")
        self.assertEqual(ok["A24"], "PASS")
        twice = once + "Does the stakeholder have data behind \"%s\"?\n" % q
        self.assertEqual(self.check("PF-N1", {"design/discovery/pf-x.md": twice}, response="done")["A23"], "FAIL")
        quoted = once.replace("parcel status", "kept out of the \"because\" clause")
        self.assertEqual(self.check("PF-N1", {"design/discovery/pf-x.md": quoted}, response="done")["A24"], "FAIL")

    def _case_study(self, claim: str, audience: str = "Audience: hiring reader (assumed)") -> tuple[dict, int]:
        body = " ".join(["word"] * 100)
        text = ("> skill: case-study-writer · date: 2026-01-01 · scope: x · sources: none\n\n## Summary\n" + body +
                "\n## Context and role\n" + audience + "\n" + body + "\n## Lessons\n" + body +
                "\n## Visuals to include\nnone\n")
        actual = len(re.search(r"^## Summary\b.*?(?=^## Visuals to include\b)", text, re.S | re.M).group(0).split())
        return {"design/docs/case-study-x-2026-01-01.md": text.replace("sources: none", "sources: none " + claim.format(n=actual))}, actual

    def test_case_study_audience_and_exact_body_word_count(self) -> None:
        # CS-E1 attempt 11 (claimed 600, body 810) and attempt 14 (claimed 974, body 970): the stated count must equal the defined body
        docs, n = self._case_study("Word count: {n}")
        res = self.check("CS-E1", docs)
        self.assertEqual((res["A25"], res["A26"]), ("PASS", "PASS"))
        off, n = self._case_study("Word count: %d" % 0)
        off = {k: v.replace("Word count: 0", "Word count: %d" % (n + 4)) for k, v in off.items()}
        self.assertEqual(self.check("CS-E1", off)["A25"], "FAIL")
        self.assertEqual(self.check("CS-E1", self._case_study("body about 600 words")[0])["A25"], "FAIL")
        # the 800 to 1200 default range is not a count of this body
        self.assertNotIn("A25", self.check("CS-E1", self._case_study("under the 800 to 1200 words default")[0]))
        # a count claimed only in the chat reply is checked too
        docs, n = self._case_study("")
        self.assertEqual(self.check("CS-E1", docs, response="The body is %d words." % (n + 30))["A25"], "FAIL")
        self.assertEqual(self.check("CS-E1", self._case_study("", audience="Role: lead designer")[0])["A26"], "FAIL")

    def test_closing_signature_present_last_and_after_figma_line(self) -> None:
        # PF-N1 attempt 17 ended on a heading with no emoticon
        ok = self.check("PF-N1", {}, response="Saved the framing.\n\n-_-\n")
        self.assertEqual(ok["A27"], "PASS")
        figma = self.check("PF-N1", {}, response="Saved.\nFigma: not used (publishing disabled)\n\n._.\n")
        self.assertEqual(figma["A27"], "PASS")
        self.assertEqual(self.check("PF-N1", {}, response="Saved the framing.\n\n## Next step\nux-research-planner")["A27"], "FAIL")
        self.assertEqual(self.check("PF-N1", {}, response="Saved.\n\n-_-\nFigma: not used (publishing disabled)")["A27"], "FAIL")
        self.assertEqual(self.check("PF-N1", {}, response="Saved. -_-\nNext step: x")["A27"], "FAIL")
        self.assertEqual(self.check("PF-N1", {}, response="Saved.\n-_-")["A27"], "FAIL")
        # the signature is the only emoticon in the reply
        self.assertEqual(self.check("PF-N1", {}, response="-_- start\n\n-_-")["A27"], "FAIL")

    def test_false_claim_that_shared_files_are_absent(self) -> None:
        # PF-N1 attempt 17 HARNESS.md: "neither is in the project" (the harness installs _shared/ in every sandbox)
        h = "- The skill cites ../_shared/personality.md and ../_shared/figma.md; neither is in the project, so they were not consulted."
        self.assertEqual(self.check_h("PF-N1", h)["A28"], "FAIL")
        self.assertNotIn("A28", self.check_h("PF-N1", "Read personality.md for the closing signature."))
        self.assertNotIn("A28", self.check_h("PF-N1", ""))

    def test_causal_wording_tagged_observed_is_flagged(self) -> None:
        # PF-N1 attempt 16: "without it they cannot collect", tagged observed, with no source stating the cause
        bad = {"design/discovery/p.md": "People need the code, and without it they cannot collect [observed: README.md]\n"}
        self.assertEqual(self.check("PF-N1", bad)["A29"], "REVIEW")
        inferred = {"design/discovery/p.md": "People need the code, and without it they may not collect [inferred: no file states why]\n"}
        self.assertNotIn("A29", self.check("PF-N1", inferred))

    def test_fact_credited_to_the_wrong_source_file(self) -> None:
        # PF-N1 attempt 17: "the roadmap says v1.4 is live" (that fact is in README.md)
        wrong = {"design/discovery/p.md": "Context: the roadmap says v1.4 is live, so the screen is shipped.\n"}
        self.assertEqual(self.check("PF-N1", wrong)["A30"], "FAIL")
        right = {"design/discovery/p.md": "Context: the README says v1.4 is live, so the screen is shipped.\n"}
        self.assertNotIn("A30", self.check("PF-N1", right))

    def test_theme_membership_needs_the_id_to_state_the_theme(self) -> None:
        # CS-E1 attempts 14 and 15, CS-N1 attempt 5: T-05 ("Arrived and the point was closed") filed under late alerts
        for line in ("Late alerts also appear (P1, T-02, T-05, T-08) [Verified].",
                     "Two missed pickups were tied to late alerts, a separate problem [observed: P1, T-02, T-05, T-08].",
                     "A separate pattern, alerts arriving after the pickup point closed, appears in P1, T-02, T-05, and T-08."):
            self.assertEqual(self.check("CS-E1", {"design/docs/c.md": line + "\n"})["A31"], "FAIL", line)
        ok = self.check("CS-E1", {"design/docs/c.md": "Late alerts (T-02, T-08) and saved pickup point (T-03, T-06).\nT-05 states no alert and is not counted.\n"})
        self.assertNotIn("A31", ok)

    def test_shared_instructions_are_available_in_a_fresh_sandbox(self) -> None:
        # Round 3: two replies lacked the closing emoticon because executors were told to read standard.md and nothing else.
        import tempfile
        std = (h.REPO / ".claude" / "skills" / "_shared" / "standard.md").read_text(encoding="utf-8")
        sec = std.split("## 1. Shared files to load", 1)[1].split("## 2.", 1)[0]
        self.assertIn("personality.md", sec)
        self.assertIn("figma.md", sec)
        self.assertRegex(sec, r"personality\.md`: always")
        self.assertRegex(sec, r"figma\.md`: only when")
        for sid in ("PF-N1", "CS-N1", "DQ-M1"):  # three different skills
            with tempfile.TemporaryDirectory() as tmp:
                out = Path(tmp) / "sbx"
                h.prepare(sid, out, Path(tmp) / "manifest.json")
                shared = out / ".claude" / "skills" / "_shared"
                for name in ("standard.md", "personality.md", "figma.md"):
                    self.assertTrue((shared / name).is_file(), f"{sid}: {name} missing from the sandbox")
                self.assertEqual((shared / "personality.md").read_text(encoding="utf-8"),
                                 (h.REPO / ".claude" / "skills" / "_shared" / "personality.md").read_text(encoding="utf-8"))
                prompt = h.exec_prompt(sid, out)
                self.assertIn("section 1", prompt)
                self.assertIn("personality.md always", prompt)
                self.assertNotIn("Do not read any other file than standard.md", prompt)
                self.assertIn("shared files you read", prompt)
                skill = (h.REPO / ".claude" / "skills" / h.get(sid)["skill"] / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("../_shared/standard.md", skill)  # the skill points at the file that names the others

    def test_every_skill_cites_personality_without_repeating_it(self) -> None:
        for d in sorted((h.REPO / ".claude" / "skills").iterdir()):
            f = d / "SKILL.md"
            if f.is_file():
                text = f.read_text(encoding="utf-8")
                self.assertIn("../_shared/personality.md", text, d.name)
                self.assertNotIn("Closing signature", text, d.name)  # the rule lives in personality.md only

    def test_more_than_one_question_in_the_reply(self) -> None:
        # CS-E1 attempt 19 (four questions), CS-N1 attempt 6 (three), CS-E1 attempt 3 ("one question" with a second ask)
        four = "Saved.\n\nOpen questions:\n- Where do the 30% and \"half\" come from?\n- Who else contributed?\n- Is design/ gitignored?\n\n-_-\n"
        self.assertEqual(self.check("CS-E1", {}, response=four)["A33"], "FAIL")
        self.assertEqual(self.check("PF-N1", {}, response=four)["A33"], "FAIL")
        compound = "Saved.\n\nOne question: what is the source? Also, who else worked on this?\n\n-_-\n"
        self.assertEqual(self.check("CS-E1", {}, response=compound)["A33"], "FAIL")
        one = "Saved. The unknowns are listed in the file.\n\nWho else worked on this?\n\n-_-\n"
        self.assertNotIn("A33", self.check("CS-E1", {}, response=one))
        # quoted source text and HMW questions the skill shows are not asks
        hmw = "Chosen: How might we show the code first?\nThe ticket says \"Where is it?\" and `why?`.\n\nWho else worked on this?\n\n-_-\n"
        self.assertNotIn("A33", self.check("PF-N1", {}, response=hmw))
        # other skills: a warning for review, not a hard failure
        self.assertEqual(self.check("UA-N1", {}, response=four)["A33"], "REVIEW")

    def test_two_requests_joined_by_and_are_two_questions(self) -> None:
        # CS-N1 attempts 15 and 16: "One question: which artifacts did you author, and what prompted the rework?"
        two = "Saved.\n\nOne question: which artifacts did you author, and what prompted the rework?\n\n-_-\n"
        self.assertEqual(self.check("CS-N1", {}, response=two)["A33"], "FAIL")
        aux = "Saved.\n\nWho said everyone hates the green banner, and was that users or the team?\n\n-_-\n"
        self.assertEqual(self.check("CS-N1", {}, response=aux)["A33"], "FAIL")  # DC-E1 attempt 4
        one = "Saved.\n\nWhich artifacts did you author?\n\n-_-\n"
        self.assertNotIn("A33", self.check("CS-N1", {}, response=one))

    def test_p1_interview_does_not_support_could_not_find_but_t01_does(self) -> None:
        # CS-N1 attempt 6 listed P1 (interview: found it after scrolling); T-01 is the ticket that says it
        bad = "Could not find the code: 3 people: P1, P3, T-12\n"
        self.assertEqual(self.check("CS-N1", {"design/docs/c.md": bad})["A32"], "FAIL")
        good = "Could not find the code: 3 people: T-01, P3, T-12 (T-01 is the same person as P1)\n"
        self.assertNotIn("A32", self.check("CS-N1", {"design/docs/c.md": good}))
        dash = "- Could not find the code: 3 people \u2014 P1, T-12, P3\n"
        self.assertEqual(self.check("CS-N1", {"design/docs/c.md": dash})["A32"], "FAIL")
        # a participant's ticket mapped to the wrong source kind: T-04 only says "looking for", so it is not a strict member
        wrong = "Could not find the code: 3 people: T-01, T-04, P3\n"
        self.assertEqual(self.check("CS-N1", {"design/docs/c.md": wrong})["A32"], "FAIL")
        # the weaker line may hold people who looked for it, and its label is not a strict line
        weaker = "Looking for the code or lost it, not stating they could not find it: 2 people - T-04, P4\n"
        self.assertNotIn("A32", self.check("CS-N1", {"design/docs/c.md": weaker}))

    def test_t05_stays_unclear_and_participant_attribution(self) -> None:
        unclear = "Late alerts (P1, T-02) and saved points (T-03, T-06).\nUnclear: T-05 (\"Arrived and the point was closed\") states a closed point, no alert.\n"
        self.assertNotIn("A31", self.check("CS-E1", {"design/docs/c.md": unclear}))
        # an interview quote credited to another person's interview is an attribution failure
        wrong = "P3 said \"Found the pickup code only after scrolling past two cards\".\n"
        self.assertEqual(self.check("CS-E1", {"design/docs/c.md": wrong})["A20"], "FAIL")

    def test_problem_statement_consequence_needs_its_own_tag(self) -> None:
        # PF-N1 attempt 21: "which causes contact with support and workarounds such as screenshots" with no class tag
        bare = "Recipients need the code because they report not finding it. Today the code is hard to locate, which causes contact with support and workarounds such as screenshots.\n"
        self.assertEqual(self.check("PF-N1", {"design/discovery/problem-framing-x-2026-11-03.md": bare})["A34"], "FAIL")
        tagged = bare.replace("screenshots.", "screenshots [inferred: P4 and P1 describe these; no file says the code is the cause].")
        self.assertNotIn("A34", self.check("PF-N1", {"design/discovery/problem-framing-x-2026-11-03.md": tagged}))
        unknown = "Today the code is hard to locate, which causes [no consequence is documented in any source].\n"
        self.assertNotIn("A34", self.check("PF-N1", {"design/discovery/problem-framing-x-2026-11-03.md": unknown}))

    def test_observed_claim_whose_citation_does_not_state_it(self) -> None:
        # PF-N1 attempt 21: "[observed] ... need the pickup code at the point of collection (T-01, T-12, P3)" (no file states the need)
        unsupported = "- `[observed]` Warehouse operators schedule overnight replenishment shipments across regional distribution centers (T-01, T-12)\n"
        res = self.check("PF-N1", {"design/discovery/problem-framing-x-2026-11-03.md": unsupported})
        self.assertEqual(res["A35"], "REVIEW")
        supported = "- `[observed]` Cannot find the code on the parcel page, cannot find pickup code at all (T-01, T-12)\n"
        self.assertNotIn("A35", self.check("PF-N1", {"design/discovery/problem-framing-x-2026-11-03.md": supported}))

    def test_reason_for_the_work_tagged_observed_is_flagged(self) -> None:
        # CS-E1 attempts 20 and 21: "responded to people having trouble finding the code [observed]" while no artifact records the reason
        bad = "The work responded to people having trouble finding their pickup code [observed: CHANGELOG.md].\n"
        self.assertEqual(self.check("CS-E1", {"design/docs/c.md": bad})["A36"], "FAIL")
        self.assertEqual(self.check("CS-E1", {"design/docs/c.md": "The shipped changes address that problem `[observed: CHANGELOG.md, git log]`.\n"})["A36"], "FAIL")
        ok = "The reason for the rework is not recorded in any artifact [TO VERIFY]; it responded to the tickets only as a reading [inferred].\n"
        self.assertNotIn("A36", self.check("CS-E1", {"design/docs/c.md": ok}))
        self.assertNotIn("A36", self.check("CS-N1", {"design/docs/c.md": "Code moved above the fold in v1.4 [observed: CHANGELOG.md].\n"}))

    def test_replay_of_saved_round4_failures_and_passes(self) -> None:
        # real saved outputs (runs/ is gitignored; skipped on a clean checkout)
        def screens(sid: str, n: int) -> dict:
            base = BEH / "runs" / sid / f"attempt-{n}"
            if not (base / "AUTO.json").exists():
                self.skipTest(f"{sid} attempt {n} not saved")
            texts = {str(p.relative_to(base / "output")): p.read_text(encoding="utf-8") for p in (base / "output").rglob("*.md")
                     if str(p.relative_to(base / "output")).startswith("design/")}
            resp = (base / "RESPONSE.md").read_text(encoding="utf-8")
            rd = json.loads((base / "AUTO.json").read_text(encoding="utf-8"))["run_date"]
            return {x["id"]: x["status"] for x in h.run_checks(h.get(sid), texts, [], resp, rd, "")}
        self.assertEqual(screens("CS-E1", 20)["A36"], "FAIL")
        self.assertEqual(screens("CS-E1", 21)["A36"], "FAIL")
        self.assertNotIn("A36", screens("CS-E1", 22))
        self.assertEqual(screens("PF-N1", 24)["A32"], "FAIL")
        self.assertEqual(screens("CS-N1", 6)["A32"], "FAIL")
        self.assertEqual(screens("CS-E1", 19)["A33"], "FAIL")
        self.assertEqual(screens("CS-E1", 19)["A27"], "FAIL")
        for sid, n in (("CS-N1", 8), ("CS-N1", 9), ("PF-N1", 22), ("PF-E1", 6)):
            res = screens(sid, n)
            self.assertEqual({k for k, v in res.items() if v == "FAIL"} - {"A20"}, set(), f"{sid} {n}")

    def test_strict_member_used_as_a_weaker_example_through_another_id(self) -> None:
        # CS-E1 attempt 24, CS-N1 attempt 10: P1 (strict via T-01) shown as a weaker example
        bad = "Weaker statements, from people not in the strict count: T-04 and P4. Also: P1 (same person as T-01) \"Found the pickup code only after scrolling past two cards\" [observed].\n"
        self.assertEqual(self.check("CS-N1", {"design/docs/c.md": bad})["A37"], "FAIL")
        bad2 = "Others had weaker trouble: one found it only after scrolling past two cards (P1).\n"
        self.assertEqual(self.check("CS-N1", {"design/docs/c.md": bad2})["A37"], "FAIL")
        ok = "Weaker statements, from people not in the strict count: T-04 and P4. P1, also T-01, is already counted and is excluded here.\n"
        self.assertNotIn("A37", self.check("CS-N1", {"design/docs/c.md": ok}))
        self.assertNotIn("A37", self.check("CS-N1", {"design/docs/c.md": "Weaker statements: 2 people - T-04, P4\n"}))

    def test_superseded_evidence_table_row_is_not_a_weaker_example(self) -> None:
        row = "| E7b | research/interviews/P1.md | P1 | \"Found the pickup code only after scrolling past two cards.\" | weaker wording | superseded (counted in strict via T-01) |\n"
        self.assertNotIn("A37", self.check("CS-E1", {"design/docs/c.md": row}))
        bad = "Weaker statements: P1 found the pickup code only after scrolling past two cards.\n"
        self.assertEqual(self.check("CS-E1", {"design/docs/c.md": bad})["A37"], "FAIL")

    def test_information_architect_names_user_groups_and_counts_cover_the_whole_source(self) -> None:
        # IA-X1 attempt 3 named no user groups; DC-E1 attempt 3 counted 2 people from a partly read tickets file (fixtures hold 3)
        no = "> skill: information-architect\n## Scope and evidence base\nScope: Help section.\n"
        yes = no + "User groups: recipients who collect parcels [inferred]\n"
        self.assertEqual(self.check("IA-X1", {"design/architecture/information-architect-x-2026-11-03.md": no})["A38"], "FAIL")
        self.assertEqual(self.check("IA-X1", {"design/architecture/information-architect-x-2026-11-03.md": yes})["A38"], "PASS")
        short = "- could not find the code: 2 people \u2014 P3, T-01 (T-01 is the same person as P1)\n"
        self.assertEqual(self.check("DC-E1", {"design/audits/c.md": short})["A39"], "FAIL")
        full = "- could not find the code: 3 people \u2014 T-01, T-12, P3\n"
        self.assertNotIn("A39", self.check("DC-E1", {"design/audits/c.md": full}))
        lower = "- could not find the code: at least 2 people \u2014 P3, T-01 (only the first rows of the tickets file were read)\n"
        self.assertNotIn("A39", self.check("DC-E1", {"design/audits/c.md": lower}))

    def test_replay_of_second_round4_runs(self) -> None:
        def screens(sid: str, n: int) -> dict:
            base = BEH / "runs" / sid / f"attempt-{n}"
            if not (base / "AUTO.json").exists():
                self.skipTest(f"{sid} attempt {n} not saved")
            texts = {str(p.relative_to(base / "output")): p.read_text(encoding="utf-8") for p in (base / "output").rglob("*.md")
                     if str(p.relative_to(base / "output")).startswith("design/")}
            rd = json.loads((base / "AUTO.json").read_text(encoding="utf-8"))["run_date"]
            return {x["id"]: x["status"] for x in h.run_checks(h.get(sid), texts, [], (base / "RESPONSE.md").read_text(encoding="utf-8"), rd, "")}
        self.assertEqual(screens("CS-E1", 24)["A37"], "FAIL")
        self.assertEqual(screens("CS-N1", 10)["A37"], "FAIL")
        self.assertEqual(screens("PF-N1", 25)["A23"], "FAIL")
        for sid, n in (("CS-E1", 25), ("CS-N1", 11), ("CS-N1", 13)):
            self.assertNotIn("A37", screens(sid, n), f"{sid} {n}")

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
