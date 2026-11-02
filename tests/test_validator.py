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
        # (user-flow-designer's contract no longer has a parenthetical heading; competitive-analysis does)
        self.edit("examples/competitive-analysis.md",
                  lambda t: t.replace("## Patterns (table-stakes, differentiators, gaps)", "## Patterns (table-stakes)", 1))
        self.assertFails("example competitive-analysis.md: output headings match skill contract exactly")

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

    # Figma adapter: structural checks on the instruction file only. None of these contacts Figma,
    # and none is a mocked MCP run; live capability evidence lives in figma.md section 9.
    FIGMA = ".claude/skills/_shared/figma.md"

    def test_figma_publishing_must_default_to_disabled(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace('"enabled": false', '"enabled": true', 1))
        self.assertFails("figma adapter: publishing is disabled by default")

    def test_figma_per_run_confirmation_default(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace('"confirm_each_run": true', '"confirm_each_run": false', 1))
        self.assertFails("figma adapter: per-run confirmation is on by default")

    def test_figma_quotes_not_published_by_default(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace('"allow_quotes": false', '"allow_quotes": true', 1))
        self.assertFails("figma adapter: quotes are not published by default")

    def test_figma_config_rejects_credentials(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace('"schema_version": 1,', '"schema_version": 1,\n  "access_token": null,', 1))
        self.assertFails("figma adapter: configuration has no credential fields")

    def test_figma_user_flows_page(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace("| user-flow-designer | User Flows |", "| user-flow-designer | Flows |", 1))
        self.assertFails("figma adapter: user flows draw on the User Flows page")

    def test_figma_page_names_unique(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace("| design-qa | Design QA |", "| design-qa | UX Audit |", 1))
        self.assertFails("figma adapter: page names are unique")

    def test_figma_page_map_covers_all_skills(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace("| case-study-writer | Case Studies | `<project>` |\n", "", 1))
        self.assertFails("figma adapter: page map covers all 19 skills")

    def test_figma_manual_edit_case_required(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace("| Owned but fingerprint differs (edited by hand) |", "| Owned |", 1))
        self.assertFails("figma adapter: decision table covers every case")

    def test_figma_tools_unavailable_case_required(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace("| Figma tools unavailable |", "| Tools |", 1))
        self.assertFails("figma adapter: decision table covers every case")

    def test_figma_ownership_needs_stored_id(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace("stored for the artifact key", "for the artifact", 1))
        self.assertFails("figma adapter: ownership needs the stored node ID and the tag")

    def test_figma_markdown_stays_source_of_truth(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace("Markdown file is always written first", "Markdown file may be skipped", 1))
        self.assertFails("figma adapter: Markdown stays the source of truth")

    def test_figma_every_skill_must_cite_adapter(self) -> None:
        # All 19 skills are integrated, so dropping any one skill's citation must fail.
        for skill in sorted(v.EXPECTED):
            with self.subTest(skill=skill):
                self.setUp()
                self.edit(f".claude/skills/{skill}/SKILL.md", lambda t: t.replace("../_shared/figma.md", "the Figma notes"))
                self.assertFails("figma adapter: cited by exactly the integrated skills")

    def test_figma_pilot_must_cite_adapter(self) -> None:
        self.edit(".claude/skills/ux-audit/SKILL.md", lambda t: t.replace("../_shared/figma.md", "the Figma notes"))
        self.assertFails("figma adapter: cited by exactly the integrated skills")

    def test_figma_unreadable_config_case_required(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace("| Configuration unreadable", "| Config bad", 1))
        self.assertFails("figma adapter: decision table covers every case")

    def test_figma_exact_fingerprint_function_required(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace("// MJC fingerprint fp1. Paste unchanged.", "// fingerprint", 1))
        self.assertFails("figma adapter: one exact fingerprint function is given")

    def test_figma_new_version_not_cloned(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace("never by cloning the edited frame", "for example by cloning the frame", 1))
        self.assertFails("figma adapter: new versions are drawn from the Markdown")

    # Decision rules for manual-edit safety. These prove the instructions state the rules,
    # not that a model follows them or that Figma behaves this way.
    def test_figma_match_row_limited_to_non_destructive(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace(
            "No tracked edit. Update in place, but only within the non-destructive update rules below",
            "No tracked edit. Update the frame in place", 1))
        self.assertFails("figma adapter: decision row 'Owned, stored fingerprint has the `fp1:`'")

    def test_figma_replacement_requires_confirmation(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace(
            "A replacement. Ask the user to confirm it. Without confirmation, draw a new version from the Markdown",
            "A replacement. Redraw the frame", 1))
        self.assertFails("figma adapter: decision row 'Owned, fingerprint matches, but the upda'")

    def test_figma_unknown_fingerprint_preserved_and_confirmed(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace(
            "Unknown. Preserve the frame and ask the user to confirm a replacement.",
            "Unknown. Update the frame in place.", 1))
        self.assertFails("figma adapter: decision row 'Stored fingerprint missing or lacks'")

    def test_figma_match_not_proof_of_no_edits(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace(
            "a matching fingerprint does not prove the frame is unchanged",
            "a matching fingerprint proves the frame is unchanged", 1))
        self.assertFails("figma adapter: a matching fingerprint is not treated as proof of no edits")

    def test_figma_in_place_update_cannot_restyle(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace(
            "may therefore only change the characters of existing text nodes and append new nodes",
            "may change any property of existing nodes", 1))
        self.assertFails("figma adapter: in-place updates are limited to non-destructive changes")

    def test_figma_in_place_update_cannot_delete(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace(
            "never deletes, recreates, reorders, or restyles existing nodes", "may delete or recreate nodes", 1))
        self.assertFails("figma adapter: in-place updates are limited to non-destructive changes")

    def test_figma_skill_line_names_wrong_page(self) -> None:
        self.edit(".claude/skills/ux-audit/SKILL.md", lambda t: t.replace("on the `UX Audit` page", "on the `Audits` page", 1))
        self.assertFails("ux-audit: figma line names its mapped page")

    def test_figma_skill_must_not_call_mcp_directly(self) -> None:
        self.edit(".claude/skills/user-flow-designer/SKILL.md",
                  lambda t: t.replace("## Quality checks\n", "## Quality checks\n- [ ] Call use_figma to draw the flow\n", 1))
        self.assertFails("user-flow-designer: figma has no direct MCP tool calls")

    def test_figma_artifact_topic_matches_filename(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace("| ux-audit | UX Audit | `<scope>` |", "| ux-audit | UX Audit | `<widget>` |", 1))
        self.assertFails("ux-audit: figma artifact topic comes from its output filename")

    def test_figma_batch_b_pages(self) -> None:
        for skill, page in (("usability-test-planner", "Usability Testing"), ("interview-guide-builder", "Interview Guides"),
                            ("ux-research-planner", "UX Research Plans"), ("persona-builder", "Personas")):
            with self.subTest(skill=skill):
                self.setUp()
                self.edit(f".claude/skills/{skill}/SKILL.md", lambda t: t.replace(f"on the `{page}` page", "on the `Research` page", 1))
                self.assertFails(f"{skill}: figma line names its mapped page")

    def test_figma_batch_b_quality_check_required(self) -> None:
        for skill in ("usability-test-planner", "interview-guide-builder", "ux-research-planner", "persona-builder"):
            with self.subTest(skill=skill):
                self.setUp()
                self.edit(f".claude/skills/{skill}/SKILL.md", lambda t: t.replace(
                    "- [ ] Any Figma output followed `../_shared/figma.md`", "- [ ] Any Figma output was checked", 1))
                self.assertFails(f"{skill}: figma quality check cites the adapter")

    def test_figma_batch_b_markdown_first(self) -> None:
        for skill in ("usability-test-planner", "interview-guide-builder", "ux-research-planner", "persona-builder"):
            with self.subTest(skill=skill):
                self.setUp()
                self.edit(f".claude/skills/{skill}/SKILL.md", lambda t: t.replace(
                    "The Markdown file stays the source of truth.", "Figma replaces the Markdown file.", 1))
                self.assertFails(f"{skill}: figma line keeps Markdown as the source of truth")

    def test_figma_batch_b_privacy_limit_required(self) -> None:
        self.edit(".claude/skills/persona-builder/SKILL.md", lambda t: t.replace(
            "never add names, photos, ages, or quotes that are not in the Markdown", "add a name and photo to each card", 1))
        self.assertFails("persona-builder: figma line limits drawing to what the Markdown supports")

    def test_figma_batch_b_no_direct_mcp(self) -> None:
        self.edit(".claude/skills/interview-guide-builder/SKILL.md",
                  lambda t: t.replace("## Quality checks\n", "## Quality checks\n- [ ] Draw the guide with create_session\n", 1))
        self.assertFails("interview-guide-builder: figma has no direct MCP tool calls")

    def test_figma_batch_b_artifact_topic(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace("| persona-builder | Personas | `<topic>` |", "| persona-builder | Personas | `<segment>` |", 1))
        self.assertFails("persona-builder: figma artifact topic comes from its output filename")

    BATCH_C = (("information-architect", "Information Architecture"), ("journey-map-builder", "Journey Maps"),
               ("design-qa", "Design QA"), ("product-metrics", "Product Metrics"))

    def test_figma_batch_c_pages(self) -> None:
        for skill, page in self.BATCH_C:
            with self.subTest(skill=skill):
                self.setUp()
                self.edit(f".claude/skills/{skill}/SKILL.md", lambda t: t.replace(f"on the `{page}` page", "on the `Overview` page", 1))
                self.assertFails(f"{skill}: figma line names its mapped page")

    def test_figma_batch_c_quality_check_required(self) -> None:
        for skill, _ in self.BATCH_C:
            with self.subTest(skill=skill):
                self.setUp()
                self.edit(f".claude/skills/{skill}/SKILL.md", lambda t: t.replace(
                    "- [ ] Any Figma output followed `../_shared/figma.md`", "- [ ] Any Figma output was checked", 1))
                self.assertFails(f"{skill}: figma quality check cites the adapter")

    def test_figma_batch_c_markdown_first(self) -> None:
        for skill, _ in self.BATCH_C:
            with self.subTest(skill=skill):
                self.setUp()
                self.edit(f".claude/skills/{skill}/SKILL.md", lambda t: t.replace(
                    "The Markdown file stays the source of truth.", "Figma replaces the Markdown file.", 1))
                self.assertFails(f"{skill}: figma line keeps Markdown as the source of truth")

    def test_figma_batch_c_source_grounding(self) -> None:
        cases = (("information-architect", "Never draw pages, routes, labels, or links that are not in the Markdown.",
                  "Add any pages the structure needs."),
                 ("journey-map-builder", "Never draw a stage, emotion, quote, or pain point that is not in the Markdown,",
                  "Fill empty emotion cells with a likely feeling,"),
                 ("design-qa", "Never draw a screenshot, never show an unverified difference as a defect, and never draw a mismatch that is not in the Markdown.",
                  "Attach a screenshot of each defect."),
                 ("product-metrics", "Never draw a baseline, target, outcome, or number that is not in the Markdown.",
                  "Fill missing baselines with a typical value."))
        for skill, old, new in cases:
            with self.subTest(skill=skill):
                self.setUp()
                self.edit(f".claude/skills/{skill}/SKILL.md", lambda t: t.replace(old, new, 1))
                self.assertFails(f"{skill}: figma line limits drawing to what the Markdown supports")

    def test_figma_batch_c_no_direct_mcp(self) -> None:
        self.edit(".claude/skills/design-qa/SKILL.md",
                  lambda t: t.replace("## Quality checks\n", "## Quality checks\n- [ ] Publish the defect log with use_figma\n", 1))
        self.assertFails("design-qa: figma has no direct MCP tool calls")

    def test_figma_batch_c_artifact_topic(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace("| journey-map-builder | Journey Maps | `<actor>-<scope>` |",
                                                  "| journey-map-builder | Journey Maps | `<persona>-<scope>` |", 1))
        self.assertFails("journey-map-builder: figma artifact topic comes from its output filename")

    def test_figma_every_skill_needs_exclusion_rule(self) -> None:
        # Strip every "never draw/add" clause from one skill's Figma line at a time.
        for skill in sorted(v.EXPECTED):
            with self.subTest(skill=skill):
                self.setUp()

                def strip(t: str) -> str:
                    lines = t.split("\n")
                    for i, l in enumerate(lines):
                        if l.startswith("Figma (optional, per `../_shared/figma.md`)"):
                            lines[i] = re.sub(r"\b([Nn])ever (draw|add)\b", r"\1o longer \2", l)
                    return "\n".join(lines)
                self.edit(f".claude/skills/{skill}/SKILL.md", strip)
                self.assertFails(f"{skill}: figma line limits drawing to what the Markdown supports")

    def test_figma_not_used_reason_must_be_fixed(self) -> None:
        # The design-critique live run reworded the reason; a free-form template allowed it.
        self.edit(self.FIGMA, lambda t: t.replace("- `Figma: not used (publishing disabled)`", "- `Figma: not used (<reason>)`", 1))
        self.assertFails("figma adapter: 'not used' reasons are the fixed set")

    def test_figma_not_used_reworded_reason_fails(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace(
            "Report `Figma: not used (publishing disabled)`",
            "Report `Figma: not used (publishing is disabled in design/figma.json)`", 1))
        self.assertFails("figma adapter: 'not used' reasons are the fixed set")

    def test_figma_unconfirmed_replacement_has_own_line(self) -> None:
        # Without it, an unconfirmed replacement would be reported as "edited by hand".
        self.edit(self.FIGMA, lambda t: t.replace(
            "- `Figma: new version <frame> v<n> created; replacement not confirmed, the earlier frame was left unchanged`\n", "", 1))
        self.assertFails("figma adapter: reporting covers unconfirmed replacement and file access failure")

    def test_figma_access_failure_line_in_reporting(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace("- `Figma: failed (file not found or no edit access)`\n", "", 1))
        self.assertFails("figma adapter: reporting covers unconfirmed replacement and file access failure")

    def test_figma_unconfirmed_run_reason_fixed(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace("report `Figma: not used (run not confirmed)`", "report `Figma: not used (user did not confirm)`", 1))
        self.assertFails("figma adapter: 'not used' reasons are the fixed set")

    def test_figma_not_used_copy_exactly_required(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace("Copy a `not used` line exactly", "Adapt a `not used` line", 1))
        self.assertFails("figma adapter: reporting lists each exact 'not used' line and says to copy it")

    BATCH_D = (("design-critique", "Design Critiques"), ("competitive-analysis", "Competitive Analysis"),
               ("design-documentation", "Design Documentation"), ("case-study-writer", "Case Studies"))

    def test_figma_batch_d_pages(self) -> None:
        for skill, page in self.BATCH_D:
            with self.subTest(skill=skill):
                self.setUp()
                self.edit(f".claude/skills/{skill}/SKILL.md", lambda t: t.replace(f"on the `{page}` page", "on the `Overview` page", 1))
                self.assertFails(f"{skill}: figma line names its mapped page")

    def test_figma_batch_d_quality_check_required(self) -> None:
        for skill, _ in self.BATCH_D:
            with self.subTest(skill=skill):
                self.setUp()
                self.edit(f".claude/skills/{skill}/SKILL.md", lambda t: t.replace(
                    "- [ ] Any Figma output followed `../_shared/figma.md`", "- [ ] Any Figma output was checked", 1))
                self.assertFails(f"{skill}: figma quality check cites the adapter")

    def test_figma_batch_d_markdown_first(self) -> None:
        for skill, _ in self.BATCH_D:
            with self.subTest(skill=skill):
                self.setUp()
                self.edit(f".claude/skills/{skill}/SKILL.md", lambda t: t.replace(
                    "The Markdown file stays the source of truth.", "Figma replaces the Markdown file.", 1))
                self.assertFails(f"{skill}: figma line keeps Markdown as the source of truth")

    def test_figma_batch_d_exclusion_rule(self) -> None:
        cases = (("design-critique", "Never draw a screenshot or a finding, defect, or element that is not in the Markdown,",
                  "Add a screenshot of each finding,"),
                 ("competitive-analysis", "Never draw a competitor capability, logo, screenshot, or claim that is not in the Markdown.",
                  "Add each competitor's logo and best-known features."),
                 ("design-documentation", "Never draw a decision, requirement, token value, or component that is not in the Markdown,",
                  "Fill unavailable sections with sensible defaults,"),
                 ("case-study-writer", "Never draw the two author-only appendix sections, and never draw an outcome,",
                  "Include the appendix sections, and add an estimated outcome,"))
        for skill, old, new in cases:
            with self.subTest(skill=skill):
                self.setUp()
                self.edit(f".claude/skills/{skill}/SKILL.md", lambda t: t.replace(old, new, 1))
                self.assertFails(f"{skill}: figma line limits drawing to what the Markdown supports")

    def test_figma_batch_d_no_direct_mcp(self) -> None:
        self.edit(".claude/skills/competitive-analysis/SKILL.md",
                  lambda t: t.replace("## Quality checks\n", "## Quality checks\n- [ ] Check the file with get_metadata first\n", 1))
        self.assertFails("competitive-analysis: figma has no direct MCP tool calls")

    def test_figma_batch_d_artifact_topic(self) -> None:
        self.edit(self.FIGMA, lambda t: t.replace("| case-study-writer | Case Studies | `<project>` |",
                                                  "| case-study-writer | Case Studies | `<client>` |", 1))
        self.assertFails("case-study-writer: figma artifact topic comes from its output filename")

    # user-flow-designer: the rules that tie each arrow to evidence.
    FLOW = ".claude/skills/user-flow-designer/SKILL.md"
    FLOW_EX = "examples/user-flow-designer.md"

    def test_flow_unknown_status_required(self) -> None:
        self.edit(self.FLOW, lambda t: t.replace("or `Unknown` (no source settles it)", "or left out", 1))
        self.assertFails("user-flow-designer: states rule 'transition statuses'")

    def test_flow_edges_match_inventory(self) -> None:
        self.edit(self.FLOW, lambda t: t.replace("Every inventory row is one labeled arrow, and every arrow is a row",
                                                 "Draw the main arrows", 1))
        self.assertFails("user-flow-designer: states rule 'one edge per inventory row'")

    def test_flow_large_flows_not_trimmed(self) -> None:
        self.edit(self.FLOW, lambda t: t.replace("never drop a branch to make it fit.", "drop minor branches if needed.", 1))
        self.assertFails("user-flow-designer: states rule 'one complete diagram, not trimmed'")

    def test_flow_individual_flows_required(self) -> None:
        self.edit(self.FLOW, lambda t: t.replace("Together the individual flows cover every inventory transition", "Draw a few flows", 1))
        self.assertFails("user-flow-designer: states rule 'individual flows cover every transition'")

    def test_example_individual_flows_cover_transitions(self) -> None:
        self.edit("examples/user-flow-designer.md", lambda t: t.replace("|T12 · leaves|", "|leaves|", 1))
        self.assertFails("example user-flow-designer.md: individual flows cover every complete-flow transition")

    def test_flow_integrity_check_required(self) -> None:
        self.edit(self.FLOW, lambda t: t.replace("**Run the flow integrity check**", "**Review the diagram**", 1))
        self.assertFails("user-flow-designer: states rule 'integrity check'")

    def test_flow_contradictions_not_resolved_silently(self) -> None:
        self.edit(self.FLOW, lambda t: t.replace("Never resolve a contradiction by choosing a side silently.",
                                                 "Prefer the code when sources disagree.", 1))
        self.assertFails("user-flow-designer: states rule 'contradictions name both sources'")

    def test_flow_example_unlabeled_edge_fails(self) -> None:
        self.edit(self.FLOW_EX, lambda t: t.replace("-->|T5 · retry|", "-->|retry|", 1))
        self.assertFails("example user-flow-designer.md: every complete-flow edge is labeled with a transition ID")

    def test_flow_example_needs_terminal_and_legend(self) -> None:
        self.edit(self.FLOW_EX, lambda t: t.replace("| Shape and text | Meaning |", "| Shape and text | Use |", 1))
        self.assertFails("example user-flow-designer.md: terminal states are marked and a legend is present")

    def test_flow_example_inventory_needs_evidence(self) -> None:
        self.edit(self.FLOW_EX, lambda t: t.replace("| Status | Evidence |", "| Status | Notes |", 1))
        self.assertFails("example user-flow-designer.md: inventory has status and evidence columns")

    def test_figma_skill_keeps_markdown_source_of_truth(self) -> None:
        self.edit(".claude/skills/design-system-audit/SKILL.md",
                  lambda t: t.replace("The Markdown file stays the source of truth.", "Figma is the primary output.", 1))
        self.assertFails("design-system-audit: figma line keeps Markdown as the source of truth")

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

    def test_personality_citation_required(self) -> None:
        self.edit(".claude/skills/design-qa/SKILL.md", lambda t: t.replace(v.PERSONALITY_LINE + "\n", "", 1))
        self.assertFails("design-qa: cites shared personality once")

    def test_personality_no_pictographic_emoji(self) -> None:
        self.edit(".claude/skills/_shared/personality.md", lambda t: t.replace("| `^_^` | Satisfied", "| \U0001F600 | Satisfied", 1))
        self.assertFails("personality: no pictographic emoji")

    def test_personality_false_success_rule(self) -> None:
        self.edit(".claude/skills/_shared/personality.md",
                  lambda t: t.replace("unless the completion conditions were met and verified", "when it feels done", 1))
        self.assertFails("personality: states rule 'no false success'")

    def test_personality_not_in_written_output(self) -> None:
        self.edit("examples/ux-audit.md", lambda t: t.replace("## Next step\n", "## Next step\n^_^ ", 1))
        self.assertFails("example ux-audit.md: written output has no emoticons")

    def test_personality_library_not_copied_into_skill(self) -> None:
        self.edit(".claude/skills/mvp-planner/SKILL.md", lambda t: t.replace("## Boundaries\n", "## Boundaries\n- Say -_- when focused\n", 1))
        self.assertFails("mvp-planner: does not copy emoticons")
    def test_personality_closing_rule_required(self) -> None:
        self.edit(".claude/skills/_shared/personality.md", lambda t: t.replace("Nothing follows it", "Anything may follow it", 1))
        self.assertFails("personality: states rule 'closing signature'")

    def test_personality_sample_form_checked(self) -> None:
        self.edit(".claude/skills/_shared/personality.md", lambda t: t.replace("All quality checks passed.\n\n^_^", "All quality checks passed. ^_^", 1))
        self.assertFails("personality: sample 3 (normal) has correct form")


class ReplyFormTests(unittest.TestCase):
    def test_good_reply(self) -> None:
        self.assertEqual(v.reply_problems("Saved the audit.\n\n-_-\n"), [])

    def test_concern_not_double_counted(self) -> None:
        self.assertEqual(v.reply_problems("Missing input.\n\n._.;"), [])

    def test_opening_only(self) -> None:
        self.assertIn("last line is not exactly one emoticon", v.reply_problems("o_o Saved the audit."))

    def test_duplicate_opening_and_closing(self) -> None:
        self.assertIn("2 emoticons; expected exactly one", v.reply_problems("o_o Found it.\n\no_o"))

    def test_text_after_signature(self) -> None:
        self.assertIn("last line is not exactly one emoticon", v.reply_problems("Done.\n\n^_^ thanks"))

    def test_no_blank_line(self) -> None:
        self.assertIn("signature not separated by exactly one blank line after content", v.reply_problems("Done.\n^_^"))

    def test_two_blank_lines(self) -> None:
        self.assertIn("signature not separated by exactly one blank line after content", v.reply_problems("Done.\n\n\n^_^"))

    def test_pictograph(self) -> None:
        self.assertIn("pictographic emoji", v.reply_problems("Done \U0001F600\n\n^_^"))

    def test_failed_with_success(self) -> None:
        self.assertIn("success expression on a failed workflow", v.reply_problems("Could not run.\n\n^_^", "failed"))

    def test_strict_untouched(self) -> None:
        self.assertEqual(v.reply_problems('{"a": 1}', "strict"), [])
        self.assertIn("emoticon in strict-format output", v.reply_problems('{"a": 1}\n\n-_-', "strict"))

if __name__ == "__main__":
    unittest.main()
