# Example: feature-prioritization

## Prompt

```
/feature-prioritization Rank these for Q1: saved carts, guest checkout, address autocomplete, order tracking map. Research in design/research/.
```

## What the skill does

1. Reads `design/research/` and `design/metrics/` for evidence per candidate.
2. Normalizes candidates as outcomes.
3. Scores RICE with source and confidence per cell; leaves unsourced cells blank with low confidence.
4. Ranks, then states which rankings flip if low-confidence inputs change.

## Output shape (`design/planning/prioritization-q1-2026-11-01.md`)

```markdown
> skill: feature-prioritization · date: 2026-11-01 · scope: 4 candidates · sources: design/research/personas-2026-10-12.md

## Scoring table
| Candidate | Reach | src | conf | Impact | src | conf | Confidence | Effort | src | conf |
|---|---|---|---|---|---|---|---|---|---|---|
| Guest checkout | — | none | L | 3 | 6 of 8 interviewees abandoned at signup [observed] | M | 0.5 | — | none | L |

## Ranking and sensitivity
Formula: (Reach × Impact × Confidence) / Effort. Reach and Effort unsourced for all candidates,
so the ranking is driven by Impact alone and could flip once engineering provides effort.

## Inputs to verify
1. Effort for guest checkout and saved carts (moves rank 1 vs 2).
2. Reach: monthly checkout starts from analytics.

## Next step
Run `mvp-planner` on the top candidate once effort is known.
```
