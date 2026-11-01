# Example: product-discovery

> **Illustrative example.** All inputs and outputs below use invented sample data to show the output shape. Kettle is a fictional meal-kit subscription app; the notes, tickets, and counts are hypothetical.

## Prompt

```
/product-discovery Should we build a "pause subscription" option for Kettle? Notes are in research/ and tickets in support/tickets.csv.
```

## Sample input (invented)

`research/interviews/` holds 4 short notes (P1 to P4, date unknown):

- P1: skipped deliveries twice by emailing support. Note says: "I couldn't find where to skip."
- P2: found Skip under Account > Plan > Deliveries after several minutes; missed the cutoff once and was charged.
- P3: never skips; changes recipes on the menu page.
- P4: wanted to pause for a month and cancelled instead, because pausing was not offered.

`support/tickets.csv`, 8 rows, ticket authors not linked to interviewees:

```
id,subject,tag
T-01,How do I skip next week?,skip
T-02,Charged after I skipped,billing
T-03,Where is the skip button,skip
T-04,Recipe swap not saving,menu
T-05,Can I pause for a month?,pause
T-06,Missed the cutoff by an hour,cutoff
T-07,Delivery late,delivery
T-08,How to skip a week,skip
```

No analytics, roadmap, or prior brief exists.

## What the skill does

1. Reads README, `docs/`, `design/`, `research/`, and the ticket export. Finds no prior brief.
2. Restates the opportunity and answers the direct question only as far as the evidence allows.
3. Builds the evidence inventory, lists gaps, and ranks hypotheses by risk.
4. Plans methods for the riskiest hypotheses, marked planned, not done.

## Output shape (`design/discovery/product-discovery-pause-subscription-<YYYY-MM-DD>.md`)

```markdown
> skill: product-discovery · date: <YYYY-MM-DD> · scope: pause subscription option · sources: research/interviews/P1-P4 (date unknown), support/tickets.csv (8 rows, date unknown)

## Opportunity statement
Subscribers who want a break from deliveries may leave instead of pausing, because the product offers no pause [observed: P4 note; T-05]. Your question, whether to build a pause option: not answerable yet. One interviewee cancelled for lack of a pause and one ticket asks for one; that is a signal, not demand. This brief reads only existing material; no discovery activity has been carried out.

## Context and constraints
- Users in the material: weekly subscribers [observed: P1 to P4]. No segments are defined [assumption].
- Today's alternatives: skip one week at a time [observed: P2 note], email support [observed: P1 note], or cancel [observed: P4 note].
- Constraints: none supplied; billing cutoff behavior is unknown [assumption].

## Evidence inventory (claim, tag, source, confidence)
| Claim | Tag | Source | Confidence |
|---|---|---|---|
| A subscriber cancelled because pause was not offered | observed | P4 note | Low: one person |
| A ticket asks for a month-long pause | observed | T-05 | Low: one ticket |
| Subscribers struggle to find skip: 3 tickets (T-01, T-03, T-08) and 2 interviewees (P1, P2) | observed | tickets.csv tag=skip; P1, P2 notes | Medium: two source types agree |
| Cutoff timing causes charges after a skip attempt: T-02, T-06, P2 | observed | tickets.csv; P2 note | Low: three items, cause not stated in T-02 |

## Knowledge gaps
1. How many cancellations cite a break as the reason. No data available; a cancellation-reason export would answer it.
2. Whether skip findability, not missing pause, drives the break-related tickets.
3. Billing cutoff rules and whether pause is technically possible.

## Hypotheses (ranked by risk)
1. We believe subscribers who want a multi-week break cancel because only single-week skip exists, because P4 cancelled for that reason [observed: P4]. If true, a pause would retain some of them. Risk: high impact if wrong, Low confidence.
2. We believe some requests for a break are really failed skips, because skip is hard to find [observed: T-01, T-03, T-08, P1, P2]. If true, improving skip comes before pause. Risk: high, Medium confidence.
3. We believe cutoff confusion causes unexpected charges [observed: T-06, P2; inferred for T-02]. If true, any pause needs clear cutoff feedback. Risk: medium, Low confidence.

## Discovery plan (hypothesis → method → signal)
| Hypothesis | Method (planned) | Confirming signal | Refuting signal |
|---|---|---|---|
| 1 | Cancellation-reason analysis; short interviews with recent cancellers | Break or time-off is a frequent stated reason | Price or menu dominates |
| 2 | Task-based test of finding Skip | Participants fail or take long to find Skip | Skip is found quickly |
| 3 | Review billing rules with the owner | Cutoff is unclear in the UI | Cutoff is shown at the point of skipping |

## Open questions / to validate
- Is pausing possible in the billing system? [assumption]
- Do the 8 tickets reflect normal volume? The export has no dates.

## Next step
Run `ux-research-planner` to design the cancellation and skip-findability studies, since gaps dominate the evidence.
```
