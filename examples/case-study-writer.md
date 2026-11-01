# Example: case-study-writer

> **Illustrative example.** All inputs and outputs below use invented sample data to show the output shape. Kettle is a fictional meal-kit subscription app; the artifacts, history, and claims are hypothetical.

## Prompt

```
/case-study-writer Write a portfolio case study of the Kettle "skip a week" redesign. I designed the new delivery list; one engineer built it and a PM ran the roadmap. Skip tickets dropped by half after launch.
```

## Sample input (invented)

- `design/discovery/problem-framing-skip-week-<YYYY-MM-DD>.md`: skip is hard to find; based on 3 tickets (T-01, T-03, T-08) and 2 interviews (P1, P2). Marked Provisional.
- `design/audits/design-critique-deliveries-<YYYY-MM-DD>.md`: two options critiqued, "Skip in Account settings" and "Skip on each week in the delivery list". The critique recommends the delivery-list option. No decision status is recorded in it.
- `CHANGELOG.md`: "v2.3: Skip week moved to the delivery list."
- `git log`: two commits touching `src/components/SkipWeek.tsx`, then the v2.3 tag (dates shown here as `<YYYY-MM-DD>`).
- No metrics, support export after launch, or launch notes exist. No confidentiality limits were given.

## What the skill does

1. Reads `design/`, the changelog, and git history, and builds a timeline. Commit dates are when work landed, not when design happened.
2. Classifies each claim: verified (with citation), recollection, interpretation, or missing (`[TO VERIFY: ...]`).
3. Uses "I" only for the contribution the user confirmed and "we" for team work.
4. Keeps the ticket claim out of the Outcome because nothing corroborates it. Anonymizes by default.

## Output shape (`design/docs/case-study-kettle-skip-week-<YYYY-MM-DD>.md`)

```markdown
> skill: case-study-writer · date: <YYYY-MM-DD> · scope: skip-a-week redesign · sources: design/discovery/problem-framing-skip-week-<YYYY-MM-DD>.md, design/audits/design-critique-deliveries-<YYYY-MM-DD>.md, CHANGELOG.md (v2.3), git log (2 commits, v2.3 tag) · audience: portfolio reader (default) · length target: 800 to 1200 words (default)

## Summary
Subscribers struggled to find where to skip a delivery week [verified: framing doc]. I designed a delivery list with skip on each week [recollection: user; role confirmed by the user]. The change shipped in v2.3 [verified: CHANGELOG.md]. Its effect has not been measured [verified: no outcome data in the project].

## Context and role
- Product: a meal-kit subscription web app; client details anonymized by default.
- My role: designer of the delivery list [recollection: user]. Engineering by one engineer; roadmap by a PM [recollection: user]. [TO VERIFY: whether the user also ran the research behind the framing doc]

## Problem
Three support tickets and two interviews pointed to skip being hard to find [verified: framing doc, citing T-01, T-03, T-08, P1, P2]. The framing was marked Provisional because the evidence was thin [verified: framing doc].

## Constraints
[TO VERIFY: timeline, team size beyond the user's account, and technical limits; no artifact records them]

## Process and key decisions
1. Two placements were compared: skip in Account settings and skip on each week in the delivery list [verified: critique doc].
2. The critique recommended the delivery-list option [verified: critique doc]. Whether it was formally approved is unknown; no artifact records the decision status. It shipped in v2.3 [verified: CHANGELOG.md].
3. The delivery-list option likely reduced the steps to skip [interpretation: hedged; no step count is recorded].

## Outcome (sourced, or "not yet available")
Outcome data: not yet available. The project contains no post-launch metrics or support export.

## Lessons
- Placing an action where the object lives can be worth testing early [interpretation].
- Recording decisions with their status would have made this write-up easier to verify [interpretation].

## Visuals to include
- The two options from the critique doc (existing artifact).
- No screenshots with subscriber data.

## Appendix: evidence base (timeline, claim classes, sources)
| Order | Artifact | What it shows | Class |
|---|---|---|---|
| 1 | Framing doc | Problem and evidence, Provisional | verified |
| 2 | Critique doc | Two options, recommendation, no decision status | verified |
| 3 | Commits on SkipWeek.tsx (2) | Code landed | verified |
| 4 | v2.3 changelog entry | Shipped | verified |
| — | "Skip tickets dropped by half" | User statement | recollection |

## Appendix: claims to verify
- [TO VERIFY: "skip tickets dropped by half after launch". Needs a dated ticket export for equal periods before and after v2.3, and the ticket definition used. Even then it shows a change that followed the launch, not that the launch caused it.]
- [TO VERIFY: the user's role in the research behind the framing doc.]
- [TO VERIFY: project timeline and constraints.]

## Open questions / to validate
- May the product and client be named, or must they stay anonymized?
- Is there any post-launch data at all?

## Next step
Run `product-metrics` to define how the skip outcome should be measured, since no outcome data exists.
```
