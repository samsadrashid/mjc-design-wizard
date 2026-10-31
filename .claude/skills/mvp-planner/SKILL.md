---
name: mvp-planner
description: Cut a scoped problem into the smallest releasable slice that tests the riskiest assumption, with explicit in/out scope, release slices, risks, and learning goals. Use when the user says "MVP", "what's the smallest version", "scope this down", "release plan", "v1 scope".
---

# MVP Planner

## Purpose
Define what ships first and why: a minimal slice tied to a hypothesis, what is deliberately excluded, how later slices build on it, and what each slice must teach the team.

## Triggers
- "Plan the MVP for X", "cut scope", "what's v1"
- Problem framing and discovery exist and the team is ready to commit
- Backlog is large and needs a first slice

## Inputs
| Input | Required | Source |
|---|---|---|
| Problem statement and riskiest assumption | yes | `design/discovery/`, user |
| Candidate features or user stories | yes | user, prioritization output |
| Constraints (team, time, platform, dependencies) | yes | user, repo |
| Existing product capabilities | yes | repo inspection |

## Workflow
1. **Inspect the project.** Read discovery, framing, prioritization, and existing features in code. Reuse what already exists.
2. **Name the learning goal.** What the first release must prove or disprove. Tie to the riskiest assumption.
3. **Define the core loop.** The minimum path from entry to value for one actor. One flow, one actor.
4. **Scope table.** Per candidate: in slice 1, later slice, or out, with a one-line reason. Default is out.
5. **Release slices.** 2 to 4 slices, each with: scope, learning goal, exit criteria, dependencies.
6. **Risks and mitigations**: technical, adoption, data, operational. Tag likelihood as `[inferred]` with reasoning.
7. **Definition of done** for slice 1, including instrumentation (link `product-metrics`).
8. **Write output**; show slice 1 scope and learning goal in chat.

## Outputs
`design/planning/mvp-plan-<topic>-<date>.md`:
```
> metadata block
## Learning goal and riskiest assumption
## Core loop
## Scope table (in / later / out with reasons)
## Release slices
## Risks and mitigations
## Definition of done (slice 1)
## Open questions / to validate
## Next step
```

## Quality checks
- [ ] Global checks in `docs/ARCHITECTURE.md` §7
- [ ] Slice 1 contains exactly one core loop
- [ ] Every excluded item has a reason
- [ ] Each slice has exit criteria that are observable
- [ ] No effort estimates in days unless the user provided them

## Boundaries
- Does not score the backlog → `feature-prioritization`
- Does not define metrics → `product-metrics`
- Does not frame the problem → `problem-framing`
