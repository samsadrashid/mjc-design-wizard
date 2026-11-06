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
| Length target | Assume 800 to 1200 words as a default for a portfolio read, counted over the body as defined in step 8 | user |

## Workflow
1. **Inspect the project.** Read every `design/` artifact, the changelog, and the git history if available (`git log` for dates and areas changed). Build a timeline of date, artifact, and decision. Commit dates show when work landed, not when design happened. Commit authors show who committed, not who designed. Do not copy author emails or other identifiers. When tickets and interviews both appear, count each person once as `../_shared/standard.md` §8 sets out. Write the strict count first; then build the weaker-statements line by removing every person already in the strict line (a ticket author who was also interviewed is one person) and only then write its number.
2. **Build the evidence table before drafting.** One row per piece of evidence, kept in `## Appendix: evidence base` with the columns `Evidence ID | Source (kind and ID or path) | Participant | Exact words or location | Claim it establishes | Class | Limits`. Kinds are kept apart: interview (P1), ticket (T-01), research artifact, product artifact, commit. Participant is the person, if known (`T-01` and `P1` can share one). Class is `Verified` (`[observed]`: the source states it), `Recollection` (`[reported]`: the user supplied it), `Interpretation` (`[inferred]`, hedged wording), or `Missing` (`[TO VERIFY: what is needed]`). Do not force evidence into a category, and do not repeat a stakeholder quotation in more than one row.
   - **Category membership is computed from the table, not from memory.** A source is listed under a category only if its own row's Claim states that category. A participant's category is the strongest one any of their rows establishes; a participant with a strict row has their other rows marked `superseded (counted in strict)`, and those rows are never used as weaker examples.
3. **Fix the audience and role.** Separate the user's own work from team work. Use "I" only for what the user confirmed, and only as far as they said it: "sole designer" does not confirm that you authored a particular spec, state, or decision, so those stay `[TO VERIFY]`. Use "we" for team outcomes.
4. **Extract the arc:** context, problem, constraints, key decisions with the alternatives considered, process, outcome, lessons. Each point cites an artifact. State a decision's status (rejected, approved, shipped) only if an artifact records it; otherwise say the status is unknown.
5. **Write the outcome carefully.** Include a number only with its source, period, and meaning, and a baseline if it is a change. Never state a conversion lift, user count, revenue effect, or timeline you cannot cite. Say a result followed a decision. Say a decision caused a result only if an experiment or other evidence supports it.
6. **Protect confidential material.** Anonymize clients, users, and unreleased details by default, and flag items for the user's clearance. Do not embed screenshots with user data.
7. **Draft** only from rows in the evidence table, citing Evidence IDs, in plain language, leading with the problem and not the solution. The narrative introduces no claim that has no row. Keep apart what happened, what participants reported, what the team inferred, what the product changed, what was measured, and what is unknown. A shipped feature does not prove an outcome, and a design decision does not prove a problem was solved. Then list the visuals to embed, using only existing artifacts.
8. **Run an honesty pass.** Remove or flag every claim without a classification. Before saving, check each of these against the source files, not from memory:
   - **Evidence rules:** apply `../_shared/standard.md` §2 (claim-level evidence). `Verified` here means `[observed]`; `Recollection` means `[reported]`; `Interpretation` means `[inferred]`. Split each sentence into its clauses and source each one. A reason for doing the work, and a statement that a shipped change addressed a problem, are Verified only when an artifact records that reason or link; the commit, changelog, or spec showing that something was done does not show why. Otherwise write it as Interpretation or `[TO VERIFY]`.
   - **Themes, causes, and counts:** every ID listed under a theme, cause, or count is the source that states that category in its own words: a ticket (T-01), an interview (P1), or an artifact path, kept apart from the person. If a person's ticket states it and their interview does not, list the ticket and note `same person as P1` beside the line; never list the interview ID, and never carry a category from one source or person to another. Check every tally, including cause tallies such as late alerts or missed pickups, by reading each listed ID's words in its source file. An outcome (a missed pickup, a closed point) and its cause (a late alert) are separate claims: file an ID under a cause only if its words state the cause, and under an outcome only if they state the outcome. An ID whose words state neither, or only one half, goes on an `Unclear:` line with its own words and is not counted. Write the strict count line first, then the weaker line holding only people not already in the strict line.
   - **Consistency:** recompute every count and category list from the evidence table with the rules above, then compare them with the narrative, tables, lessons, and both appendices. Before saving, list every count, ID, category, and example in the narrative, the tables, the lessons, and both appendices, and confirm each says the same thing. A strict member, through any of their IDs (P1 and T-01 are one person), appears in no weaker line, example, or claim row, only in an exclusion note such as "P1, also T-01, is already counted"; an ID never changes category between sections; a number in prose matches its list.
   - **Attribution:** for every participant or ticket statement you quote or credit, search the cited source file for those words and confirm the ID is the file that contains them.
   - **Reasons:** a reason for a decision is Verified only if an artifact states that reason. A reading of the research is Interpretation, and an unrecorded reason is `[TO VERIFY]`.
   - **Questions:** the reply asks at most one question in total, as `../_shared/standard.md` §8 defines it: two requests joined by "and" or "also" are two. If the role was given, ask none.
   - **Audience:** state it in `## Context and role` as `Audience: <who>`, marked as assumed when the user did not give it.
   - **Word count:** state one only if you computed it with this command over the saved file, and copy the number exactly: `awk '/^## Summary/{f=1} /^## Visuals to include/{f=0} f' <file> | wc -w`. The body is the text from `## Summary` up to, not including, `## Visuals to include`, so it excludes the metadata block, both appendices, `## Open questions / to validate`, and `## Next step`. Write that definition beside the figure, in the file and in the reply alike.
   Write the output per §8.

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

Figma (optional, per `../_shared/figma.md`): when publishing is enabled, draw on the `Case Studies` page one frame per narrative section from Summary to Visuals to include, each claim keeping its class and any `[TO VERIFY]` marker, and the outcome as written, including "not yet available". Never draw the two author-only appendix sections, and never draw an outcome, metric, quote, client name, or contribution that is not in the Markdown. The Markdown file stays the source of truth.

`## Next step` names exactly one handoff, the first condition below that fits, and writes only that skill: `design-documentation` if technical detail is missing, or `product-metrics` if outcome measurement is missing.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] Chat replies follow `../_shared/personality.md`; no emoticons in written files or structured output
- [ ] Every decision cites an artifact; every claim is classified verified, recollection, interpretation, or missing
- [ ] No outcome number, lift, user count, quote, or timeline without a source
- [ ] No causal claim without supporting evidence
- [ ] The user's contribution and the team's are distinguished, as confirmed by the user
- [ ] Placeholders are labeled `[TO VERIFY]`, and confidential details are anonymized or flagged
- [ ] Length is within the target, labeled as a default; any stated word count was computed over the defined body
- [ ] The audience is stated; every credited statement was found in its cited source; no reason is marked Verified without an artifact that states it
- [ ] Any Figma output followed `../_shared/figma.md`, and the reply reports only Figma results a tool confirmed

## Boundaries
- Does not write specs → `design-documentation`
- Does not define or compute metrics → `product-metrics`
- Does not critique the design → `design-critique`
