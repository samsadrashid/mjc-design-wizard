# Example: usability-test-planner

> **Illustrative example.** All inputs and outputs below use invented sample data to show the output shape. Kettle is a fictional meal-kit subscription app; the prototype and plan are hypothetical. No sessions have been run and no results exist.

## Prompt

```
/usability-test-planner Test the new Deliveries prototype in design/prototypes/deliveries-v2.md. We want to know if subscribers can skip a week and understand the cutoff.
```

## Sample input (invented)

- `design/prototypes/deliveries-v2.md`: a clickable prototype covering the Deliveries list (4 weeks), a skip confirmation dialog, and a "Skipped" row state. It does not include the past-cutoff state or any error state. Each row shows the cutoff time.
- Persona A (week-by-week skipper) in `design/research/`. No research plan, recruiting channel, or thresholds were supplied.

## What the skill does

1. Reads the prototype and lists what a participant can actually reach. The past-cutoff and error states are not built, so no task depends on them.
2. Writes tasks with realistic scenarios and prompts that avoid interface labels such as "Skip" or "Deliveries".
3. Sets measures, and tags thresholds `[assumption]` because nobody agreed them yet.
4. Writes consent, accessibility, the moderator script, a pilot checklist, and an empty results template.

## Output shape (`design/research/usability-test-plan-deliveries-v2-<YYYY-MM-DD>.md`)

```markdown
> skill: usability-test-planner · date: <YYYY-MM-DD> · scope: Deliveries prototype v2 · sources: design/prototypes/deliveries-v2.md, design/research/personas-kettle-subscribers-<YYYY-MM-DD>.md

## Test goals and artifact
- G1: Can subscribers stop next week's delivery without help?
- G2: Do subscribers understand when changes close for a week?
Artifact: clickable prototype v2 [observed: deliveries-v2.md]. Reachable: list, confirmation dialog, skipped row. Not reachable: past-cutoff and error states, so no task covers them.

## Participants and recruiting criteria
5 active subscribers (moderated default; enough to surface recurring issues within one round, not a statistical sample). Criteria: subscribed for at least one month; has stopped or wanted to stop a delivery [assumption: from Persona A]. Include at least one participant who uses assistive technology, since the app serves all subscribers.

## Consent, accessibility, and logistics
- Consent: purpose, screen and voice recording, storage in the research drive, participant codes in notes, the right to stop at any time, compensation (amount to confirm).
- Accessibility: the screener asks only which device and input method or assistive technology the participant uses. Sharing this is optional, and the consent text says so. No question asks why. Sessions allow the participant's own device and settings.
- Logistics: remote, moderated, 30 minutes, one moderator and one note-taker.

## Tasks (scenario, prompt, success criteria, observation points)
| # | Scenario and prompt | Start state | Success (observable) | Observe |
|---|---|---|---|---|
| T1 | "You'll be away next week and don't want a box to arrive. Show me what you'd do." | Prototype home | Next week's row shows the skipped state | Where they look first; any detours |
| T2 | "Before doing anything, tell me until when you could still change next week's box." | Deliveries list | States the cutoff shown on the row | Whether they find and read the cutoff |
| T3 | "You changed your mind about next week. Show me what you'd do now." | After T1 | Row returns to scheduled, or participant says it cannot be done | Whether an undo path is noticed |
| T4 | "You want no boxes for the next two weeks. Show me what you'd do." | Deliveries list | Two upcoming rows show the skipped state | Repetition, frustration, requests for a longer break |
Tasks run easy to hard. No prompt uses an interface label.

## Measures and thresholds
- Completion per task: yes, partial, no. Errors, assists, and a 1 to 5 ease rating after each task.
- Threshold for G1: at least 4 of 5 complete T1 without assistance [assumption: not agreed; set before testing by the product owner].
- Time is not measured: think-aloud slows participants, so time would mislead.

## Moderator script
"Thanks for helping. We're testing the app, not you. Please think aloud as you go. I may not answer questions during tasks, so we can see how the app works on its own." Then T1 to T4 verbatim. Neutral probes: "What are you looking for?", "What did you expect to happen?" Wrap-up: "What, if anything, was unclear?"

## Pilot checklist
- [ ] One dry run with a colleague
- [ ] Every task reachable in the prototype
- [ ] Recording works with screen readers on
- [ ] Prompts read aloud without naming interface labels

## Capture and analysis plan (empty results template, severity scale)
| Participant | Task | Completion | Errors | Assists | Ease (1-5) | Observations | Issues |
|---|---|---|---|---|---|---|---|
| P_ | T1 | | | | | | |
| P_ | T2 | | | | | | |
| P_ | T3 | | | | | | |
| P_ | T4 | | | | | | |
Issues are rated Blocker, Major, Minor, or Cosmetic (shared severity scale). The designer synthesizes; issues feed `feature-prioritization` after real sessions.

## Open questions / to validate
- Who sets the completion threshold, and when?
- Which recruiting channel can reach active subscribers?

## Next step
Run `ux-research-planner` to settle recruiting, since no channel or screener exists yet.
```
