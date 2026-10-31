---
name: design-critique
description: Give structured critique on a specific design proposal - goals alignment, clarity, hierarchy, interaction, content, accessibility - with ranked, actionable feedback. Use when the user says "critique this", "feedback on this design", "review my mockup", "what would you change", or shares a design for review.
---

# Design Critique

## Purpose
Deliver critique that a designer can act on: tied to stated goals, specific to elements, ranked by impact, and separated into must-fix, should-fix, and consider. Opinions are labeled as such.

## Triggers
- "Critique this screen", "review this prototype", "feedback please"
- A design is shared before handoff or stakeholder review
- Crit session prep

## Inputs
| Input | Required | Source |
|---|---|---|
| Design artifact (image, file, prototype, description) | yes | user |
| Design goal and target user | yes | user, `design/discovery/`, `design/research/` |
| Constraints (platform, system, timeline) | optional | user, repo |
| What kind of feedback is wanted (direction vs polish) | optional | user |

## Workflow
1. **Inspect the project.** Read problem framing, personas, design system docs. Use them as the critique baseline.
2. **Restate the goal** the design must achieve. If absent, ask once; otherwise critique against a stated `[assumption]`.
3. **Describe what is seen** before judging: layout, primary action, content, states shown.
4. **Evaluate** across lenses: goal fit, hierarchy and first read, interaction clarity, content and tone, consistency with system, accessibility, edge states missing.
5. **Write feedback items.** Each: element, observation, why it matters (tied to goal or evidence), suggestion, confidence (opinion vs principle vs evidence).
6. **Rank**: must-fix (blocks goal), should-fix, consider. Max 10 items; note what works in two lines.
7. **Write output**; show must-fix list in chat.

## Outputs
`design/audits/design-critique-<artifact>-<date>.md`:
```
> metadata block
## Goal and audience
## What I see
## What works
## Feedback (ranked; element, observation, why, suggestion, confidence)
## Missing states and edge cases
## Open questions / to validate
## Next step
```

## Quality checks
- [ ] Global checks in `docs/ARCHITECTURE.md` §7
- [ ] Every item names a specific element
- [ ] Every item links to goal, evidence, or a named principle
- [ ] Opinions labeled as opinions
- [ ] No rewrite of the design; suggestions only

## Boundaries
- Does not do a systematic heuristic sweep → `ux-audit`
- Does not compare to competitors → `competitive-analysis`
- Does not check build fidelity → `design-qa`
