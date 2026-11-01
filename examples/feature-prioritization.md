# Example: feature-prioritization

> **Illustrative example.** All inputs and outputs below use invented sample data to show the output shape. The notes, export, estimates, and scores are hypothetical.

## Prompt

```
/feature-prioritization Goal: reduce checkout drop-off. Rank these for next quarter: saved carts, guest checkout, address autocomplete, order tracking map. Notes are in design/research/notes.md and the funnel export in analytics/checkout-month.csv. Engineering estimates, in person-weeks: guest checkout 3, saved carts 5, address autocomplete 2, order tracking map 8. Our support lead says address typos cause some redeliveries.
```

## Sample input (invented)

`design/research/notes.md`, 4 participants, date unknown:

- P1: stopped at the account creation step and left.
- P2: stopped at account creation and left.
- P3: completed checkout; said they wished the cart was still there when they came back.
- P4: completed checkout; no related comments.

`analytics/checkout-month.csv`, one month of sessions (month not stated in the file):

```
step,sessions
cart_viewed,5000
account_step_reached,4000
address_step_reached,3200
order_placed,2600
```

The export has no data on returning carts or on order tracking.

## What the skill does

1. Reads `design/research/` and `analytics/` for evidence per candidate, with dates or `date unknown`.
2. Normalizes candidates as outcomes and defines RICE scales.
3. Records each input with value, source, basis, and confidence. Missing inputs stay `Missing`; no value is substituted.
4. Ranks only complete candidates. Candidates with a missing factor go to an unranked provisional tier, with a labeled scenario table where one factor is missing.

## Output shape (`design/planning/prioritization-next-quarter-<YYYY-MM-DD>.md`)

```markdown
> skill: feature-prioritization · date: <YYYY-MM-DD> · scope: 4 candidates · sources: design/research/notes.md (sample, date unknown), analytics/checkout-month.csv (sample, one month, month unknown), engineering estimates and support lead remark in prompt

## Goal and framework (scales defined)
Goal: reduce checkout drop-off [reported: user, in the prompt].
Framework: RICE (default), score = Reach × Impact × Confidence ÷ Effort.
- Reach: sessions per month that reach the step the candidate changes, from the export.
- Impact, 1 to 3: 3 removes a step where users were seen leaving; 2 addresses a wish stated by a user; 1 reduces friction with no observed drop-off.
- Confidence: High 100%, Medium 80%, Low 50% (default mapping). A candidate's Confidence is the lowest confidence among its Reach and Impact inputs.
- Effort: person-weeks as estimated by engineering.
The ranking supports a decision; it does not replace judgment.

## Normalized candidates
1. Guest checkout: customers can pay without creating an account.
2. Saved carts: customers return to a cart they left.
3. Address autocomplete: customers enter a delivery address with fewer errors.
4. Order tracking map: customers see delivery progress after ordering.

## Scoring table (factor, value, source, basis, confidence)
| Candidate | Factor | Value | Source | Basis | Confidence |
|---|---|---|---|---|---|
| Guest checkout | Reach | 4,000 | account_step_reached [observed: checkout-month.csv] | measured (one month) | High |
| Guest checkout | Impact | 3 | P1, P2 left at account creation [observed: notes.md] | hypothesis | Medium |
| Guest checkout | Effort | 3 | Engineering [reported: prompt] | stakeholder estimate (engineering) | Medium |
| Saved carts | Reach | Missing | No returning-cart data in the export | — | — |
| Saved carts | Impact | 2 | P3 wished the cart was kept [observed: notes.md] | hypothesis | Low |
| Saved carts | Effort | 5 | Engineering [reported: prompt] | stakeholder estimate (engineering) | Medium |
| Address autocomplete | Reach | 3,200 | address_step_reached [observed: checkout-month.csv] | measured (one month) | High |
| Address autocomplete | Impact | 1 | Support lead: typos cause some redeliveries [reported: prompt]; no drop-off at this step in the notes | stakeholder estimate (support lead) | Low |
| Address autocomplete | Effort | 2 | Engineering [reported: prompt] | stakeholder estimate (engineering) | Medium |
| Order tracking map | Reach | Missing | No tracking data in the export | — | — |
| Order tracking map | Impact | Missing | Nothing in the notes concerns tracking | — | — |
| Order tracking map | Effort | 8 | Engineering [reported: prompt] | stakeholder estimate (engineering) | Medium |

## Ranking and sensitivity (complete scores, provisional tier, scenarios)
Complete candidates:
| Rank | Candidate | Calculation | Score |
|---|---|---|---|
| 1 | Guest checkout | 4,000 × 3 × 0.8 ÷ 3 | 3,200 |
| 2 | Address autocomplete | 3,200 × 1 × 0.5 ÷ 2 | 800 |

Provisional tier (unranked, no point score):
- Saved carts: missing Reach.
- Order tracking map: missing Reach and Impact.

Scenarios, not estimates. Saved carts with Reach set to placeholder values taken from the known Reach values (3,200 and 4,000), Impact 2, Confidence Low 50%, Effort 5:
| Scenario Reach | Calculation | Scenario score |
|---|---|---|
| 3,200 | 3,200 × 2 × 0.5 ÷ 5 | 640 |
| 4,000 | 4,000 × 2 × 0.5 ÷ 5 | 800 |
Saved carts could sit at or below autocomplete; the placeholders are not data. No scenario is shown for the tracking map: with two factors missing, a range would say nothing.

Sensitivity (complete rows): autocomplete overtakes guest checkout only if its Impact is shown to be 3 at Medium confidence (3,200 × 3 × 0.8 ÷ 2 = 3,840). Guest checkout stays first even at Impact 1 (4,000 × 1 × 0.8 ÷ 3 = 1,067). Four participants cannot settle either.

Not in the formula: guest checkout depends on the payment provider supporting guest orders [assumption]; the tracking map depends on courier data access [assumption].

## Now / next / later / drop
- Now: guest checkout. Highest complete score, and the drop-off evidence is the strongest available.
- Next: address autocomplete. Complete but Low confidence; cheap to validate.
- Later: saved carts and order tracking map. Provisional; neither can be "now" on score alone.
- Drop: none. Missing data is not evidence against a candidate.

## Inputs to verify
1. Reach for saved carts: sessions that return to an abandoned cart.
2. Reach and impact for the tracking map.
3. Autocomplete impact: redelivery rate linked to address errors (would move rank 2 above rank 1 if Impact reached 3).

## Open questions / to validate
- Can the payment provider accept guest orders? [assumption]
- Are four participants representative of customers who abandon at the account step? [assumption]
- Which month does the export cover?

## Next step
Run `product-metrics` to define the reach measures missing for saved carts and the tracking map.
```
