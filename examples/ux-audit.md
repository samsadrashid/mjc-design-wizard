# Example: ux-audit

> **Illustrative example.** All inputs and outputs below use invented sample data to show the output shape. The screens and findings are hypothetical and come from no real product.

## Prompt

```
/ux-audit Checkout flow. I attached cart.png and payment.png in checkout-screens/. Cover cart through confirmation.
```

## Sample input (invented)

- `checkout-screens/cart.png`: a cart with two items, a quantity stepper (− and +), an icon-only remove control, a primary "Checkout" button, and a grey secondary "Continue shopping" button. The annotation on the file gives the secondary text color as `#9AA0A6` on `#FFFFFF`.
- `checkout-screens/payment.png`: a card form with number, expiry, and CVC fields, each labeled only by placeholder text, and a Pay button.
- In scope: cart, payment, confirmation (3 screens). No confirmation screen, build, or code was provided. No prior audits exist.

## What the skill does

1. Checks `design/audits/` and `design/research/` for prior work and the repo for design system docs. None found in this sample.
2. Defines coverage: 3 screens in scope, 2 inspected. Records the build as `version unknown`.
3. Walks each screenshot, logs findings with location, affected task, criterion, evidence, severity, and a separate confidence.
4. Computes contrast only from the stated color values, and lists what static images cannot show as not verified.

## Output shape (`design/audits/ux-audit-checkout-<YYYY-MM-DD>.md`)

```markdown
> skill: ux-audit · date: <YYYY-MM-DD> · scope: cart to confirmation · coverage: 2 of 3 screens inspected · build: version unknown (screenshots only) · sources: checkout-screens/cart.png, checkout-screens/payment.png

## Method and heuristic set
Nielsen's 10 heuristics and WCAG 2.2 AA (defaults; no override given), applied to two static screenshots. No browser, build, or code was used. Severity: Blocker, Major, Minor, Cosmetic, rating impact on the task. Confidence (High, Medium, Low) rates the evidence and is separate.

## Findings table (status, location, affected task, criterion, evidence, severity, confidence, recommendation)
| id | status | location | affected task | criterion | evidence | severity | confidence | recommendation |
|---|---|---|---|---|---|---|---|---|
| F1 | Observed | Payment, card fields | Enter card details | Nielsen: recognition rather than recall; WCAG 3.3.2 Labels or instructions | Fields are labeled only by placeholder text, which disappears on input [observed: payment.png] | Major | High | Add persistent visible labels above each field |
| F2 | Observed | Payment, card number field | Enter card details | Nielsen: error prevention | No format hint or digit grouping is shown [observed: payment.png] | Minor | Medium | Group digits as typed and show the expected format |
| F3 | Observed | Cart, remove control | Change cart contents | Nielsen: visibility of system status | Control is an icon with no visible label [observed: cart.png] | Minor | Medium | Add a text label; keep the icon |
| H1 | Hypothesis (unrated) | Cart, remove control | Change cart contents | Nielsen: user control and freedom | Whether removal can be undone is not visible in a static image [assumption] | — | Low | Validate in a build or a task-based test |

## Accessibility findings
| id | criterion | evidence | status |
|---|---|---|---|
| A1 | 1.4.3 Contrast (minimum) | "Continue shopping" text `#9AA0A6` on `#FFFFFF`: computed ratio 2.6:1 from the annotated values, below 4.5:1 for normal text [observed: cart.png annotation] | Fails; severity Major (secondary path hard to read), confidence High |
| A2 | 2.5.8 Target size (minimum) | Quantity stepper buttons look small [observed: cart.png] | Not verified: pixel dimensions not available |
| A3 | 1.3.1 Info and relationships; 4.1.2 Name, role, value | Accessible names of fields and the remove control cannot be read from an image | Not verified: needs code or a screen reader on a build |

## Systemic patterns
- Controls and fields that rely on placeholder or icon alone appear on both screens [inferred: F1, F3]. Two screens and two findings make this a hypothesis to check across the flow, not an established pattern.

## Not verified / out of scope
- Confirmation screen: in scope but not provided (1 of 3 screens).
- Keyboard focus order, screen reader names, motion, and error messages: not testable from static images.
- Loading, error, empty-cart states and responsive layouts: not shown.

## Open questions / to validate
- Can the confirmation screen and a running build be provided?
- Does removing an item offer undo? (H1)
- Do the screenshots match what is live?

## Next step
Run `usability-test-planner` to test card entry and item removal with users, since F1 and H1 concern task completion.
```

Contrast check (reproducible): relative luminance of `#9AA0A6` is 0.348 and of `#FFFFFF` is 1.000 (WCAG 2.x formula), so (1.000 + 0.05) ÷ (0.348 + 0.05) = 2.64, reported as 2.6:1.
