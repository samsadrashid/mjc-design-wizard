---
name: design-qa
description: Check whether an implementation matches its design specification and intended behavior, logging verified mismatches with expected value, actual value, evidence, severity, confidence, and repro steps, and separating what could not be verified. Use when the user says "design QA", "does the build match the design", "visual QA", "pixel check", "pre-release design review". Not for usability problems (use `ux-audit`), subjective feedback on a design (use `design-critique`), consistency of tokens and components (use `design-system-audit`), or writing the missing spec (use `design-documentation`).
---

# Design QA

## Purpose
Report where the built product differs from what was designed. A mismatch is logged only when a reference the user named, or one marked approved, supplies the expected value. Naming a reference authorizes it as the input for the run; it does not approve the decisions in it, so each expected value states whether it is approved or `approval unknown`. Anything that rests on a guess or a preference is kept apart as unverified, so engineers are not sent to fix things nobody specified.

## Triggers
- "QA this screen against the design", "check the implementation"
- A feature is in staging or a pull request and has a design reference
- Visual regressions are reported after release

## Inputs
| Input | If missing | Source |
|---|---|---|
| Design reference for the screen: a spec or design file that the user names or that is marked approved. Tokens or Storybook alone do not describe a screen. A phrase that identifies no file, such as "the design spec", is not naming one; use a reference only if the user identifies the file or it is marked approved | Stop: QA without a screen-level reference is guesswork. Point to `design-documentation` | user, `design/docs/` |
| Build under review: URL, branch, screenshots, or component code | Stop: nothing to compare | user, repo |
| Scope: screens, breakpoints, states | Assume the reference's screens and the default breakpoints in the code, and state them | user, repo |
| Approval status of the design decisions | Assume a reference the user names is authorized as this run's input, not that its decisions are approved. Mark an expected value `approved` only when the user or an authoritative project source marks that decision approved, citing the approver or `approver unknown`; otherwise mark it `approval unknown`, and say so in the log | user, reference |

## Workflow
1. **Inspect the project.** Read the spec, token files, Storybook stories if any, and the relevant routes and component code. Record the reference version and the build or commit reviewed, or `version unknown`. Do not copy personal data from screenshots or fixtures.
2. **Build the coverage matrix:** screens by breakpoints by states (default, hover, focus, disabled, loading, empty, error). Mark each cell checked, not reachable, or not provided.
3. **Compare each checked cell** across layout and spacing, typography, color and tokens, iconography, component variants, interaction states, copy, responsive behavior, and motion. Prefer evidence that is measurable: computed styles, token names in code, or annotated screenshots.
4. **Log verified mismatches** only with an expected value cited from the reference. Fields: id, screen, breakpoint, element, expected with its source and its approval (`approved` or `approval unknown`), actual with evidence, type, severity from `../_shared/standard.md` §8 (Blocker, Major, Minor, Cosmetic), confidence (High, Medium, Low), and repro steps another person can follow. Values read from code or computed styles are verified. Sizes estimated from a description or an image are unverified.
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

Figma (optional, per `../_shared/figma.md`): when publishing is enabled, draw on the `Design QA` page the coverage matrix and one card per verified mismatch, grouped by severity, each with its screen or component, expected value and source, actual value and evidence path, confidence, repro steps, and recommended fix; then the unverified differences, spec gaps, and the Not checked list as separate groups. Never draw a screenshot, never show an unverified difference as a defect, and never draw a mismatch that is not in the Markdown. The Markdown file stays the source of truth.

`## Next step` names exactly one handoff, the first condition below that fits, and writes only that skill: `design-documentation` to close spec gaps, `design-system-audit` when mismatches trace to shared components or tokens, or `ux-audit` for usability issues seen along the way.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] Chat replies follow `../_shared/personality.md`; no emoticons in written files or structured output
- [ ] Every verified mismatch cites an expected value from the reference the user named or that is marked approved, and states whether that value is `approved` or `approval unknown`; no value is called approved without a mark from the user or an authoritative source
- [ ] Differences without a reference are in the unverified section, not the defect log
- [ ] Severity uses only the shared scale; confidence is separate
- [ ] Unreachable and unprovided states are marked not checked, never passed
- [ ] Repro steps work without the designer present
- [ ] No usability opinions in the defect log
- [ ] Any Figma output followed `../_shared/figma.md`, and the reply reports only Figma results a tool confirmed

## Boundaries
- Does not evaluate usability → `ux-audit`
- Does not give subjective design feedback → `design-critique`
- Does not audit the system itself → `design-system-audit`
- Does not write the spec → `design-documentation`
