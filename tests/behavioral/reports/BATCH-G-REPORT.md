# Batch G report: examples for all 19 skills

> **Historical report.** This records the state at the end of Batch G; its counts are not updated. Current behavioral results are maintained in [tests/behavioral/RESULTS.md](../tests/behavioral/RESULTS.md).

Examples are illustrative. They show what each skill's output contract asks for, using invented data. They do not show that a skill reliably produces that output; behavioral evidence lives in [tests/behavioral/](../tests/behavioral/), which this batch did not rerun or change.

## Starting state

- HEAD `8f53466`, with earlier batches uncommitted.
- 4 of 19 skills had examples: `feature-prioritization`, `ux-audit`, `problem-framing`, `user-flow-designer`.
- Known defects in those four:
  - `feature-prioritization` filled missing factors with a "lowest plausible value", which the current skill forbids. It also lacked the basis column and the provisional tier, and its heading text had drifted.
  - `ux-audit` lacked the status, affected-task, and confidence columns, coverage numbers, the build line, and hypothesis rows. Its Next step named two actions.
  - `problem-framing` did not list the counted tickets or the supporting evidence under the statement. It noted no rejected alternatives, and its Next step (`product-metrics`) is not in the skill's Outputs handoff list.
  - `user-flow-designer` shortened the heading "Flow diagram (Mermaid or list)" and had no entry points with intent.

## Example inventory

| # | Skill | Example | Created or updated |
|---|---|---|---|
| 1 | `product-discovery` | [examples/product-discovery.md](../examples/product-discovery.md) | Created |
| 2 | `ux-audit` | [examples/ux-audit.md](../examples/ux-audit.md) | Updated |
| 3 | `design-system-audit` | [examples/design-system-audit.md](../examples/design-system-audit.md) | Created |
| 4 | `design-qa` | [examples/design-qa.md](../examples/design-qa.md) | Created |
| 5 | `product-metrics` | [examples/product-metrics.md](../examples/product-metrics.md) | Created |
| 6 | `information-architect` | [examples/information-architect.md](../examples/information-architect.md) | Created |
| 7 | `journey-map-builder` | [examples/journey-map-builder.md](../examples/journey-map-builder.md) | Created |
| 8 | `usability-test-planner` | [examples/usability-test-planner.md](../examples/usability-test-planner.md) | Created |
| 9 | `interview-guide-builder` | [examples/interview-guide-builder.md](../examples/interview-guide-builder.md) | Created |
| 10 | `ux-research-planner` | [examples/ux-research-planner.md](../examples/ux-research-planner.md) | Created |
| 11 | `persona-builder` | [examples/persona-builder.md](../examples/persona-builder.md) | Created |
| 12 | `user-flow-designer` | [examples/user-flow-designer.md](../examples/user-flow-designer.md) | Updated |
| 13 | `design-critique` | [examples/design-critique.md](../examples/design-critique.md) | Created |
| 14 | `competitive-analysis` | [examples/competitive-analysis.md](../examples/competitive-analysis.md) | Created |
| 15 | `problem-framing` | [examples/problem-framing.md](../examples/problem-framing.md) | Updated |
| 16 | `mvp-planner` | [examples/mvp-planner.md](../examples/mvp-planner.md) | Created |
| 17 | `feature-prioritization` | [examples/feature-prioritization.md](../examples/feature-prioritization.md) | Rewritten |
| 18 | `design-documentation` | [examples/design-documentation.md](../examples/design-documentation.md) | Created |
| 19 | `case-study-writer` | [examples/case-study-writer.md](../examples/case-study-writer.md) | Created |

The index [examples/README.md](../examples/README.md) lists all 19 and states that they are illustrative and not evidence of behavior. Fifteen examples follow one fictional product (Kettle, a meal-kit subscription app) so outputs can build on each other. Four keep their own invented scenarios: checkout audit, order-lookup framing, password reset, and checkout backlog.

## Contract checks performed

- **Structure:** every output block uses the skill's headings verbatim, in order. This was compared as raw text by a one-off script, which also catches drift inside parentheses that the validator ignores. Each block starts with the `> skill:` line and uses the skill's output path with `<YYYY-MM-DD>`.
- **Next step:** each block names exactly one skill, drawn from that skill's handoff list and never the skill itself. Script check: 19 of 19.
- **Numbers:** every number shown as observed is derivable from sample data inside the example. RICE scores, journey ratios of counts, metric rates, and the WCAG contrast ratio (2.64:1 for `#9AA0A6` on white) were recomputed with commands.
- **Quotation marks:** quotes in each output were checked against that example's prompt and sample input. Two coined or paraphrased quotes in `product-discovery` were removed. The remaining quoted text is authored content (questions, task prompts, UI copy) and is not attributed to a source.
- **Per-skill requirements:**
  - `feature-prioritization`: no missing factor is filled. Two candidates are complete and ranked. Two are provisional with no point score, and one scenario table is labeled as scenarios. The candidate-confidence rule and the "supports a decision, does not replace judgment" line are stated.
  - `ux-audit`: every finding has status, location, affected task, criterion, evidence with source, severity, separate confidence, and a recommendation. Coverage is stated as 2 of 3 screens, the build as `version unknown`, and the hypothesis row is unrated. Contrast is computed from stated values only; unverified checks are listed.
  - `design-documentation`: all 13 headings are in order, and the metadata adds `type` and `status`. Statements are marked Approved, Inferred, Recommended, or Unavailable, and the one raw value is flagged. `Unavailable: <what is missing>` is used where facts do not exist. A note after the block shows `Not applicable: <reason>` for a decision record, since no spec section was genuinely inapplicable.
  - `design-qa`: the reference is approved and named. Verified mismatches cite the expected value and the code evidence. The image estimate is unverified, and spec gaps are separate.
  - `information-architect`: the audited current structure and the proposal are separate, with change markers and all 10 inventory items mapped.
  - `journey-map-builder`: Emotion reads `Not reported` because no participant stated one. Event ratios are labeled as ratios of counts, not conversion.
  - Research examples: the consent scripts, participant codes, and optional accessibility questions are all covered in consent text. The persona sensitive aside is omitted with the generic sentence only.
  - `persona-builder`: counts are of independent people, ticket-to-interviewee matches are recorded by code, and the 3-person gate is a stated default.
  - `mvp-planner`: only the five user-supplied candidates appear, each with its source. There are no dates, and the ship-date question is answered under Risks.
  - `case-study-writer`: claims are classed verified, recollection, interpretation, or `[TO VERIFY]`. The user's "dropped by half" claim stays out of the Outcome. Decision status is reported as unknown because no artifact records it.

## Validation

| Command | Result |
|---|---|
| `bash tests/run.sh` | `640 passed, 0 failed, 640 total`; `Ran 50 tests` `OK` |
| `git diff --check` | No output (clean) for tracked files; untracked example files checked for trailing whitespace separately, none found |
| Strict heading and Next-step script (one-off, not committed) | 19 of 19 OK |

The structural count rose from 504 to 640 because the validator checks each new example file and this report's links. Its code was not changed.

## Scope confirmation

- Only files under `examples/` and this report were changed in Batch G. A modification-time check after the batch found no other changed file.
- `.claude/skills/_shared/standard.md`, all `SKILL.md` files, and everything under `tests/behavioral/` (including `PF-N1`, still FAIL) were not modified.
- The behavioral suite was not rerun.
- No commits or pushes were made. Claude was the only coding agent.

## Known gaps and inconsistencies (documented, not fixed)

1. **Validator heading check is loose.** `norm_heading` drops a trailing parenthetical, so drift such as "Flow diagram (Mermaid)" for "Flow diagram (Mermaid or list)" passes. A strict raw-text comparison for examples would close this. It was not added in this batch.
2. **`problem-framing` contract inconsistency.** The Inputs table says the next step can be `product-metrics` when no baseline exists, but the Outputs handoff list names only `ux-research-planner`, `feature-prioritization`, and `mvp-planner`. The example follows the Outputs list.
3. **`ux-research-planner` handoff wording** ("names `interview-guide-builder` or `usability-test-planner`, and `persona-builder` once…") can be read as naming two skills. The example names one.
4. **Examples use the same product as their sources** (for example, the design-qa reference is an approved revision of the design-documentation draft). The narrative continuity is invented. It does not mean the skills were chained in a real run.
5. **Examples cannot show behavior.** `PF-N1` remains an open behavioral failure (coined labels in quotation marks). The `problem-framing` example shows the correct form but does not change that result.
