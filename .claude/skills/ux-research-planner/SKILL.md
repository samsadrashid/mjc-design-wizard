---
name: ux-research-planner
description: Plan a UX research study - research questions, method choice, participants, recruiting, timeline, and analysis plan. Use when the user says "plan research", "what method should we use", "research plan", "study design", or needs to validate assumptions before design.
---

# UX Research Planner

## Purpose
Turn open questions into a research plan that picks the cheapest valid method, defines participants, and states how results will be analyzed. The plan is the container; guides and protocols come from sibling skills.

## Triggers
- "Plan a study on X", "how should we research this", "what method"
- Discovery or problem-framing output lists assumptions to validate
- User asks whether to run interviews, surveys, or usability tests

## Inputs
| Input | Required | Source |
|---|---|---|
| Questions or assumptions to answer | yes | user, `design/discovery/` |
| Constraints (time, budget, access to users) | yes | user |
| Existing research and personas | optional | `design/research/` |
| Product stage (concept, prototype, live) | yes | repo inspection, user |

## Workflow
1. **Inspect the project.** Read `design/discovery/`, `design/research/`. List prior studies so the plan does not repeat them.
2. **Write research questions.** 3 to 6, answerable, not leading. Map each to the assumption it tests.
3. **Choose method per question** using the table below. State why alternatives were rejected.
4. **Define participants.** Criteria from evidence, not invented segments. Sample size with rationale (e.g. 5 to 8 per segment for qualitative).
5. **Recruiting plan.** Channels available to the team, screener questions, incentives, consent note.
6. **Timeline and roles.** Prep, fieldwork, synthesis. Who moderates, notes, observes.
7. **Analysis plan.** How findings will be coded and what output they feed (persona, journey, prioritization).
8. **Write output**; summarize method and sample in chat.

Method guide:
| Question type | Method |
|---|---|
| Why do users do X / what matters | Interviews, contextual inquiry |
| Can users complete task Y | Usability test (moderated or unmoderated) |
| How widespread is Z | Survey, analytics (only if instrumented) |
| Which label or structure works | Card sort, tree test |
| Which variant performs better | A/B test (needs traffic and instrumentation) |

## Outputs
`design/research/ux-research-planner-<topic>-<date>.md`:
```
> metadata block
## Research questions (mapped to assumptions)
## Method selection and rationale
## Participants and screener
## Recruiting, consent, incentives
## Timeline and roles
## Analysis plan
## Open questions / to validate
## Next step
```

## Quality checks
- [ ] Global checks in `docs/ARCHITECTURE.md` §7
- [ ] Each research question maps to a stated assumption
- [ ] Method choice justified; quantitative methods only where data access exists
- [ ] Participant criteria sourced or marked `[assumption]`
- [ ] Plan contains no findings, only how findings will be obtained

## Boundaries
- Does not write interview questions → `interview-guide-builder`
- Does not write test tasks → `usability-test-planner`
- Does not synthesize into personas → `persona-builder`
