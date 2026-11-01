---
name: product-metrics
description: Define precisely how a product goal will be measured - metric definitions, a metric tree, guardrails, instrumentation, data-quality limits, and how results feed decisions - and read existing numbers only when data is supplied. Use when the user says "metrics", "how do we measure", "KPIs", "what events to track", "success metrics", "instrumentation". Not for stating the problem or success in words (use `problem-framing`), designing experiments or surveys (use `ux-research-planner`), or ranking features (use `feature-prioritization`).
---

# Product Metrics

## Purpose
Connect a goal and the decision it serves to metrics that are defined exactly enough to compute, with the events needed to collect them and the limits of what they can show. Observed values appear only if the user supplies the data. Targets, estimates, and expected effects are kept visibly separate from measurement.

## Triggers
- "Define metrics for X", "what should we track", "set up analytics events"
- Problem framing has success criteria with no baseline
- An MVP plan needs launch metrics

## Inputs
| Input | If missing | Source |
|---|---|---|
| Product goal | Stop: metrics need a purpose. Ask for the goal | user, `design/discovery/` |
| Decision the metrics will inform | Ask one. If unanswered, assume the decision is which candidate to build first and tag it `[assumption]` | user, `design/discovery/` |
| Existing analytics setup: events, tools, definitions | Assume none and search the repo for tracking code | repo, user |
| Data exports or reports | Assume none; report no observed values | user files |
| User flows for the scope | Assume from the repo and tag them | `design/journeys/`, repo |
| Privacy and consent constraints | Assume strict minimization and flag it as an open question | user, repo |

## Workflow
1. **Inspect the project.** Find analytics code, event names, dashboards docs, and any metric definitions. List existing events with the file that emits them. Note when each data source was produced, or `date unknown`.
2. **State the decision and the goal.** What choice will change depending on the numbers, and who makes it.
3. **Define each metric fully:** purpose, formula, unit, population, time window, segments, data source, and status (existing or proposed). A metric missing any field is not yet defined.
4. **Build the metric tree:** goal, one primary metric, a few input metrics, and the events behind them. Keep it small enough to act on. Limit proxies and say what each proxy does not capture.
5. **Add guardrails and consequences.** For each metric, what it must not harm and how it could be gamed or push behavior the wrong way.
6. **Specify instrumentation:** event name, trigger, properties, screen, owner. Reuse existing events and flag naming conflicts. Properties exclude personal identifiers unless a reason is recorded, and consent applies.
7. **Assess data quality:** coverage gaps, missing events, definition drift, sampling, bots and duplicates, with a confidence (High, Medium, Low) per source.
8. **Report observed values** only from supplied data, with period, definition, and source. Mark targets as user-stated, estimates as estimates, and expected effects as hypotheses. Invent no baseline, cause, or experiment result.
9. **Write interpretation limits:** correlation is not causation, and a significance claim needs the sample and method. Write the output per §8.

## Outputs
Metadata block (§4), then path, date, collisions, and reruns (§8), follow `../_shared/standard.md`. File:
`design/metrics/product-metrics-<goal>-<date>.md`:
```
> metadata block (data sources and their dates)
## Decision and goal
## Metric definitions (purpose, formula, unit, population, window, segments, source, status)
## Metric tree
## Guardrails and unintended consequences
## Instrumentation and data quality
## Observed values (supplied data only)
## Targets and estimates (labeled)
## Interpretation limits
## Open questions / to validate
## Next step
```
`## Next step` names one handoff: `problem-framing` when success is still undefined, `ux-research-planner` for experiments or surveys, or `feature-prioritization` when metrics supply impact inputs.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] Every metric has all definition fields, or is marked not yet defined
- [ ] Numbers appear only with a source, period, and definition
- [ ] Observed, proposed, target, estimated, and hypothesized values are labeled apart
- [ ] No invented baselines, causes, or experiment results
- [ ] Each metric has a guardrail and a note on how it could mislead
- [ ] Event properties avoid personal identifiers or record the reason

## Boundaries
- Does not state the problem or success in words → `problem-framing`
- Does not design experiments or surveys → `ux-research-planner`
- Does not rank features by impact → `feature-prioritization`
