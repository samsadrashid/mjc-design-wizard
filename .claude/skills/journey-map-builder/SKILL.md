---
name: journey-map-builder
description: Build an end-to-end journey map for one actor - stages, goals, actions, touchpoints, pain points, transitions, and opportunities - where every cell traces to supplied evidence and gaps are shown. Use when the user says "journey map", "end-to-end experience", "map the customer journey", "where do users struggle across the lifecycle". Not for screen-level task flows (use `user-flow-designer`), defining the actor (use `persona-builder`), or ranking the opportunities it finds (use `feature-prioritization`).
---

# Journey Map Builder

## Purpose
Show one actor's experience across stages and touchpoints so the team can see where it breaks and where problems cluster. Each cell cites evidence. Where there is none, the cell says so. The map is a view of what evidence supports, not a story invented to fill the grid.

## Triggers
- "Map the journey for X", "what does the end-to-end look like"
- Research or support data exists and the team needs a shared picture
- Pain points are known in isolation but not in sequence

## Inputs
| Input | If missing | Source |
|---|---|---|
| Actor (a persona, role, or described user) | Ask one: the map is meaningless without whose journey it is. If unanswered, use the best-evidenced actor in `design/research/` and tag it `[inferred]`; if none can be inferred, stop | `design/research/`, user |
| Scope: first and last moment, current or future state | Assume current state and a scope inferred from the evidence; tag it | user |
| Evidence (research notes, support tickets, analytics, observed product) | Stop: do not draw a map from nothing. If the user wants a workshop starter, label every cell `[assumption]` and the map a hypothesis | `design/research/`, repo, user files |
| Existing personas or maps | Assume none | `design/research/`, `design/journeys/` |

Do not assume any evidence file exists. Use only what the project or the user supplies.

## Workflow
1. **Inspect the project.** Read personas, research notes, support exports, analytics exports, product code or docs, and prior maps. List each source with type, size (for example interviews, tickets, rows), and date or `date unknown`. Replace names and identifiers with codes (P1, T1) per §8 privacy. When tickets and interviews both appear, count each person once as `../_shared/standard.md` §8 sets out.
2. **Fix scope.** Name the first and last moment and the actor. Reuse actor definitions from `persona-builder` output.
3. **Define stages** from the actor's point of view, not the product's funnel names. 4 to 7 is a default because fewer hides the sequence and more stops fitting on one view. Each stage must be visible in some source.
4. **Fill each lane from evidence only:**
   - Goal and actions: from notes, tickets, or observed product behavior.
   - Touchpoints and channels: only those seen in the evidence, named as the source names them ("notification", not "push"). Count entries by listing them.
   - Pain points: from tickets, notes, or measured drop-off. Count how many sources support each.
   - Emotion: include only if a participant stated it or it was observed. Otherwise write `Not reported`.
   - Metrics: only from supplied analytics, with the period and definition. Never estimate. Do not derive funnel or conversion rates from event counts that are not linked to the same people. Label a ratio of two counts as a ratio of counts, with its definition.
   Each cell carries a source code and a tag. Mark cell confidence (High, Medium, Low per §8) where sources conflict or are thin.
5. **Describe stage transitions:** what moves the actor from one stage to the next, what stalls them, and where they leave. Cite evidence or tag `[inferred]`.
6. **Mark moments of truth:** the stages with the strongest pain or drop-off evidence. Three is a default cap that keeps focus.
7. **List opportunities** as problem spaces, not features. Each links to the pain it addresses and is tagged `[inferred]`.
8. **List gaps:** stages or lanes with thin or no evidence, and what would fill them. Write the output per §8 and show the stage list and moments of truth in chat.

## Outputs
Metadata block (§4), then path, date, collisions, and reruns (§8), follow `../_shared/standard.md`. File:
`design/journeys/journey-map-<actor>-<scope>-<date>.md`:
```
> metadata block (sources, types, counts, dates)
## Actor and scope
## Evidence base (source, type, count, date, confidence)
## Journey map (lanes as rows, stages as columns)
## Stage transitions
## Moments of truth
## Opportunities (problem spaces, linked to pain)
## Evidence gaps and uncertainties
## Open questions / to validate
## Next step
```

Figma (optional, per `../_shared/figma.md`): when publishing is enabled, draw on the `Journey Maps` page the journey as a grid with stages as columns and lanes as rows, each cell keeping its evidence tag and source, plus the moments of truth, the opportunities linked to their pain points, and the evidence gaps. Show an empty cell as `Not reported`. Never draw a stage, emotion, quote, or pain point that is not in the Markdown, and never present an assumption or hypothesis as observed. The Markdown file stays the source of truth.

`## Next step` names exactly one handoff, the first condition below that fits, and writes only that skill: `user-flow-designer` to detail a stage, `ux-research-planner` to close evidence gaps, or `feature-prioritization` to rank the opportunities.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] Chat replies follow `../_shared/personality.md`; no emoticons in written files or structured output
- [ ] Every cell cites a source code and a tag, or reads `Not reported` or `Not observed`
- [ ] No emotions, channels, or metrics that the evidence does not contain
- [ ] A map with no evidence is labeled a hypothesis and every cell is `[assumption]`
- [ ] Transitions are described, and evidence gaps are listed
- [ ] Opportunities are problem spaces and each links to a cited pain point
- [ ] No personal identifiers from sources appear in the output
- [ ] Any Figma output followed `../_shared/figma.md`, and the reply reports only Figma results a tool confirmed

## Boundaries
- Does not detail screen-level flows or states → `user-flow-designer`
- Does not define or segment the actor → `persona-builder`
- Does not plan research to fill gaps → `ux-research-planner`
- Does not rank opportunities → `feature-prioritization`
