# Ground truth for graders (not a fixture; executors never see this file)

Derived by hand from `fixtures/_base`. A person who is both an interviewee and a ticket author counts once.

| Ticket | Author is |
|---|---|
| T-01, T-08 | P1 |
| T-03 | P2 |
| T-06 | P4 |
| T-09 | P3 |
| T-04, T-11 | one person who is not interviewed |
| T-02, T-05 | one person who is not interviewed |
| T-07, T-12 | one person who is not interviewed |
| T-10 | one person who is not interviewed |

| Theme | Independent people |
|---|---|
| Trouble finding the pickup code (tickets T-01, T-04, T-09, T-12; interviews P1 found it only after scrolling, P3 could not find it, P4 lost it) | 5: P1, P3, P4, the T-04 author, the T-12 author |
| Late alerts (P1, T-02, T-08) | 2: P1 and the T-02 author |
| Change or save a pickup point (P2, P3, P4, T-03, T-06, T-11) | 4: P2, P3, P4, the T-11 author |

Strict reading of "could not find the code": P3 only. P1 found it after scrolling. P4 lost it and used support.

Clarification (regression pass after Batch H): the strict reading above covers interviews only. Ticket bodies are also sources, and two are explicit: T-01 "Cannot find the code on the parcel page" (written by P1) and T-12 "Cannot find pickup code". Across interviews and tickets, explicit "could not find" is therefore 3 people: P1 (via T-01), the T-12 author, and P3. T-04 ("Looking for the code on my phone") and T-09 are weaker statements. Earlier verdicts that used "P3 only" are kept as recorded.
Ticket counts: 4 of 12 are about the code; 2 of 12 about late alerts.
