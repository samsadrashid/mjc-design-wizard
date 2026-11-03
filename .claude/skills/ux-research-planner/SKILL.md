---
name: ux-research-planner
description: Plan a UX research study - the decision it informs, research questions, method choice, participants, ethics, capture, analysis, and a feasible timeline. Plans research only; it never invents findings. Use when the user says "plan research", "what method should we use", "research plan", "study design", or needs to validate assumptions before design. Not for writing interview questions (use `interview-guide-builder`), task-based test protocols (use `usability-test-planner`), or synthesizing results into personas (use `persona-builder`).
---

# UX Research Planner

## Purpose
Turn open questions into a feasible plan: the decision the study must inform, the cheapest valid method, who to include, how to treat participants ethically, and how data will be captured and analyzed. The plan contains no findings. Sibling skills write the instruments.

## Triggers
- "Plan a study on X", "how should we research this", "what method"
- Discovery or problem framing lists assumptions to validate
- The user asks whether to run interviews, a survey, or a usability test

## Inputs
| Input | If missing | Source |
|---|---|---|
| Decision the research will inform | Ask one: without it the questions cannot be prioritized. If unanswered, assume the decision is whether to proceed with the opportunity in `design/discovery/` and tag it `[assumption]` | user, `design/discovery/` |
| Questions or assumptions to answer | Assume: derive them from `design/discovery/` and tag `[inferred]` | user, repo |
| Constraints (time, budget, access to users) | Assume: plan for the lowest-cost option and say so | user |
| Product stage (concept, prototype, live) | Assume from the repo and tag it | repo, user |
| Prior research and personas | Assume none; avoid repeating studies you cannot see | `design/research/` |

## Workflow
1. **Inspect the project.** Read `design/discovery/` and `design/research/`. List prior studies with their dates or `date unknown` so the plan does not repeat or contradict them. Copy no participant identifiers. When tickets and interviews both appear, match ticket authors to interviewees by identity, internally and without printing the identifiers; count each person once and list the members beside every count.
2. **State the decision and uncertainty.** What choice depends on this study, and what is the cost of being wrong. This sets how much rigor is justified.
3. **Write 3 to 6 research questions.** Answerable, not leading. Map each to the assumption it tests. The range is a default that keeps a study focused.
4. **Choose a method per question** from the table. Say why cheaper or alternative methods were rejected. Choose quantitative methods only where data access and sample size make them valid.
5. **Define participants** from evidence, not invented segments. Give the criteria, the exclusions, and a sample size with its rationale. 5 to 8 per segment is a common default for qualitative work because it tends to surface recurring themes within budget. It is not a statistical guarantee.
6. **Plan recruiting and ethics.** Channels the team really has, screener questions, consent, compensation, recording and data handling (retention, access, anonymization per §8), and care for vulnerable or sensitive topics.
7. **Plan capture and analysis.** Where notes go, the coding approach, who reviews, and which outputs the data feeds. Say who owns synthesis, since no dedicated synthesis skill exists.
8. **Check feasibility:** timeline, roles, tools. Cut scope before stretching the plan. Write the output per §8.

Method guide (starting points, not rules):
| Question type | Method |
|---|---|
| Why do people do X, what matters to them | Interviews, contextual inquiry |
| Can people complete task Y | Usability test (moderated or unmoderated) |
| How widespread is Z | Survey or analytics, only if instrumented |
| Which structure or label fits | Card sort, tree test |
| Which variant performs better | A/B test, needs traffic and instrumentation |

## Outputs
Metadata block (§4), then path, date, collisions, and reruns (§8), follow `../_shared/standard.md`. File:
`design/research/ux-research-planner-<topic>-<date>.md`:
```
> metadata block
## Decision and research questions (mapped to assumptions)
## Method selection and rationale
## Participants and screener
## Recruiting, consent, and ethics
## Data capture and analysis plan
## Timeline, roles, and feasibility
## Open questions / to validate
## Next step
```

Figma (optional, per `../_shared/figma.md`): when publishing is enabled, draw on the `UX Research Plans` page the decision, each research question beside the assumption it tests and its chosen method, the participant criteria with the sample size labeled as a default, and the timeline. Label everything as planned; never draw findings or expected results. The Markdown file stays the source of truth.

`## Next step` names exactly one handoff, the first condition below that fits, and writes only that skill: `interview-guide-builder` for an interview study, `usability-test-planner` for task testing, or `persona-builder` once enough sessions have been synthesized.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] Chat replies follow `../_shared/personality.md`; no emoticons in written files or structured output
- [ ] The plan names the decision it informs
- [ ] Each research question maps to a stated assumption
- [ ] Method choice is justified, and quantitative methods are used only where valid
- [ ] Sample sizes are labeled as defaults with a reason
- [ ] Consent, data handling, and anonymization are specified
- [ ] The plan contains no results or expected findings
- [ ] Any Figma output followed `../_shared/figma.md`, and the reply reports only Figma results a tool confirmed

## Boundaries
- Does not write interview questions → `interview-guide-builder`
- Does not write task-based test protocols → `usability-test-planner`
- Does not synthesize findings into profiles → `persona-builder`
- Does not frame the opportunity or problem → `product-discovery`, `problem-framing`
