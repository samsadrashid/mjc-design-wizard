---
name: ux-audit
description: Heuristic and accessibility review of a live product, prototype, or design files, producing severity-rated findings with evidence and fixes. Use when the user says "UX audit", "heuristic evaluation", "review the UX", "accessibility review", "what's wrong with this flow".
---

# UX Audit

## Purpose
Systematically evaluate an experience against usability heuristics and accessibility criteria, logging each finding with location, evidence, severity, and a recommended fix. Findings describe what was observed, never what users "would" feel.

## Triggers
- "Audit X", "heuristic review", "accessibility check", "why is this confusing"
- Pre-redesign baseline or post-launch review
- Usability test identified issues and the team wants full coverage

## Inputs
| Input | Required | Source |
|---|---|---|
| Subject: URL, build, screenshots, or design files | yes | user, browser if available |
| Scope: flows or screens to cover | yes | user |
| Heuristic set | optional | default: Nielsen 10 + WCAG 2.2 AA |
| Known issues, prior audits | optional | `design/audits/` |

## Workflow
1. **Inspect the project.** Read prior audits, test results, design system docs. Note what to skip (already logged).
2. **Walk the scope** screen by screen. For each, record: what is shown, what the user can do, what happened on key actions. Screenshots or text descriptions as evidence.
3. **Evaluate against heuristics.** For each finding: heuristic violated, location, evidence, severity (0 to 4: cosmetic, minor, major, critical, blocker), fix.
4. **Accessibility pass**: contrast, focus order, keyboard reach, labels, alt text, target size, motion. Mark what could not be verified without tools.
5. **Group findings** into systemic patterns (e.g. inconsistent error handling) vs one-offs.
6. **Score coverage**: screens examined vs scope.
7. **Write output**; show counts by severity and top five findings in chat.

## Outputs
`design/audits/ux-audit-<scope>-<date>.md`:
```
> metadata block (scope coverage)
## Method and heuristic set
## Findings table (id, location, heuristic, evidence, severity, fix)
## Accessibility findings
## Systemic patterns
## Not verified / out of scope
## Open questions / to validate
## Next step
```

## Quality checks
- [ ] Global checks in `docs/ARCHITECTURE.md` §7
- [ ] Every finding has location and observable evidence
- [ ] Severity uses the defined scale consistently
- [ ] No claims about user behavior without research citation
- [ ] Unverifiable accessibility checks listed, not assumed passing

## Boundaries
- Does not log design-vs-build mismatches → `design-qa`
- Does not check token or component consistency → `design-system-audit`
- Does not critique a proposal in review → `design-critique`
