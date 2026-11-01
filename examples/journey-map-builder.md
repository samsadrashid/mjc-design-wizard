# Example: journey-map-builder

> **Illustrative example.** All inputs and outputs below use invented sample data to show the output shape. Kettle is a fictional meal-kit subscription app; the notes, tickets, and event counts are hypothetical.

## Prompt

```
/journey-map-builder Map the current journey of the week-by-week skipper persona, from deciding to skip a week to the next delivery. Use design/research/, support/tickets.csv, and analytics/skip-events.csv.
```

## Sample input (invented)

- `design/research/personas-kettle-subscribers-<YYYY-MM-DD>.md`: Persona A, week-by-week skipper, built from P1, P2, U3, U7.
- Interview notes (date unknown): P1 skipped by emailing support, "I couldn't find where to skip."; P2 found Skip under Account > Plan > Deliveries after several minutes and was charged once after missing the cutoff.
- Tickets (date unknown): T-01 "How do I skip next week?", T-03 "Where is the skip button", T-08 "How to skip a week", T-06 "Missed the cutoff by an hour", T-02 "Charged after I skipped". The persona doc records that T-01 was written by P1 and T-06 by P2; the other tickets have different authors.
- `analytics/skip-events.csv`, 4 weeks, event counts not linked to people:

```
week,deliveries_page_view,skip_confirmed
1,410,120
2,395,131
3,430,118
4,402,127
```

## What the skill does

1. Reads the persona, notes, tickets, and events, and codes every source. No identifiers are copied.
2. Defines stages from the subscriber's point of view and fills each lane only from evidence.
3. Writes `Not reported` where no participant stated an emotion. Labels the event ratio a ratio of counts, not a conversion rate.
4. Marks moments of truth and lists opportunities as problem spaces linked to cited pains.

## Output shape (`design/journeys/journey-map-week-by-week-skipper-skip-a-week-<YYYY-MM-DD>.md`)

```markdown
> skill: journey-map-builder · date: <YYYY-MM-DD> · scope: current state, deciding to skip to next delivery · sources: persona doc (4 people), interview notes P1-P2 (date unknown), tickets T-01, T-02, T-03, T-06, T-08 (date unknown), analytics/skip-events.csv (4 weeks, weeks not dated)

## Actor and scope
Actor: week-by-week skipper (Persona A, from `persona-builder`). Scope: current state, from deciding not to take next week's box to the following delivery.

## Evidence base (source, type, count, date, confidence)
| Code | Source | Type | Count | Date | Confidence |
|---|---|---|---|---|---|
| P1, P2 | Interview notes | Interviews | 2 | date unknown | Medium |
| T-01, T-02, T-03, T-06, T-08 | tickets.csv | Tickets | 5 | date unknown | Medium |
| A1 | skip-events.csv | Event counts | 4 weeks | weeks not dated | Medium |

## Journey map (lanes as rows, stages as columns)
| Lane | 1 Decide to skip | 2 Look for skip | 3 Skip the week | 4 Cutoff and billing | 5 Next delivery |
|---|---|---|---|---|---|
| Goal | Not take next week's box [observed: T-01, T-08] | Find where to skip [observed: T-03] | Confirm the week is skipped [inferred: from stage 2 goal] | Not be charged for the skipped week [observed: T-02] | Not reported |
| Actions | Not observed | Searches account settings [observed: P2]; emails support [observed: P1] | Uses Skip in Account > Plan > Deliveries [observed: P2] | Not observed | Not observed |
| Touchpoints | Not observed | Account settings page [observed: P2]; support email [observed: P1] | Deliveries page [observed: P2; A1] | Billing [observed: T-02, T-06] | Not observed |
| Pain points | Not observed | Cannot find skip: P1 explicit; P2 found it after several minutes; T-01, T-03, T-08 ask how or where (T-01 is P1) | Not observed | Charged after missing the cutoff [observed: P2, T-06]; charged after skipping, cause not stated [observed: T-02] | Not observed |
| Emotion | Not reported | Not reported | Not reported | Not reported | Not reported |
| Metrics | Not observed | Deliveries page views: 410, 395, 430, 402 per week [observed: A1] | skip_confirmed per week: 120, 131, 118, 127 [observed: A1] | No data available | No data available |

Ratio of counts (not a conversion rate): skip_confirmed ÷ deliveries_page_view per week = 0.293, 0.332, 0.274, 0.316 [observed: A1]. The counts are not linked to the same people, so this does not show how many viewers went on to skip.

## Stage transitions
- 1 → 2: the subscriber goes looking for skip; how they start is not observed.
- 2 → 3: stalls when skip is not found; P1 left the app and emailed support instead [observed: P1].
- 3 → 4: the cutoff applies; P2 missed it once and was charged [observed: P2].
- 4 → 5: no evidence on what happens before the next delivery [Not observed].

## Moments of truth
1. Stage 2, look for skip: the most supported pain, 4 people with trouble finding skip (P1, P2, and the authors of T-03 and T-08; T-01 is P1) [observed].
2. Stage 4, cutoff and billing: 2 people report a charge around skipping: P2 (missed the cutoff; also wrote T-06) and the author of T-02 (cause not stated) [observed; the cutoff link for T-02 is inferred].

## Opportunities (problem spaces, linked to pain)
- Subscribers cannot find where to skip a week, linked to the stage 2 pain [inferred].
- Subscribers do not know when the cutoff falls before acting, linked to the stage 4 pain [inferred].

## Evidence gaps and uncertainties
- Stage 1 and stage 5 have no evidence for actions, touchpoints, or pains.
- No participant stated an emotion; the Emotion lane is empty by design.
- Event weeks are undated, and events are not linked to people.

## Open questions / to validate
- What prompts a subscriber to skip (stage 1)?
- Does anything happen between billing and the next delivery?

## Next step
Run `user-flow-designer` to detail stage 2, where the strongest pain sits.
```
