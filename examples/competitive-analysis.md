# Example: competitive-analysis

> **Illustrative example.** All inputs and outputs below use invented sample data to show the output shape. Kettle and the three competitors (Basil Box, Pantry Run, Forkful) are fictional; every observation below is hypothetical.

## Prompt

```
/competitive-analysis How do other meal-kit apps handle pausing a subscription? Compare Basil Box, Pantry Run, and Forkful. My screenshots and notes are in research/competitors/.
```

## Sample input (invented)

`research/competitors/`, all supplied by the user, capture dates not recorded:

- `basil-box-pause.png` and notes: Pause offered on the plan page; choice of 1, 2, or 4 weeks; a banner states "Changes close Wednesday 23:59".
- `pantry-run-notes.md`: Pause offered only inside the cancel flow, up to 8 weeks; the cutoff was not visible on the screens captured.
- `forkful-skip.png`: per-week skip on the delivery list; no pause option was seen in the screens supplied. Pricing page not captured.

No browser tool was used in this session. Kettle offers per-week skip only.

## What the skill does

1. Reads `design/discovery/` and `design/audits/` for earlier analyses. None exists.
2. Picks criteria tied to the scope, not a generic feature list.
3. Records how each source was accessed and when. Model memory is not used as evidence.
4. Fills the matrix with tagged facts or `Not observed`, checks each gap against every row, and keeps interpretations separate.

## Output shape (`design/discovery/competitive-analysis-pause-subscription-<YYYY-MM-DD>.md`)

```markdown
> skill: competitive-analysis · date: <YYYY-MM-DD> · scope: pausing a subscription · sources: research/competitors/ (user-supplied screenshots and notes, capture dates unknown)

## Scope and criteria
Scope: how a subscriber stops deliveries for a while without cancelling [reported: user]. Criteria (6, within the default 5 to 8):
1. Where pause or skip is offered
2. Pause lengths available
3. Single-week skip available
4. Cutoff shown at the point of change
5. Pause offered before cancelling
6. Pause offered only in the cancel flow

## Sources inspected (name, type, access method, date)
| Competitor | Source | Type | Access | Date |
|---|---|---|---|---|
| Basil Box | basil-box-pause.png, notes | Screenshot, notes | Provided by the user | date unknown |
| Pantry Run | pantry-run-notes.md | Notes | Provided by the user (user notes) | date unknown |
| Forkful | forkful-skip.png | Screenshot | Provided by the user | date unknown |
No source was fetched live.

## Comparison matrix
| Criterion | Basil Box | Pantry Run | Forkful |
|---|---|---|---|
| 1 Where offered | Plan page [observed: basil-box-pause.png] | Cancel flow [reported: user notes] | Delivery list, skip only [observed: forkful-skip.png] |
| 2 Pause lengths | 1, 2, 4 weeks [observed] | Up to 8 weeks [reported: user notes] | Not observed |
| 3 Single-week skip | Not observed | Not observed | Yes [observed] |
| 4 Cutoff shown at change | Yes, banner [observed] | Not observed | Not observed |
| 5 Pause before cancelling | Yes, on the plan page [observed] | No, only in cancel flow [reported] | Not observed |
| 6 Pause only in cancel flow | No [observed] | Yes [reported] | Not observed |

## Patterns (table-stakes, differentiators, gaps)
- Table-stakes: none. No criterion is observed in most (2 or more) of the three.
- Differentiators (1 of 3): multi-week pause on the plan page (Basil Box); cutoff shown at the change (Basil Box); pause up to 8 weeks (Pantry Run); per-week skip on the delivery list (Forkful).
- Gaps (0 of 3, checked against every row): none can be claimed. Every criterion is observed for at least one competitor, and "Not observed" cells mean the screens were not captured, not that the feature is absent.

## Interpretations
- Competitors place pause in different spots: plan page, cancel flow, or not observed (rows 1, 5, 6) [inferred] · confidence Low: three competitors, user-supplied screens, dates unknown.
- Showing the cutoff at the change is not common in this sample (row 4: 1 of 3) [inferred] · confidence Low.

## Implications for us
- Kettle could test pause outside the cancel flow, as one competitor does (from interpretation 1) [inferred]; not a recommendation on its own.
- Showing the cutoff where the change happens is worth testing, given Kettle's own cutoff tickets (from interpretation 2) [inferred].

## Unknowns and evidence gaps
- Whether Forkful offers pause anywhere not captured.
- Pricing effects of pausing for all three: not captured.
- Capture dates: unknown, so the screens may be out of date.

## Open questions / to validate
- Can the screens be re-captured with dates?
- Should pricing during a pause be added as a criterion?

## Next step
Run `product-discovery` to fold these observations into the pause opportunity brief.
```
