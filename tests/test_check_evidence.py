"""Tests for .claude/skills/_shared/check_evidence.py, run against the synthetic Parcelo fixtures."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / ".claude" / "skills" / "_shared" / "check_evidence.py"
PROJECT = REPO / "tests" / "behavioral" / "fixtures" / "_base"


class CheckEvidence(unittest.TestCase):
    def run_check(self, doc: str, reply: str | None = None) -> tuple[int, str]:
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "doc.md"
            d.write_text(doc, encoding="utf-8")
            args = [sys.executable, str(SCRIPT), str(d)]
            if reply is not None:
                r = Path(tmp) / "reply.md"
                r.write_text(reply, encoding="utf-8")
                args += ["--reply", str(r)]
            p = subprocess.run(args, cwd=PROJECT, capture_output=True, text=True, env={**os.environ, "PYTHONIOENCODING": "utf-8"})
            return p.returncode, p.stdout

    def test_clean_document_passes(self) -> None:
        code, out = self.run_check('Could not find the code: 3 people — T-01, P3, T-12\n'
                                   'Weaker statements: 2 people — T-04, P4\n'
                                   'T-05 "Arrived and the point was closed"\n', reply="Saved.\n\n-_-\n")
        self.assertEqual(code, 0, out)

    def test_quote_credited_to_wrong_source(self) -> None:
        # CS-N1 attempt 19: T-01's words credited to P1
        code, out = self.run_check('P1 "Cannot find the code on the parcel page"\n')
        self.assertEqual(code, 1)
        self.assertIn("Q1", out)

    def test_quote_shared_by_two_sources(self) -> None:
        # UF-N1 attempt 5: only T-12 has these words
        code, out = self.run_check('T-01, T-12 "Cannot find pickup code"\n')
        self.assertIn("Q1", out)

    def test_count_repeats_strict_member(self) -> None:
        # CS-E1 attempt 10: P1 is the author of T-01
        code, out = self.run_check('Could not find the code: 3 people — P3, T-01, T-12 [observed]\n'
                                   'Weaker statements: 3 people — T-04, P1, P4 [observed]\n')
        self.assertIn("C3", out)

    def test_count_mismatch_and_weak_member(self) -> None:
        code, out = self.run_check('Could not find the code: 3 people — P1, T-01, P3\n')
        self.assertIn("C1", out)
        code, out = self.run_check('Could not find the code: 4 people — P1, P3, T-12, T-04\n')
        self.assertIn("C2", out)

    def test_reply_with_two_questions(self) -> None:
        # DC-E1 attempt 4
        code, out = self.run_check("ok\n", reply="Who said everyone hates the green banner, and was that users or the team?\n")
        self.assertIn("R1", out)
        code, out = self.run_check("ok\n", reply="Who said everyone hates it?\n\n._.\n")
        self.assertEqual(code, 0, out)

    def test_names_are_never_printed(self) -> None:
        code, out = self.run_check('Could not find the code: 4 people — P1, P3, T-12, T-04\n')
        self.assertNotIn("@example.test", out)
        self.assertNotIn("Quenby", out)


if __name__ == "__main__":
    unittest.main()
