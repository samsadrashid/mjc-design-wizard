# Behavioral findings

Companion to `RESULTS.md` (generated). Everything here comes from graded runs in `runs/`. Runs are single samples made by fresh Claude subagents instructed to use each skill, and graded by separate Claude subagents against explicit criteria. Treat results as evidence of failure modes, not as pass rates. Structural checks (`tests/validate_skills.py`) prove structure only and are kept separate from these results.

## Current result
Latest attempt of each of the 76 scenarios (see `RESULTS.md`, generated):
- 73 PASS
- 3 FAIL: PF-N1, RP-M1, CS-E1 (details under "Open failures after the last rerun")
- 0 BLOCKED
- 0 NOT EXECUTED

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
- Scope: the 19 Tier 1 scenarios from `docs/BATCH-H-REPORT.md` §6, all previously PASS on v2: CA-M1, IA-M1, IG-M1, JM-M1, MP-M1, MP-X1, PD-M1, RP-M1, JM-X1, PD-X1, DQ-E1, PD-N1, JM-E1, IG-N1, CS-N1, CS-X1, IA-N1, RP-E1, PM-E1. Each ran as a new attempt on standard `49700991f7`; `META.json` records that hash and the skill hash.
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

## Not done / risks
- After the targeted regression, 19 scenarios still have their latest attempt on v2 (Tier 2 and Tier 3 in `docs/BATCH-H-REPORT.md` §6). The four skills edited in this pass have other scenarios whose latest attempt predates the edit.
- 38 scenarios have a passing latest attempt on standard v2 (`8f4607ccef`) and were not rerun on v5. v2 to v5 changes are additions and clarifications, but passing under v2 is not evidence under v5. `docs/BATCH-H-REPORT.md` proposes a targeted regression set for them.
- Several scenarios pass on one effective sample; the failures above show the same skill can pass and fail on the same scenario (see attempt histories). A pass is not a rate.
- The `problem-framing` and `product-metrics` stop rows can still be read two ways when another skill could create the missing input (for example `problem-framing` for a missing goal); graders accepted both.
- Automated screens are heuristics (A9 to A16). Semantic privacy, count correctness, and "single-idea question" were judged by graders. The IG-X1 a6 run read only the first lines of one interview, so source-content privacy was barely exercised there.
- A hand-written tally is still the most frequent failure class; the screens do not recompute counts.

## Limitations
- Executor and grader are both Claude models. Each scenario has 1 to 6 effective samples.
- Executors were subagents told to load the skill, not a human typing a slash command.
- Mermaid syntax was checked only for bracket balance.
