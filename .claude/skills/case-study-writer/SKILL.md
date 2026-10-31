---
name: case-study-writer
description: Write a portfolio or internal case study for a finished project - context, problem, process, decisions, outcome - using only documented evidence and clearly marked gaps. Use when the user says "case study", "write up this project", "portfolio piece", "project retrospective narrative".
---

# Case Study Writer

## Purpose
Turn a project's real artifacts into a narrative that shows the designer's reasoning and impact. Outcomes appear only when documented; the absence of outcome data is stated, never papered over.

## Triggers
- "Write a case study for X", "portfolio write-up", "summarize this project for review"
- Project reaches a milestone and `design/` holds its artifacts
- Performance review or hiring prep

## Inputs
| Input | Required | Source |
|---|---|---|
| Project artifacts (discovery, research, flows, specs, audits) | yes | `design/`, repo |
| Outcome data (metrics, feedback, launch notes) | optional | user, `design/metrics/` |
| Audience (hiring manager, leadership, team) | yes | user |
| Designer's role and collaborators | yes | user |
| Length target | optional | user (default 800 to 1200 words) |

## Workflow
1. **Inspect the project.** Read every `design/` artifact and the changelog. Build a timeline table: date, artifact, decision.
2. **Confirm audience and role.** Adjust depth: hiring (process and judgment), leadership (outcome and tradeoffs), team (lessons).
3. **Extract the arc**: context → problem → constraints → key decisions (with alternatives) → outcome → lessons. Each point cites an artifact.
4. **Outcome section**: include only sourced numbers or quotes. If none, write "Outcome data: not yet available" and describe what was measured or planned.
5. **Draft** in plain language, first person if portfolio. Lead with the problem, not the solution.
6. **Visuals list**: which artifacts to embed and captions. Do not fabricate images.
7. **Honesty pass**: remove claims not traceable to the timeline table.
8. **Write output**; show the outline in chat.

## Outputs
`design/docs/case-study-<project>-<date>.md`:
```
> metadata block (artifacts used)
## Summary (3 lines)
## Context and role
## Problem
## Constraints
## Process and key decisions
## Outcome (sourced or "not yet available")
## Lessons
## Visuals to include
## Open questions / to validate
## Next step
```

## Quality checks
- [ ] Global checks in `docs/ARCHITECTURE.md` §7
- [ ] Every decision cites an artifact in the timeline table
- [ ] No outcome numbers, quotes, or testimonials without source
- [ ] Role and collaborators attributed accurately per user input
- [ ] Length within target

## Boundaries
- Does not write specs → `design-documentation`
- Does not compute metrics → `product-metrics`
- Does not run a retrospective critique → `design-critique`
