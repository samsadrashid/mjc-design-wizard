# Example: problem-framing

## Prompt

```
/problem-framing Stakeholders want a "dashboard" on the home screen. Support tickets in support/export.csv mention users can't find their recent orders.
```

## What the skill does

1. Reads README, `design/discovery/`, and `support/export.csv`.
2. Splits the request: symptom (tickets), problem (recent orders not findable), proposed solution (dashboard).
3. Writes one problem statement with no solution words.
4. Drafts HMWs, success definition, falsification criteria.

## Output shape (`design/discovery/problem-framing-recent-orders-2026-11-01.md`)

```markdown
> skill: problem-framing · date: 2026-11-01 · scope: home screen request · sources: support/export.csv, README.md

## Symptom / problem / solution split
| Symptom | Problem | Proposed solution |
|---|---|---|
| 14 tickets mention "where are my orders" [observed: support/export.csv] | Recent orders not reachable from home | Dashboard [reported: stakeholder request] |

## Problem statement
Returning customers need to reach their most recent order quickly because they check status
repeatedly after purchase [observed: ticket text]. Today the orders list sits three taps deep
under Account [observed: app navigation], which causes repeated support contacts.

## How might we (ranked)
1. HMW surface the latest order where returning users land? (chosen: narrow, testable)
2. HMW reduce the need to check status at all?
3. HMW make account content discoverable?

## Success definition
Qualitative: returning users locate their latest order without support.
Quantitative: Baseline: none measured. See `product-metrics`.

## What would falsify this
Tickets come from first-time buyers rather than returning users [assumption: segment not in export].

## Open questions / to validate
- Are ticket authors returning customers? Need user IDs joined to orders.

## Next step
Run `product-metrics` to define a baseline for order lookup.
```
