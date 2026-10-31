---
name: product-metrics
description: Define a metric tree, instrumentation spec, and reporting plan for a product goal, and read existing analytics only when data is provided. Use when the user says "metrics", "how do we measure", "KPIs", "what events to track", "success metrics", "instrumentation".
---

# Product Metrics

## Purpose
Connect a product goal to measurable signals: a north-star and supporting metrics, the events needed to compute them, and how they will be reviewed. Reports numbers only from data the user supplies.

## Triggers
- "Define metrics for X", "what should we track", "set up analytics events"
- Problem framing has success criteria without a baseline
- MVP plan needs launch metrics

## Inputs
| Input | Required | Source |
|---|---|---|
| Product goal or problem statement | yes | user, `design/discovery/` |
| Existing analytics setup (events, tools) | optional | repo (tracking code, config), user |
| Data exports | optional | user files |
| User flows for the scope | optional | `design/journeys/` |

## Workflow
1. **Inspect the project.** Search for analytics code, event names, dashboards docs. List existing events.
2. **Metric tree.** Goal → north-star metric → 3 to 5 input metrics → events. Each metric: definition, formula, unit, segment, guardrail (what it must not harm).
3. **Instrumentation spec.** Table: event name, trigger, properties, screen, owner. Reuse existing events; flag naming conflicts.
4. **Baseline.** If data provided, compute and show method. Otherwise `Baseline: none` and how to collect it.
5. **Targets** only if the user states them; never invent.
6. **Review cadence** and who reads what.
7. **Pitfalls**: vanity metrics, gaming risk, sample size needs for A/B.
8. **Write output**; show metric tree in chat.

## Outputs
`design/metrics/product-metrics-<goal>-<date>.md`:
```
> metadata block (data sources)
## Goal
## Metric tree (with definitions and guardrails)
## Instrumentation spec
## Baseline and data status
## Targets (user-stated or "none")
## Review cadence
## Pitfalls
## Open questions / to validate
## Next step
```

## Quality checks
- [ ] Global checks in `docs/ARCHITECTURE.md` §7
- [ ] Every metric has formula and unit
- [ ] Numbers appear only with a cited data source
- [ ] Events reuse existing names where found in repo
- [ ] Every input metric has a guardrail

## Boundaries
- Does not frame the problem → `problem-framing`
- Does not design the A/B study → `ux-research-planner`
- Does not rank features by metric impact → `feature-prioritization`
