# Behavioral findings

Companion to `RESULTS.md` (generated). Everything here comes from graded runs in `runs/`. Runs are single samples made by fresh Claude subagents instructed to use each skill, and graded by separate Claude subagents against explicit criteria. Treat results as evidence of failure modes, not as pass rates. Structural checks (`tests/validate_skills.py`) prove structure only and are kept separate from these results.

## Current result
Latest attempt of each of the 76 scenarios (see `RESULTS.md`, generated): 75 PASS, 1 FAIL (DS-X1), 0 BLOCKED, 0 NOT EXECUTED.

Latest-attempt scoring flatters the suite. Under the 3-of-3 rule used since 2026-11-02, these scenarios are not fixed:

| Scenario | Last three attempts | Open failure |
|---|---|---|
| PF-N1 | 1 of 3 | a ticket filed under a theme its words do not state; tags in the statement disagree with the ledger |
| CS-E1 | 1 of 3 | quotes merged across two lines or reworded from the user's request |
| CS-N1 | 2 of 3 | a strict-count member's interview reused as extra evidence |
| DS-X1 | 2 of 3 | a hex count from a 6-digit-only pattern (maintainer override, see below) |
| UF-N1 | 1 of 3 (2026-11-02) | not rerun since its skill fix |

Holding at 3 of 3: DC-E1, RP-M1, UF-E1, UF-X1.

The sections below keep the history in the order it happened; earlier counts in them were true at that point and are superseded by this summary. Run artifacts under `runs/` are kept locally and are not part of the public repository.

## Standard versions
Every attempt has a `META.json` with the SHA-256 prefix of the shared standard it ran against. Skill hashes are recorded only for attempts collected after that field was added (`unknown` for backfilled ones). Earlier attempts and their verdicts are kept in `runs/`; the final status of a scenario is its latest attempt.

| Version | SHA-256 prefix | What changed |
|---|---|---|
| v1 | `6f77df46b5` | Original standard (no scenarios remain on it as their latest attempt) |
| v2 | `8f4607ccef` | Computed counts; headings are a contract; one skill in Next step |
| v3 | `6426474b14` | One-skill rule for chat stop replies; omission wording; separate count for weaker statements |
| v4 | `87b1ad1860` | Stop replies name a skill only if one can create the input; "Not done here" line; labelled counts with listed members; privacy rule covers bias and sensitivity sections; accessibility needs optional and in consent |
| v5 | `49700991f7` | Participants by code or "they"; no first names, ages, or age words; tallies list their members; verbatim quotes only; age of evidence computed |

Graders sometimes reported a different hash (`d58d8ff18654`, `2e9c1c3ace`): that is SHA-1 (`shasum` without `-a 256`) or a transcription error, not a change to the file.

## What was executed
- 76 scenarios, 4 per skill, on a synthetic project (`fixtures/`). Total attempts on disk: see `RESULTS.md` (each has `META.json` and `EVAL.md`; no duplicate fingerprints).
- Batch F reruns: 38 runs on v3, covering every scenario whose latest attempt was on v1 (this is a different set from the 38 scenarios still on v2, listed under risks); product-metrics PM-N1/M1/X1 were rerun on the patched skill (3); then the failures were rerun after each fix: 13 on v4, 5 on v5, one more rerun of IG-X1, and two more of PF-N1.
- One verdict was superseded: DD-N1 attempt 4 was first graded against a stale scenario plan (`scenarios/*.md` was not regenerated after `scenarios.json` changed). The stale verdict is kept as `EVAL.superseded-stale-C5.md` and the attempt was regraded.

## Defects found and fixed (with the rerun that confirms each)
| Defect | Failing attempt | Fix | Confirming rerun |
|---|---|---|---|
| Stop reply chained two skills or said "rerun" (DQ-M1, DS-M1, UA-M1, UT-M1, PM-M1) | DQ-M1 a2, DS-M1 a2, PM-M1 a3 | Standard: one skill or none in a stop reply; none when only the user can supply the input | DQ-M1 a3, DS-M1 a3, UA-M1 a3, UT-M1 a3, PM-M1 a4 pass |
| Second declined job not routed (DC-X1) | DC-X1 a2 | "Not done here: <job>, which belongs to `<skill>`" line outside Next step | DC-X1 a3 pass |
| Omission note named a category, in the reply or in a bias section (JM-N1, IG-E1) | JM-N1 a3, IG-E1 a3 | Generic sentence only; rule covers every section | JM-N1 a6, IG-E1 a4 pass |
| User-typed names repeated when declining (IG-E1) | IG-E1 a2 | Standard: do not repeat them; "the names you listed" | IG-E1 a4 pass |
| "Found with difficulty" counted as "could not find"; unlabelled counts; people double-counted across interviews and tickets (CS-E1, PB-N1, PF-N1, JM-N1, PB-X1) | CS-E1 a3, PB-N1 a2, PF-N1 a2, JM-N1 a4 | Standard: label every count, list members, count each person once; skill steps for persona-builder | CS-E1 a4, PB-N1 a4, JM-N1 a6, PB-X1 a4 pass; PF-N1 counts correct from a3 on |
| Compound or option-listing interview questions; "rewrite" identical to the draft (IG-X1) | IG-X1 a3, a4, a5 | Skill step 8: check every question, compare rewrite to draft, no shipped "or" | IG-X1 a6 pass |
| Unsupported channel ("push"), wrong help-entry count, misattributed detail (JM-N1) | JM-N1 a4, a5 | Standard: names as sources name them; attribute a detail only to the source containing it | JM-N1 a6 pass |
| Pronoun for a participant inferred from a name; first name used to explain a ticket match; age restated (PB-N1, PF-N1) | PB-N1 a3, PF-N1 a3 | Standard privacy rule; harness screens A9 (first names) and A14 (gendered pronouns) | PB-N1 a4 pass; PF-N1 no first names from a4 |
| Accessibility information not marked optional or covered in consent (UT-X1) | UT-X1 a2 | Skill and standard | UT-X1 a3, a4 pass |
| Missing decision stopped product-metrics although the goal was given | PM-N1 a2 | Inputs table: missing goal stops, missing decision asks one and tags an assumption | PM-N1 a3 pass |
| Paraphrase put in quotation marks as the stakeholder's words (PF-N1) | PF-N1 a3 to a6 | Standard + skill rules; harness screen A16 for short quotes not in the sources | see "Open failures" |

## Scenario and harness corrections (not skill defects) and why
- DD-N1 C5: it required code-read issues to be tagged `inferred`. The standard defines reading project files as `observed`; what matters is that nothing is presented as approved. Criterion now accepts observed (code) or inferred with the file cited.
- PM-M1 C3: it required a question about the decision even when the missing input is the goal. Now: ask for the goal; a decision question is optional.
- DC-X1 C2: the routing of the second job may sit outside Next step.
- PB-N1 C6: the theme label "code findability" was ambiguous; the criterion now accepts 5 for "trouble with the code" (weaker statements listed) or a stricter label with correct members.
- Earlier this batch: PM-E1 accepts a stop or an answer; DS-N1, IG-E1, JM-E1, FP-E1 reworded; four regexes moved to review-only.
- Harness: duplicate-collection guard (fingerprint), `META.json` on every attempt, scenario plans regenerated with `harness.py docs`, new screens A14 (pronouns), A15 (compound "or" in questions), A16 (short quotes absent from sources), A9 now flags bare first names.
- JM-N1 attempt 1 is BLOCKED (the agent never saved its reply file) and is kept as history.

## Targeted regression on v5 (after Batch H)
- Scope: the 19 Tier 1 scenarios from `tests/behavioral/reports/BATCH-H-REPORT.md` §6, all previously PASS on v2: CA-M1, IA-M1, IG-M1, JM-M1, MP-M1, MP-X1, PD-M1, RP-M1, JM-X1, PD-X1, DQ-E1, PD-N1, JM-E1, IG-N1, CS-N1, CS-X1, IA-N1, RP-E1, PM-E1. Each ran as a new attempt on standard `49700991f7`; `META.json` records that hash and the skill hash.
- First round: 14 PASS, 5 FAIL (IA-N1, CS-N1, RP-M1, JM-X1, JM-M1).
- Defect, skill: four failures miscounted people when tickets and interviews were combined (author of a ticket who was also interviewed counted twice, or a weaker statement counted as explicit). `persona-builder` had an explicit dedup step; `information-architect`, `case-study-writer`, `ux-research-planner`, and `journey-map-builder` did not. Fix: one sentence in step 1 of each ("match ticket authors to interviewees by identity ... count each person once and list the members beside every count"). Reruns: IA-N1 a4 PASS, CS-N1 a4 PASS, JM-X1 a4 PASS, RP-M1 a4 FAIL (counts now correct; failed on a new G2 issue: a release-timing claim tagged `[observed]` with no dated source, and an evidence age of 642 days where the dates give 643).
- JM-M1 a3 FAIL, not fixed: the fixture removes research, tickets, and analytics but leaves product code and design files, and the skill's Inputs table counts "observed product" as evidence, so the run drew a product-only map instead of stopping. Attempt 2 stopped on the same fixture. Cause: scenario/skill inconsistency, not a clear skill defect; recorded as FAIL. Resolution needs a decision: either the fixture also removes product files, or the skill states that product-only evidence still requires a stop (or an all-`[assumption]` hypothesis map).
- Ground-truth correction: `GROUND_TRUTH.md` said the strict "could not find" set is P3 only. Ticket bodies T-01 (P1) and T-12 are explicit, so across interviews and tickets the set is 3 people. A clarification was added; the original line is kept, and earlier verdicts stand as recorded.
- Harness: `collect --attempt N` used to delete an existing attempt N; it now refuses (test `test_collect_never_overwrites_a_stored_attempt`).
- Net effect at that point (superseded; see Current result): 75 PASS / 1 FAIL became 73 PASS / 3 FAIL. The two new FAILs (JM-M1, RP-M1) are scenarios that passed on v2 and fail on v5; no PASS was lost to a skill regression introduced by a fix.

## JM-M1 fixture correction (release closeout)
- Old fixture: `fixtures/JM-M1/.remove` listed `research`, `support`, `analytics`. That left `README.md`, `docs/`, `src/`, `design/`, and `build/` in place.
- Why it was incorrect: the scenario is titled "No evidence to map from" and its criteria assume no evidence, but `journey-map-builder` explicitly accepts observed product as evidence. The narrow removal matched PB-M1 and PF-M1, where product files are not evidence, instead of the suite's "nothing to work from" convention (UA-M1, DS-M1, IA-M1, IG-M1, UF-M1, UT-M1, DC-M1, DD-M1, CS-M1, PD-M1 remove all seven directories).
- New fixture: removes `docs`, `research`, `support`, `analytics`, `src`, `design`, `build`. No skill, standard, scenario criterion, or ground truth changed.
- Attempts 1 to 3 ran on the old fixture and are unchanged, including attempt 3's FAIL. `META.json` does not record a fixture version, so this note is the record. Later attempts use the corrected fixture.
- Closeout run on the corrected fixture: JM-M1 attempt 4 PASS (stopped, no deliverable, "Next step: supply the recipient research…"). Attempt 3's FAIL is kept.
- Closeout regression for the step-1 counting sentence added to `information-architect`, `case-study-writer`, `ux-research-planner`, and `journey-map-builder`: the materially affected scenarios are those whose latest attempt predated the edit, whose fixture has both tickets and interviews, and whose critical criteria grade person counts. That is CS-E1, JM-N1, JM-E1 (IA-N1, CS-N1, RP-M1, JM-X1 had already run after the edit; the other scenarios of these skills are stops or have no count criterion). Results: JM-N1 attempt 7 PASS, JM-E1 attempt 4 PASS, CS-E1 attempt 5 FAIL. CS-E1 a5 put T-04 ("Looking for the code on my phone") and T-09 ("hard to see") into a count labelled "could not find or see" (4 people where the explicit set is 3). The same failure class occurred in CS-E1 a2 and a3 before the sentence existed and a4 passed, so this is recorded as run-to-run variance in a known class, not a regression caused by the edit. No retry.

## Open failures after the last rerun
- **PF-N1 (problem-framing, evidence criterion G2): unresolved.** Four consecutive attempts (a3 to a6) put a coined framing label in quotation marks and attribute it to the stakeholder, whose only words are "People keep asking where their stuff is." The standard rule (quotation marks only around words a source contains) and a skill rule written for this case (a5 to a6) did not stop it; a6 also merged explicit "cannot find" statements with weaker ones in one quoted composite. Counts, date arithmetic and privacy are correct in a4 to a6. Cause: model behavior on a framing label the skill asks it to name; the rules are present and the executor does not follow them reliably. Not fixable by more wording in this pass; a structural change (for example, a fixed template line for "Rejected framing" that carries no quotation marks) is the next candidate. A16 screens short quotes but cannot tell a coined label from a source word.
- **RP-M1 (ux-research-planner, G2): unresolved.** Counts correct after the fix; a4 failed on an unsourced release-timing claim and a wrong evidence age (642 vs 643 days).
- **CS-E1 (case-study-writer, C5 and G2): FAIL on the latest attempt (a5).** A weaker ticket statement counted under "could not find or see". Earlier attempts alternate PASS and FAIL on this criterion.

## Targeted fix round for PF-N1, RP-M1, CS-E1 (2026-11-02, standard `c99bdcc284`)
- Reproduction on the unchanged skills (one attempt each): PF-N1 a7 FAIL, RP-M1 a5 PASS, CS-E1 a6 PASS. PF-N1 a7 was graded PASS and overridden to FAIL on review: it wrote "whether older ... users are disproportionately affected" beside P3, whose note records an age (G4). RP-M1 a5 asked its one question and wrote no plan, so the a4 path (ages, release timing) was not exercised. CS-E1 a6 counted correctly. Single samples: a PASS does not show the defect is gone.
- Root causes from a4 to a7 and earlier: (1) the age rule did not say it covers segment hypotheses and `[assumption]` lines; (2) the "could not find" rule said "explicit" without saying what counts as explicit, so "looking for" and "hard to see" tickets were counted; (3) the age rule did not say which end of a date range to use, and nothing barred placing evidence before or after an undated release.
- Fix, standard only (three sentences in §8 and the privacy list): ages for both ends of a range copied from command output; release order stated as unknown without a dated source; a "could not find" count holds only statements that themselves say so, with "looking for", "hard to see", and "where is" named as weaker; no age descriptor ("older", "retired") even as a hypothesis or assumption.
- Harness screens added (deterministic detection, not prevention): A17 age words (REVIEW), A18 evidence age in days vs its date and the run date (FAIL on mismatch; adjacent pairs and range tables only), A19 tickets in a "could not find/see" count whose own text does not say so (REVIEW). Unit tests in `tests/test_behavioral_suite.py` failed before the code existed and pass now. Re-screening stored attempts: A19 flags PF-N1 a6 and CS-E1 a5, A18 flags RP-M1 a4 (642 vs 643), A17 flags PF-N1 a7; no stored PASS attempt is flagged. A18 first paired ages with the wrong date when the age came first; that produced a false FAIL in PF-N1 a8's AUTO.md (written at collection, before the fix). The corrected screen passes a8; a8's AUTO.md is kept as collected.
- Post-fix attempts: PF-N1 a8 PASS, a9 FAIL (a merged paraphrase of three ticket subjects in quotation marks, the original class); RP-M1 a6 FAIL (T-05 "Arrived and the point was closed" listed under late notifications); CS-E1 a7 FAIL (weaker group labelled "3 more people" while one of the three, P1, is already in the strict count). In every post-fix attempt the targeted defects did not recur: ages correct, release order stated as unknown, T-04 and T-09 never in a "could not find" count, no age words.
- Status: all three remain FAIL. The targeted classes are fixed in the observed attempts; each scenario failed on a different evidence-integrity slip (quotation marks, ticket-to-theme attribution, a count label). Earlier rounds show that adding wording for each new slip does not hold, so no further wording was added. These are model-reliability limits on single samples, not a proven fix.

## Structural fix round, steps 1 to 3 (2026-11-02, not yet rerun)
Wording alone did not hold across three rounds, so this round changes the output form and makes the checks deterministic.
- Step 1, quotes. Standard: copy each passage before quoting it, write a source quote as `"exact words" (ID)`, never join, shorten, or reword quoted words, and never put an own label or summary in quotation marks. Harness: A20 (FAIL) checks every quote attributed to a ticket or participant (`"words" (T-01)`, `P3 "words"`) word for word against that item; A21 (REVIEW) flags unattributed quotes that nearly match source wording. A check over every quotation mark was tried first and dropped: skills legitimately quote their own questions, tasks, and labels, so it flagged at least 30 of the 76 latest attempts.
- Step 2, counts. Standard: one line per person count in the form `<label>: N people — ID, ID`, only IDs after the dash; a weaker line lists only people not in the strict count. Harness: A22 (FAIL), on lines in that form, checks N against the distinct people listed (ticket authors matched to interviewees through the fixtures), that each strict member has a source of their own that says it could not be found, and that a weaker or "more" line repeats nobody from the strict line. Making A19 a FAIL was tried and reverted: it matches any line mentioning "could not find" and flagged 22 attempts that had passed.
- Step 3, themes. Standard: when items are grouped into themes, each item's ID and its own words sit beside the theme, and an item is filed only under a theme its words state. A20 then verifies those words; whether the theme fits stays with the grader.
- Re-screen of all 225 stored attempts with the new checks (stored AUTO and EVAL files unchanged): A20 fails 8 attempts, all real misquotes (for example JM-N1 a5 gives P4's "felt silly" to P1; PF-N1 a1 attributes T-12's subject to P4). One of them is a latest PASS, IA-N1 a4, whose grader had noted the paraphrase as non-critical; a rerun would now fail it. A22 fires on no stored attempt, since none uses the new count form.
- Also seen on re-screen, not caused by this round: UF-E1, UF-N1, UF-X1 fail A4 because the user-flow-designer contract changed after they ran, and PM-E1 a4 fails A8 as before.
- Status before rerun: PF-N1, RP-M1, CS-E1 FAIL.

## Rerun of the structural fix (2026-11-02, standard `f729c98cb1`, 3 attempts each)
18 new attempts, graded by separate grader agents against the scenario criteria, GROUND_TRUTH.md, and the standard. `RESULTS.md` still scores the latest attempt only, so it reads 74 PASS / 2 FAIL; under the 3-of-3 rule used for this round, 3 of the 6 scenarios hold.

| Scenario | Attempts | Result | Failures |
|---|---|---|---|
| RP-M1 | 7, 8, 9 | 3 of 3 PASS | none; every attempt stopped with one question, so the plan-writing path that failed before (ages, theme filing) was not exercised |
| UF-E1 | 3, 4, 5 | 3 of 3 PASS | none (new user-flow contract) |
| UF-X1 | 3, 4, 5 | 3 of 3 PASS | none (new user-flow contract) |
| PF-N1 | 10, 11, 12 | 2 of 3 | a11 G2: the stakeholder's sentence reworded inside quotation marks ("where is my stuff"), the original class |
| CS-E1 | 8, 9, 10 | 2 of 3 | a10 C5, G2: weaker line "3 people — T-04, P1, P4" repeats P1, already in the strict count through T-01 |
| UF-N1 | 3, 4, 5 | 1 of 3 | a4 C2: a decision with no rejected branch and a pending state with no failure exit; a5 G2: one quote credited to T-01 and T-12, only T-12 has those words |

- The count form worked as intended in CS-E1 a10: the slip sat on one line in the new form, where a check can see it. A22 missed it at collection because the line ended with an `[observed]` tag; the pattern now allows trailing tags and fails a10 on re-screen (regression test added).
- A20 accepted a quote credited to several sources if any one contained it, and read only the last ID before a quote. It now reads the whole ID list; IDs written before a quote must each contain the words, a list after a quote (often a theme's members) needs at least one. Re-screen fails UF-N1 a5, matching its grader (regression test added).
- PF-N1 a11 was flagged by A16 and A21 (REVIEW). Unattributed quotes stay review-only, because skills quote their own labels and copy.
- Grader template corrected: non-critical findings are `[N]`, not `[F]`, as the suite's integrity test expects (CS-E1 a8 G7 relabelled).
- Next fixes, by cause: PF-N1, a fixed form for the stakeholder's words (verbatim line plus `(our reading)` for any rewording); CS-E1, a case-study-writer step that writes the weaker line only after removing everyone in the strict line; UF-N1, an integrity-check rule that a known dead end is a failure to fix, not a note. RP-M1 needs a fixture or prompt that reaches the plan to test the earlier slip.
- Applied (skills only, not yet rerun): problem-framing step 3 writes the stakeholder's sentence once as `Stakeholder said: "<exact sentence>" (<file>)` and any rewording as `Our reading: <words>` without quotation marks; case-study-writer step 1 builds the weaker line by removing everyone in the strict line before writing its number; user-flow-designer step 9 treats a dead end or a decision or pending state with no failure exit as a defect to fix before saving. The validator checks each rule (`EVIDENCE_FORM_RULES`, `FLOW_SKILL_RULES`) with mutation tests. RP-M1's scenario is unchanged: changing it to reach the plan is a scenario decision left to the maintainer.

## Round after audit fixes #1 to #12 (2026-11-03, 14 new attempts, skills at the working tree after these edits)
Skills had changed since the last graded runs (one-skill Next step, ask-one fallbacks, design-qa approval wording, information-architect step 7, plus edits to ux-research-planner, usability-test-planner, feature-prioritization, user-flow-designer, problem-framing, case-study-writer). Ran fresh executors and separate graders on the three open scenarios (3 attempts each) and on the scenarios touching the other changes (1 attempt each). Single samples; executor and grader are both Claude.

| Scenario | New attempts | Result | Notes |
|---|---|---|---|
| UF-N1 | 6, 7, 8 | PASS, PASS, PASS (3 of 3) | Grader scripts: diagram edges and inventory rows match one to one by ID in all three (22, 26, 24); status counts match; individual flows cover every transition. Noncritical: "Get a new code" marked Verified though its destination is in no source (no skill rule covers a verified trigger with an unverified destination); in attempts 7 and 8 Unknown recovery edges are drawn like decided arrows. |
| PF-N1 | 13, 14, 15 | PASS, FAIL, FAIL | Counts match GROUND_TRUTH in all three. Failures are quote discipline (G2): stakeholder sentence quoted twice (14, 15), quotation marks inside `Our reading:` (14), coined phrases in quotation marks (15). The old screens showed no flag on attempt 14. |
| CS-E1 | 11, 12, 13 | FAIL, FAIL, FAIL (0 of 3) | C1 to C4 pass everywhere (30% and halving excluded, not asserted, no causal claim). 11: audience never stated and the body word count claimed in the metadata is wrong; 12: no strict could-not-find line, a statement credited to P3 that is in P4; 13: T-05 filed under a late-alert theme its words do not state, and a reason tagged observed that no artifact records. |
| IA-N1 | 5 | PASS | Step 7 change complies (lists what needs validation, designs no study). One minor own-wording quote. |
| IA-M1, JM-M1 | 4, 5 | PASS, PASS | Stop with no skill named; closing order correct. JM-M1 minor: reply asks for several items without defaults. |
| DQ-N1 | 3 | PASS | All four required mismatches logged; values marked approved with approver unknown. |
| DQ-M1 | 4 | PASS | Stopped because "the design spec" names no file. The grader found the new approval wording ambiguous here; `design-qa` now says a phrase that identifies no file is not naming one. That clarification has not been rerun. |

Harness changes: A23 (a stakeholder's exact sentence is quoted once) and A24 (no quotation marks in `Our reading:` lines), with a regression test; replayed on PF-N1 attempts 13 to 15 they agree with the graders (13 PASS; 14 FAIL both; 15 FAIL A23). Also regenerated MATRIX.md, which had been stale for RP-M1.

Status after this round: latest-attempt headline is 74 PASS, 2 FAIL (CS-E1, PF-N1). Under 3 of 3: UF-N1 now holds; PF-N1 and CS-E1 do not. Not rerun: the other 62 scenarios, and nothing after the A23/A24 and design-qa edits.

## Repair round for PF-N1, CS-E1, DQ-M1 (2026-11-03, 13 new attempts)
Edits before this round: `problem-framing` step 3 (quotation marks only on the one `Stakeholder said:` line and around verbatim cited source quotes) and its checklist; `case-study-writer` step 8 (attribution, themes and counts, reasons, `Audience:` line, defined body word count) and its checklist; harness screens A23 and A24 (PF) and A25 and A26 (CS), each with a regression test. Fresh executors, separate graders, single samples.

| Scenario | New attempts | Result | Remaining failures |
|---|---|---|---|
| PF-N1 | 16, 17, 18 | FAIL, FAIL, PASS (1 of 3) | No quotation-mark violation in any attempt and A23/A24 pass on all three. 16: "without it they cannot collect" tagged observed with no source. 17: "the roadmap says v1.4 is live" (the fact is in README.md); its reply also lacks the closing emoticon. |
| CS-E1 | 14, 15, 16 | FAIL, FAIL, PASS (1 of 3) | 14 and 15 file T-05 under late alerts though its words state no alert; 14 also states a body count of 974 where the defined body is 970. Audience, attribution and the unverified 30% and halving held in all three. Attempt 16 passes with non-critical count-line form defects. |
| DQ-M1 | 5 | PASS | Generic phrase not treated as a file; mockup not used; nothing written. Per-decision approval recording was not reached (untested). |
| Regression: PF-M1, PF-X1, CS-M1, CS-X1 | 3, 4, 3, 5 | PASS | Minor non-critical notes in the EVAL files. |
| Regression: PF-E1 | 4 | PASS | Breaks the new quote rule outside the critical criteria: a quoted `"because"` and a quoted stakeholder sentence in the chat reply. A23 and A24 read only the deliverable. |
| Regression: CS-N1 | 5 | FAIL | Previously PASS. T-05 and T-02 tallied under a missed-pickup cause that their words do not state, tagged observed. Same slip as CS-E1 14 and 15. |

Acceptance (3 of 3 for PF-N1 and CS-E1) was not met. The targeted quote failures are fixed; the dominant remaining failure is a claim tagged observed or verified that the cited source does not state (T-05 filed under late alerts is the recurring case). The "themes and counts" check names the code-count lines only. Not caught by any automated check: T-05 theme filing, unsourced causal clauses, chat-reply quotation marks.

## Provenance and theme-mapping round (2026-11-03, 9 new attempts)
Edits before this round: `problem-framing` step 4 provenance rule (cite only the file that states the fact; `[observed]` only when that file states it; unstated causes are `[inferred]` or `[assumption]`) and checklist line; `case-study-writer` step 8 (every ID in a theme, cause or count must state the category itself, outcome and cause kept separate, `Unclear:` line for insufficient evidence, word count only via the exact `awk | wc -w` command). Harness: A25 now exact and also reads the chat reply; new A27 (closing signature), A28 (false "shared file absent" claim), A29 (causal wording tagged observed, REVIEW), A30 (version or percentage credited to the wrong file), A31 (IDs listed beside an alert claim must state an alert); each has a regression test. Replayed on the stored runs they agree with the earlier graders (A31 flags CS-E1 13 to 15 and CS-N1 5; A25 flags CS-E1 11 and 14; A30 flags PF-N1 17; A27 and A28 flag PF-N1 17). Single samples; executors and graders are Claude.

| Scenario | New attempts | Result | Remaining failures |
|---|---|---|---|
| PF-N1 | 19, 20, 21 | PASS, PASS, FAIL (2 of 3) | 21: a consequence ("which causes contact with support and workarounds") stated without a tag and an `[observed]` tag on "need the pickup code at the point of collection" that none of the cited files states; its reply also has no closing emoticon because the executor did not read personality.md. |
| CS-E1 | 17, 18, 19 | PASS, PASS, FAIL (2 of 3) | 19: four questions in the reply where the policy is one (G3); no closing emoticon (executor did not read personality.md). T-05 was handled correctly in all three; word counts 946, 1075 and 813 matched an independent recount. |
| CS-N1 | 6, 7 | FAIL, PASS (1 of 2) | 6: P1 listed as a "could not find" member; P1's interview says the code was found after scrolling and the strict statement is in P1's ticket T-01. |
| PF-E1 | 5 | PASS | Minor: a `Not done here` line names a second skill; "not gitignored" stated as fact. |
| DQ-M1 | not rerun | not rerun | No edit to design-qa since attempt 5 (PASS). |

Findings: the T-05 theme-misfiling and wrong-source failures did not recur in any of the nine attempts. Three of the four remaining FAILs are a different slip in each (an untagged consequence, four questions, a person listed under the wrong ID). Two attempts (CS-E1 19, PF-N1 21) ended without the closing emoticon because the executor read only standard.md; the run prompt says to read the installed standard and not other repository files, and the skill only cites personality.md. This is a harness prompt ambiguity, recorded here and not corrected mid-round. The closing signature is checked by A27 and recorded by graders outside the fixed criteria. Acceptance (PF-N1 3 of 3, CS-E1 3 of 3, CS-N1 2 of 2) was not met.

## Round 4: shared-instruction loading and claim-level provenance (2026-11-03, 11 new attempts)

Changes: `standard.md` gains section 1 (read `personality.md` always, `figma.md` only when `design/figma.json` exists or Figma is asked for); the executor prompt now follows that section instead of limiting reads to `standard.md`; `standard.md` section 8 says the reply asks at most one question; `problem-framing` step 4 requires a class tag on the `which causes` clause and a per-clause claim ledger; `case-study-writer` step 8 lists the source ID that states the category (T-01, not P1). Screens A32 to A35 added.

| Scenario | Attempts | Result |
|---|---|---|
| PF-N1 | 22 PASS, 23 FAIL, 24 FAIL | 1 of 3 |
| CS-E1 | 20 FAIL, 21 FAIL, 22 PASS | 1 of 3 |
| CS-N1 | 8 PASS, 9 PASS, 10 FAIL | 2 of 3 |
| PF-E1 | 6 PASS | PASS |
| DQ-M1 | 6 PASS | PASS |

Shared loading: all 11 executors recorded reading `personality.md`; all 11 replies ended with one library emoticon (A27 PASS), and no reply had more than one question (A33 PASS). The missing-emoticon failure did not recur.

Remaining failures (grader findings, not retried):
- PF-N1 23: a `which causes` consequence tagged `[observed]` where no file states it; the file also names categories of omitted personal data instead of the generic sentence.
- PF-N1 24: P1 listed in the strict count (the quote that says it is T-01); missed pickup tied to code findability from P1's words, which do not state it.
- CS-E1 20, 21: a reason for the work ("responded to people having trouble finding the code") tagged observed while the same file says no artifact records the reason.
- CS-N1 10: P1 (a strict member via T-01) listed as a weaker-trouble example in the body.

Screens: A32 caught PF-N1 24 and replays flag P1 listings in earlier runs. A34 passes when any class tag is present, so it did not catch PF-N1 23's `[observed]` consequence (A29 flagged it for review only). Nothing automated catches a reason tagged observed (CS-E1 20, 21) or the P1 weaker-line placement in CS-N1 10. A20 gave two false positives (PF-N1 22, CS-E1 22). A35 is review-only and noisy.

## Rounds 5 and 6: claim-level evidence, Case Study Writer, four Figma skills (2026-11-03)

Changes. `standard.md`: section 1 (shared files to load), section 2 claim-level evidence (items 1 to 9: split clauses, ledger row, four classes, a source supports only what it states, four kinds of ID kept apart, no forced content, whole-source counts, one account per fact, the source's own words), section 8 (at most one question; two requests joined by "and" are two). `case-study-writer`: evidence table built before drafting, category membership computed from it, narrative only from table rows. `problem-framing`: claim ledger, no forced consequence. `information-architect`, `design-system-audit`, `design-critique`, `product-discovery`: required content and finding fields added under the existing headings, Figma board sections listed, one-question quality line. `figma.md`: verified one-way arrow recipe. Harness: A23 to A39, `quality` subcommand and `QUALITY.md`, `figma.json` update allowed on collect.

Case Study Writer (one targeted repair cycle, then stop): CS-E1 29, 30, 31 all FAIL (G2: Summary cites Evidence IDs that point at weaker-statement rows, or counts with no rows); CS-N1 17 PASS, 18 FAIL (a reason tagged observed), 19 FAIL (P1 and T-09 in the strict list). Earlier in the same effort the pre-table version scored CS-E1 1/3 and 2/3, CS-N1 2/3 and 0/3. The evidence table did not improve reliability. It moved the failures from wrong lists to wrong citations. No further rewriting was done, per the plan.

Problem Framing: with the claim ledger, PF-N1 28, 29, 30 FAIL (0/3), worse than the 1/3 before the ledger. The ledger gives the executor more clauses to tag and the tags are where it errs (strict persons reused in weaker rows, lumped rows, stakeholder sentence repeated, context tagged observed). Not retried; the ledger rule should be simplified before another run.

Other four skills, first pass: IA-M1 PASS, IA-X1 FAIL (no user groups), DS-X1 FAIL (one question with "and"), DS-E1 PASS, DC-E1 FAIL (count of 2 from a partly read tickets file), DC-X1 PASS, PD-M1 PASS, PD-X1 FAIL (P1 listed as the strict source). Complete-input runs (Figma-enabled sandboxes): IA-N1 6, DS-N1 3, DC-N1 3, PD-N1 4 all PASS. After one targeted repair each: IA-X1 4 PASS, PD-X1 5 PASS, DS-X1 4 FAIL (a different defect: 8 occurrences stated, 7 by recount), DC-E1 4 FAIL (a question joined by "and was", which A33 then missed; the pattern is now covered). Not repeated further.

Not tested: a polished-screen Design Critique scenario (no fixture exists, none invented); the ambiguous-opportunity Product Discovery case is covered by PD-X1 only; DS incomplete-documentation is covered by DS-X1 only.

Figma (file CzIBqJ7D8zakgFsfgfo0yP, BracIT scratch file): smoke test passed (page, editable frame, text, rectangles, ellipse, arrow vector, idempotent re-run, a hand-edited frame kept and a v2 drawn beside it, a manual sibling frame untouched, an invalid file key reported as no edit access). Defect found and fixed in the docs: `createLine` with `ARROW_LINES` draws both ends. User Flow Designer, Information Architect, Design System Audit, Design Critique and Product Discovery were each drawn; IA, DS, DC and PD a second time, where the adapter drew v2 beside the existing owned frame and left v1 unchanged. All 12 artifact frames and the manual nodes read back with their drawn fingerprints, no image fills. Limits: one reviewer (a model) judged usefulness; the Overview page holds 8 index frames because each isolated sandbox had its own manifest; the Design Critique board uses a schematic drawn from the mockup description because the source is text and images cannot be added.

## Self-check round (2026-11-06, 15 attempts)
- Change: `_shared/check_evidence.py`, a script the skills run before saving (standard §1 and §7). It checks quotes credited to a ticket, interview, or file; `N people — IDs` count lines against distinct people and each strict member's own words; and the one-question rule on the draft reply. Unit tests in `tests/test_check_evidence.py` use the stored failing attempts. design-system-audit now pastes the command and output beside every count.
- Reruns, 3 each, graded by separate agents: DC-E1 3 of 3 (fixed), DS-X1 2 of 3, CS-N1 2 of 3, PF-N1 1 of 3, CS-E1 1 of 3.
- Every run reported the checker at 0 problems, and the failures that remain are outside what it can see: quotes credited to the user's request or merged from two lines of a file, a theme filing, tags that disagree between sections, and a regex that missed 3-digit colors. Some executors also fed it a placeholder reply; the standard now requires the full draft.
- Run date: the collection script passed 2026-11-02 for runs executed on 2026-11-06, so A8 and A18 failed falsely. META.json was corrected and the checks re-run for all 15 attempts (noted in each META.json); graders had already marked those A8 failures as false positives.
- Maintainer override: DS-X1 attempt 7 reported 7 hex occurrences (6 distinct); the fixtures hold 8 (7 distinct) with `#fff`. Its grader called this non-critical; it is a wrong derived count, so G2 fails (original grading kept as EVAL.grader-original.md). The same recount shows DS-X1 attempt 4, graded FAIL for reporting 8 (7), was a grading error; a note is appended there and its status is left as recorded.
- Checker gap seen once: a quote on a line that names two IDs can be credited to the nearer one. The executor reworded the line; the checker is unchanged.

## Not done / risks
- After the targeted regression, 19 scenarios still have their latest attempt on v2 (Tier 2 and Tier 3 in `tests/behavioral/reports/BATCH-H-REPORT.md` §6). The four skills edited in this pass have other scenarios whose latest attempt predates the edit.
- 38 scenarios have a passing latest attempt on standard v2 (`8f4607ccef`) and were not rerun on v5. v2 to v5 changes are additions and clarifications, but passing under v2 is not evidence under v5. `tests/behavioral/reports/BATCH-H-REPORT.md` proposes a targeted regression set for them.
- Several scenarios pass on one effective sample; the failures above show the same skill can pass and fail on the same scenario (see attempt histories). A pass is not a rate.
- The `problem-framing` and `product-metrics` stop rows can still be read two ways when another skill could create the missing input (for example `problem-framing` for a missing goal); graders accepted both.
- Automated screens are heuristics (A9 to A16). Semantic privacy, count correctness, and "single-idea question" were judged by graders. The IG-X1 a6 run read only the first lines of one interview, so source-content privacy was barely exercised there.
- A hand-written tally is still the most frequent failure class; the screens do not recompute counts.

## Limitations
- Executor and grader are both Claude models. Each scenario has 1 to 6 effective samples.
- Executors were subagents told to load the skill, not a human typing a slash command.
- Mermaid syntax was checked only for bracket balance.
