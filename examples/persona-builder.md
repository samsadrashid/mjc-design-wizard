# Example: persona-builder

> **Illustrative example.** All inputs and outputs below use invented sample data to show the output shape. Kettle is a fictional meal-kit subscription app; the notes, tickets, and profiles are hypothetical.

## Prompt

```
/persona-builder Build personas for Kettle subscribers from research/interviews/ and support/tickets.csv.
```

## Sample input (invented)

`research/interviews/`, 4 notes, date unknown:

- P1: skipped deliveries twice by emailing support. Note says: "I couldn't find where to skip."
- P2: found Skip under Account > Plan > Deliveries after several minutes; missed the cutoff once and was charged.
- P3: never skips; changes recipes on the menu page.
- P4: wanted to pause for a month and cancelled instead, because pausing was not offered. The note also holds a personal aside unrelated to the product (redacted in this example).

`support/tickets.csv`, 8 rows, date unknown. Matching authors by contact details (done internally, identifiers not printed): T-01 was written by P1 and T-06 by P2. The other six tickets have six different authors, coded U2 to U7 below.

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

## What the skill does

1. Reads all research, codes every source, and counts independent people: 4 interviewees plus 6 ticket-only authors = 10.
2. Extracts attributes with source codes and the number of independent people behind each.
3. Clusters on behavior and goals. A cluster becomes a persona only if at least 3 independent people show the core pattern (default gate); below that it is a provisional profile.
4. Omits the personal aside with the generic sentence only, and lists what remains unknown.

## Output shape (`design/research/personas-kettle-subscribers-<YYYY-MM-DD>.md`)

```markdown
> skill: persona-builder · date: <YYYY-MM-DD> · scope: Kettle subscribers · sources: research/interviews/P1-P4 (4 notes, date unknown), support/tickets.csv (8 tickets, date unknown) · independent people: 10 · gate: 3 independent people (default)

## Evidence base (sources, counts, dates)
| Source | Type | Count | Date |
|---|---|---|---|
| research/interviews/ | Interview notes | 4 people (P1 to P4) | date unknown |
| support/tickets.csv | Tickets | 8 tickets; 6 authors not interviewed (U2 to U7); T-01 is P1, T-06 is P2 | date unknown |
Independent people: P1, P2, P3, P4, U2 (T-02), U3 (T-03), U4 (T-04), U5 (T-05), U6 (T-07), U7 (T-08) = 10.
Some personal details in the sources were left out for privacy.

## Attribute extraction table
| Attribute | Evidence (paraphrase or minimal quote) | Sources | Independent people |
|---|---|---|---|
| Pain: could not find skip (explicit) | "I couldn't find where to skip." | P1 | 1 |
| Pain: asked how or where to skip | Ticket subjects ask how or where to skip | U3 (T-03), U7 (T-08); T-01 is P1, already counted | 2 |
| Pain: had trouble finding skip, including weaker statements | P1, U3, U7 as above; P2 found it only after several minutes (weaker, listed as such) | P1, P2, U3, U7 | 4 |
| Behavior: skips week by week | Skipped by email; found Skip in settings | P1, P2 | 2 |
| Pain: charged after missing the cutoff (explicit) | Missed the cutoff and was charged | P2 (note and T-06) | 1 |
| Pain: charged around a skip, including tickets that state no cause | As above, plus "Charged after I skipped" with no cause stated | P2, U2 (T-02) | 2 |
| Goal: a break of several weeks | Wanted to pause a month; asked for a month's pause | P4, U5 (T-05) | 2 |
| Behavior: changes recipes, does not skip | Changes recipes on the menu page | P3 | 1 |

## Patterns and personas (provisional profiles marked)
**Persona A: week-by-week skipper.** Gate met: 4 independent people (P1, P2, U3, U7).
- Goal: skip a single upcoming week without help [observed: P1, U3, U7] · confidence Medium.
- Key behaviors: skips occasionally; asks support when skip is not found [observed: P1] · confidence Low.
- Pains: cannot find skip, or finds it only after a search [observed: P1, P2, U3, U7] · confidence Medium.
- Tools today: the web app's account settings and support email [observed: P1, P2] · confidence Low.
- Design implication: put skip where the upcoming weeks are shown [inferred].

**Provisional profile B: break-seeker.** Below the gate: 2 people (P4, U5).
- Goal: stop deliveries for several weeks without cancelling [observed: P4, U5] · confidence Low.

**Provisional profile C: cutoff-caught subscriber.** Below the gate: 2 people (P2, U2).
- Pain: charged for a week they meant to skip [observed: P2; inferred for U2, whose ticket does not state the cause] · confidence Low.

## What remains unknown
- How often subscribers skip, and how many want multi-week breaks: no analytics supplied.
- Whether break-seekers and week-by-week skippers are different people or the same people at different times.
- Device and context of use: not in any source.

## Anti-persona (optional)
None: the evidence does not support one.

## Open questions / to validate
- Is the 3-person gate right for this decision, or should the team set another?
- Would interviews with recent cancellers move profile B above the gate?

## Next step
Run `ux-research-planner` to gather evidence for the two provisional profiles.
```
