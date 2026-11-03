---
name: user-flow-designer
description: Design the complete, evidence-grounded screen- and state-level flow for one task - entry points, user intent, decisions, every supported branch, errors and recovery, loops, and terminal outcomes - with a transition inventory that ties each arrow to its source and unresolved behavior made visible. Use when the user says "user flow", "map the flow", "what screens do we need", "edge cases for this flow", or before wireframing a feature. Not for lifecycle-level journeys (use `journey-map-builder`), navigation structure (use `information-architect`), or visual and interaction specs (use `design-documentation`).
---

# User Flow Designer

## Purpose
Specify how a user completes one task: where they enter, what they intend, each decision, and every way the task can succeed, fail, be cancelled, or be abandoned, including recovery and repeat attempts. The flow is traced from the product as it exists (code, tests, specifications, existing design artifacts) and from stated requirements, so designers can rely on it. Every arrow is backed by a source or labeled as inferred or unknown. Anything the product has not decided is shown as an open decision, not silently invented, and the diagram never looks more complete than the evidence.

## Triggers
- "Design the flow for X", "map out signup", "what states does this need"
- A feature is scoped and needs definition before interface design
- A journey map identifies a stage to detail, or an existing flow doc needs checking against the build

## Inputs
| Input | If missing | Source |
|---|---|---|
| Task and actor | Stop: a flow needs one task and one primary actor | user, `design/journeys/` |
| Entry points and preconditions | Assume from routes or navigation in the repo and tag it | repo, user |
| Implementation: screens, routes, state rules, handlers, tests | Assume none and say the flow is greenfield; every transition is then `Inferred` or `Unknown` | repo |
| Specifications, decision docs, earlier flow docs | Assume none | `docs/`, `design/` |
| Backend behavior, permissions, constraints | Ask one if a branch depends on it; otherwise assume and tag | user, repo |

## Workflow
1. **Inspect the project.** Read routes and navigation, the screens and dialogs of the task, state rules or state machines, permission checks, repository or API calls and their error handling, tests that exercise the task, specifications, and earlier flow docs. List each source read. Do not copy personal data from fixtures or logs.
2. **Define the task, actors, and states.** Primary actor and goal; other actors whose actions move the task (an approver, an admin); start states; success, failure, cancelled, and abandoned end states. Record role differences: who sees which action.
3. **Discover before drawing.** Trace the task through the sources and list, only where the evidence shows them: entry points with the intent each brings; user actions and system responses; every decision and its supported outcomes; validation errors and recovery; loading, pending, empty, and failure states; retry, resubmission, back navigation, repeat actions, and loops; actions by other actors; terminal outcomes and their effect on what the user sees next. These are discovery prompts, not boxes to fill: a branch the product does not have is left out, and a branch it should have but does not is a gap (step 6).
4. **Build the transition inventory.** One row per transition: ID (`T1`, `T2`, …), from state, trigger (action or event), condition, to state, user-visible feedback, status, and evidence. Status is `Verified` (a source shows it; cite `path` or `path:line`), `Inferred` (a reasonable reading that needs confirmation; say why), or `Unknown` (no source settles it). A `Verified` row is `[observed]` in the standard's terms; `Inferred` is `[inferred]`.
5. **Draw the complete flow from the inventory.** Every inventory row is one labeled arrow, and every arrow is a row: label each edge `T<n> · <trigger or branch>`. Conventions: rounded nodes `id("...")` for screens, actions, and states; diamonds `id{"..."}` for genuine decisions only, each outgoing edge labeled; terminal states as stadium nodes `id(["End · ..."])`. Prefix node text with its kind so meaning never depends on color: `End ·`, `Error ·`, `Pending ·`, `Cancelled ·`. Color classes may add emphasis. Route loops and return paths as edges back to the earlier node. Add a legend table under the diagram. The complete flow is always one diagram that holds every transition, however large; never split it into sections, and never drop a branch to make it fit.
6. **Record gaps and contradictions.** List behavior the evidence leaves `Unknown`, behavior that is expected but missing (no handler, no state, no copy), and sources that disagree (spec versus code, code versus test, earlier flow doc versus code), each with both sources. Never resolve a contradiction by choosing a side silently.
7. **Draw each individual flow.** Break the complete flow into its sub-flows, one diagram each: the primary journey first (the most common path, with its step count and any steps that could be removed), then every other path a person can take to an outcome, such as each alternative entry, each error and recovery loop, each other actor's path (an approver, an admin), and each cancel or abandon path. Give each a `### F<n> · <name>` heading, a one-line purpose, the actor, and its end state. Use the same node conventions and only transition IDs from the inventory, labeled the same way. Together the individual flows cover every inventory transition at least once. They make the complete flow readable and never replace it.
8. **Complete the screen state table** per screen: empty, loading, partial, error, success, and permission-denied where the screen is gated. Cite the source or tag each cell; write `Not applicable` instead of leaving a cell blank.
9. **Run the flow integrity check** and write its result: every entry point reaches at least one terminal state; every non-terminal node has an outgoing edge; every node except entry points has an incoming edge; every decision has two or more labeled outgoing edges; diagram edges and inventory rows match one to one by ID; the complete flow is one diagram; individual flows use only inventory transitions, and together they cover every transition (list any transition no individual flow covers). Count nodes, edges, and transitions by status, and list anything unreachable or dead-ended. A dead end, or a decision or pending state with no failure exit, is a defect to fix before saving: add the missing branch from the evidence, or route it to an `Unknown` node with its inventory row; never leave it in the diagram with only a note. State which sources were compared and which were not (for example, tests not run). Do not call the flow exhaustive; report coverage. Write the output per §8.

## Outputs
Metadata block (§4), then path, date, collisions, and reruns (§8), follow `../_shared/standard.md`. File:
`design/journeys/user-flow-<task>-<date>.md`:
```
> metadata block
## Task, actors, entry and exit states
## Evidence base
## Complete flow
## Transition inventory
## Individual flows
## Screen state table
## Gaps, contradictions, and unknowns
## Flow integrity check
## Open questions / to validate
## Next step
```
Entry points, intents, and role differences go under the first section. `## Evidence base` lists every source read with its date or `date unknown`. `## Complete flow` holds the one complete diagram (Mermaid; a plain list only for a strictly linear task) and the legend. `## Individual flows` holds one diagram per sub-flow, primary journey first; when no single path dominates, say so and order the flows by entry point. A rerun next to an earlier flow doc for the same task lists, under gaps, what the earlier doc got wrong or left out.

Figma (optional, per `../_shared/figma.md`): when publishing is enabled, draw on the `User Flows` page the complete flow as editable shapes with labels and arrow vectors for every inventory transition, edges labeled with their transition IDs, decisions as diamonds, terminal states visibly distinct by shape and text, the legend, each individual flow as a separate group, and the gaps list. Never draw a screen, branch, or error path that is not in the Markdown, and never show an open product decision or an `Unknown` transition as decided. The Markdown file stays the source of truth.

`## Next step` names exactly one handoff, the first condition below that fits, and writes only that skill: `design-documentation` once the flow is approved, `usability-test-planner` to test it, or `information-architect` if the problem is navigation.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] Chat replies follow `../_shared/personality.md`; no emoticons in written files or structured output
- [ ] Every transition has from state, trigger, condition, to state, feedback, status, and evidence; `Verified` rows cite a source
- [ ] Diagram edges and inventory rows match one to one by transition ID
- [ ] The complete flow is one diagram; individual flows, primary journey first, together cover every transition
- [ ] Every decision has all its supported branches, each labeled, and every branch reaches a named node
- [ ] Terminal states use the stadium shape and `End ·` text; meaning never depends on color alone; a legend is present
- [ ] The integrity check ran and its counts, unreachable nodes, and dead ends are written down
- [ ] Contradictions name both sources; nothing missing from the evidence is drawn as fact
- [ ] Every screen has all applicable states, or `Not applicable`
- [ ] Mermaid has valid syntax and balanced brackets
- [ ] Existing screens and routes are reused where the repo shows them
- [ ] Any Figma output followed `../_shared/figma.md`, and the reply reports only Figma results a tool confirmed

## Boundaries
- Does not map lifecycle-level journeys → `journey-map-builder`
- Does not define navigation or labels → `information-architect`
- Does not write visual or interaction specs → `design-documentation`
- Does not audit usability or accessibility → `ux-audit`
- Does not decide what to build or why → `product-discovery`
