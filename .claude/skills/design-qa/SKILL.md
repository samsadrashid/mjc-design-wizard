---
name: design-qa
description: Check whether an implementation matches its approved design specification and intended behavior, logging verified mismatches with expected value, actual value, evidence, severity, confidence, and repro steps, and separating what could not be verified. Use when the user says "design QA", "does the build match the design", "visual QA", "pixel check", "pre-release design review". Not for usability problems (use `ux-audit`), subjective feedback on a design (use `design-critique`), consistency of tokens and components (use `design-system-audit`), or writing the missing spec (use `design-documentation`).
---

# Design QA

## Purpose
Report where the built product differs from what was designed and approved. A mismatch is logged only when an approved reference supplies the expected value. Anything that rests on a guess or a preference is kept apart as unverified, so engineers are not sent to fix things nobody specified.

## Triggers
- "QA this screen against the design", "check the implementation"
- A feature is in staging or a pull request and has a design reference
- Visual regressions are reported after release

## Inputs
| Input | If missing | Source |
|---|---|---|
| Design reference for the screen: an approved spec or design file that the user names or that is marked approved. Tokens or Storybook alone do not describe a screen | Stop: QA without a screen-level reference is guesswork. Point to `design-documentation` | user, `design/docs/` |
| Build under review: URL, branch, screenshots, or component code | Stop: nothing to compare | user, repo |
| Scope: screens, breakpoints, states | Assume the reference's screens and the default breakpoints in the code, and state them | user, repo |
| Approval status of the reference | Assume `approval unknown` and say so in the log | user |

## Workflow
1. **Inspect the project.** Read the spec, token files, Storybook stories if any, and the relevant routes and component code. Record the reference version and the build or commit reviewed, or `version unknown`. Do not copy personal data from screenshots or fixtures.
2. **Build the coverage matrix:** screens by breakpoints by states (default, hover, focus, disabled, loading, empty, error). Mark each cell checked, not reachable, or not provided.
3. **Compare each checked cell** across layout and spacing, typography, color and tokens, iconography, component variants, interaction states, copy, responsive behavior, and motion. Prefer evidence that is measurable: computed styles, token names in code, or annotated screenshots.
4. **Log verified mismatches** only with an expected value cited from the reference. Fields: id, screen, breakpoint, element, expected with its source, actual with evidence, type, severity from `../_shared/standard.md` §8 (Blocker, Major, Minor, Cosmetic), confidence (High, Medium, Low), and repro steps another person can follow. Values read from code or computed styles are verified. Sizes estimated from a description or an image are unverified.
5. **Keep unverified differences separate.** Where the reference is incomplete, ambiguous, or the build cannot be inspected, record the difference as unverified, with what is missing. Treat a visual preference as feedback for `design-critique`, not as a defect.
6. **List spec gaps:** states or breakpoints the reference never defined. These are spec defects, not build defects.
7. **Summarize** by severity and screen, and list what was not checked. Write the output per §8.

## Outputs
Metadata block (§4), then path, date, collisions, and reruns (§8), follow `../_shared/standard.md`. File:
`design/audits/design-qa-<feature>-<date>.md`:
```
> metadata block (reference version, build or commit)
## Coverage matrix (screen × breakpoint × state)
## Verified mismatches (defect log)
## Unverified or ambiguous differences
## Spec gaps found
## Summary by severity and screen
## Not checked
## Open questions / to validate
## Next step
```
`## Next step` names one handoff: `design-documentation` to close spec gaps, `design-system-audit` when mismatches trace to shared components or tokens, or `ux-audit` for usability issues seen along the way.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] Every verified mismatch cites an expected value from an approved reference
- [ ] Differences without a reference are in the unverified section, not the defect log
- [ ] Severity uses only the shared scale; confidence is separate
- [ ] Unreachable and unprovided states are marked not checked, never passed
- [ ] Repro steps work without the designer present
- [ ] No usability opinions in the defect log

## Boundaries
- Does not evaluate usability → `ux-audit`
- Does not give subjective design feedback → `design-critique`
- Does not audit the system itself → `design-system-audit`
- Does not write the spec → `design-documentation`
