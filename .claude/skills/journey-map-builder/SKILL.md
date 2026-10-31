---
name: journey-map-builder
description: Build an end-to-end customer journey map - stages, actions, touchpoints, thoughts, pain points, and opportunities - from research evidence. Use when the user says "journey map", "end-to-end experience", "map the customer journey", "where do users struggle across the lifecycle".
---

# Journey Map Builder

## Purpose
Map one actor's experience across stages and touchpoints, grounding each cell in evidence, to expose where the experience breaks and where opportunities sit. Operates above the screen level.

## Triggers
- "Map the journey for X", "what does the end-to-end look like"
- Personas or research synthesis exist and the team needs a shared picture
- Pain points are known in isolation but not in sequence

## Inputs
| Input | Required | Source |
|---|---|---|
| Actor (persona or role) | yes | `design/research/`, user |
| Scope: start and end moments | yes | user |
| Evidence: research notes, support data, analytics, observed product | yes | `design/research/`, repo, user files |
| Current-state vs future-state | yes | user (default current) |

## Workflow
1. **Inspect the project.** Read personas, research, prior journeys. Reuse actor definitions.
2. **Fix scope.** Name the first and last moment. Confirm actor. If evidence for the actor is missing, label the map `[assumption]` and say so.
3. **Define stages.** 4 to 7 stages from the actor's view (not the product's funnel names).
4. **Fill lanes per stage**: actions, touchpoints/channels, goals, thoughts, pain points, emotion (only if reported). Each cell cites evidence or is tagged.
5. **Mark moments of truth**: stages with highest pain or drop-off evidence.
6. **List opportunities** per moment of truth, tagged `[inferred]`, linked to the pain they address.
7. **Write output**; present the stage list and top three moments of truth in chat.

## Outputs
`design/journeys/journey-map-<actor>-<scope>-<date>.md`:
```
> metadata block
## Actor and scope
## Stage table (lanes as rows, stages as columns)
## Moments of truth
## Opportunities (linked to evidence)
## Evidence gaps
## Open questions / to validate
## Next step
```

## Quality checks
- [ ] Global checks in `docs/ARCHITECTURE.md` §7
- [ ] Emotion lane only populated from reported or observed evidence
- [ ] Stages named from actor perspective
- [ ] Every pain point cites source or is `[assumption]`
- [ ] Opportunities are not features; they are problem spaces

## Boundaries
- Does not define actors → `persona-builder`
- Does not design screen-level flows → `user-flow-designer`
- Does not prioritize opportunities → `feature-prioritization`
