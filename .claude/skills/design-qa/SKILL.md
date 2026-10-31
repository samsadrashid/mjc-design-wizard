---
name: design-qa
description: Compare an implemented build against its design spec and log defects - spacing, type, color, states, copy, responsive behavior - with repro steps and severity. Use when the user says "design QA", "does the build match the design", "visual QA", "pixel check", "pre-release design review".
---

# Design QA

## Purpose
Produce a defect log of differences between what was designed and what was built, with precise locations and expected vs actual values, so engineers can fix them without interpretation.

## Triggers
- "QA this screen against the design", "check the implementation"
- A feature is in staging or PR and has a design reference
- Post-release visual regressions reported

## Inputs
| Input | Required | Source |
|---|---|---|
| Design reference (spec doc, design file export, screenshots) | yes | user, `design/docs/` |
| Build under review (URL, branch, screenshots) | yes | user, browser if available |
| Scope: screens and breakpoints | yes | user |
| Design tokens | optional | repo, `design/audits/` |

## Workflow
1. **Inspect the project.** Read the design spec and token definitions. If no spec exists, stop and point to `design-documentation`; QA without a reference is guesswork.
2. **Set up comparison.** List screens × breakpoints × states to check. Mark any not reachable.
3. **Check each cell**: layout and spacing, typography, color and tokens, iconography, component variants, interactive states (hover, focus, disabled, error), copy, responsive behavior, motion.
4. **Log defects.** Per defect: id, screen, breakpoint, element, expected (with source), actual (with evidence), severity (blocker, major, minor, cosmetic), repro steps.
5. **Separate** spec defects (design was wrong or incomplete) from build defects.
6. **Summarize** pass rate per screen and blocker count.
7. **Write output**; show blockers and majors in chat.

## Outputs
`design/audits/design-qa-<feature>-<date>.md`:
```
> metadata block (spec and build versions)
## Coverage matrix (screen × breakpoint × state)
## Defect log
## Spec gaps found
## Summary by severity and screen
## Not checked
## Open questions / to validate
## Next step
```

## Quality checks
- [ ] Global checks in `docs/ARCHITECTURE.md` §7
- [ ] Every defect has expected and actual with evidence
- [ ] Repro steps allow an engineer to reproduce without the designer
- [ ] Unreachable states listed as not checked, not passed
- [ ] No usability opinions in the defect log

## Boundaries
- Does not evaluate usability → `ux-audit`
- Does not audit the system itself → `design-system-audit`
- Does not write the spec → `design-documentation`
