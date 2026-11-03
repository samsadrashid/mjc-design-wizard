---
name: feature-prioritization
description: Score and order a supplied backlog with a transparent framework (RICE by default), showing every input, its basis, and its confidence, and treating missing inputs as missing instead of filling them in. Use when the user says "prioritize", "rank these features", "what should we build next", "RICE", "what to cut". Not for generating candidates (use `product-discovery`), cutting a release (use `mvp-planner`), or defining the metrics behind impact (use `product-metrics`).
---

# Feature Prioritization

## Purpose
Produce an ordering the team can argue with by inspecting inputs, not totals. Every score traces to a value, a source, and a basis. A missing input stays visibly missing, and its effect on the ranking is shown. Scores support a decision. They do not replace judgment, and a ranking is only as sound as its weakest input.

## Triggers
- "Prioritize this list", "rank the backlog", "RICE these"
- Roadmap planning with more candidates than capacity
- MVP planning needs an ordered candidate list

## Inputs
| Input | If missing | Source |
|---|---|---|
| Candidate list | Stop: this skill does not invent candidates. Ask for a list or point to `product-discovery` | user, issues, `design/` |
| Goal or problem the candidates serve | Ask one: scores mean nothing without a goal. If unanswered, state an `[assumption]` | `design/discovery/`, user |
| Evidence per candidate (research, data, requests) | Assume none; the factor stays missing | `design/`, user |
| Reach, impact, and effort inputs | Assume none; leave each missing factor blank and mark the score provisional | user, engineering |
| Framework preference | Assume RICE as a default; use another if asked | user |

## Workflow
1. **Inspect the project.** Read discovery, metrics, and research outputs for evidence on each candidate, with the source's date or `date unknown`. Copy no personal data from requests or notes.
2. **Normalize candidates** to one line each: user and outcome, not implementation. Merge duplicates and split bundles.
3. **Choose the framework and define its scales.** RICE is a default: score is Reach × Impact × Confidence ÷ Effort. Define each factor's unit or scale, for example Reach as people per period, Impact on a stated 1 to 3 scale, and Effort in person-weeks. Confidence maps High, Medium, Low to 100%, 80%, 50% as a default; state it.
4. **Record every input** with value, source, basis, and confidence. Basis is one of: measured (data with period and definition), stakeholder estimate (name who), assumption, or hypothesis. Confidence (High, Medium, Low) is separate from basis.
5. **Handle missing inputs, never fill them.** Do not substitute a low, high, or neutral value. A low plausible value inflates a score when the missing factor is Effort and deflates it when the factor is Reach or Impact. Show the cell as missing. A candidate with any missing factor gets no point score and is marked provisional. If the user insists on guessed values, label each as a user-directed assumption with Low confidence, keep the score provisional, and show it only in the scenario table.
6. **Rank complete candidates.** List provisional candidates in a separate unranked tier with their missing factors. Where it helps, add a labeled scenario table. For each provisional candidate it recomputes the score at stated low and high values for the missing factor. The range comes from the user, or from the known values for that factor with a note that it is a placeholder. Scenarios show how the order could move. They are not estimates.
7. **Test sensitivity** on the complete rows: which low-confidence inputs would change the order, and by how much.
8. **Flag what the formula omits,** where relevant: dependencies, risk, strategic fit, and cost of delay. Note them beside each candidate and do not fold them into the score.
9. **Group** into now, next, later, and drop with a reason each. A provisional candidate cannot be "now" on score alone. Write the output per §8.

Illustrative arithmetic, not data: Reach 2, Impact 3, Confidence 80%, Effort 4 gives 2 × 3 × 0.8 ÷ 4 = 1.2. If Effort is missing, scenarios at 2 and 8 give 2.4 and 0.6. The candidate stays provisional, and its rank could sit anywhere between those scores.

## Outputs
Metadata block (§4), then path, date, collisions, and reruns (§8), follow `../_shared/standard.md`. File:
`design/planning/prioritization-<topic>-<date>.md`:
```
> metadata block
## Goal and framework (scales defined)
## Normalized candidates
## Scoring table (factor, value, source, basis, confidence)
## Ranking and sensitivity (complete scores, provisional tier, scenarios)
## Now / next / later / drop
## Inputs to verify
## Open questions / to validate
## Next step
```
Missing cells read `Missing` and are never blank or defaulted.

Figma (optional, per `../_shared/figma.md`): when publishing is enabled, draw on the `Feature Prioritization` page the scoring table as a matrix (one row per candidate; value, basis, and confidence for each factor), the ranked complete candidates with their calculation, a separate provisional tier that shows each `Missing` factor, and any scenario table labeled as scenarios, not estimates. Never fill a missing cell, and never draw a score or input value that is not in the Markdown. The Markdown file stays the source of truth.

`## Next step` names exactly one handoff, the first condition below that fits, and writes only that skill: `mvp-planner` to scope the top candidates, `product-metrics` when reach or impact need data, or `ux-research-planner` to verify low-confidence inputs.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] Chat replies follow `../_shared/personality.md`; no emoticons in written files or structured output
- [ ] No missing input has been replaced with a favorable, neutral, or default value
- [ ] Any candidate with a missing factor is provisional and has no point score
- [ ] The formula and scales are shown, and every score can be recomputed from the table
- [ ] Each input shows its basis (measured, stakeholder estimate, assumption, hypothesis) and a separate confidence
- [ ] Scenario tables are labeled as scenarios, not estimates
- [ ] The output says the ranking supports a decision and does not replace judgment
- [ ] Dependencies, risk, and strategic fit are noted where they matter
- [ ] Any Figma output followed `../_shared/figma.md`, and the reply reports only Figma results a tool confirmed

## Boundaries
- Does not generate candidate features → `product-discovery`
- Does not cut release slices or define the MVP → `mvp-planner`
- Does not define the metrics used as impact → `product-metrics`
- Does not verify inputs by research → `ux-research-planner`
