---
name: information-architect
description: Define or audit navigation, hierarchy, labels, content groupings, and content relationships for a product or section, grounded in the content that exists and in user needs, with a plan to validate it. Use when the user says "information architecture", "site map", "navigation structure", "how should we organize", "labeling", "content model". Not for task-level flows (use `user-flow-designer`), running the card sort or tree test (use `ux-research-planner`), or visual and interaction audits (use `ux-audit`).
---

# Information Architect

## Purpose
Make a product's structure explicit: what content exists, how it is grouped and labeled, how people reach it, and how items relate. The skill keeps the audited current structure apart from the proposed one. It reports a problem only where evidence supports it, and it plans validation without claiming any was done.

## Triggers
- "Design the IA for X", "reorganize the navigation", "site map"
- People cannot find things (support data, test results, search logs)
- A new content type or section is being added

## Inputs
| Input | If missing | Source |
|---|---|---|
| Scope (whole product or one section) | Ask one: scope sets the inventory | user |
| Content inventory (routes, pages, data types, navigation config) | Stop: there is nothing to organize. Ask for a sitemap, routes, or a content list | repo, CMS schema, user |
| Top user tasks or needs | Assume up to 5 from evidence and tag them; recommend `ux-research-planner` | `design/research/`, tickets, search logs |
| Findability evidence (card sorts, tree tests, search terms, support) | Assume none exists | `design/research/`, user |
| Constraints (CMS limits, URLs and redirects, locales) | Assume none and flag URL impact | repo, user |

## Workflow
1. **Inspect the project.** Extract routes, navigation components, CMS or data schema, search configuration, and existing IA documents. Build the inventory table: item, type, location, how it is reached, and source. Note the date of each evidence source or `date unknown`. Copy no personal data from search logs or tickets. When tickets and interviews both appear, match ticket authors to interviewees by identity, internally and without printing the identifiers; count each person once and list the members beside every count.
2. **Audit the current structure** from the inventory only. Record depth, breadth, and organizing scheme per level. Report these only where the inventory or other evidence shows them:
   - orphaned: reachable by URL or code but not from navigation
   - duplicate: the same content in more than one place
   - ambiguous: labels that overlap or differ from user terms in the evidence
   - hard to find: deep or hidden, with a path count or supporting tickets
   Each finding cites its source, with confidence per §8. Where evidence is missing, list it as unverified.
3. **State top tasks and user vocabulary** with sources. Use the users' words from the evidence, not internal names.
4. **Propose a structure.** Choose an organizing scheme per level (task, audience, topic, or type) and say why. Three levels is a default maximum because deeper menus hide content. Justify exceptions. Show the tree as an indented list and mark each node new, moved, renamed, or unchanged.
5. **Decide labels.** Plain language, one meaning per label, alternatives rejected with a reason. Flag labels that are guesses and should be tested.
6. **Define the content model** for structured types: fields, relationships, required versus optional, reuse. Note URL and redirect impact when structure changes.
7. **Plan validation:** a card sort for grouping and labels, a tree test for findability, with the tasks to run. These are planned, not conducted. Hand the study design to `ux-research-planner`.
8. **Map every inventory item** to the proposed tree or to a removal, inside the proposed-structure section. Write the output per §8.

## Outputs
Metadata block (§4), then path, date, collisions, and reruns (§8), follow `../_shared/standard.md`. File:
`design/architecture/information-architect-<scope>-<date>.md`:
```
> metadata block
## Scope and evidence base
## Content inventory
## Current structure (audited)
## Findings on the current structure (evidence and confidence)
## Top tasks and user vocabulary
## Proposed structure (tree, change markers, inventory mapping)
## Labeling decisions
## Content model
## Validation plan (planned, not conducted)
## Open questions / to validate
## Next step
```

Figma (optional, per `../_shared/figma.md`): when publishing is enabled, draw on the `Information Architecture` page the current structure and the proposed structure as two separate trees of labeled shapes joined by arrow lines, parent above child, each proposed node carrying its change marker, plus the labeling decisions and the content model as tables. Mark anything not confirmed in the Markdown as proposed or `[assumption]`, and the validation plan as planned. Never draw pages, routes, labels, or links that are not in the Markdown. The Markdown file stays the source of truth.

`## Next step` names one handoff: `ux-research-planner` to run the validation, `user-flow-designer` to design flows for the top tasks, or `design-documentation` once the structure is approved.

## Quality checks
- [ ] Global checks in `../_shared/standard.md` §7 and §8
- [ ] Chat replies follow `../_shared/personality.md`; no emoticons in written files or structured output
- [ ] The current structure is derived from the inventory, and the proposal is clearly separate
- [ ] Every finding cites a source, and unsupported suspicions are listed as unverified
- [ ] Every inventory item appears in the proposed tree or is marked removed
- [ ] Labels use evidence vocabulary or are flagged for testing
- [ ] The validation plan says nothing was conducted
- [ ] Depth and breadth are stated, and exceptions are justified
- [ ] Any Figma output followed `../_shared/figma.md`, and the reply reports only Figma results a tool confirmed

## Boundaries
- Does not design task-level flows → `user-flow-designer`
- Does not design or run the card sort or tree test → `ux-research-planner`
- Does not review visual or interaction usability → `ux-audit`
- Does not document the approved structure in detail → `design-documentation`
