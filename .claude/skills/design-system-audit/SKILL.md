---
name: design-system-audit
description: Audit the design system as it exists in code and design sources - tokens, components, variants, typography, spacing, color, states, naming, accessibility, and documented usage - separating real inconsistencies from intentional variants, with coverage limits stated. Use when the user says "design system audit", "component inventory", "token drift", "how consistent is our UI", "which components are unused". Not for usability review (use `ux-audit`), checking one build against one spec (use `design-qa`), or writing component documentation (use `design-documentation`).
---

# Design System Audit

## Purpose
Inventory what the design system actually is, from files, and report where it is inconsistent, duplicated, undocumented, or unused. A difference counts as an inconsistency only if nothing shows it is intended. The audit does not assume a system exists, and it says exactly what it scanned.

## Triggers
- "Audit the design system", "inventory components", "find hardcoded colors"
- Before adopting or migrating a component library
- Visual inconsistency is reported without a known cause

## Inputs
| Input | If missing | Source |
|---|---|---|
| UI code paths: components, styles, theme or token files | Stop: nothing to audit | repo |
| Design source: token export, Figma variables, style guide | Assume none; skip design-to-code comparison and say so | user, `design/` |
| Scope: tokens, components, patterns, or all | Assume all and list what was reachable | user |
| Documented usage rules, if any | Assume none exist | repo docs, Storybook |

## Workflow
1. **Inspect the project.** Locate token and theme files, component directories, global styles, documentation, and Storybook. Record paths scanned and excluded, file types covered, and the commit audited or `version unknown`. If no tokens or shared components exist, say so. Then inventory repeated hardcoded values and near-duplicate components as candidates, not as a system.
2. **Inventory tokens** (color, type, spacing, radius, shadow, motion): defined tokens, hardcoded values found by search, and each with its occurrence count and file references. Record the search used.
3. **Inventory components:** name, path, variants, props, states handled, accessibility attributes, documented usage, usage count, and duplicates (same role, different name) with both paths.
4. **Inventory recurring patterns** (forms, tables, dialogs, empty states) and whether each is implemented consistently.
5. **Classify each difference:** *inconsistency* if no rationale appears in code, comments, docs, naming, or design source; *intentional variant* if a rationale does; *unclear* if neither. For unclear cases, record the question for the owner rather than deciding.
6. **Compare with the design source** if provided: items in design but not in code, and the reverse.
7. **Report measures as counts with the method** (for example tokenized versus hardcoded color values). Derive no score that cannot be recomputed from the doc.
8. **Prioritize recommendations** by impact and effort, each with a severity from `../_shared/standard.md` §8 (Blocker, Major, Minor, Cosmetic) for its finding and a confidence (High, Medium, Low). Write the output per §8.

## Outputs
Metadata block (§4), then path, date, collisions, and reruns (§8), follow `../_shared/standard.md`. File:
`design/audits/design-system-audit-<date>.md`:
```
> metadata block (paths scanned, commit audited)
## Scope and coverage
## Token inventory and drift
## Component inventory and variants
## Pattern inventory
## Design-to-code gaps
## Findings (classification, severity, confidence)
## Measures (counts with method)
## Recommendations (prioritized)
## Open questions / to validate
## Next step
```
Figma (optional, per `../_shared/figma.md`): when publishing is enabled, draw token swatches, the component inventory, and findings as documentation frames on the `Design System Audit` page. Never create or change variables, styles, or components in the Figma file, and never draw a token value, occurrence count, or component that is not in the Markdown or show an intentional variant or unclear difference as an inconsistency. The Markdown file stays the source of truth.

`## Next step` names exactly one handoff, the first condition below that fits, and writes only that skill: `design-qa` to verify fixes in a build, or `design-documentation` to document components and usage.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] Chat replies follow `../_shared/personality.md`; no emoticons in written files or structured output
- [ ] Coverage states paths scanned, paths excluded, and what could not be reached
- [ ] All counts come from searches that are recorded or reproducible
- [ ] Each finding is classified inconsistency, intentional variant, or unclear
- [ ] Duplicates list both paths; findings cite the file or token
- [ ] No design system is assumed; absence is reported as absence
- [ ] No recommendation to adopt a specific external library unless the user asked
- [ ] Any Figma output followed `../_shared/figma.md`, and the reply reports only Figma results a tool confirmed

## Boundaries
- Does not evaluate usability → `ux-audit`
- Does not check one build against one spec → `design-qa`
- Does not write component documentation → `design-documentation`
