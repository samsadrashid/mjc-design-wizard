---
name: competitive-analysis
description: Compare competitors and alternatives on a defined scope, separating verified observations from interpretation and unknowns, with the sources inspected and when. Use when the user says "competitive analysis", "how do others do this", "benchmark against", "compare with", or names competitor products. Not for critiquing the user's own design (use `design-critique`), ranking the user's own features (use `feature-prioritization`), or framing the wider opportunity (use `product-discovery`).
---

# Competitive Analysis

## Purpose
Produce a grounded comparison of how competitors and alternatives handle a scope. Every matrix cell traces to a source that was actually inspected, and the document says how and when. Interpretation and recommendations are kept apart from observation.

## Triggers
- "Compare us to A, B, C", "how does X handle onboarding", "benchmark"
- The user provides screenshots, URLs, recordings, exports, or notes about other products
- Discovery or critique needs an external reference point

## Inputs
| Input | If missing | Source |
|---|---|---|
| Scope (feature, flow, or product area) | Ask one: the scope drives every criterion. If unanswered, state the scope inferred from the request and tag it `[assumption]` | user |
| Competitor or alternative list | Stop: nothing to compare | user |
| Evidence per competitor (screenshots, pages, docs, notes) | Assume: mark that competitor `Not observed`; if all are unobserved, stop and say what to provide | user; browser only if available |
| Own product state for the same scope | Assume: compare competitors only | repo, `design/` |

## Workflow
1. **Inspect the project.** Read `design/discovery/` and `design/audits/` and reuse earlier analyses. Note which earlier sources are now stale.
2. **Choose 5 to 8 criteria** tied to the scope (steps to complete, defaults, error handling, pricing visibility). This range is a default that keeps the matrix readable. Do not use generic feature lists.
3. **Record sources inspected.** For each: name, type, how it was accessed, and the date. Access is one of: provided by the user, fetched live with a tool this session, or user notes. Claim live verification only if a tool fetched it this session. Take the date from the session per §8, or write `date unknown`. Knowledge from model memory is not evidence.
4. **Fill the matrix.** One short fact per cell with a tag and source, or `Not observed`.
5. **Extract patterns:** table-stakes (most competitors), differentiators (one), gaps (none). Mark each with its count of competitors observed. Check every gap against every matrix row before writing it. A gap means no observed competitor does it.
6. **Interpret.** Each interpretation is `[inferred]` and names the matrix rows it rests on, with confidence.
7. **Derive implications** for the user's product. Each cites an interpretation; none is stated as fact.
8. **List unknowns** and what evidence would settle them. Write the output per §8.

## Outputs
Metadata block (§4), then path, date, collisions, and reruns (§8), follow `../_shared/standard.md`. File:
`design/discovery/competitive-analysis-<scope>-<date>.md`:
```
> metadata block
## Scope and criteria
## Sources inspected (name, type, access method, date)
## Comparison matrix
## Patterns (table-stakes, differentiators, gaps)
## Interpretations
## Implications for us
## Unknowns and evidence gaps
## Open questions / to validate
## Next step
```

Figma (optional, per `../_shared/figma.md`): when publishing is enabled, draw on the `Competitive Analysis` page the comparison matrix with each cell keeping its source and date and showing `Not observed` where nothing was seen, one card per source inspected, the patterns, and the interpretations and unknowns as separately labeled groups marked `[inferred]` or unknown. Never draw a competitor capability, logo, screenshot, or claim that is not in the Markdown. The Markdown file stays the source of truth.

`## Next step` names exactly one handoff, the first condition below that fits, and writes only that skill: `product-discovery` to fold in the findings, or `design-critique` to apply them to a specific design.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] Chat replies follow `../_shared/personality.md`; no emoticons in written files or structured output
- [ ] Every cell is an observed fact with a source, a reported fact with its origin, or `Not observed`
- [ ] The sources section states how each source was accessed and when
- [ ] No pricing, market share, user counts, or traffic without a dated source
- [ ] Interpretations and implications trace to matrix rows
- [ ] Observation, interpretation, and unknown are visibly separate
- [ ] Any Figma output followed `../_shared/figma.md`, and the reply reports only Figma results a tool confirmed

## Boundaries
- Does not frame the opportunity or hypotheses → `product-discovery`
- Does not critique the user's own design → `design-critique`
- Does not rank the user's own features → `feature-prioritization`
