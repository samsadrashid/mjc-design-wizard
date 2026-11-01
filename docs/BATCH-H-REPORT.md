# Batch H report: final audit and release readiness

> **Historical report.** This records the state at the end of Batch H; its counts are not updated, and later regression passes changed the results. Current behavioral results are maintained in [tests/behavioral/RESULTS.md](../tests/behavioral/RESULTS.md). Paths under `tests/behavioral/runs/` refer to local run artifacts that are not part of the public repository.

## 1. Executive summary

Verdict: **READY WITH DOCUMENTED LIMITATIONS.**

- **Structure.** All 19 skills, their contracts, 19 of 19 examples, the docs, and the validator are structurally consistent: `bash tests/run.sh` gives 679 checks passed and 54 unit tests OK.
- **Fixes.** This batch fixed 4 confirmed defects: 2 validator false negatives, 1 contradictory handoff declaration, and 1 ambiguous handoff sentence. It also fixed 1 documentation mismatch, 3 inaccuracies in `FINDINGS.md`, and 1 whitespace defect in the results generator.
- **Behavior.** 75 of 76 behavioral scenarios pass on their latest attempt and 1 fails (`PF-N1`). Of the passing scenarios, 38 last ran on standard v2, not the current v5. A targeted regression set is proposed below and was **not run**.
- **What this means.**
  - Structural correctness is verified.
  - Behavioral evidence is limited: single samples, Claude executing and grading, a synthetic project.
  - Production reliability is not established.

## 2. Git baseline and working-tree state

Recorded before any Batch H edit:

- Branch `main`, HEAD `8f53466` ("ci: add automated skill validation workflow"). No commits since.
- 28 tracked files modified: 19 `SKILL.md`, `README.md`, `docs/ARCHITECTURE.md`, `examples/README.md`, 4 examples, `tests/run.sh`, `tests/validate_skills.py`. The diff against HEAD was 1,260 insertions and 703 deletions.
- 1,395 untracked files. Inspected separately, since `git diff` does not include them:
  - `.claude/skills/_shared/standard.md`
  - `CONTRIBUTING.md`
  - `docs/BATCH-G-REPORT.md`
  - 15 new examples
  - `tests/test_validator.py`, `tests/test_behavioral_suite.py`
  - `tests/behavioral/`: 6.2 MB in total; `runs/` alone is 5.8 MB and about 1,300 files
- No file over 500 KB. `.gitignore` covers `.DS_Store`, `__pycache__/`, `*.pyc`, `.venv/`.

## 3. Audit matrix (19 skills)

Evidence used for every row:
- The validator: frontmatter, section order, Inputs table, §8 references, heading contract, and the architecture handoffs, which must appear in Outputs.
- A one-off cross-check of the Next-step handoffs in Outputs against the architecture table and against any Inputs text mentioning a next step.
- The new exact-heading and Next-step checks on each example.
- A quote check of each example against its own sample input.

"Behavioral latest" is each scenario's latest verdict and standard version (N1, M1, E1, X1).

| Skill | Contract consistent | Example headings exact | Example Next step | Behavioral latest (N1 M1 E1 X1) | Notes |
|---|---|---|---|---|---|
| product-discovery | Yes | Yes | One allowed | P/v2 P/v2 P/v2 P/v2 | Example quotes re-inspected: no paraphrase or coined label in quotation marks |
| ux-audit | Yes | Yes | One allowed | P/v3 P/v4 P/v2 P/v3 | Example carries location, affected task, criterion, evidence, severity, separate confidence, recommendation, coverage 2 of 3, `version unknown` |
| design-system-audit | Yes | Yes | One allowed | P/v2 P/v4 P/v3 P/v2 | |
| design-qa | Yes | Yes | One allowed | P/v2 P/v3 P/v2 P/v2 | |
| product-metrics | Yes | Yes | One allowed | P/v3 P/v4 P/v2 P/v3 | |
| information-architect | Yes | Yes | One allowed | P/v2 P/v2 P/v2 P/v2 | |
| journey-map-builder | Yes | Yes | One allowed | P/v5 P/v2 P/v2 P/v2 | |
| usability-test-planner | Yes after doc fix | Yes | One allowed | P/v3 P/v4 P/v3 P/v5 | Architecture table lacked `ux-research-planner`, which Outputs names; fixed (F3) |
| interview-guide-builder | Yes | Yes | One allowed | P/v2 P/v2 P/v4 P/v5 | The Inputs "stop and point to `ux-research-planner`" names a skill that can create the missing input, which §8 allows for stops; it does not conflict with "never point back" in Next step |
| ux-research-planner | Yes after fix | Yes | One allowed | P/v3 P/v2 P/v2 P/v3 | "names A or B, and C once…" could be read as two skills; reworded to one handoff (F2) |
| persona-builder | Yes | Yes | One allowed | P/v5 P/v3 P/v3 P/v3 | |
| user-flow-designer | Yes | Yes | One allowed | P/v3 P/v3 P/v3 P/v3 | Heading "Flow diagram (Mermaid or list)" and intent-tagged entry points confirmed; exact heading now enforced |
| design-critique | Yes | Yes | One allowed | P/v3 P/v3 P/v2 P/v4 | |
| competitive-analysis | Yes | Yes | One allowed | P/v2 P/v2 P/v2 P/v2 | |
| problem-framing | Yes after fix | Yes | One allowed | **F**/v5 P/v3 P/v3 P/v3 | Inputs said "next step can be `product-metrics`" but Outputs and the architecture table exclude it; resolved in Inputs (F1). `PF-N1` FAIL unchanged |
| mvp-planner | Yes | Yes | One allowed | P/v2 P/v2 P/v2 P/v2 | |
| feature-prioritization | Yes | Yes | One allowed | P/v2 P/v2 P/v2 P/v2 | Example: no missing factor filled; 2 complete candidates ranked; 2 provisional with no point score; all scores recomputed |
| design-documentation | Yes | Yes (13 of 13, in order) | One allowed | P/v4 P/v3 P/v2 P/v3 | Example metadata has `type` and `status`; `Unavailable:` used; `Not applicable:` shown for a decision record |
| case-study-writer | Yes | Yes | One allowed | P/v2 P/v3 P/v4 P/v2 | |

No skill promises research, results, live verification, or behavior beyond its tools. A scan for "rerun", "then run", "come back", and overclaiming phrases found none in skills or docs. The one "rerun" match is the §8 path rule ("collisions, reruns").

## 4. Example coverage

19 of 19. Every skill has `examples/<skill>.md` listed in `examples/README.md`, labeled illustrative, using invented data (Kettle and four other fictional scenarios). The index says examples are not evidence of behavior. No exceptions.

## 5. Validator review and regression tests

**Gap confirmed.** `norm_heading` drops a trailing parenthetical before comparing example headings with the skill template. Two mutations on a temporary copy both passed validation with 0 failures before the fix:
- "Flow diagram (Mermaid or list)" changed to "Flow diagram (Mermaid)".
- A Next step changed to chain two skills.

The Next step of an example was not validated at all.

**Fix** (`tests/validate_skills.py`, `validate_example`, additive; no existing check weakened):
- "output headings match skill contract exactly": compares raw heading text, whitespace collapsed, with the skill's Outputs template.
- "Next step names one allowed handoff": the example's Next step names exactly one skill, not itself, from the skill's Outputs handoff sentence. Names after "Never" are excluded, so `interview-guide-builder`'s "Never point back to `ux-research-planner`" does not count as allowed.

**Regression tests** (`tests/test_validator.py`, 4 new, all pass):
- `test_example_heading_parenthetical_drift`
- `test_example_next_step_chains_two_skills`
- `test_example_next_step_not_an_allowed_handoff`
- `test_example_next_step_disallowed_never_clause`

**Still not validated** (documented, not changed):
- Skill-specific metadata fields in examples, such as `type` and `status` for design-documentation.
- Table columns inside an example, such as the ux-audit findings columns.
- Semantic content: quotes, counts, arithmetic. These remain review and behavioral concerns.

## 6. Behavioral results and standard-version coverage

Recomputed from `scenarios.json`, each scenario's latest `runs/<id>/attempt-N/EVAL.md`, and its `META.json`:
- 76 scenarios: 75 PASS, 1 FAIL (`PF-N1`), 0 BLOCKED, 0 NOT EXECUTED. This matched `RESULTS.md` at the end of Batch H; it is a snapshot, not the current result.
- Latest attempt by standard version: v5 `49700991f7` 5, v4 `87b1ad1860` 8, v3 `6426474b14` 25, v2 `8f4607ccef` 38. No latest attempt is on v1 or has an unknown standard.
- 53 historical attempts have `standard_sha: unknown`. They were backfilled before hashes were recorded; none is a latest attempt.
- Skill hashes are `unknown` for all v1 and v2 attempts, so skill drift since those runs cannot be shown from metadata.
- History is preserved. No attempt was relabeled.

**v2 to v5 changes**, from a saved v2 copy of the standard diffed against the current file:
- (A) Stop and hand-back replies follow the one-skill rule, never "rerun" or "or". A declined job goes on a "Not done here" line.
- (B) When only the user can supply the input, a stop names no skill and writes "Next step: supply <input>".
- (C) Counting and attribution: list counted members, attribute details only to their source, verbatim quotes only, compute the age of evidence, label counts by category, count each person once.
- (D) Privacy: participant codes or "they", no first names or ages, no sensitive category named in any section, accessibility needs optional and in consent.

**Classification of the 38 v2 scenarios:**

| Tier | Scenarios | Why |
|---|---|---|
| 1, materially affected (19) | CA-M1, IA-M1, IG-M1, JM-M1, MP-M1, MP-X1, PD-M1, RP-M1 | Stop scenarios: rules A and B change what a correct stop reply is |
| | JM-X1, PD-X1, DQ-E1 | Requests that span skills: rule A adds the "Not done here" line |
| | PD-N1, JM-E1, IG-N1, CS-N1, CS-X1, IA-N1, RP-E1 | Read interviews or tickets and report counts or research content: rules C and D. CS, IG, and JM skills were also edited after v2 |
| | PM-E1 | product-metrics Inputs changed after v2 |
| 2, possibly affected (5) | PD-E1, MP-N1, FP-M1, FP-N1, IA-E1 | Cite research evidence incidentally |
| 3, not materially affected (14) | CA-E1, CA-N1, CA-X1, DC-E1, DD-E1, DQ-N1, DQ-X1, DS-N1, DS-X1, FP-E1, FP-X1, MP-E1, IA-X1, UA-E1 | Work from code, specs, competitor notes, or scoring inputs, with no stop, no spanning request, and little research content. The privacy rules still apply in principle |

**Recommendation:** rerun Tier 1 (19 runs plus 19 gradings) on v5, then decide on Tier 2 from those results. An exhaustive rerun of all 38 is not needed: Tier 3 scenarios do not exercise any rule that changed.

**Batch H skill edits not covered by any run:** `problem-framing` (Inputs wording) and `ux-research-planner` (Next-step wording). Both are wording-only. The latest attempts of PF-* and RP-* predate them.

## 7. PF-N1 status

FAIL, unchanged. Attempts 3 to 6 each put a coined framing label in quotation marks and attributed it to the stakeholder, whose only words are "People keep asking where their stuff is."

The standard rule (verbatim quotes only) and two skill rules written for this case did not stop it. Counts, dates, and privacy were correct in attempts 4 to 6.

The defect is recorded under "Open failures" in `tests/behavioral/FINDINGS.md`. `RESULTS.md` shows FAIL with history PASS → FAIL ×5. No report describes the suite as fully passing. No fix was attempted in Batch H.

## 8. Security and privacy

- **Scanner:** none available (`gitleaks`, `trufflehog`, `detect-secrets`, `ggshield` not installed). Installing one was not done because it requires a download.
- **Text review instead:** a regex scan covered AWS, GitHub, OpenAI/Anthropic-style, Slack, and Google keys, private-key headers, JWTs, and `api_key`/`secret`/`token`/`password` assignments. Scope: the whole working tree including untracked files, and `git log -p --all`. Result: no matches. This does not prove the repository is free of secrets.
- **Emails:** only synthetic `@example.test` addresses, all in fixtures. No local paths, usernames, or the maintainer's email appear in any file.
- **Synthetic personal data:**
  - Planted names, phone numbers, and sensitive asides exist by design in `tests/behavioral/fixtures/` and `_pii.json`, to test privacy handling.
  - Across all saved skill outputs and replies, one contains planted data: `runs/CS-X1/attempt-2/RESPONSE.md` names withheld categories. That is a historical, graded, superseded attempt. Every latest attempt is clean.
  - Grader and screening files name the synthetic terms while checking for them.
  - If `runs/` is published, this synthetic material is published with it.
- **Links:** no broken relative links in any Markdown file outside fixtures and runs.
- **Claims:** no document claims full behavioral validation, production readiness, or that all scenarios pass.
- **Hygiene:**
  - No stray generated files.
  - `runs/` (about 1,300 files, 5.8 MB) is the main publishing decision. The full test suite also passes in a copy without `runs/` (678 checks, 54 tests), so excluding it would not break CI.
  - Trailing whitespace exists in 9 saved run outputs and 1 EVAL file. These are left untouched as historical artifacts. The `RESULTS.md` instance was a generator defect and is fixed (F7).

## 9. Validation commands and results

| Command | Result |
|---|---|
| `bash tests/run.sh` | `679 passed, 0 failed, 679 total`; `Ran 54 tests` `OK` (the count includes this report's links) |
| `bash tests/run.sh` in a copy without `tests/behavioral/runs/`, run before this report existed | `678 passed, 0 failed, 678 total`; `Ran 54 tests` `OK` |
| `python3 -m unittest tests.test_validator` | `Ran 39 tests` `OK` (includes the 4 new regression tests) |
| `git diff --check` | No output (clean) |
| Untracked files: trailing whitespace, conflict markers, CR | None outside historical run artifacts (listed in §8) |
| 19 skill/example pairs: exact headings and Next step | 19 of 19 pass both checks |
| Behavioral suite | **Not rerun** in Batch H |

## 10. Files changed in Batch H

| # | File | Defect | Change | Verification |
|---|---|---|---|---|
| F1 | `.claude/skills/problem-framing/SKILL.md` | Inputs said "next step can be `product-metrics`", contradicting Outputs and the architecture table | Inputs now says to state `Baseline: none` and how a baseline could be obtained (for example with `product-metrics`); handoff list unchanged | Validator pass; handoff cross-check clean |
| F2 | `.claude/skills/ux-research-planner/SKILL.md` | Next-step sentence could be read as naming two skills | "names one handoff: A or B to build the study instrument, or C once…"; same skills | Validator pass |
| F3 | `docs/ARCHITECTURE.md` | usability-test-planner row omitted `ux-research-planner`, which its Outputs names | Row lists both handoffs | Handoff cross-check clean |
| F4 | `tests/validate_skills.py` | Example headings compared without parentheticals; example Next step unchecked | Two additive checks | Mutations now fail; 679 checks pass |
| F5 | `tests/test_validator.py` | No regression tests for F4 | 4 tests | `Ran 39 tests` OK |
| F6 | `tests/behavioral/FINDINGS.md` | "38 runs on v3" read as the 38 v2 scenarios; PF-N1 failing attempts listed as a3 to a5 (a6 also failed); no pointer to the regression proposal | Corrected wording and attempt range; pointer added | Read back |
| F7 | `tests/behavioral/harness.py` | Summary truncated a failure note at 700 characters leaving trailing whitespace | `.rstrip()` after truncation | `RESULTS.md` regenerated: 0 trailing-space lines; counts unchanged (75 PASS, 1 FAIL) |
| — | `tests/behavioral/RESULTS.md` | — | Regenerated by `harness.py summary` | Counts unchanged |
| — | `docs/BATCH-H-REPORT.md` | — | This report | Links pass |

`docs/BATCH-G-REPORT.md` is left as the Batch G record. Its validator counts (640) and known gaps 1 to 3 describe that batch's state; gaps 1 to 3 are resolved here by F1 to F5. No other file changed; no historical attempt was edited or deleted.

## 11. Remaining risks and recommended regressions

1. **PF-N1** remains failing. The likely next fix is structural: a fixed "Rejected framing" line with no quotation marks.
2. **38 scenarios lack v5 evidence.** Rerun Tier 1 (19) first; this needs your approval because of the model usage.
3. **Two Batch H wording edits are not behaviorally rerun:** problem-framing Inputs and ux-research-planner Next step.
4. **Behavioral evidence is thin:** 1 to 6 samples per scenario; Claude as both executor and grader; synthetic fixtures; subagents rather than a person typing slash commands. Passing scenarios have also failed on other attempts.
5. **Publishing decision:** whether to commit `tests/behavioral/runs/` (5.8 MB, synthetic sensitive terms in grader text).
6. **Validator scope:** structure only; example metadata fields and table columns are not checked.
7. **No real secret scanner was run.**

## 12. Release-readiness verdict

**READY WITH DOCUMENTED LIMITATIONS.**

- No structural defect or validation failure remains.
- The one behavioral failure (`PF-N1`) is a known, documented defect in one scenario of one skill, not a blocker for publishing instruction files.
- The limitations are behavioral (§6, §7, §11), plus the publishing decision on `runs/`.
- "Ready" here means structurally correct and honestly documented. It does not mean the skills behave reliably in production.

## 13. Commits and pushes

Nothing was committed, pushed, merged, reset, stashed, or discarded. HEAD is still `8f53466`. Claude was the only coding agent.
