---
name: product-discovery
description: Frame a product opportunity from existing material - what is known, what is assumed, and what must be learned - and plan how to close the gaps. Produces a discovery brief; it does not conduct research. Use when the user says "discovery", "should we build", "explore this opportunity", "what do we know about", or starts a new product or feature area. Not for writing the problem statement (use `problem-framing`), designing studies (use `ux-research-planner`), or comparing competitors in depth (use `competitive-analysis`).
---

# Product Discovery

## Purpose
Map the context around an opportunity: users, desired outcomes, constraints, alternatives, and above all the knowledge gaps. The brief separates facts from assumptions and plans how to learn what is missing. This skill only reads existing material. It never reports research that has not happened.

## Triggers
- "Run discovery on X", "is X worth building", "what do we know about X"
- A new feature area with no prior research in the project
- A goal, request, or market signal arrives and the next move is unclear

## Inputs
| Input | If missing | Source |
|---|---|---|
| Opportunity or request | Stop: nothing to frame | user |
| Project context (README, docs, roadmap) | Assume: list what could not be found | repo |
| Existing research, tickets, analytics | Assume none exists; record it as a gap | `design/`, `research/`, user files |
| Constraints (time, budget, platform, regulation) | Ask one, only if it changes the plan's depth. If unanswered, record constraints as unknown and give no time or cost estimates | user |

If several inputs are missing, ask the single question whose answer most changes the plan. Handle everything else per `../_shared/standard.md` §8.

## Workflow
1. **Inspect the project.** Read the README, `docs/`, `design/`, `research/`, and any file the user names. List each source with its own date, or `date unknown`. Extend a prior brief in `design/discovery/` instead of restarting. Copy no personal identifiers from tickets or notes.
2. **Restate the opportunity** in one sentence: who, what need, what signal prompted it, tagged `[observed]` or `[reported]`.
3. **Map the context.** Users or segments named in the material, outcomes sought and by whom, constraints, and alternatives users have today. Keep only what a source supports. Under `## Context and constraints`, add `### User needs` (goals, frictions, needs, workarounds, unmet expectations, each tagged and sourced; invent no research finding).
4. **Build the evidence inventory.** Claim, tag, source, confidence (High, Medium, Low per §8). The source is the ticket, interview, or file whose own words state the claim (`T-01`, not `P1`, for what T-01 says); note `same person as P1` beside it instead of listing the other ID. Count over every row of each source file and list the source IDs beside each count.
5. **List knowledge gaps**, ordered by how much each would change the decision. Keep "unknown" separate from "assumed".
6. **Group the evidence into opportunity areas** under `## Hypotheses`, in `### Opportunity areas and priority`: for each, its supporting evidence rows, the user need, why it matters, and the uncertainty. Rank them with a stated framework (evidence strength, impact if true, and uncertainty, each High, Medium, Low, with the rule for combining them); fabricate no market size, conversion, revenue, or demand. Then state `### Recommended direction`: the recommended opportunity, rationale, alternatives, assumptions, risks, what needs validation, and the next action, and say it is a recommendation and not a validated decision. Then **write hypotheses** as `We believe [user] has [problem] because [evidence]. If true, [outcome].` Five is a default cap that keeps the plan testable. Rank by impact if wrong against confidence.
7. **Draft the discovery plan** for the riskiest hypotheses: method type, who to learn from, and what would confirm or refute it. Method types only. Mark every item as planned, not done.
8. **Write the output** per §8 (path, date, collisions, reruns) and give a five-line summary in chat.

## Outputs
Metadata block (§4), then path, date, collisions, and reruns (§8), follow `../_shared/standard.md`. File:
`design/discovery/product-discovery-<topic>-<date>.md`:
```
> metadata block (sources with their dates)
## Opportunity statement
## Context and constraints
## Evidence inventory (claim, tag, source, confidence)
## Knowledge gaps
## Hypotheses (ranked by risk)
## Discovery plan (hypothesis → method → signal)
## Open questions / to validate
## Next step
```

Figma (optional, per `../_shared/figma.md`): when publishing is enabled, draw on the `Product Discovery` page one board with: product context, the evidence and insights as one card per inventory row (claim, tag, source, confidence), the user needs, the opportunity clusters, the prioritization with its criteria, the recommended direction, the assumptions and risks, the knowledge gaps, the ranked hypotheses beside their planned method and signal, and the next steps. Label every plan item as planned, not done. Never draw research results, metrics, or user quotes that are not in the Markdown; discovery plans research and does not conduct it. The Markdown file stays the source of truth.

`## Next step` names exactly one handoff, the first condition below that fits, and writes only that skill: `problem-framing` when evidence is enough to state the problem, `ux-research-planner` when gaps dominate, `competitive-analysis` when alternatives are poorly understood. If the user asked a direct question (for example whether to build), answer it under `## Opportunity statement`, as far as the evidence allows, or say it cannot be answered yet.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] Chat replies follow `../_shared/personality.md`; no emoticons in written files or structured output
- [ ] The reply asks at most one question in total, as `../_shared/standard.md` §8 defines it (two requests joined by "and" are two); counts were computed over the whole source
- [ ] The brief states that only existing material was read; no discovery activity is implied
- [ ] Every hypothesis cites an evidence row or is tagged `[assumption]`
- [ ] No market size, user count, or revenue figure unless sourced and dated
- [ ] Gaps are listed as gaps and not filled with plausible detail
- [ ] The plan tests the riskiest hypotheses first
- [ ] Any Figma output followed `../_shared/figma.md`, and the reply reports only Figma results a tool confirmed

## Boundaries
- Does not write the problem statement → `problem-framing`
- Does not design studies or choose recruiting → `ux-research-planner`
- Does not compare competitors in depth; a short list of known alternatives is fine → `competitive-analysis`
- Does not scope releases → `mvp-planner`
