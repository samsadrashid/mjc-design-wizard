---
name: problem-framing
description: Turn evidence and stakeholder context into one bounded problem statement with supporting evidence, assumptions, How-Might-We questions, and a success definition. Use when the user says "frame the problem", "what problem are we solving", "write a problem statement", or when a brief jumps to a solution before naming the problem. Not for broad opportunity exploration (use `product-discovery`) or for designing studies (use `ux-research-planner`).
---

# Problem Framing

## Purpose
Produce one testable problem statement the team can agree on, with the evidence behind it and the assumptions it still rests on. The statement is bounded: it says who, in what situation, and what is going wrong, without naming a solution. Gaps stay visible. Nothing is invented to make the statement feel complete.

## Triggers
- "Frame this", "what's the real problem", "write the problem statement"
- A request arrives as a feature ("add a dashboard") with no stated user problem
- A discovery brief exists and needs to become one focused statement

## Inputs
| Input | If missing | Source |
|---|---|---|
| Request, brief, or discovery output | Stop: nothing to frame | user, `design/discovery/` |
| Evidence of the problem (tickets, notes, data) | Assume: write a statement marked Provisional with Low confidence; next step is research planning | repo, user files |
| Affected user and situation | Assume: tag `[assumption]`; invent no persona | evidence, user |
| Current success measures | Assume: `Baseline: none`, and say how a baseline could be obtained (for example by defining a metric with `product-metrics`) | `design/metrics/`, user |

Ask one question only if its answer would change which problem is framed. Otherwise follow `../_shared/standard.md` §8.

## Workflow
1. **Inspect the project.** Read `design/discovery/`, the request, and any evidence the user names. Reuse an existing statement if one covers this scope, and list sources with their dates or `date unknown`. Copy no personal identifiers from tickets or notes.
2. **Split symptom, problem, and proposed solution** into a three-column table. Tag each cell.
3. **Name the affected user and situation** only as far as evidence supports. Mark the rest `[assumption]`. Tag any claim the user supplies as `[reported]` with who said it. When you give a stakeholder's framing, write it once as `Stakeholder said: "<their exact sentence>" (<source file>)`, copied from the file, and refer to it after that only in plain text; any rewording or reading of it goes on its own line as `Our reading: <words>`, with no quotation marks. Never put quotation marks around a framing label you coined, such as a rejected framing's name; write it in plain text. If the evidence does not support it, say so beside the claim and keep it out of the "because" clause. Quotation marks appear only on that one `Stakeholder said:` line and around verbatim source quotes cited by ID. Everywhere else in the file and the chat reply, including `Our reading:`, the split table, the how-might-we questions, open questions, rejected alternatives, and the falsification section, refer to the stakeholder's wording in plain text, as the stakeholder's framing, without quotation marks, and never put a phrase you wrote yourself, such as a paraphrase of a ticket or of the request, in quotation marks.
4. **Draft the statement** as `[User] needs [need] because [evidence-backed reason]. Today [current state].` Add `Consequence: <consequence> [class]` only when a source states or supports it; otherwise write `Consequence: unknown` in the evidence list. No solution words, and no consequence the statement does not need. Apply the claim-level evidence rules in `../_shared/standard.md` §2: split each clause, and keep the `because` and consequence out of `[observed]` unless the cited text states them. Under `## Problem statement`, add a claim ledger table with the columns `Claim | Source (kind + ID or path) | Supporting words | Class | Limit` that covers each clause of the statement, every count, and each quoted need. In `Supporting words`, quote ticket or interview text only; for the stakeholder's claim write `see Stakeholder said line` and do not repeat the sentence. Search each cited source for the words before you save. Count lines list the source IDs that state the category (`T-01`, not `P1`), per §2.
5. **Generate 3 to 5 HMW questions** at different altitudes. Mark the one to pursue and why. Five is a default cap.
6. **Define success.** Qualitative always. Quantitative only if a metric with a baseline exists; otherwise write `Baseline: none` and say how one could be obtained.
7. **State what would falsify the framing**, using specific missing evidence.
8. **Write the output** per §8 and show the statement and chosen HMW in chat.

## Outputs
Metadata block (§4), then path, date, collisions, and reruns (§8), follow `../_shared/standard.md`. File:
`design/discovery/problem-framing-<topic>-<date>.md`:
```
> metadata block
## Symptom / problem / solution split
## Problem statement
## Affected user and context
## How might we (ranked)
## Success definition (with baseline or "none")
## What would falsify this
## Open questions / to validate
## Next step
```
Supporting evidence, assumptions, and rejected alternatives with reasons sit directly under `## Problem statement`.

Figma (optional, per `../_shared/figma.md`): when publishing is enabled, draw on the `Problem Framing` page the symptom, problem, and solution split as three columns, a problem statement card with its supporting evidence, assumptions, and its Provisional label when it applies, the ranked How Might We list, and the success definition with its baseline or `Baseline: none`. Never draw evidence, a baseline, or a success target that is not in the Markdown. Show a stakeholder's framing only in their exact words; never put quotation marks around a label you coined. The Markdown file stays the source of truth.

`## Next step` names exactly one handoff, the first condition below that fits, and writes only that skill: `ux-research-planner` when evidence is thin, `feature-prioritization` when candidate solutions exist, `mvp-planner` when scope is ready to cut.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] Chat replies follow `../_shared/personality.md`; no emoticons in written files or structured output
- [ ] The statement contains no solution or feature name
- [ ] Each "because" clause cites evidence, or the statement is labeled Provisional
- [ ] Assumptions the statement depends on are listed, not hidden in wording
- [ ] Success definition has a baseline or says none exists
- [ ] One statement only; rejected alternatives noted with reasons
- [ ] Claim ledger present; every clause classed per `../_shared/standard.md` §2; `[observed]` only where the cited words state it; causes and consequences no file states are `[inferred]` or unknown
- [ ] Quotation marks appear only on the one `Stakeholder said:` line and around verbatim cited source quotes; none in `Our reading:` or around wording you wrote
- [ ] Any Figma output followed `../_shared/figma.md`, and the reply reports only Figma results a tool confirmed

## Boundaries
- Does not explore the wider opportunity or plan discovery → `product-discovery`
- Does not design research to close evidence gaps → `ux-research-planner`
- Does not define metric trees or instrumentation → `product-metrics`
- Does not rank solutions → `feature-prioritization`
- Does not scope releases → `mvp-planner`
