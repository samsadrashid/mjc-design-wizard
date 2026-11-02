---
name: persona-builder
description: Synthesize user research already in the project into behavioral patterns and personas, or provisional profiles when evidence is thin, listing what remains unknown. Never invents demographics or quotes. Use when the user says "build personas", "who are our users", "segment users", "proto-persona", or after interviews and surveys are synthesized. Not for planning research (use `ux-research-planner`), mapping end-to-end experiences (use `journey-map-builder`), or framing the problem (use `problem-framing`).
---

# Persona Builder

## Purpose
Turn existing research evidence into useful behavioral patterns. Patterns backed by several independent sources become personas. Patterns with thin support become provisional profiles with their gaps stated. Details are never added only to make a persona feel complete.

## Triggers
- "Create personas", "who are we designing for", "segment our users"
- Research notes, survey results, or tickets exist in the project
- A journey map or flow needs a defined actor

## Inputs
| Input | If missing | Source |
|---|---|---|
| Research data (interview notes, surveys, tickets, analytics) | Stop: personas need evidence. Offer a hypothesis profile labeled `[assumption]` only if the user asks, and point to `ux-research-planner` | `design/research/`, `research/`, user files |
| Product context | Assume from the repo | repo |
| Existing personas | Assume none | `design/research/` |
| Business segments | Assume none; do not map to them unprompted | user |

## Workflow
1. **Inspect the project.** Read all research material. Count sources by type (participants, tickets, records) and record each source's date or `date unknown`. Replace names and identifiers with codes (P1, T1) from the first pass, per §8 privacy.
2. **Count independent people, not documents.** Match ticket authors to interviewees by identity, internally and without printing the identifiers, and count each person once. Extract attributes into a table: attribute (goal, task, pain, context, tool, trigger), evidence excerpt as a paraphrase or minimal quote, source code, and how many independent sources support it.
3. **Cluster on behavior and goals**, not demographics. Usually 2 to 4 clusters. Record which sources fall in each. Do not infer age, gender, ethnicity, health, or similar attributes.
4. **Apply the sufficiency gate.** A cluster becomes a persona only if its core pattern recurs across at least 3 independent sources. That number is a default that guards against single-story personas. It is not a statistical rule, and the user may set another. Anything below it is a provisional profile.
5. **Write each profile.** Role or behavior-based label, goal, key behaviors, pains, context, tools used today, and design implications. Each field cites sources and carries confidence (High, Medium, Low per §8), or is tagged `[assumption]`. Omit any field with no evidence.
6. **State what remains unknown** and the evidence that would resolve it. List only gaps in the product evidence. Never describe a gap in a way that reveals a withheld personal detail or its category. This list is required even for strong personas.
7. **Add an anti-persona** only if the evidence supports one.
8. **Write the output** per §8 and show the cluster summary in chat.

## Outputs
Metadata block (§4), then path, date, collisions, and reruns (§8), follow `../_shared/standard.md`. File:
`design/research/personas-<topic>-<date>.md`:
```
> metadata block (source counts and dates)
## Evidence base (sources, counts, dates)
## Attribute extraction table
## Patterns and personas (provisional profiles marked)
## What remains unknown
## Anti-persona (optional)
## Open questions / to validate
## Next step
```

Figma (optional, per `../_shared/figma.md`): when publishing is enabled, draw on the `Personas` page one card per persona and per provisional profile (marked provisional), each with goals, behaviors, pains, and design implications plus their sources and confidence, and the What remains unknown list. Use behavior-based labels and participant codes only; never add names, photos, ages, or quotes that are not in the Markdown. The Markdown file stays the source of truth.

`## Next step` names `journey-map-builder` to place the actor in an experience, or `ux-research-planner` when provisional profiles need more evidence.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] Chat replies follow `../_shared/personality.md`; no emoticons in written files or structured output
- [ ] No invented names, ages, photos, job titles, or quotes
- [ ] No personal identifiers from sources appear in the output
- [ ] Withheld sensitive details are not restated when explaining the omission
- [ ] Every field cites sources or is tagged `[assumption]`; empty fields are omitted
- [ ] Profiles below the sufficiency gate are labeled provisional
- [ ] Clusters rest on behavior and goals, not demographics
- [ ] "What remains unknown" is present
- [ ] Any Figma output followed `../_shared/figma.md`, and the reply reports only Figma results a tool confirmed

## Boundaries
- Does not plan or run research → `ux-research-planner`
- Does not map end-to-end journeys → `journey-map-builder`
- Does not frame the problem → `problem-framing`
