---
name: design-documentation
description: Write design specs and rationale for a feature or component - behavior, states, content, accessibility, tokens, and decisions with reasons - for engineering handoff or system docs. Use when the user says "write the spec", "document this design", "handoff doc", "component documentation", "design decisions record".
---

# Design Documentation

## Purpose
Produce documentation that lets someone build or maintain the design without the designer present: precise behavior, every state, content rules, accessibility requirements, and the reasoning behind decisions.

## Triggers
- "Spec this feature", "document the component", "handoff notes"
- A flow or design is approved and moving to build
- Design-qa found that no reference spec exists

## Inputs
| Input | Required | Source |
|---|---|---|
| Design artifact (flow, mockups, prototype, component code) | yes | user, `design/journeys/`, repo |
| Decisions and their reasons | yes | user, critique or discovery outputs |
| Design tokens and system components | optional | repo, `design/audits/` |
| Accessibility requirements | optional | user (default WCAG 2.2 AA) |

## Workflow
1. **Inspect the project.** Read the flow, tokens, existing component docs, and the design system. Match naming to what exists in code.
2. **Choose doc type**: feature spec, component doc, or decision record. Use the matching template below.
3. **Describe behavior** per screen or component: triggers, transitions, validation, feedback. Reference flow diagram rather than redrawing.
4. **State table**: all states with visual and content for each. Mark unspecified ones as `TBD` rather than inventing.
5. **Content rules**: labels, error messages, empty states, character limits, tone.
6. **Accessibility**: roles, names, focus order, keyboard, contrast, motion.
7. **Tokens and measurements** from the system; raw values only when no token exists, flagged.
8. **Decision log**: decision, alternatives, reason, evidence, date.
9. **Write output**; show the state table in chat.

Templates:
- Feature spec: overview, flow reference, screens and behavior, states, content, accessibility, tokens, decisions, open items.
- Component doc: purpose, anatomy, variants, props/options, states, content, accessibility, do/don't, decisions.
- Decision record: context, decision, alternatives, consequences, evidence.

## Outputs
`design/docs/spec-<feature>-<date>.md` or `design/docs/component-<name>-<date>.md` or `design/docs/adr-<topic>-<date>.md`

## Quality checks
- [ ] Global checks in `docs/ARCHITECTURE.md` §7
- [ ] Every interactive element has all states documented or `TBD`
- [ ] Token names match repo; raw values flagged
- [ ] Each decision has a reason and alternatives
- [ ] No usability claims without evidence link

## Boundaries
- Does not design the flow → `user-flow-designer`
- Does not verify build fidelity → `design-qa`
- Does not write narrative case studies → `case-study-writer`
