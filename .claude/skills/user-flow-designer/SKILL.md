---
name: user-flow-designer
description: Design screen- and state-level user flows for one task - entry points, decisions, screens, states (empty, loading, error, success), and exits - as text diagrams. Use when the user says "user flow", "map the flow", "what screens do we need", "edge cases for this flow", or before wireframing a feature.
---

# User Flow Designer

## Purpose
Specify how a user completes one task through the product: every screen, decision, and state, including unhappy paths. Output is a text diagram plus a state table that engineers and designers can build from.

## Triggers
- "Design the flow for X", "map out signup", "what states does this need"
- A feature is scoped and needs definition before UI design
- A journey map identifies a stage to detail

## Inputs
| Input | Required | Source |
|---|---|---|
| Task and actor | yes | user, `design/journeys/` |
| Entry points and preconditions | yes | user, repo |
| Existing screens, routes, components | optional | repo (routes, UI code, design files) |
| Constraints (platform, auth, offline) | optional | user, repo |

## Workflow
1. **Inspect the project.** Read routes, navigation, existing flow docs, design system. List existing screens the flow can reuse.
2. **Define the task** with a start state, success end state, and known failure end states.
3. **Draw the happy path** as a Mermaid flowchart: screens as nodes, user decisions as diamonds, system checks labeled.
4. **Add alternate and error paths**: validation, permission denied, network failure, empty data, timeout, back navigation, abandonment.
5. **State table** per screen: empty, loading, partial, error, success, plus what the user can do in each.
6. **Annotate data and permissions** needed at each step. Mark unknown backend behavior `[assumption]`.
7. **Count steps** on the happy path and flag any step that could be removed.
8. **Write output**; show the Mermaid diagram in chat.

## Outputs
`design/journeys/user-flow-<task>-<date>.md`:
```
> metadata block
## Task, actor, entry and exit states
## Flow diagram (Mermaid)
## Alternate and error paths
## Screen state table
## Data and permission notes
## Step count and simplification candidates
## Open questions / to validate
## Next step
```

## Quality checks
- [ ] Global checks in `docs/ARCHITECTURE.md` §7
- [ ] Every screen has all five states or an explicit "not applicable"
- [ ] Every decision node has all branches resolved
- [ ] Mermaid renders (balanced brackets, valid syntax)
- [ ] Reuses existing screens where repo shows them

## Boundaries
- Does not map lifecycle-level journeys → `journey-map-builder`
- Does not define navigation structure → `information-architect`
- Does not write visual specs → `design-documentation`
