---
name: product-discovery
description: Frame a product opportunity from existing evidence. Produces an opportunity brief with hypotheses, riskiest assumptions, and a discovery plan. Use when the user says "discovery", "should we build", "explore this opportunity", "what do we know about", or starts a new product or feature area.
---

# Product Discovery

## Purpose
Turn a vague opportunity into a brief that states what is known, what is assumed, and what must be learned before committing design or build effort. Evidence-first: the brief distinguishes facts from guesses.

## Triggers
- "Run discovery on X", "is X worth building", "what do we know about X"
- A new feature area with no prior research in the project
- User shares a goal, request, or market signal and asks what to do next

## Inputs
| Input | Required | Source |
|---|---|---|
| Opportunity statement or request | yes | user |
| Project context (README, docs, roadmap) | yes | repo inspection |
| Existing research, support tickets, analytics exports | optional | `design/`, `research/`, user-provided files |
| Business constraints (timeline, budget, platform) | optional | user |

## Workflow
1. **Inspect the project.** Read README, `docs/`, `design/`, `research/`. List found sources. If `design/discovery/` has prior briefs, extend them.
2. **Restate the opportunity** in one sentence: who, what need, what signal prompted it. Tag the signal `[observed]` or `[reported]`.
3. **Inventory evidence.** Table: claim, tag, source. Separate user need, business value, feasibility.
4. **Write hypotheses** in the form `We believe [user] has [problem] because [evidence]. If true, [outcome].` Max five.
5. **Rank risk.** For each hypothesis: impact if wrong (H/M/L), confidence (H/M/L), evidence strength. Flag the riskiest two.
6. **Draft discovery plan.** For each risky hypothesis: cheapest method to test it, who to talk to, what would confirm or refute. Methods only; detailed research design belongs to `ux-research-planner`.
7. **Write output** and present a five-line summary in chat.

## Outputs
`design/discovery/product-discovery-<topic>-<date>.md`:
```
> metadata block
## Opportunity statement
## Evidence inventory (table with tags)
## Hypotheses (ranked by risk)
## Riskiest assumptions
## Discovery plan (hypothesis → method → signal)
## Open questions / to validate
## Next step
```

## Quality checks
- [ ] Global checks in `docs/ARCHITECTURE.md` §7
- [ ] Every hypothesis cites at least one evidence row or is marked `[assumption]`
- [ ] No market sizes, user counts, or revenue figures unless sourced
- [ ] Discovery plan tests the riskiest assumptions first, not the easiest
- [ ] Brief fits on two screens

## Boundaries
- Does not write a problem statement or HMW → `problem-framing`
- Does not design studies or guides → `ux-research-planner`
- Does not compare competitors in depth → `competitive-analysis`
- Does not scope releases → `mvp-planner`
