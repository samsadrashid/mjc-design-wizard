---
name: feature-prioritization
description: Score and rank a given backlog with a transparent framework (RICE, ICE, value/effort, or Kano) using only evidence the team has, exposing every input and its confidence. Use when the user says "prioritize", "rank these features", "what should we build next", "RICE", "what to cut".
---

# Feature Prioritization

## Purpose
Produce a ranked backlog where every score is traceable to an input and a confidence level, so the team debates inputs rather than totals. Never fills in reach or impact numbers without a source.

## Triggers
- "Prioritize this list", "rank the backlog", "RICE these"
- Roadmap planning with more candidates than capacity
- MVP planning needs an ordered candidate list

## Inputs
| Input | Required | Source |
|---|---|---|
| Candidate list | yes | user, issues, `design/` outputs |
| Goal or problem being served | yes | `design/discovery/`, user |
| Evidence per candidate (research, data, requests) | optional | `design/`, user |
| Effort inputs | optional | user, engineering |
| Framework preference | optional | user (default: RICE with confidence) |

## Workflow
1. **Inspect the project.** Read discovery, metrics, research. Collect any evidence that bears on candidates.
2. **Normalize candidates.** One line each: user, outcome, not implementation. Merge duplicates; split bundles.
3. **Pick framework** and state why. Define each factor's scale in a table.
4. **Score each factor** per candidate with: value, source, confidence (H/M/L). Where no source: value blank, confidence L, scored with the lowest plausible value and flagged.
5. **Compute** and rank. Show the formula and a sensitivity note: which rankings flip if low-confidence inputs change.
6. **Group** into now, next, later, drop, with a one-line reason each.
7. **List inputs to verify** before committing, ordered by how much they move the ranking.
8. **Write output**; show the top five and the sensitivity note in chat.

## Outputs
`design/planning/prioritization-<topic>-<date>.md`:
```
> metadata block
## Goal and framework (scales defined)
## Normalized candidates
## Scoring table (factor, value, source, confidence)
## Ranking and sensitivity
## Now / next / later / drop
## Inputs to verify
## Open questions / to validate
## Next step
```

## Quality checks
- [ ] Global checks in `docs/ARCHITECTURE.md` §7
- [ ] Every score cell has a source or is flagged low confidence
- [ ] Formula shown; totals recomputable from the table
- [ ] Sensitivity note names at least one ranking that could flip
- [ ] Candidates phrased as outcomes, not solutions

## Boundaries
- Does not define release slices → `mvp-planner`
- Does not define the metrics used as impact → `product-metrics`
- Does not generate new candidates → `product-discovery`
