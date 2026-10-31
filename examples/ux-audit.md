# Example: ux-audit

## Prompt

```
/ux-audit Checkout flow, screenshots in design/inputs/checkout/*.png. Cover cart through confirmation.
```

## What the skill does

1. Reads prior audits in `design/audits/` and the design system docs.
2. Walks each screenshot, records what is shown and what the user can do.
3. Logs findings against Nielsen heuristics and WCAG 2.2 AA with severity 0 to 4.
4. Lists what could not be verified from static images (focus order, contrast ratios).

## Output shape (`design/audits/ux-audit-checkout-2026-11-01.md`)

```markdown
> skill: ux-audit · date: 2026-11-01 · scope: cart → confirmation (4 of 4 screens) · sources: design/inputs/checkout/*.png

## Findings table
| id | location | heuristic | evidence | sev | fix |
|---|---|---|---|---|---|
| F1 | Payment, card field | Error prevention | No inline format hint; error appears only on submit [observed: payment.png] | 3 | Add input mask and inline validation |
| F2 | Cart, remove item | Visibility of system status | No confirmation after removal [observed: cart.png] | 2 | Toast with undo |

## Accessibility findings
| id | criterion | evidence | status |
|---|---|---|---|
| A1 | 1.4.3 Contrast | Secondary button text on grey [observed: cart.png] | Not verified: need computed ratio |

## Not verified / out of scope
- Keyboard focus order (static screenshots).

## Next step
Run `design-qa` once fixes land in staging.
```
