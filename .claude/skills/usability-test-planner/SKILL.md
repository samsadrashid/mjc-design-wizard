---
name: usability-test-planner
description: Design a task-based usability test - scenarios, tasks, success criteria, metrics, script, and results template. Use when the user says "usability test", "test the prototype", "can users complete", "test plan", or has a prototype or build ready to evaluate with users.
---

# Usability Test Planner

## Purpose
Produce a complete test protocol for a prototype or live product: realistic tasks with measurable success criteria, moderator script, and a results sheet that records what happened, not what was hoped.

## Triggers
- "Plan a usability test for X", "test this flow with users"
- Prototype, staging build, or user flow exists in the project
- Research plan selects usability testing

## Inputs
| Input | Required | Source |
|---|---|---|
| Artifact under test (prototype link, build, flow doc) | yes | user, `design/journeys/` |
| Goals or flows to evaluate | yes | user, research plan |
| Participant criteria | yes | plan or user |
| Moderated vs unmoderated | yes | user (default moderated) |
| Known concerns from critique or audit | optional | `design/audits/` |

## Workflow
1. **Inspect the project.** Read the artifact and any user flows. Enumerate screens and states the test can reach. Note gaps in the prototype.
2. **Define tasks.** 4 to 7 tasks, each from a realistic scenario, with a start state, a success condition, and an optional path. Order easy to hard.
3. **Set measures.** Completion (yes/partial/no), time (if meaningful), errors, assists, post-task rating (SEQ). Define thresholds the team agreed to, or mark `[assumption]`.
4. **Write the script.** Intro, think-aloud instruction, task prompts verbatim, neutral probes, wrap-up questions.
5. **Pilot checklist.** Run one dry session; list what to fix.
6. **Results template.** Per participant per task: measures, observations, quotes, severity of issues found.
7. **Severity scale** for issues: blocker, major, minor, cosmetic, with definitions.
8. **Write output**; show the task list in chat.

## Outputs
`design/research/usability-test-plan-<topic>-<date>.md`:
```
> metadata block
## Test goals and artifact
## Participants and sessions
## Tasks (scenario, prompt, success criteria, optimal path)
## Measures and thresholds
## Moderator script
## Pilot checklist
## Results template and severity scale
## Open questions / to validate
## Next step
```

## Quality checks
- [ ] Global checks in `docs/ARCHITECTURE.md` §7
- [ ] Each task has an observable success condition
- [ ] Task prompts do not contain UI labels that give away the path
- [ ] Measures are recordable with the tools the team has
- [ ] Results template is empty; no pre-filled outcomes

## Boundaries
- Does not pick method or recruit → `ux-research-planner`
- Does not log build defects → `design-qa`
- Does not run heuristic review → `ux-audit`
