---
name: persona-builder
description: Synthesize personas or user segments strictly from existing research evidence in the project. Refuses to invent demographics or quotes. Use when the user says "build personas", "who are our users", "segment users", "proto-persona", or after interviews and surveys are synthesized.
---

# Persona Builder

## Purpose
Produce evidence-backed personas (or explicitly labeled proto-personas) that capture goals, behaviors, pains, and context. Each attribute cites its source. Where evidence is thin, the output is a proto-persona with an evidence gap list, not a polished fiction.

## Triggers
- "Create personas", "who are we designing for", "segment our users"
- Research synthesis exists in `design/research/` or user-provided notes
- Journey map or flow needs a defined actor

## Inputs
| Input | Required | Source |
|---|---|---|
| Research data (interview notes, survey results, support logs, analytics) | yes | `design/research/`, `research/`, user files |
| Product context | yes | repo inspection |
| Existing personas | optional | `design/research/` |
| Business segments | optional | user |

## Workflow
1. **Inspect the project.** Read all research material. Count sources (participants, tickets, records). If none, stop and offer proto-personas marked `[assumption]` throughout, and point to `ux-research-planner`.
2. **Extract attributes.** Table: attribute, evidence excerpt, source, count. Attributes: goals, tasks, pains, context, tools, decision triggers.
3. **Cluster** on behavior and goals, not demographics. 2 to 4 clusters. Record which sources fall in each.
4. **Write persona cards.** Name-free or role-named (e.g. "Weekend meal planner"). Fields: role, goal, key behaviors, pains, context, what they use today, design implications. Every field cites evidence or is tagged.
5. **State confidence** per persona: sources count, evidence strength (H/M/L).
6. **Anti-persona** (who this is not for) only if evidence supports it.
7. **Write output**; show cluster summary in chat.

## Outputs
`design/research/personas-<topic>-<date>.md`:
```
> metadata block (source counts)
## Evidence base
## Attribute extraction table
## Personas (or proto-personas) with confidence
## Anti-persona (optional)
## Evidence gaps
## Open questions / to validate
## Next step
```

## Quality checks
- [ ] Global checks in `docs/ARCHITECTURE.md` §7
- [ ] No invented names, ages, photos, quotes, or job titles
- [ ] Each persona attribute cites source or is tagged `[assumption]`
- [ ] Title says "Proto-persona" when evidence is below 5 sources per cluster
- [ ] Clusters based on behavior and goals, not demographics

## Boundaries
- Does not plan research → `ux-research-planner`
- Does not map journeys → `journey-map-builder`
- Does not frame the problem → `problem-framing`
