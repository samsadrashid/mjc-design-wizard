---
name: information-architect
description: Define navigation structure, content taxonomy, labeling, and content model for a product or section, grounded in existing content inventory and research. Use when the user says "information architecture", "site map", "navigation structure", "how should we organize", "labeling", "content model".
---

# Information Architect

## Purpose
Produce a navigation and content structure that matches how users think, with labels tested against evidence where available. Starts from a content inventory, not a blank slate.

## Triggers
- "Design the IA for X", "reorganize the navigation", "site map"
- Users can't find things (support data, test results)
- New content type or section is being added

## Inputs
| Input | Required | Source |
|---|---|---|
| Scope (whole product or section) | yes | user |
| Content inventory (routes, pages, data types) | yes | repo (routes, CMS schema, nav code), user |
| Findability evidence (card sorts, tree tests, search logs, support) | optional | `design/research/`, user |
| Personas or top tasks | optional | `design/research/` |

## Workflow
1. **Inspect the project.** Extract routes, navigation config, content types, and existing IA docs. Build the inventory table: item, type, current location, owner.
2. **List top tasks** from evidence. If none, mark `[assumption]` and limit to 5.
3. **Audit current structure**: depth, breadth, orphan pages, duplicate labels, mixed organizing schemes.
4. **Propose structure.** Organizing scheme per level (task, audience, topic, type). Max depth 3 unless justified. Tree as indented list.
5. **Label each node**: plain language, user vocabulary from evidence, no internal jargon. Note alternatives rejected.
6. **Content model** for structured types: fields, relationships, required vs optional.
7. **Validation plan**: tree test or card sort tasks to run before build (link to `ux-research-planner`).
8. **Write output**; show the proposed tree in chat.

## Outputs
`design/architecture/ia-<scope>-<date>.md`:
```
> metadata block
## Content inventory
## Top tasks
## Current structure audit
## Proposed structure (tree)
## Labeling decisions
## Content model
## Validation plan
## Open questions / to validate
## Next step
```

## Quality checks
- [ ] Global checks in `docs/ARCHITECTURE.md` §7
- [ ] Inventory derived from repo or provided files, not guessed
- [ ] Every inventory item appears in proposed tree or is marked removed
- [ ] Labels use evidence vocabulary or are flagged for testing
- [ ] Depth and breadth stated; exceptions justified

## Boundaries
- Does not design task flows → `user-flow-designer`
- Does not run the tree test → `ux-research-planner`
- Does not audit visual consistency → `design-system-audit`
