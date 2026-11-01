# Example: problem-framing

> **Illustrative example.** All inputs and outputs below use invented sample data to show the output shape. Nothing here comes from a real product, study, or dataset.

## Prompt

```
/problem-framing Stakeholders want a "dashboard" on the home screen. Support tickets in support/export.csv mention users can't find their recent orders.
```

## Sample input (invented)

`support/export.csv`, 5 rows, date unknown:

```
ticket_id,subject,tag
T-1,Where is my last order?,orders
T-2,Can't find order status,orders
T-3,Refund policy question,billing
T-4,How do I see my recent order,orders
T-5,Password reset email late,account
```

The stakeholder request is stated in the prompt. No navigation docs or analytics are provided.

## What the skill does

1. Reads README, `design/discovery/`, and `support/export.csv`. Finds no prior statement.
2. Splits the request into symptom, problem, and proposed solution, and tags each cell.
3. Writes one statement with no solution words. The evidence is thin, so the statement is marked Provisional.
4. Lists supporting evidence and assumptions under the statement, ranks HMWs, and states what would falsify the framing.

## Output shape (`design/discovery/problem-framing-recent-orders-<YYYY-MM-DD>.md`)

```markdown
> skill: problem-framing · date: <YYYY-MM-DD> · scope: home screen request · sources: support/export.csv (sample, 5 rows, date unknown), stakeholder request in prompt

## Symptom / problem / solution split
| Symptom | Problem | Proposed solution |
|---|---|---|
| 3 of 5 sample tickets ask where an order is: T-1, T-2, T-4 [observed: support/export.csv, tag=orders] | Customers cannot quickly reach an order they placed [inferred: from the three ticket subjects] | A home screen "dashboard" [reported: stakeholders, in the prompt] |

## Problem statement
**Provisional, Low confidence.** Customers who have placed an order need to reach it without help, because three of five sampled tickets ask where an order is [observed: T-1, T-2, T-4]. Today the path to an order is unknown [assumption: navigation not inspected], which causes at least some customers to contact support [observed: same tickets].

Supporting evidence:
- T-1, T-2, T-4 subjects ask where an order or its status is [observed: support/export.csv] · confidence Low: five rows, no dates, no volume.

Assumptions the statement depends on:
- The five rows are representative of ticket volume [assumption].
- The difficulty is reaching the order, not missing status detail inside it [assumption].

Rejected alternatives:
- Framing the need as a home screen dashboard: rejected because it names a solution, and no evidence says customers look for orders on the home screen.
- Framing it as general account discoverability: rejected because only order lookup appears in the evidence.

## Affected user and context
Customers with at least one order [inferred: the tickets ask about an existing order]. Whether they are first-time or returning buyers is not in the export [assumption].

## How might we (ranked)
1. HMW let a customer reach their latest order without contacting support? (chosen: narrow, testable, closest to the evidence)
2. HMW reduce the need to check order status at all? (broader; needs shipping data)
3. HMW make account content easier to discover? (broadest; weakest link to the evidence)

## Success definition (with baseline or "none")
Qualitative: customers locate an order without contacting support.
Quantitative: Baseline: none. The sample has five rows and no period, so it gives no rate. A dated full ticket export, or an analytics event for order views, would provide one.

## What would falsify this
- A full, dated ticket history in which order-lookup tickets are a small share of volume.
- Tickets showing customers reach the order but cannot read its status.

## Open questions / to validate
- How are orders reached today, and in how many steps?
- What share of all tickets concern order lookup, over what period?
- Is the cause discoverability or missing status information?

## Next step
Run `ux-research-planner` to plan how to confirm the framing, since the evidence is five undated tickets.
```
