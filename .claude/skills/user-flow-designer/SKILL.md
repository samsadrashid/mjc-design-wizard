---
name: user-flow-designer
description: Design the screen- and state-level flow for one task - entry points, user intent, decisions, alternate paths, errors and recovery, and completion - with unresolved product decisions made visible. Use when the user says "user flow", "map the flow", "what screens do we need", "edge cases for this flow", or before wireframing a feature. Not for lifecycle-level journeys (use `journey-map-builder`), navigation structure (use `information-architect`), or visual and interaction specs (use `design-documentation`).
---

# User Flow Designer

## Purpose
Specify how a user completes one task: where they enter, what they intend, each decision, and every way the task can succeed, fail, or be abandoned, including recovery. The flow is built from the product as it exists and from stated requirements. Anything the product has not decided is shown as an open decision, not silently invented.

## Triggers
- "Design the flow for X", "map out signup", "what states does this need"
- A feature is scoped and needs definition before interface design
- A journey map identifies a stage to detail

## Inputs
| Input | If missing | Source |
|---|---|---|
| Task and actor | Stop: a flow needs one task and one actor | user, `design/journeys/` |
| Entry points and preconditions | Assume from routes or navigation in the repo and tag it | repo, user |
| Existing screens, routes, components, auth rules | Assume none and say the flow is greenfield | repo |
| Backend behavior, permissions, constraints | Ask one if a branch depends on it; otherwise assume and tag | user, repo |

## Workflow
1. **Inspect the project.** Read routes, navigation, auth and permission logic, existing flow docs, and the design system. List existing screens the flow can reuse, with their paths. Do not copy personal data from fixtures or logs.
2. **Define the task and intent.** Actor, goal, start state, success end state, and known failure end states.
3. **Enumerate entry points,** each with the intent the user brings. A flow often starts in several places.
4. **Draw the happy path.** Mermaid is used here because branching is easier to read in a diagram. Use a plain list when the flow is linear.
5. **Add branches:** validation errors, permission denied, empty data, loading and timeout, network failure, back navigation, abandonment, and resume. Every branch must reach a named outcome: a screen, a recovery action, or an exit. No dead ends and no unexplained jumps.
6. **Complete the state table** per screen: empty, loading, partial, error, success, and permission-denied where the screen is gated. Write `Not applicable` instead of leaving a cell blank.
7. **Separate what is known from what is not.** Mark behavior inferred from code or convention as `[inferred]` and anything the product has not decided as `[assumption]` and an open question. Do not turn a guess into a requirement.
8. **Count steps** on the happy path and flag steps that could be removed. Write the output per §8.

## Outputs
Metadata block (§4), then path, date, collisions, and reruns (§8), follow `../_shared/standard.md`. File:
`design/journeys/user-flow-<task>-<date>.md`:
```
> metadata block
## Task, actor, entry and exit states
## Flow diagram (Mermaid or list)
## Alternate and error paths
## Screen state table
## Data and permission notes
## Step count and simplification candidates
## Open questions / to validate
## Next step
```
Entry points and intent go under the first section. Each decision node and branch outcome appears in the diagram or the paths list. `## Next step` names one handoff: `design-documentation` once the flow is approved, `usability-test-planner` to test it, or `information-architect` if the problem is navigation.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] Every decision has all its branches, and every branch reaches a named outcome
- [ ] Every screen has all applicable states, or `Not applicable`
- [ ] Mermaid, if used, has valid syntax and balanced brackets
- [ ] Existing screens and routes are reused where the repo shows them
- [ ] Inferred behavior and open product decisions are labeled, not stated as fact
- [ ] No disconnected nodes

## Boundaries
- Does not map lifecycle-level journeys → `journey-map-builder`
- Does not define navigation or labels → `information-architect`
- Does not write visual or interaction specs → `design-documentation`
- Does not decide what to build or why → `product-discovery`
