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
3. **Name the affected user and situation** only as far as evidence supports. Mark the rest `[assumption]`. Tag any claim the user supplies as `[reported]` with who said it. When you give a stakeholder's framing, either quote their exact words or paraphrase without quotation marks. Never put quotation marks around a framing label you coined, such as a rejected framing's name; write it in plain text. If the evidence does not support it, say so beside the claim and keep it out of the "because" clause.
4. **Draft the statement** as `[User] needs [need] because [evidence-backed reason]. Today [current state], which causes [consequence].` No solution words. Below it list the supporting evidence with tag and confidence, and the assumptions it depends on.
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
Supporting evidence and assumptions sit directly under `## Problem statement`. `## Next step` names one handoff: `ux-research-planner` when evidence is thin, `feature-prioritization` when candidate solutions exist, `mvp-planner` when scope is ready to cut.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] The statement contains no solution or feature name
- [ ] Each "because" clause cites evidence, or the statement is labeled Provisional
- [ ] Assumptions the statement depends on are listed, not hidden in wording
- [ ] Success definition has a baseline or says none exists
- [ ] One statement only; rejected alternatives noted with reasons

## Boundaries
- Does not explore the wider opportunity or plan discovery → `product-discovery`
- Does not design research to close evidence gaps → `ux-research-planner`
- Does not define metric trees or instrumentation → `product-metrics`
- Does not rank solutions → `feature-prioritization`
- Does not scope releases → `mvp-planner`
