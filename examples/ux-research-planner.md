# Example: ux-research-planner

> **Illustrative example.** All inputs and outputs below use invented sample data to show the output shape. Kettle is a fictional meal-kit subscription app; the brief, decision, and plan are hypothetical. No research has been conducted.

## Prompt

```
/ux-research-planner We need to decide whether to build a pause option or fix skip first. Use the discovery brief in design/discovery/.
```

## Sample input (invented)

- `design/discovery/product-discovery-pause-subscription-<YYYY-MM-DD>.md`: hypotheses H1 (subscribers wanting a break cancel because only single-week skip exists), H2 (some "break" requests are failed skips), H3 (cutoff confusion causes charges). Evidence: 4 interview notes (P1 to P4) and 8 tickets, dates unknown.
- No prior study plans or personas exist. No budget, timeline, or recruiting channel was supplied.

## What the skill does

1. Reads the brief and `design/research/`; finds no earlier plan to repeat or contradict.
2. Takes the decision from the prompt and states the cost of being wrong.
3. Writes research questions mapped to the brief's assumptions, picks a method per question, and says why cheaper options were rejected.
4. With no constraints supplied, plans the lowest-cost option and says so. Records nothing as a finding.

## Output shape (`design/research/ux-research-planner-pause-vs-skip-<YYYY-MM-DD>.md`)

```markdown
> skill: ux-research-planner · date: <YYYY-MM-DD> · scope: pause vs skip decision · sources: design/discovery/product-discovery-pause-subscription-<YYYY-MM-DD>.md (date unknown)

## Decision and research questions (mapped to assumptions)
Decision: build a multi-week pause first, or fix skip findability first [reported: user]. Cost of being wrong: one quarter of work on the less useful option [inferred].
| # | Research question | Assumption tested |
|---|---|---|
| RQ1 | What reasons do recent cancellers give for leaving, in their own words? | H1: wanting a break drives cancellation |
| RQ2 | Can current subscribers find and complete Skip for next week? | H2: skip findability, not missing pause, drives break requests |
| RQ3 | How do subscribers understand the weekly cutoff? | H3: cutoff confusion causes unexpected charges |
| RQ4 | How long a break do subscribers who want one describe? | Pause length, an open decision in the brief |

## Method selection and rationale
| RQ | Method | Why this method | Rejected alternative and why |
|---|---|---|---|
| RQ1, RQ4 | Remote interviews with recent cancellers | Reasons and context need conversation | Exit survey: Kettle has none instrumented, and free text alone gives no follow-up |
| RQ2 | Moderated remote usability test on the live site | Directly shows whether Skip is found | Analytics funnel: skip events are counts not linked to people, so they cannot show where individuals fail |
| RQ3 | Questions inside the RQ2 sessions | Same participants, no extra recruiting | Separate study: costs more for a narrow question |
No quantitative method is planned: there is no instrumented cancellation-reason data and no sample size that would support one.

## Participants and screener
- Segment A, recent cancellers: 5 to 8 (default for qualitative work, chosen because it tends to surface recurring themes within budget; not a statistical guarantee).
- Segment B, active subscribers who have never skipped: 5 (same default).
- Exclusions: employees; anyone in another Kettle study in the last 3 months (default).
- Screener: "How long have you had a Kettle subscription?", "In the last two months, did you skip, pause, or cancel any deliveries?", "Which device do you use most for Kettle?"

## Recruiting, consent, and ethics
- Channel: email to opted-in subscribers [assumption: the team's real channels were not supplied].
- Consent: purpose, recording, storage, right to stop, and that answers do not affect the account. Compensation: amount to confirm [assumption].
- Data handling: recordings stored in the team's research drive, access limited to the study team, participant codes only in notes, deletion after synthesis (default retention to confirm).
- Cancellation reasons can be personal; the guide must not probe reasons a participant does not offer.

## Data capture and analysis plan
- Notes per session with participant code, task outcome (RQ2), and paraphrased reasons (RQ1, RQ4).
- Coding: affinity grouping by reason and by failure point, reviewed by a second person.
- Synthesis owner: the product designer (no dedicated synthesis skill exists). Output feeds `persona-builder` and the pause-vs-skip decision.

## Timeline, roles, and feasibility
- Lowest-cost plan (no constraints were supplied): remote sessions only, about 2 weeks for recruiting and 1 week for sessions [assumption].
- Roles: one moderator, one note-taker (to confirm).
- If only one week is available, cut Segment B and run RQ2 with 5 cancellers.

## Open questions / to validate
- What budget and timeline are available?
- Which recruiting channels does the team actually have?
- Is the compensation policy set?

## Next step
Run `interview-guide-builder` to write the canceller interview guide for RQ1 and RQ4.
```
