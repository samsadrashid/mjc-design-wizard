---
name: problem-framing
description: Sharpen a fuzzy request into one evidence-backed problem statement, How-Might-We questions, and a success definition. Use when the user says "frame the problem", "what problem are we solving", "write a problem statement", or when a brief jumps to solutions before naming the problem.
---

# Problem Framing

## Purpose
Produce a single, testable problem statement that the team can agree on, plus HMW questions and a definition of success. Prevents solution-first design.

## Triggers
- "Frame this", "what's the real problem", "write the problem statement"
- A request arrives as a feature ("add a dashboard") with no stated user problem
- Discovery brief exists but hypotheses are unfocused

## Inputs
| Input | Required | Source |
|---|---|---|
| Request, brief, or discovery output | yes | user or `design/discovery/` |
| Evidence of the problem (tickets, quotes, data) | optional | repo, user files |
| Current success metrics, if any | optional | `design/metrics/`, user |

## Workflow
1. **Inspect the project.** Read `design/discovery/` and any brief. Note existing problem statements to avoid duplicates.
2. **Separate symptom, problem, and proposed solution.** Three-column table from the request. Tag each row.
3. **Identify the affected user** and the situation. If unknown, mark `[assumption]`; do not invent a persona.
4. **Draft the problem statement**: `[User] needs [need] because [evidence-backed reason]. Today [current state], which causes [consequence].` One paragraph, no solution words.
5. **Generate 3 to 5 HMW questions** at different altitudes (narrow, medium, broad). Mark which the team should pick and why.
6. **Define success** qualitatively, and quantitatively only if a metric with baseline exists. Otherwise write `Baseline: none measured` and point to `product-metrics`.
7. **List what would prove the framing wrong.**
8. **Write output**; show the statement and chosen HMW in chat.

## Outputs
`design/discovery/problem-framing-<topic>-<date>.md`:
```
> metadata block
## Symptom / problem / solution split
## Problem statement
## Affected user and context
## How might we (ranked)
## Success definition (with baseline or "none")
## What would falsify this
## Open questions / to validate
## Next step
```

## Quality checks
- [ ] Global checks in `docs/ARCHITECTURE.md` §7
- [ ] Problem statement contains no solution or feature name
- [ ] Evidence cited for the "because" clause or statement marked `[assumption]`
- [ ] Success definition has a baseline or explicitly says none exists
- [ ] Exactly one problem statement; alternates listed as rejected with reason

## Boundaries
- Does not plan discovery or hypotheses → `product-discovery`
- Does not define metric trees → `product-metrics`
- Does not scope solutions → `mvp-planner`
