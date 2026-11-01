# Example: mvp-planner

> **Illustrative example.** All inputs and outputs below use invented sample data to show the output shape. Kettle is a fictional meal-kit subscription app; the framing, backlog, and constraints are hypothetical.

## Prompt

```
/mvp-planner Scope the smallest version of "taking a break" for Kettle. Problem framing is in design/discovery/. Backlog: pause for up to 4 weeks, skip from the delivery list, cutoff countdown, reactivation reminder email, gift a skipped week to a friend. When can we ship it?
```

## Sample input (invented)

- `design/discovery/problem-framing-taking-a-break-<YYYY-MM-DD>.md` (Provisional, Low confidence): subscribers who want a multi-week break need a way to stop deliveries without cancelling, because one interviewee cancelled for lack of a pause (P4) and one ticket asks for a month's pause (T-05).
- The five backlog items in the prompt. No prioritization output exists.
- The repo has a per-week skip (`/account/plan/deliveries`) and a billing job that runs at each weekly cutoff. No pause state exists in the subscription model.
- Team, time, and platform constraints: not supplied (the skill asks one question; unanswered here).

## What the skill does

1. Reads the framing and finds the existing skip feature to reuse. Asks one question about constraints; with no answer, records them as unknown and gives no dates.
2. Names the riskiest assumption and the single core loop for one user type.
3. Puts each backlog item in MVP, later, or out, with a reason tied to the loop or learning goal. Adds nothing that was not in the backlog.
4. Answers "when can we ship?" under Risks: no date can be given without the constraints.

## Output shape (`design/planning/mvp-plan-taking-a-break-<YYYY-MM-DD>.md`)

```markdown
> skill: mvp-planner · date: <YYYY-MM-DD> · scope: taking a break · sources: design/discovery/problem-framing-taking-a-break-<YYYY-MM-DD>.md (date unknown), backlog in prompt, src/ (skip route, billing job)

## Problem, users, and outcome (evidence and confidence)
- Problem: subscribers who want a multi-week break may cancel because only single-week skip exists [observed: framing doc, citing P4 and T-05]. Confidence Low: one interviewee and one ticket.
- Users: active weekly subscribers [inferred: from the framing; no persona exists].
- Outcome: subscribers who want a break stop deliveries without cancelling [reported: framing doc].

## Learning goal and riskiest assumption
Riskiest assumption: subscribers who would otherwise cancel will choose a pause when offered one [assumption].
Confirm: some subscribers who reach cancellation pick pause instead and later resume. Refute: pause is rarely chosen, or paused subscribers do not resume.

## Core loop
One user type: an active weekly subscriber. Loop: Deliveries page → choose "pause" → pick 1 to 4 weeks → see paused weeks and the resume week → deliveries resume automatically.

## Scope table (in MVP, later, out, with reasons and dependencies)
| Candidate (source) | Decision | Reason | Dependencies |
|---|---|---|---|
| Pause for up to 4 weeks (backlog) | In MVP | It is the core loop and tests the learning goal | A pause state in the subscription model; billing job must skip paused weeks |
| Skip from the delivery list (backlog) | Out | Already exists in the product [observed: skip route] | None |
| Cutoff countdown (backlog) | Later | Helps skip and pause timing, but the learning goal does not need it | Cutoff time available to the UI |
| Reactivation reminder email (backlog) | Later | Improves resuming, not the decision to pause | Email service; consent for messages |
| Gift a skipped week (backlog) | Out | Unrelated to the core loop and learning goal | — |

## Release slices
| Slice | Scope | Learning goal | Exit criteria (observable) | Dependencies |
|---|---|---|---|---|
| 1 | Pause 1 to 4 weeks from the Deliveries page; automatic resume | Do subscribers choose pause over cancel? | Pause can be set, billing skips paused weeks, deliveries resume; events below are recorded | Pause state; billing change |
| 2 | Offer pause at the start of cancellation | Does offering pause at cancellation change the choice? | Offer shown and choice recorded | Slice 1 |

## Risks, assumptions, and unresolved decisions
| Item | Type | Reasoning | Owner |
|---|---|---|---|
| Billing may charge a paused week if the job is not changed | Risk, high impact | The job runs at every weekly cutoff [inferred: billing job in src/] | owner unknown |
| Maximum pause length of 4 weeks | Unresolved decision | Came from the backlog item; no evidence for 4 over another length [inferred] | owner unknown |
| Subscribers want pause rather than easier skip | Assumption | Rests on one interview and one ticket [inferred: framing confidence Low] | owner unknown |
| Ship date | Unresolved | You asked when this can ship. No date can be given: team size, time available, and platform constraints were not supplied. Needed: team capacity, an engineering estimate for the pause state and billing change, and any release windows | owner unknown |

## Validation plan and plan-change triggers
- Measures to define with `product-metrics`: pause starts, resumes after pause, and cancellations, each with a definition and window. No targets are set here.
- Research to plan with `ux-research-planner`: short interviews with subscribers who paused or cancelled.
- Expand (build slice 2) if subscribers choose pause and resume. Cut the cancellation offer if pause is rarely chosen. Stop if paused subscribers mostly cancel at resume.
- No results are claimed; nothing has been built or measured.

## Definition of done (slice 1)
- Pause of 1 to 4 weeks can be set and cancelled before the cutoff.
- The billing job does not charge paused weeks.
- Events `pause_started` and `pause_resumed` are emitted with week count and no personal identifiers [proposed; names to confirm with `product-metrics`].
- Paused weeks and the resume week are visible on the Deliveries page.

## Open questions / to validate
- What team and time are available? (asked; unanswered)
- Is 4 weeks the right maximum?
- Can the billing job skip paused weeks without a migration?

## Next step
Run `product-metrics` to define the pause, resume, and cancellation measures the validation plan depends on.
```
