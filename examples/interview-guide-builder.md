# Example: interview-guide-builder

> **Illustrative example.** All inputs and outputs below use invented sample data to show the output shape. Kettle is a fictional meal-kit subscription app; the plan and questions are hypothetical. No interviews have been run.

## Prompt

```
/interview-guide-builder Write the guide for the canceller interviews in design/research/. Participants are people who cancelled Kettle in the last two months.
```

## Sample input (invented)

- `design/research/ux-research-planner-pause-vs-skip-<YYYY-MM-DD>.md`: RQ1 (reasons recent cancellers give for leaving) and RQ4 (break length subscribers describe), remote interviews, recordings kept in the research drive, participant codes in notes.
- Session length not given (default 45 minutes applies). Sensitive topics: the plan warns that cancellation reasons can be personal.
- No prior guides exist.

## What the skill does

1. Reads the plan and takes its objectives; adds one about the cancellation moment, which the plan's RQ1 implies.
2. Writes a consent and privacy script aligned with the plan.
3. Writes open, past-behavior questions with probes, then time-boxes them to 45 minutes.
4. Runs the bias check on every question, including the opener and the closing catch-all, and logs each rewrite.

## Output shape (`design/research/interview-guide-cancellers-<YYYY-MM-DD>.md`)

```markdown
> skill: interview-guide-builder · date: <YYYY-MM-DD> · scope: recent cancellers, 45 min (default) · sources: design/research/ux-research-planner-pause-vs-skip-<YYYY-MM-DD>.md

## Study objectives (from plan)
- O1: Understand the reasons recent cancellers give for leaving, in their own words (RQ1).
- O2: Understand what happened in the days before they cancelled (implied by RQ1) [inferred].
- O3: Understand how long a break, if any, they wanted (RQ4).
Dropped: "How many subscribers would use a pause?" Interviews cannot measure how widespread something is.

## Participants and logistics
Recent cancellers, 5 to 8 per the plan. Remote video call, 45 minutes (default). One moderator, one note-taker. Participants are addressed by nothing or by participant code in notes.

## Consent and privacy script
"Thanks for joining. We want to learn how people decide to stop a meal-kit subscription. There are no right or wrong answers, and nothing you say affects your account. Taking part is voluntary. You can skip any question or stop at any time without giving a reason. With your permission we will record the call. The recording stays in our research drive, only the study team can access it, and notes use a code, not your name. We delete recordings after analysis. Is it OK to start recording?"

## Guide (timed sections with probes)
| Section | Minutes | Question | Probes |
|---|---|---|---|
| Warm-up | 5 | Tell me about how meals were planned in your home while you had Kettle. | What did a typical week look like? |
| O2 | 12 | Tell me about the last week before you cancelled. | What changed that week? · What did you try first? |
| O2 | | Walk me through the moment you decided to cancel. | Where were you? · What did you look at on the screen? |
| O1 | 15 | What led you to stop the subscription? | What else played a part? · What would have needed to be different? |
| O1 | | Before cancelling, what did you try in the app? | How did that go? |
| O3 | 8 | Tell me about a time you wanted fewer deliveries for a while. | How long was that? · What did you do then? |
| Wrap-up | 5 | Is there anything about stopping your subscription we have not asked about? | — |
Total: 5 + 12 + 15 + 8 + 5 = 45 minutes (default split; adjust per session).

Sensitive area: reasons for cancelling can be personal. The moderator does not probe reasons the participant does not offer, and reminds the participant they can skip. No question asks about money, health, or household circumstances directly.

## Objective-to-question map
| Objective | Questions |
|---|---|
| O1 | "What led you to stop…", "Before cancelling, what did you try…" |
| O2 | "Tell me about the last week…", "Walk me through the moment…" |
| O3 | "Tell me about a time you wanted fewer deliveries…" |
The warm-up and wrap-up serve all objectives.

## Capture and synthesis plan (note template)
| Code | Question | Observation | Paraphrase or minimal quote | Tag |
|---|---|---|---|---|
| P_ | | | | observed / reported |
Notes are coded by reason and by moment (before, during, after cancelling) and feed `persona-builder` and the pause-vs-skip decision.

## Bias and sensitivity check
| Draft | Problem | Rewrite (shipped) |
|---|---|---|
| "Did you cancel because there was no pause option?" | Leading; names a feature | "What led you to stop the subscription?" |
| "Would you use a pause if we built one?" | Hypothetical preference | "Tell me about a time you wanted fewer deliveries for a while." |
| "Was it the price or the recipes?" | Compound "or"; lists answer options | "What led you to stop the subscription?" (merged with the first rewrite) |
| "How easy was the cancellation flow?" | Leading ("easy"); jargon ("flow") | "Walk me through the moment you decided to cancel." |
| "Anything else about pricing, delivery, or the app?" | Catch-all that lists answer options | "Is there anything about stopping your subscription we have not asked about?" |
Every shipped question was checked, including the warm-up and the closing catch-all. Timing sums to 45.

## Open questions / to validate
- Is the 45-minute default right for this group?
- Will a show-and-tell of the cancellation screens be allowed, or is recall enough?

## Next step
Run `persona-builder` once several interviews have been synthesized, to look for patterns across cancellers.
```
