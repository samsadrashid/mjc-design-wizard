---
name: competitive-analysis
description: Compare competitor or reference products on features, flows, and UX patterns using only sources the user provides or that are observed directly. Use when the user says "competitive analysis", "how do others do this", "benchmark against", "compare with", or names competitor products.
---

# Competitive Analysis

## Purpose
Produce a grounded comparison of how competitors or reference products handle a scope, with observed patterns, gaps, and implications. Never guesses competitor behavior from memory alone.

## Triggers
- "Compare us to A, B, C", "how does X handle onboarding", "benchmark"
- User provides screenshots, URLs, recordings, or notes about other products
- Discovery or critique needs an external reference point

## Inputs
| Input | Required | Source |
|---|---|---|
| Scope (feature, flow, or whole product) | yes | user |
| Competitor list | yes | user |
| Evidence per competitor (screenshots, URLs, notes, public docs) | yes | user or browser if available |
| Own product state for the same scope | optional | repo, `design/` |

## Workflow
1. **Inspect the project.** Read `design/discovery/` and `design/audits/`. Reuse prior analyses.
2. **Confirm scope and criteria.** Propose 5 to 8 comparison criteria tied to the scope (e.g. steps to complete, error handling, defaults, pricing visibility). Ask the user only if scope is unclear.
3. **Gather evidence per competitor.** Only from provided material or pages actually visited. Record source and date for each. Where none exists, write `Not observed`.
4. **Fill the matrix.** Rows: criteria. Columns: competitors plus own product. Cells: short observed fact with tag.
5. **Extract patterns.** Table-stakes (most do it), differentiators (one does it), gaps (none do it).
6. **Derive implications** for own product, each tagged `[inferred]` with the matrix rows it rests on.
7. **Write output**; show the pattern summary in chat.

## Outputs
`design/discovery/competitive-analysis-<scope>-<date>.md`:
```
> metadata block (sources with dates)
## Scope and criteria
## Comparison matrix
## Patterns: table-stakes / differentiators / gaps
## Implications for us
## Evidence gaps
## Open questions / to validate
## Next step
```

## Quality checks
- [ ] Global checks in `docs/ARCHITECTURE.md` §7
- [ ] Every matrix cell is observed, reported with a source, or `Not observed`
- [ ] No pricing, user counts, or market share without a dated source
- [ ] Criteria map to the stated scope, not generic feature lists
- [ ] Implications reference matrix rows

## Boundaries
- Does not frame the opportunity → `product-discovery`
- Does not critique own design → `design-critique`
- Does not rank own features → `feature-prioritization`
