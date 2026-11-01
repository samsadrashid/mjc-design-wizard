---
name: design-documentation
description: Write a design spec, component doc, or decision record that lets someone build and maintain a design without the designer - behavior, components and props, tokens, states, accessibility, sources, and decisions - separating approved requirements from inferred behavior and recommendations. Use when the user says "write the spec", "document this design", "handoff doc", "component documentation", "design decisions record". Not for designing the flow (use `user-flow-designer`), verifying a build against a spec (use `design-qa`), or writing a narrative of a finished project (use `case-study-writer`).
---

# Design Documentation

## Purpose
Record what a design is, how it behaves, and why, in a form engineers can build from and later maintainers can trust. Each statement is marked as approved, inferred, or recommended, and its source is cited. Nothing is invented to complete a section. A missing fact is written as unavailable.

## Triggers
- "Spec this feature", "document the component", "handoff notes"
- A flow or design is approved and moving to build
- `design-qa` found there is no reference spec

## Inputs
| Input | If missing | Source |
|---|---|---|
| Design artifact: flow, mockups, prototype, or component code | Stop: nothing to document | user, `design/journeys/`, repo |
| Document type: feature spec, component doc, or decision record | Assume from the artifact and say so | user |
| Decisions and their reasons | Ask one: a spec without reasons is easy to misread. Otherwise record decisions as `Unavailable` | user, `design/` outputs |
| Existing tokens, components, and docs | Assume none and say the spec is standalone | repo, Storybook |
| Accessibility requirements | Assume WCAG 2.2 AA as a default | user |

## Workflow
1. **Inspect the project.** Read the flow, route definitions, component files and their props or types, token files, Storybook stories, and existing docs. Use names and values found there. Record the commit or version documented, or `version unknown`. Copy no personal data from fixtures.
2. **Choose the type** and file name (see Outputs). The heading contract is the same for all types.
3. **Fill each section from sources.** Mark every statement:
   - **Approved:** a cited source and an approver, or `approver unknown`.
   - **Inferred:** read from code or convention. Say where.
   - **Recommended:** the author's suggestion.
   - **Unavailable:** the fact does not exist in the material. Say what is missing.
4. **Describe behavior** per flow step or component: triggers, transitions, validation, feedback. Link the flow instead of redrawing it.
5. **Cover states:** default, interaction, loading, empty, error, and permission-denied, for each screen or component where relevant.
6. **Record tokens and measurements** by token name from the repo. Give a raw value only when no token exists, and flag it.
7. **Write the decision log:** decision, alternatives considered, reason, evidence, and status. Add assumptions and dependencies.
8. **Complete the handoff checklist** and open questions, then write the output per §8.

## Outputs
Metadata block (§4), then path, date, collisions, and reruns (§8), follow `../_shared/standard.md`. Files:
`design/docs/spec-<feature>-<date>.md`, `design/docs/component-<name>-<date>.md`, or `design/docs/adr-<topic>-<date>.md`. The metadata block adds `type: spec | component | decision-record` and `status: draft | in review | approved`.
```
> metadata block
## Purpose and status
## Context
## Scope and out of scope
## Flows and expected behavior
## Components, variants, and props
## Tokens and references
## States (interaction, loading, empty, error, permission)
## Accessibility and responsive requirements
## Implementation notes and sources
## Decisions, assumptions, and dependencies
## Handoff checklist
## Open questions / to validate
## Next step
```
Adapting the contract: never delete a heading. If a section does not apply, write `Not applicable: <reason>`. If it applies but the information does not exist, write `Unavailable: <what is missing>`. A component doc fills components, tokens, states, and accessibility in depth and marks flows as not applicable. A decision record fills purpose, context, and decisions, and marks the rest as not applicable.

`## Next step` names one handoff: `design-qa` to verify the build against this document, or `case-study-writer` once the project is complete.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] All thirteen headings are present, in order, for every document type
- [ ] Every statement is marked approved, inferred, recommended, or unavailable, with a source
- [ ] Inapplicable sections say `Not applicable` with a reason; missing facts say `Unavailable`
- [ ] Props, token names, and routes match the repo, and raw values are flagged
- [ ] Each interactive element has its relevant states documented or marked unavailable
- [ ] Decisions list alternatives and reasons
- [ ] No usability claims without a linked evidence source

## Boundaries
- Does not design the flow itself → `user-flow-designer`
- Does not verify a build against a spec → `design-qa`
- Does not write project narratives → `case-study-writer`
