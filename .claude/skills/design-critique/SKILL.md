---
name: design-critique
description: Give constructive critique of a specific design proposal against its goals, users, and design principles, separating usability and accessibility risks from preference and ranking everything by impact. Use when the user says "critique this", "feedback on this design", "review my mockup", "what would you change", or shares a design for review. Not for a systematic heuristic sweep of an experience (use `ux-audit`), checking a build against its spec (use `design-qa`), or comparing against competitors (use `competitive-analysis`).
---

# Design Critique

## Purpose
Give feedback a designer can act on: tied to the design's goal and users, specific to named elements, and honest about its basis. Risks to usability or accessibility are kept apart from taste, so the team can tell what needs a fix from what is an opinion. Findings are ranked by impact, not trimmed to a number.

## Triggers
- "Critique this screen", "review this prototype", "feedback please"
- A design is shared before handoff or stakeholder review
- Preparing for a critique session

## Inputs
| Input | If missing | Source |
|---|---|---|
| Design artifact (image, file, prototype, or description) | Stop: nothing to critique | user |
| Design goal and target user | Ask one: critique is only meaningful against a goal. If unanswered, state an `[assumption]` and proceed | user, `design/discovery/`, `design/research/` |
| Design system and constraints (platform, tokens, timeline) | Assume none and say so | repo, user |
| Kind of feedback wanted (direction or polish) | Assume direction first, then polish | user |

## Workflow
1. **Inspect the project.** Read problem framing, personas, and design system docs, and use them as the baseline. Do not repeat personal data visible in the artifact.
2. **Restate the goal and user** the design serves, and where each came from.
3. **Describe before judging.** Layout, primary action, content, and states shown, plainly. Note what the artifact does not show, such as error and empty states.
4. **Evaluate across lenses:** goal fit, hierarchy and first read, interaction clarity, content and tone, consistency with the system, accessibility, and missing states.
5. **Write feedback items,** each naming an element. Classify each:
   - **Risk:** a likely usability or accessibility problem. Give the severity from `../_shared/standard.md` §8 (Blocker, Major, Minor, Cosmetic), the reason it matters tied to the goal, a principle, or evidence, and the confidence (High, Medium, Low).
   - **Preference:** a matter of taste or direction. Mark it as an opinion with no severity.
6. **Suggest, do not redesign.** Offer a concrete direction per item and the trade-off. Do not rewrite the design.
7. **Prioritize** by impact on the goal and relevance to the feedback wanted. Group related items. Recognize what works, briefly.
8. **Route systemic findings** onward. Write the output per §8.

## Outputs
Metadata block (§4), then path, date, collisions, and reruns (§8), follow `../_shared/standard.md`. File:
`design/audits/design-critique-<artifact>-<date>.md`:
```
> metadata block
## Goal, audience, and basis
## What the design shows
## What works
## Findings: usability and accessibility risks
## Observations: preference
## Missing states and edge cases
## Open questions / to validate
## Next step
```

Figma (optional, per `../_shared/figma.md`): when publishing is enabled, draw on the `Design Critiques` page the goal and basis, the What works list, one card per usability or accessibility finding ranked by impact (element, evidence, principle or criterion, severity, confidence, recommendation), the preference observations in a separate group marked as opinion, and the missing states. Never draw a screenshot or a finding, defect, or element that is not in the Markdown, and never show a preference as a usability risk. The Markdown file stays the source of truth.

`## Next step` names one handoff: `ux-audit` for systemic issues across the experience, `design-qa` once it is built, or `usability-test-planner` to test the riskiest assumptions with users.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] Chat replies follow `../_shared/personality.md`; no emoticons in written files or structured output
- [ ] Every item names a specific element
- [ ] Risks cite the goal, a named principle, or evidence; preferences are marked as opinions
- [ ] Severity appears only on risks and uses the shared scale; confidence is separate
- [ ] Items are ranked by impact; no count limit is applied
- [ ] Critique stays constructive and does not rewrite the design
- [ ] Unshown states are listed, not assumed to be fine
- [ ] Any Figma output followed `../_shared/figma.md`, and the reply reports only Figma results a tool confirmed

## Boundaries
- Does not sweep an entire experience against heuristics → `ux-audit`
- Does not compare a build to its spec → `design-qa`
- Does not benchmark competitors → `competitive-analysis`
- Does not plan tests → `usability-test-planner`
