---
name: design-system-audit
description: Audit design tokens, components, and patterns for consistency, duplication, and adoption across code and design files. Use when the user says "design system audit", "component inventory", "token drift", "how consistent is our UI", "which components are unused".
---

# Design System Audit

## Purpose
Produce an inventory of tokens, components, and patterns as they actually exist in the codebase and design sources, flag drift and duplication, and recommend consolidation. Observed from files, never from assumptions about intent.

## Triggers
- "Audit the design system", "inventory components", "find hardcoded colors"
- Before adopting or migrating a component library
- Visual inconsistency reported without a known cause

## Inputs
| Input | Required | Source |
|---|---|---|
| Codebase paths for UI (components, styles, tokens) | yes | repo inspection |
| Design source (tokens export, Figma variables, style guide) | optional | user, `design/` |
| Scope (tokens, components, patterns, or all) | yes | user (default all) |

## Workflow
1. **Inspect the project.** Locate token files, theme config, component directories, global styles. Record paths.
2. **Token inventory.** Colors, type, spacing, radius, shadow, motion: defined tokens vs hardcoded values found by search. Count occurrences per hardcoded value.
3. **Component inventory.** Table: component, path, variants, props, usage count, duplicates (same role, different name).
4. **Pattern inventory.** Recurring compositions (forms, tables, dialogs, empty states): where implemented, consistent or divergent.
5. **Compare to design source** if provided: tokens or components in design but not code, and vice versa.
6. **Score**: adoption (tokenized vs hardcoded ratio), duplication count, coverage of common patterns. Only from counted data.
7. **Recommend** consolidation steps ordered by impact and effort.
8. **Write output**; show scores and top duplicates in chat.

## Outputs
`design/audits/design-system-audit-<date>.md`:
```
> metadata block (paths scanned)
## Token inventory and drift
## Component inventory and duplicates
## Pattern inventory
## Design-to-code gaps
## Scores (with counts)
## Recommendations
## Open questions / to validate
## Next step
```

## Quality checks
- [ ] Global checks in `docs/ARCHITECTURE.md` §7
- [ ] All counts come from actual searches; commands or paths noted
- [ ] Duplicates listed with both paths
- [ ] Scores derived from inventory numbers shown in the doc
- [ ] No recommendation to adopt a specific external library without user request

## Boundaries
- Does not evaluate usability → `ux-audit`
- Does not verify a build matches a design → `design-qa`
- Does not write component docs → `design-documentation`
