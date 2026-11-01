# Example: product-metrics

> **Illustrative example.** All inputs and outputs below use invented sample data to show the output shape. Kettle is a fictional meal-kit subscription app; the events, counts, and definitions are hypothetical.

## Prompt

```
/product-metrics Goal: fewer subscribers cancel when they only want a break. Define how we measure the pause MVP. Events are in src/analytics.ts and last month's export is analytics/subscription-month.csv.
```

## Sample input (invented)

`src/analytics.ts` emits: `deliveries_page_view` (Deliveries page), `skip_confirmed` (skip dialog confirm), `subscription_cancelled` with property `reason_code` (cancel flow). No pause events exist.

`analytics/subscription-month.csv`, one month (month not stated):

```
metric,value
active_subscriptions_start,2000
subscription_cancelled,180
cancelled_reason_break,27
skip_confirmed,496
```

The decision the metrics inform was not stated, and no answer came to the one question asked.

## What the skill does

1. Lists existing events with the file that emits them. Asks one question about the decision; with no answer, assumes it is which candidate to build first and tags it.
2. Defines each metric with every field, or marks it not yet defined.
3. Builds a small metric tree with guardrails, specifies the new events, and assesses data quality.
4. Reports observed values only from the export, labels targets and estimates apart, and states interpretation limits.

## Output shape (`design/metrics/product-metrics-break-retention-<YYYY-MM-DD>.md`)

```markdown
> skill: product-metrics · date: <YYYY-MM-DD> · scope: pause MVP · sources: src/analytics.ts (date unknown), analytics/subscription-month.csv (one month, month not stated)

## Decision and goal
Goal: fewer subscribers cancel when they only want a break [reported: user]. Decision: which candidate to build first, pause or other retention work [assumption: the skill's default; the decision was asked once and not answered]. Decision owner: unknown.

## Metric definitions (purpose, formula, unit, population, window, segments, source, status)
| Metric | Purpose | Formula | Unit | Population | Window | Segments | Source | Status |
|---|---|---|---|---|---|---|---|---|
| Break-reason cancellation rate (primary) | Track the goal directly | subscriptions cancelled with reason_code = break ÷ active subscriptions at window start | % | Active subscriptions at window start | Calendar month | Plan size | `subscription_cancelled.reason_code` | Existing |
| Pause adoption | Shows whether pause is used | subscriptions with ≥1 `pause_started` ÷ active subscriptions at window start | % | Same | Calendar month | Pause length | `pause_started` | Proposed |
| Resume rate | Shows paused subscribers come back | pauses ending in a delivery ÷ pauses ended in window | % | Pauses ended in window | Calendar month | Pause length | `pause_resumed` | Proposed |
| Total cancellation rate (guardrail) | Pause must not just move cancellations later | all `subscription_cancelled` ÷ active subscriptions at window start | % | Same | Calendar month | — | `subscription_cancelled` | Existing |

## Metric tree
- Goal: fewer break-driven cancellations
  - Primary: break-reason cancellation rate
    - Input: pause adoption (`pause_started`)
    - Input: resume rate (`pause_resumed`)
  - Guardrail: total cancellation rate
Proxy note: reason_code is self-reported at cancellation and misses subscribers who choose another reason.

## Guardrails and unintended consequences
- Total cancellation rate must not rise: pause could delay a cancellation instead of preventing it.
- Gaming: pushing pause hard in the cancel flow could raise adoption without retention. Watch resume rate alongside adoption.

## Instrumentation and data quality
| Event | Trigger | Properties | Screen | Owner | Status |
|---|---|---|---|---|---|
| `pause_started` | Pause confirmed | weeks (1 to 4) | Deliveries | owner unknown | Proposed |
| `pause_resumed` | First delivery after a pause | weeks_paused | Billing job | owner unknown | Proposed |
No personal identifiers in properties; subscription ID is used only for joining and follows existing consent [assumption: consent setup not inspected].
Data quality: reason_code depends on what the subscriber selects (Medium confidence); the export's month is not stated (Low confidence for trend use); no bot or duplicate handling is documented.

## Observed values (supplied data only)
From analytics/subscription-month.csv, one month, month not stated:
- Break-reason cancellation rate: 27 ÷ 2,000 = 1.35%.
- Total cancellation rate: 180 ÷ 2,000 = 9.0%.
- Break-reason share of cancellations: 27 ÷ 180 = 15%.
Pause adoption and resume rate: No data available; the events do not exist yet.

## Targets and estimates (labeled)
No target was supplied. Any target is for the decision owner to set; none is proposed here.

## Interpretation limits
- One month is a baseline candidate, not a trend.
- A fall in break-reason cancellations after launch would follow the release, not prove it caused the fall; seasonality and other changes could explain it. A holdout would be needed for a causal claim.

## Open questions / to validate
- What decision will these numbers inform, and who owns it?
- Which month does the export cover?
- Who owns the new events?

## Next step
Run `ux-research-planner` to design a holdout comparison, since a causal reading of pause needs one.
```
