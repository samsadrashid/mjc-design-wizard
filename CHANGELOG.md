# Changelog

All notable changes to MJC Design Wizard. Versions follow [Semantic Versioning](https://semver.org/).

## 1.1.0 (unreleased)

### Added
- Plugin packaging (`.claude-plugin/plugin.json`, `marketplace.json`) so the skills install with `/plugin install`.
- Optional Figma output for all 19 skills through the shared adapter `_shared/figma.md` (publishing off by default).
- MJC Emotional Layer (`_shared/personality.md`): one closing text emoticon per chat reply, never in files or structured output.
- `_shared/check_evidence.py`: a self-check the skills run before saving, for quotes credited to a source, person counts, and the one-question rule.
- Behavioral evaluation suite (`tests/behavioral/`) with automated screens and graded runs.

### Changed
- `user-flow-designer`: transition inventory with evidence status, one complete diagram plus one diagram per individual flow, and an integrity check.
- Shared standard: claim-level evidence rules, fixed forms for quotes and counts, and a section listing the shared files to load.
- Every skill's `## Next step` names exactly one handoff; "ask one" inputs state their fallback.
- `design-qa`: naming a reference authorizes it as input; each expected value is marked approved or approval unknown.

### Fixed
- Contradictions between the skills and the shared standard found in the November 2026 audit.

## 1.0.0

- First release: 19 skills, shared standard, examples, validator, and CI.
