# Architecture and Quality Standards

Shared contract for every skill in `mjc-design-wizard`. Each `SKILL.md` follows it; the validation suite enforces the checkable parts.

## 1. Skill format

Claude Code project skills live at `.claude/skills/<skill-name>/SKILL.md`.

```yaml
---
name: <skill-name>          # matches directory, lowercase, hyphens, <=64 chars
description: <what + when>  # <=1024 chars, includes trigger phrases
---
```

Body sections, in this order, each a `## ` heading:

| Section | Content |
|---|---|
| Purpose | One paragraph. What the skill produces and why. |
| Triggers | Phrases and situations that should invoke it. |
| Inputs | What to gather first. Marks each as required or optional. |
| Workflow | Numbered steps. Step 1 is always "inspect the project". |
| Outputs | Files or chat deliverables, with paths and structure. |
| Quality checks | Checklist the skill must pass before finishing. |
| Boundaries | What it does not do, and which sibling skill owns that. |

Target length: 50 to 130 lines. Prefer tables and checklists over prose.

## 2. Evidence-first rule

Moved to `.claude/skills/_shared/standard.md` (section 2) so that installed skills carry it. Skills cite it from there.

## 3. Project awareness

Moved to `.claude/skills/_shared/standard.md` (section 3) so that installed skills carry it. Skills cite it from there.

## 4. Output locations

Moved to `.claude/skills/_shared/standard.md` (section 4) so that installed skills carry it. Skills cite it from there.

## 5. Skill boundaries (no overlap)

| Phase | Skill | Owns | Hands off to |
|---|---|---|---|
| Discover | product-discovery | Context, knowledge gaps, hypotheses, discovery plan (no research performed) | problem-framing, ux-research-planner, competitive-analysis |
| Discover | problem-framing | One bounded problem statement with evidence, assumptions, HMW, success definition | ux-research-planner, feature-prioritization, mvp-planner |
| Discover | competitive-analysis | Competitor comparison from inspected sources, with interpretation kept separate | product-discovery, design-critique |
| Research | ux-research-planner | Decision, research questions, method, participants, ethics, analysis plan | interview-guide-builder, usability-test-planner, persona-builder |
| Research | interview-guide-builder | Discussion guide, consent script, capture template for one study | persona-builder, journey-map-builder (synthesis) |
| Research | usability-test-planner | Task-based test protocol, accessibility, capture and analysis plan | ux-research-planner (recruiting or method unsettled), feature-prioritization (ranking fixes) |
| Research | persona-builder | Personas or provisional profiles from existing evidence, with unknowns listed | journey-map-builder, ux-research-planner (evidence gaps) |
| Model | journey-map-builder | End-to-end experience across touchpoints and time | user-flow-designer (stage detail), ux-research-planner (evidence gaps), feature-prioritization (opportunities) |
| Model | user-flow-designer | Screen and state-level flows for one task | design-documentation (approved flow), usability-test-planner (test paths), information-architect (navigation problems) |
| Model | information-architect | Navigation, taxonomy, content model, labels | ux-research-planner (validation), user-flow-designer (top-task flows), design-documentation (approved structure) |
| Evaluate | ux-audit | Heuristic and accessibility review of a live or designed product | design-qa (verify fixes), usability-test-planner (validate hypotheses), design-system-audit (shared-component patterns) |
| Evaluate | design-system-audit | Token, component, and pattern consistency | design-qa (verify fixes), design-documentation (component and usage docs) |
| Evaluate | design-qa | Build-vs-design defect log before or after release | design-documentation (spec gaps), design-system-audit (shared-component mismatches), ux-audit (usability issues) |
| Evaluate | design-critique | Structured feedback on a specific design proposal | ux-audit (systemic issues), design-qa (once built), usability-test-planner (test risky assumptions) |
| Measure | product-metrics | Metric trees, instrumentation specs, and reading existing data | problem-framing (undefined success), ux-research-planner (experiments, surveys), feature-prioritization (impact inputs) |
| Plan | mvp-planner | Scope cut, release slices, risks | problem-framing (unclear problem), feature-prioritization (candidates to rank), product-metrics (validation measures), user-flow-designer (core loop) |
| Plan | feature-prioritization | Scoring and ranking a given backlog | mvp-planner (scope top candidates), product-metrics (reach and impact data), ux-research-planner (verify low-confidence inputs) |
| Communicate | design-documentation | Specs and rationale for a shipped or in-progress design | design-qa (verify the build), case-study-writer (completed project) |
| Communicate | case-study-writer | Narrative of a finished project for portfolio or review | design-documentation (missing technical detail), product-metrics (outcome measurement) |

Rule: a skill never performs a sibling's job. It links to the sibling and stops.

The "Hands off to" column lists the next-step handoffs a skill's Outputs section must name. It is one-directional: two skills may point at each other when the condition differs.

## 6. Style

- Concise. Short sentences, tables, checklists. No filler or motivational prose.
- Missing information follows the shared standard (section 8): stop only when an essential input is absent, ask at most one question when the answer materially changes the output, otherwise proceed with labeled assumptions.
- Every output ends with `## Open questions / to validate` and `## Next step` (one line, may name a sibling skill).
- No external AI API integrations. Optional session tools (a browser, design-tool connectors) are used only on targets the user names or provides.

## 7. Quality checks (global)

Moved to `.claude/skills/_shared/standard.md` (section 7) so that installed skills carry it. Skills cite it from there.

## 8. Shared quality standard

Moved to `.claude/skills/_shared/standard.md` (section 8) so that installed skills carry it. Skills cite it from there.
