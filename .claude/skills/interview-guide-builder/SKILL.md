---
name: interview-guide-builder
description: Build a moderated interview guide - objectives, consent and privacy script, neutral timed questions with probes, an objective-to-question map, and a capture template. Use when the user says "interview guide", "discussion guide", "what should I ask users", or a research plan calls for interviews. Not for choosing the method or participants (use `ux-research-planner`) or for task-based testing of a prototype (use `usability-test-planner`).
---

# Interview Guide Builder

## Purpose
Produce a guide a moderator can run: clear objectives, a consent and privacy script, neutral past-behavior questions in a timed sequence, follow-up probes, and a way to capture notes so they can be synthesized later. Every question traces to an objective.

## Triggers
- "Write an interview guide for X", "questions for user interviews"
- A research plan in `design/research/` selects interviews
- The user wants to validate a problem statement with people

## Inputs
| Input | If missing | Source |
|---|---|---|
| Research objectives or questions | Assume: derive from `design/discovery/` and tag `[inferred]`; if nothing exists, stop and point to `ux-research-planner` | plan, user |
| Participant type | Ask one: wording and sensitivity depend on it. If unanswered, assume the users named in the research plan or problem framing, tag it `[assumption]`, and use no sensitive probes | plan, user |
| Session length | Assume 45 minutes; say it is a default | user |
| Sensitive topics to avoid, or an artifact to show | Assume none; flag any sensitive probes found | user |

## Workflow
1. **Inspect the project.** Read the research plan, problem framing, and prior guides. Note decisions the interviews must inform. Copy no names or identifiers from earlier notes.
2. **Set objectives** (usually 3 to 5) from the plan. Drop any objective that interviews cannot answer, and say so.
3. **Write the consent and privacy script:** purpose, voluntary participation, right to skip or stop, recording and storage, anonymization (participant codes), and who sees the data. Align it with the plan's ethics section.
4. **Write questions.** Open, about past behavior and real situations ("tell me about the last time..."), one idea per question, no product names or answers inside the question. Add two or three probes for each core question. Avoid sensitive topics unless an objective needs them. If one does, mark it, explain why, and give the participant an easy way to skip. Address participants by nothing or by participant code. Do not add a name greeting or a name placeholder.
5. **Time-box the sections.** Warm-up, one block per objective, wrap-up. Totals must equal the session length. These splits are defaults to adjust.
6. **Map questions to objectives** in a table. Remove any question with no objective.
7. **Prepare capture:** a note template with question, observation, short paraphrase or minimal quote, and tag. Say how notes will be coded and which skill or process consumes them.
8. **Run the bias check on every question, including opening, closing, and catch-all questions:** leading, double-barreled, hypothetical-preference, and jargon questions, plus compound "or" questions and questions that list answer options. Rewrite each as one open question and compare it with the draft: a rewrite identical to the draft is not a rewrite. No shipped question joins two asks with "or"; split it into two questions or keep one ask. Never leave a note that the moderator may split it. Check that block minutes sum to the session length. Log each rewrite. Write the output per §8.

## Outputs
Metadata block (§4), then path, date, collisions, and reruns (§8), follow `../_shared/standard.md`. File:
`design/research/interview-guide-<topic>-<date>.md`:
```
> metadata block
## Study objectives (from plan)
## Participants and logistics
## Consent and privacy script
## Guide (timed sections with probes)
## Objective-to-question map
## Capture and synthesis plan (note template)
## Bias and sensitivity check
## Open questions / to validate
## Next step
```

Figma (optional, per `../_shared/figma.md`): when publishing is enabled, draw on the `Interview Guides` page one block per timed section with its minutes, the questions and probes inside each block, the objective-to-question map, and the consent script. Mark sensitive questions optional and skippable. Never draw participant names, greetings with names, or sample answers. The Markdown file stays the source of truth.

`## Next step` names exactly one handoff, the first condition below that fits, and writes only that skill: `persona-builder` when patterns across several interviews should be synthesized, or `journey-map-builder` when the goal is an end-to-end experience map. Never point back to `ux-research-planner` or to this skill.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] Chat replies follow `../_shared/personality.md`; no emoticons in written files or structured output
- [ ] Every core question maps to an objective
- [ ] No leading, double-barreled, or hypothetical-preference questions
- [ ] Sensitive questions are justified, flagged, and skippable
- [ ] Timing sums to the session length, labeled as a default
- [ ] The guide contains no sample answers or expected findings
- [ ] Any Figma output followed `../_shared/figma.md`, and the reply reports only Figma results a tool confirmed

## Boundaries
- Does not choose the method, sample, or recruiting → `ux-research-planner`
- Does not write task-based test protocols → `usability-test-planner`
- Does not synthesize results → `persona-builder`, `journey-map-builder`
