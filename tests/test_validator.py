"""Unit tests proving the validator catches representative violations.

Each test copies the repo to a temp dir, applies one mutation, and asserts
that a specific check fails. Run via `bash tests/run.sh`.
"""
from __future__ import annotations

import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_skills as v  # noqa: E402


class ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name) / "repo"
        shutil.copytree(v.DEFAULT_ROOT, self.root,
                        ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def edit(self, rel: str, fn: Callable[[str], str]) -> None:
        path = self.root / rel
        before = path.read_text(encoding="utf-8")
        after = fn(before)
        self.assertNotEqual(before, after, f"mutation of {rel} changed nothing")
        path.write_text(after, encoding="utf-8")

    def assertFails(self, fragment: str) -> None:
        failed = v.validate(self.root, echo=False).failed
        self.assertTrue(any(fragment in label for label in failed),
                        f"expected a failure containing {fragment!r}; got {failed}")

    def test_baseline_passes(self) -> None:
        self.assertEqual(v.validate(self.root, echo=False).failed, [])

    def test_section_order(self) -> None:
        self.edit(".claude/skills/ux-audit/SKILL.md", lambda t: t.replace("\n## Triggers\n", "\n## Trigger\n"))
        self.assertFails("ux-audit: sections in required order")

    def test_name_mismatch(self) -> None:
        self.edit(".claude/skills/ux-audit/SKILL.md", lambda t: t.replace("name: ux-audit", "name: ux-audits", 1))
        self.assertFails("ux-audit: name matches directory")

    def test_missing_use_when(self) -> None:
        self.edit(".claude/skills/design-qa/SKILL.md", lambda t: t.replace("Use when", "Trigger on", 1))
        self.assertFails("design-qa: description has 'Use when'")

    def test_unknown_boundary_reference(self) -> None:
        def corrupt_first_boundary_ref(t: str) -> str:
            head, sep, tail = t.partition("## Boundaries\n")
            return head + sep + re.sub(r"`[a-z0-9-]+`", "`no-such-skill`", tail, count=1)
        self.edit(".claude/skills/mvp-planner/SKILL.md", corrupt_first_boundary_ref)
        self.assertFails("mvp-planner: boundaries refs exist")

    def test_example_missing_banner(self) -> None:
        self.edit("examples/ux-audit.md", lambda t: t.replace("Illustrative example", "Sample", 1))
        self.assertFails("example ux-audit.md: labeled illustrative")

    def test_example_missing_contract_heading(self) -> None:
        self.edit("examples/problem-framing.md", lambda t: t.replace("## What would falsify this\n", "", 1))
        self.assertFails("example problem-framing.md: output headings match skill contract")

    def test_example_heading_parenthetical_drift(self) -> None:
        # norm_heading ignores trailing parentheticals; the exact-text check must still catch drift
        self.edit("examples/user-flow-designer.md",
                  lambda t: t.replace("## Flow diagram (Mermaid or list)", "## Flow diagram (Mermaid)", 1))
        self.assertFails("example user-flow-designer.md: output headings match skill contract exactly")

    def test_example_next_step_chains_two_skills(self) -> None:
        self.edit("examples/ux-audit.md",
                  lambda t: t.replace("Run `usability-test-planner`", "Run `usability-test-planner`, then `design-qa`", 1))
        self.assertFails("example ux-audit.md: Next step names one allowed handoff")

    def test_example_next_step_not_an_allowed_handoff(self) -> None:
        self.edit("examples/problem-framing.md",
                  lambda t: t.replace("Run `ux-research-planner` to plan", "Run `product-metrics` to plan", 1))
        self.assertFails("example problem-framing.md: Next step names one allowed handoff")

    def test_example_next_step_disallowed_never_clause(self) -> None:
        # interview-guide-builder says "Never point back to `ux-research-planner`"; that name is not allowed
        self.edit("examples/interview-guide-builder.md",
                  lambda t: t.replace("Run `persona-builder` once", "Run `ux-research-planner` once", 1))
        self.assertFails("example interview-guide-builder.md: Next step names one allowed handoff")

    def test_example_literal_date(self) -> None:
        self.edit("examples/user-flow-designer.md", lambda t: t.replace("<YYYY-MM-DD>", "2026-01-15", 1))
        self.assertFails("example user-flow-designer.md: no literal dates")

    def test_example_wrong_output_area(self) -> None:
        self.edit("examples/feature-prioritization.md",
                  lambda t: t.replace("design/planning/", "design/audits/", 1))
        self.assertFails("example feature-prioritization.md: output path")

    def test_example_metadata_wrong_skill(self) -> None:
        self.edit("examples/ux-audit.md", lambda t: t.replace("> skill: ux-audit ·", "> skill: design-qa ·", 1))
        self.assertFails("example ux-audit.md: metadata line names the skill")

    def test_example_not_listed(self) -> None:
        self.edit("examples/README.md", lambda t: t.replace("[ux-audit.md](ux-audit.md)", "ux-audit", 1))
        self.assertFails("examples/README.md: lists ux-audit.md")

    def test_broken_link(self) -> None:
        self.edit("README.md", lambda t: t.replace("(CONTRIBUTING.md)", "(MISSING.md)", 1))
        self.assertFails("README.md: relative links resolve")

    def test_missing_contributing(self) -> None:
        (self.root / "CONTRIBUTING.md").unlink()
        self.assertFails("repo: CONTRIBUTING.md exists")

    def test_architecture_missing_standard_heading(self) -> None:
        self.edit(".claude/skills/_shared/standard.md", lambda t: t.replace("### Date handling", "### Dates", 1))
        self.assertFails("shared standard: covers 'Date handling'")

    def test_standard_skill_missing_not_for(self) -> None:
        self.edit(".claude/skills/persona-builder/SKILL.md", lambda t: t.replace(" Not for ", " Instead of ", 1))
        self.assertFails("persona-builder: description has 'Not for'")

    def test_standard_skill_not_for_unknown_sibling(self) -> None:
        self.edit(".claude/skills/competitive-analysis/SKILL.md",
                  lambda t: t.replace("(use `design-critique`)", "(use `design-nothing`)", 1))
        self.assertFails("competitive-analysis: description has 'Not for'")

    def test_standard_skill_missing_if_missing_column(self) -> None:
        self.edit(".claude/skills/product-discovery/SKILL.md", lambda t: t.replace("| If missing |", "| Required |", 1))
        self.assertFails("product-discovery: Inputs table has an 'If missing' column")

    def test_standard_skill_bad_missing_action(self) -> None:
        self.edit(".claude/skills/problem-framing/SKILL.md",
                  lambda t: t.replace("| Stop: nothing to frame |", "| Maybe |", 1))
        self.assertFails("problem-framing: every input declares")

    def test_standard_skill_missing_section_reference(self) -> None:
        self.edit(".claude/skills/usability-test-planner/SKILL.md",
                  lambda t: t.replace("`../_shared/standard.md` §7 and §8", "`../_shared/standard.md` §7", 1))
        self.assertFails("usability-test-planner: Quality checks references §8")

    def test_standard_skill_missing_architecture_handoff(self) -> None:
        # section 5 says journey-map-builder hands off to user-flow-designer
        self.edit(".claude/skills/journey-map-builder/SKILL.md",
                  lambda t: t.replace("`user-flow-designer`", "`user-flow-x`"))
        self.assertFails("journey-map-builder: section 5 handoffs named in Outputs")

    def test_handoff_only_outside_outputs_is_not_enough(self) -> None:
        def drop_from_outputs(t: str) -> str:
            head, sep, tail = t.partition("## Quality checks")
            return head.replace("`user-flow-designer`", "`user-flow-x`") + sep + tail
        self.edit(".claude/skills/journey-map-builder/SKILL.md", drop_from_outputs)
        self.assertFails("journey-map-builder: section 5 handoffs named in Outputs")

    def test_evaluative_skill_must_use_shared_severity_scale(self) -> None:
        self.edit(".claude/skills/ux-audit/SKILL.md", lambda t: t.replace("Cosmetic", "Trivial"))
        self.assertFails("ux-audit: uses the section 8 severity scale")

    def test_evaluative_skill_rejects_legacy_numeric_scale(self) -> None:
        self.edit(".claude/skills/design-qa/SKILL.md", lambda t: t + "\nSeverity 0 to 4.\n")
        self.assertFails("design-qa: uses the section 8 severity scale")

    def test_design_documentation_contract_heading_removed(self) -> None:
        self.edit(".claude/skills/design-documentation/SKILL.md", lambda t: t.replace("## Tokens and references\n", "", 1))
        self.assertFails("design-documentation: output contract headings match")

    def test_design_documentation_contract_reordered(self) -> None:
        self.edit(".claude/skills/design-documentation/SKILL.md",
                  lambda t: t.replace("## Context\n## Scope and out of scope\n", "## Scope and out of scope\n## Context\n", 1))
        self.assertFails("design-documentation: output contract headings match")

    def test_design_documentation_missing_marking_rules(self) -> None:
        self.edit(".claude/skills/design-documentation/SKILL.md", lambda t: t.replace("Not applicable", "N/A"))
        self.assertFails("design-documentation: contract says how to mark")

    def test_output_template_must_end_with_shared_headings(self) -> None:
        self.edit(".claude/skills/case-study-writer/SKILL.md",
                  lambda t: t.replace("## Next step\n```", "## Wrap up\n```", 1))
        self.assertFails("case-study-writer: output template ends with open questions and next step")

    def test_batch_e_skill_is_held_to_standard(self) -> None:
        self.edit(".claude/skills/feature-prioritization/SKILL.md", lambda t: t.replace(" Not for ", " Instead of ", 1))
        self.assertFails("feature-prioritization: description has 'Not for'")

    def test_batch_d_skill_is_held_to_standard(self) -> None:
        self.edit(".claude/skills/product-metrics/SKILL.md", lambda t: t.replace("| If missing |", "| Required |", 1))
        self.assertFails("product-metrics: Inputs table has an 'If missing' column")

    def test_batch_c_skill_is_held_to_standard(self) -> None:
        self.edit(".claude/skills/information-architect/SKILL.md", lambda t: t.replace(" Not for ", " Instead of ", 1))
        self.assertFails("information-architect: description has 'Not for'")

    def test_skill_must_not_cite_a_file_that_is_not_installed(self) -> None:
        # Regression for the dangling-reference defect found by the behavioral pilot.
        self.edit(".claude/skills/ux-audit/SKILL.md",
                  lambda t: t.replace("../_shared/standard.md", "docs/ARCHITECTURE.md", 1))
        self.assertFails("ux-audit: cites nothing that is not installed with the skills")

    def test_skill_must_not_cite_a_missing_shared_file(self) -> None:
        self.edit(".claude/skills/ux-audit/SKILL.md",
                  lambda t: t.replace("_shared/standard.md", "_shared/nope.md", 1))
        self.assertFails("ux-audit: cited shared files exist")

    def test_shared_standard_is_required(self) -> None:
        (self.root / ".claude" / "skills" / "_shared" / "standard.md").unlink()
        self.assertFails("repo: shared standard ships with the skills")

    def test_shared_directory_is_not_counted_as_a_skill(self) -> None:
        self.assertFalse([l for l in v.validate(self.root, echo=False).failed if "19 skill directories" in l])

    def test_readme_missing_skill(self) -> None:
        self.edit("README.md", lambda t: t.replace("persona-builder", "persona-x"))
        self.assertFails("repo: README mentions all skills")


if __name__ == "__main__":
    unittest.main()
