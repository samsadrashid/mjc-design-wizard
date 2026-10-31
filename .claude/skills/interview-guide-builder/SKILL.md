---
name: interview-guide-builder
description: Build a moderated interview discussion guide with warm-up, core, and probe questions tied to research goals, plus note-taking template. Use when the user says "interview guide", "discussion guide", "what should I ask users", or a research plan calls for interviews.
---

# Interview Guide Builder

## Purpose
Produce a ready-to-run interview guide for one study: timed sections, non-leading questions, probes, and a note template. Grounded in the study's stated research questions.

## Triggers
- "Write an interview guide for X", "questions for user interviews"
- `design/research/` has a plan selecting interviews
- User wants to validate a problem statement with users

## Inputs
| Input | Required | Source |
|---|---|---|
| Research questions or goals | yes | user, `design/research/` plan |
| Participant type | yes | plan or user |
| Session length | yes | user (default 45 min) |
| Topics to avoid, sensitivities | optional | user |
| Prototype or artifact to show | optional | user |

## Workflow
1. **Inspect the project.** Read the research plan and problem framing. If no plan exists, ask for research questions or derive them from `design/discovery/` and mark `[inferred]`.
2. **Map goals to sections.** Each research question gets one core section. Drop questions the method cannot answer.
3. **Write questions.** Open, past-behavior focused ("tell me about the last time..."), no yes/no, no product names in warm-up. Two to three probes per core question.
4. **Time-box.** Warm-up 5 min, core sections, wrap-up 5 min. Total matches session length.
5. **Add moderator notes.** Consent script, recording ask, what to do if participant goes off-topic.
6. **Build note template.** One row per question, columns: observation, quote, tag.
7. **Self-check for bias**: leading, double-barreled, hypothetical questions. Rewrite.
8. **Write output**; show the core questions in chat.

## Outputs
`design/research/interview-guide-<topic>-<date>.md`:
```
> metadata block
## Study goals (from plan)
## Logistics and consent script
## Guide (timed sections with probes)
## Note-taking template
## Bias check log
## Open questions / to validate
## Next step
```

## Quality checks
- [ ] Global checks in `docs/ARCHITECTURE.md` §7
- [ ] Every core question traces to a research question
- [ ] No leading, double-barreled, or hypothetical-preference questions
- [ ] Timing sums to session length
- [ ] Guide contains no sample answers or expected findings

## Boundaries
- Does not choose the method or participants → `ux-research-planner`
- Does not write task-based protocols → `usability-test-planner`
- Does not synthesize results → `persona-builder`, `journey-map-builder`
