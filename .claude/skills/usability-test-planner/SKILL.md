---
name: usability-test-planner
description: Plan a task-based usability study - participant criteria, realistic tasks with success criteria, observation points, consent and accessibility, a moderator script, and a capture and analysis plan. Plans only; it never presents hypothetical results. Use when the user says "usability test", "test the prototype", "can users complete", "test plan", or has a prototype or build to evaluate with people. Not for choosing among research methods (use `ux-research-planner`), logging build-versus-design defects (use `design-qa`), or heuristic review (use `ux-audit`).
---

# Usability Test Planner

## Purpose
Produce a protocol for evaluating a prototype or product with real participants: realistic tasks, measurable success criteria, what to observe, how to treat participants and accommodate access needs, and how results will be recorded and analyzed. The results template stays empty until real sessions happen.

## Triggers
- "Plan a usability test for X", "test this flow with users"
- A prototype, staging build, or user flow exists in the project
- A research plan selects usability testing

## Inputs
| Input | If missing | Source |
|---|---|---|
| Artifact under test (prototype, build, flow doc) | Stop: tasks cannot be written against nothing | user, `design/journeys/` |
| Goals or flows to evaluate | Ask one: tasks follow from them | user, research plan |
| Participant criteria | Assume from the research plan or personas and tag it | plan, `design/research/` |
| Moderated or unmoderated | Assume moderated; say it is a default | user |
| Known concerns from audits or critique | Assume none | `design/audits/` |

## Workflow
1. **Inspect the project.** Read the artifact and flows. List the screens, states, and data the test can actually reach, and note prototype gaps that would block a task. Copy no participant identifiers from earlier material.
2. **Define tasks.** Typically 4 to 7, a default that fits one session. Each has a realistic scenario, a start state, an observable success condition, and the expected path. Order easy to hard. Prompts must not use interface labels that reveal the route.
3. **Choose measures** that the team can record: completion (yes, partial, no), errors, assists, time if meaningful, and a post-task rating. Agree success thresholds before testing and record who set them. Otherwise tag them `[assumption]`.
4. **Define participants** and the sample, with the reason. Include people who use assistive technology when the product serves them, and prepare accessible materials and sessions. Ask about input method and assistive technology only, never reasons or conditions; say sharing is optional and cover it in the consent text.
5. **Write consent and logistics:** purpose, recording, storage, anonymization (participant codes per §8), the right to stop, equipment, and compensation.
6. **Write the moderator script:** intro, think-aloud instructions, task prompts verbatim, neutral probes, wrap-up questions.
7. **Plan capture and analysis.** An empty results template per participant per task (measures, observations, minimal quotes, issues), the severity scale from `../_shared/standard.md` §8 (Blocker, Major, Minor, Cosmetic), and who synthesizes. Issues found feed `feature-prioritization`.
8. **Add a pilot checklist.** Run one dry session and fix what it exposes. Write the output per §8.

## Outputs
Metadata block (§4), then path, date, collisions, and reruns (§8), follow `../_shared/standard.md`. File:
`design/research/usability-test-plan-<topic>-<date>.md`:
```
> metadata block
## Test goals and artifact
## Participants and recruiting criteria
## Consent, accessibility, and logistics
## Tasks (scenario, prompt, success criteria, observation points)
## Measures and thresholds
## Moderator script
## Pilot checklist
## Capture and analysis plan (empty results template, severity scale)
## Open questions / to validate
## Next step
```

Figma (optional, per `../_shared/figma.md`): when publishing is enabled, draw on the `Usability Testing` page the test goals and artifact, one task card per task (scenario, prompt, success criteria, observation points), the measures with any threshold not yet agreed marked `[assumption]`, and the empty results template. Never draw results, completion rates, or findings; none exist until real sessions run. The Markdown file stays the source of truth.

`## Next step` names `ux-research-planner` if recruiting or method is unsettled, or `feature-prioritization` to rank fixes after real sessions.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] Chat replies follow `../_shared/personality.md`; no emoticons in written files or structured output
- [ ] Each task has an observable success condition
- [ ] Task prompts do not leak interface labels
- [ ] Thresholds are agreed before testing or marked `[assumption]`
- [ ] Accessibility needs of participants are addressed
- [ ] The results template is empty and no outcomes are pre-filled
- [ ] Any Figma output followed `../_shared/figma.md`, and the reply reports only Figma results a tool confirmed

## Boundaries
- Does not choose methods or recruit → `ux-research-planner`
- Does not log build-versus-design defects → `design-qa`
- Does not run a heuristic review → `ux-audit`
- Does not write open interviews → `interview-guide-builder`
