---
name: ux-audit
description: Heuristic and accessibility review of a product, flow, or set of screens, producing findings with evidence, affected task, severity, confidence, and a recommendation, and stating what was not inspected. Use when the user says "UX audit", "heuristic evaluation", "review the UX", "accessibility review", "what's wrong with this flow". Not for build-versus-design defects (use `design-qa`), feedback on a single proposal against its goals (use `design-critique`), or token and component consistency (use `design-system-audit`).
---

# UX Audit

## Purpose
Evaluate an experience against usability heuristics and accessibility criteria, and log what was actually observed. Each finding says what is wrong, where, for whom, how bad, how sure the evidence is, and what to do. The audit also says what it did not inspect, so no one reads partial coverage as a clean bill of health.

## Triggers
- "Audit X", "heuristic review", "accessibility check", "why is this confusing"
- A baseline before a redesign, or a review after launch
- Usability test findings exist and the team wants fuller coverage

## Inputs
| Input | If missing | Source |
|---|---|---|
| Subject: build or URL, screenshots, design files, or code | Stop: nothing to evaluate | user, repo, browser only if available |
| Scope: flows and screens to cover | Assume the supplied material is the scope and state it | user |
| Heuristic set | Assume Nielsen's 10 heuristics and WCAG 2.2 AA as defaults; the user may override | user |
| Users and tasks the subject serves | Assume from the repo or evidence and tag them | `design/research/`, repo |
| Prior audits and test results | Assume none | `design/audits/`, `design/research/` |

## Workflow
1. **Inspect the project.** Read prior audits, test results, and design system docs, and skip what is already logged. Record the commit or build evaluated (for example `git rev-parse --short HEAD`) or `version unknown`. Do not transcribe personal data visible in screenshots or fixtures.
2. **Define coverage.** List the screens, states, and flows in scope, then the ones actually inspected. Every claim of coverage uses these two numbers.
3. **Inspect each screen** and record what is shown and what the user can do. Use a browser or running build only if one is available and was used. Say so in the method.
4. **Inspect code when available.** Where feasible, read routes, accessible names (labels, `alt`, ARIA), semantic elements versus clickable `div`s, heading and landmark structure, focus handling, interaction states (hover, focus, disabled, loading, error, empty), and user-facing copy. Findings from code are `[inferred]` about runtime behavior until seen running.
5. **Log findings.** One row each: observed issue, location, affected user and task, heuristic or criterion, evidence with source, severity, confidence, recommendation. Severity is from `../_shared/standard.md` §8 (Blocker, Major, Minor, Cosmetic) and rates impact on the task. Confidence (High, Medium, Low) rates the evidence and is separate.
6. **Run the accessibility pass.** Report a contrast ratio only if it was computed from known color values. List checks that need tools or a live build as not verified, never as passing.
7. **Separate hypotheses.** Suspected issues without direct evidence go in as `Hypothesis` rows, unrated, with the way to validate them. Group repeated issues into systemic patterns only when several findings support the pattern.
8. **State what was not inspected,** and write the output per §8.

## Outputs
Metadata block (§4), then path, date, collisions, and reruns (§8), follow `../_shared/standard.md`. File:
`design/audits/ux-audit-<scope>-<date>.md`:
```
> metadata block (build or commit, coverage as inspected of in scope)
## Method and heuristic set
## Findings table (status, location, affected task, criterion, evidence, severity, confidence, recommendation)
## Accessibility findings
## Systemic patterns
## Not verified / out of scope
## Open questions / to validate
## Next step
```
Figma (optional, per `../_shared/figma.md`): when publishing is enabled, draw one frame on the `UX Audit` page with a card per finding (location, severity, confidence, recommendation) and a coverage card that keeps the not-inspected list. Never draw a finding, severity, or location that is not in the Markdown, never show an unverified accessibility check as passed, and never transcribe personal data from screenshots. The Markdown file stays the source of truth.

`## Next step` names exactly one handoff, the first condition below that fits, and writes only that skill: `design-qa` once fixes are built, `usability-test-planner` to validate hypotheses with users, or `design-system-audit` when patterns point to shared components.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] Chat replies follow `../_shared/personality.md`; no emoticons in written files or structured output
- [ ] Every finding has a location, evidence with a source, severity, and confidence
- [ ] Severity uses only Blocker, Major, Minor, Cosmetic; confidence is a separate column
- [ ] Observed issues, hypotheses, and uninspected areas are visibly separate
- [ ] Coverage is stated as inspected of in scope; no claim of full coverage otherwise
- [ ] Code-derived findings are marked as inferred until observed running
- [ ] Unverified accessibility checks are listed, not assumed to pass
- [ ] Any Figma output followed `../_shared/figma.md`, and the reply reports only Figma results a tool confirmed

## Boundaries
- Does not log build-versus-design differences → `design-qa`
- Does not critique one proposal against its goals → `design-critique`
- Does not audit tokens or component consistency → `design-system-audit`
- Does not plan tests with users → `usability-test-planner`
