---
name: case-study-writer
description: Write a credible portfolio or internal case study for a finished project from documented artifacts, git history, and the user's own account, separating verified facts from recollection and interpretation, representing the user's contribution accurately, and flagging every claim to verify. Use when the user says "case study", "write up this project", "portfolio piece", "project retrospective narrative". Not for writing specs (use `design-documentation`) or defining and computing metrics (use `product-metrics`).
---

# Case Study Writer

## Purpose
Turn a project's real artifacts into a narrative that shows the problem, the constraints, the decisions and their reasons, and what came of it. Outcomes, numbers, and impact appear only when sourced. The user's role is stated as the user confirms it. Anything unproven is marked for the user to verify. The result must survive a reader asking "how do you know?".

## Triggers
- "Write a case study for X", "portfolio write-up", "summarize this project for review"
- A project reaches a milestone and `design/` holds its artifacts
- Review or hiring preparation

## Inputs
| Input | If missing | Source |
|---|---|---|
| Project artifacts: `design/` outputs, repo, changelog, git history | Stop: nothing to ground the narrative. Point to the skills that produce the artifacts | `design/`, repo |
| The user's role and collaborators | Ask one: accurate attribution depends on it. If unanswered, write the contribution as `[TO VERIFY]` | user |
| Audience | Assume a hiring or portfolio reader and say so | user |
| Outcome data: metrics, feedback, launch notes | Assume none; write "Outcome data: not yet available" | user, `design/metrics/` |
| Confidentiality limits on clients, users, or internal details | Assume strict: anonymize and flag | user |
| Length target | Assume 800 to 1200 words as a default for a portfolio read | user |

## Workflow
1. **Inspect the project.** Read every `design/` artifact, the changelog, and the git history if available (`git log` for dates and areas changed). Build a timeline of date, artifact, and decision. Commit dates show when work landed, not when design happened. Commit authors show who committed, not who designed. Do not copy author emails or other identifiers. When tickets and interviews both appear, match ticket authors to interviewees by identity, internally and without printing the identifiers; count each person once and list the members beside every count.
2. **Classify every claim** you may use:
   - **Verified:** supported by an artifact or the history, with a citation.
   - **Recollection:** supplied by the user. Label it so, and keep it out of the Outcome unless corroborated.
   - **Interpretation:** a reasonable reading. Use hedged wording.
   - **Missing:** write `[TO VERIFY: what is needed]`.
3. **Fix the audience and role.** Separate the user's own work from team work. Use "I" only for what the user confirmed. Use "we" for team outcomes.
4. **Extract the arc:** context, problem, constraints, key decisions with the alternatives considered, process, outcome, lessons. Each point cites an artifact. State a decision's status (rejected, approved, shipped) only if an artifact records it; otherwise say the status is unknown.
5. **Write the outcome carefully.** Include a number only with its source, period, and meaning, and a baseline if it is a change. Never state a conversion lift, user count, revenue effect, or timeline you cannot cite. Say a result followed a decision. Say a decision caused a result only if an experiment or other evidence supports it.
6. **Protect confidential material.** Anonymize clients, users, and unreleased details by default, and flag items for the user's clearance. Do not embed screenshots with user data.
7. **Draft** in plain language, leading with the problem and not the solution. Then list the visuals to embed, using only existing artifacts.
8. **Run an honesty pass.** Remove or flag every claim without a classification. Write the output per §8.

## Outputs
Metadata block (§4), then path, date, collisions, and reruns (§8), follow `../_shared/standard.md`. File:
`design/docs/case-study-<project>-<date>.md`. The two appendix sections are for the author and are removed before publishing.
```
> metadata block (artifacts and history used)
## Summary
## Context and role
## Problem
## Constraints
## Process and key decisions
## Outcome (sourced, or "not yet available")
## Lessons
## Visuals to include
## Appendix: evidence base (timeline, claim classes, sources)
## Appendix: claims to verify
## Open questions / to validate
## Next step
```
`## Next step` names one handoff: `design-documentation` if technical detail is missing, or `product-metrics` if outcome measurement is missing.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] Every decision cites an artifact; every claim is classified verified, recollection, interpretation, or missing
- [ ] No outcome number, lift, user count, quote, or timeline without a source
- [ ] No causal claim without supporting evidence
- [ ] The user's contribution and the team's are distinguished, as confirmed by the user
- [ ] Placeholders are labeled `[TO VERIFY]`, and confidential details are anonymized or flagged
- [ ] Length is within the target, labeled as a default

## Boundaries
- Does not write specs → `design-documentation`
- Does not define or compute metrics → `product-metrics`
- Does not critique the design → `design-critique`
