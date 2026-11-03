---
name: mvp-planner
description: Turn an understood problem and desired outcome into a bounded, testable minimum viable product - target users, essential versus later capabilities with reasons, dependencies, risks, unresolved decisions, and how the MVP will be validated. Use when the user says "MVP", "what's the smallest version", "scope this down", "release plan", "v1 scope". Not for clarifying an undefined problem (use `problem-framing`), ranking a candidate list (use `feature-prioritization`), or defining metrics (use `product-metrics`).
---

# MVP Planner

## Purpose
Decide what ships first and why. The MVP is the smallest release that tests the riskiest assumption for a defined user, built around one core loop. Every capability is placed in, later, or out with a reason. The plan names what would change it. It works only from capabilities, users, and constraints the project or the user supplies.

## Triggers
- "Plan the MVP for X", "cut scope", "what's v1"
- Problem framing exists and the team is ready to commit to a first release
- A backlog is large and needs a first slice

## Inputs
| Input | If missing | Source |
|---|---|---|
| Problem statement and desired outcome | Stop: an unclear problem cannot be scoped. Point to `problem-framing` | `design/discovery/`, user |
| Candidate capabilities | Stop: this skill does not invent features. Ask for a backlog or point to `product-discovery` | user, issues, `design/` |
| Target users | Assume from the problem statement and tag them; invent no persona | `design/research/`, user |
| Constraints (team, time, platform, regulation, dependencies) | Ask one. If unanswered, record them as unknown and give no date estimates | user, repo |
| Existing product capabilities | Assume from the repo and tag them | repo |
| Prioritization output | Assume none; follow the user's stated priorities or mark the order unprioritized | `design/planning/` |

## Workflow
1. **Inspect the project.** Read discovery, framing, prioritization, and research outputs, and find existing features in code that the MVP can reuse. List sources with dates or `date unknown`. Copy no personal data from research notes.
2. **Restate** the problem, target users, and desired outcome with evidence tags and confidence (High, Medium, Low per `../_shared/standard.md` §8). Flag anything assumed.
3. **Name the learning goal:** the riskiest assumption the MVP must test, and what result would confirm or refute it.
4. **Define the core loop:** the shortest path from entry to value for one user type. One loop and one user type is a default, because a single loop keeps the result interpretable.
5. **Build the scope table.** For each candidate: in the MVP, later, or out. The reason must tie to the core loop or the learning goal. The default is later unless the loop or the learning goal needs it. Add the dependencies for each row.
6. **Cut release slices.** One to three is a default, because more slices imply certainty the plan does not have. Each has scope, learning goal, observable exit criteria, and dependencies.
7. **List risks, assumptions, and unresolved decisions** with the reasoning behind each likelihood or impact judgment, tagged `[inferred]`. Name an owner or `owner unknown`.
8. **Plan validation.** How the MVP will be tested (the metrics to define with `product-metrics`, the research to plan with `ux-research-planner`) and what evidence would change the plan: expand, cut, or stop. Claim no result.
9. **Define done for slice 1,** including instrumentation. Give effort or dates only if the user provided them, labeled as stakeholder estimates. Write the output per §8.

## Outputs
Metadata block (§4), then path, date, collisions, and reruns (§8), follow `../_shared/standard.md`. File:
`design/planning/mvp-plan-<topic>-<date>.md`:
```
> metadata block
## Problem, users, and outcome (evidence and confidence)
## Learning goal and riskiest assumption
## Core loop
## Scope table (in MVP, later, out, with reasons and dependencies)
## Release slices
## Risks, assumptions, and unresolved decisions
## Validation plan and plan-change triggers
## Definition of done (slice 1)
## Open questions / to validate
## Next step
```
If the user asks for dates or staffing, say under `## Risks, assumptions, and unresolved decisions` that none can be given without the constraints, and list what is needed.

Figma (optional, per `../_shared/figma.md`): when publishing is enabled, draw on the `MVP Planning` page the core loop as shapes with arrow vectors, the scope table as in MVP, later, and out columns with each candidate's source, reason, and dependencies, the release slices with exit criteria, and the risks with owners or `owner unknown`. Never draw a candidate that is not in the Markdown, or a date or estimate the user did not supply. The Markdown file stays the source of truth.

`## Next step` names exactly one handoff, the first condition below that fits, and writes only that skill: `problem-framing` if the problem is still unclear, `feature-prioritization` if candidates still need ranking, `product-metrics` to define the validation measures, or `user-flow-designer` to design the core loop.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] Chat replies follow `../_shared/personality.md`; no emoticons in written files or structured output
- [ ] Every candidate capability came from the user or the project; none was invented
- [ ] Each in, later, and out decision has a reason tied to the core loop or learning goal
- [ ] Slice 1 contains one core loop for one user type, or the exception is justified
- [ ] Assumptions, dependencies, and unresolved decisions are listed with owners or `owner unknown`
- [ ] The plan states what evidence would change it and claims no results
- [ ] No dates or effort figures the user did not provide
- [ ] Any Figma output followed `../_shared/figma.md`, and the reply reports only Figma results a tool confirmed

## Boundaries
- Does not define or clarify the problem → `problem-framing`
- Does not rank or score candidates → `feature-prioritization`
- Does not define metrics or instrumentation in detail → `product-metrics`
- Does not design the flow itself → `user-flow-designer`
