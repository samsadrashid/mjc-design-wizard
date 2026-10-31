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

Target length: 60 to 130 lines. Prefer tables and checklists over prose.

## 2. Evidence-first rule

No skill invents data. Every claim in an output carries a tag:

| Tag | Meaning |
|---|---|
| `[observed]` | Seen directly in repo, files, screenshots, or user-provided material. Cite the path or source. |
| `[reported]` | Stated by the user or a stakeholder. Name who said it. |
| `[inferred]` | Reasoned from observed or reported facts. State the reasoning. |
| `[assumption]` | Not yet validated. Must appear in an "Open questions / to validate" list. |

Forbidden: fabricated user quotes, personas, analytics, conversion rates, test results, NPS, revenue, dates, or competitor facts. When data is missing, the output says `No data available` and proposes how to obtain it.

## 3. Project awareness

Step 1 of every workflow inspects the project before writing:

1. Read `README*`, `docs/`, `design/`, `research/`, `CHANGELOG*`, and any file the user names.
2. Look for prior outputs from this toolkit under `design/` (see §4) and build on them instead of restarting.
3. Identify product type, platform, users, and constraints from what exists. Record gaps as `[assumption]`.
4. Never modify source code, `raw/`, or `.obsidian/` directories. Skills write only under `design/` unless the user names another path.

## 4. Output locations

All artifacts are Markdown under `design/` in the project root:

```
design/
  discovery/         product-discovery, problem-framing, competitive-analysis
  research/          ux-research-planner, interview-guide-builder, usability-test-planner, persona-builder
  journeys/          journey-map-builder, user-flow-designer
  architecture/      information-architect
  audits/            ux-audit, design-system-audit, design-qa, design-critique
  metrics/           product-metrics
  planning/          mvp-planner, feature-prioritization
  docs/              design-documentation, case-study-writer
```

Filename: `<skill>-<topic>-<YYYY-MM-DD>.md`. Each file starts with a metadata block:

```markdown
> skill: <name> · date: <date> · scope: <what was examined> · sources: <paths or "none">
```

## 5. Skill boundaries (no overlap)

| Phase | Skill | Owns | Hands off to |
|---|---|---|---|
| Discover | product-discovery | Opportunity framing, hypotheses, discovery plan | problem-framing, ux-research-planner |
| Discover | problem-framing | One sharp problem statement, HMW, success definition | mvp-planner, feature-prioritization |
| Discover | competitive-analysis | Competitor feature and UX comparison from observed sources | product-discovery, design-critique |
| Research | ux-research-planner | Research questions, method selection, recruiting, schedule | interview-guide-builder, usability-test-planner |
| Research | interview-guide-builder | Discussion guide for one study | ux-research-planner (method choice) |
| Research | usability-test-planner | Task-based test protocol and scoring | design-qa (defect logging) |
| Research | persona-builder | Personas and segments from existing evidence only | journey-map-builder |
| Model | journey-map-builder | End-to-end experience across touchpoints and time | user-flow-designer (screen-level) |
| Model | user-flow-designer | Screen and state-level flows for one task | information-architect |
| Model | information-architect | Navigation, taxonomy, content model, labels | user-flow-designer |
| Evaluate | ux-audit | Heuristic and accessibility review of a live or designed product | design-qa, design-critique |
| Evaluate | design-system-audit | Token, component, and pattern consistency | design-qa |
| Evaluate | design-qa | Build-vs-design defect log before or after release | ux-audit |
| Evaluate | design-critique | Structured feedback on a specific design proposal | ux-audit (systemic issues) |
| Measure | product-metrics | Metric trees, instrumentation specs, and reading existing data | problem-framing |
| Plan | mvp-planner | Scope cut, release slices, risks | feature-prioritization |
| Plan | feature-prioritization | Scoring and ranking a given backlog | mvp-planner |
| Communicate | design-documentation | Specs and rationale for a shipped or in-progress design | case-study-writer |
| Communicate | case-study-writer | Narrative of a finished project for portfolio or review | design-documentation |

Rule: a skill never performs a sibling's job. It links to the sibling and stops.

## 6. Style

- Concise. Short sentences, tables, checklists. No filler or motivational prose.
- Ask at most three clarifying questions, and only when an answer changes the output. Otherwise proceed and list assumptions.
- Every output ends with `## Open questions / to validate` and `## Next step` (one line, may name a sibling skill).
- No external AI APIs, no network calls beyond what the user asks for.

## 7. Quality checks (global)

Every skill's final checklist includes these, plus its own:

- [ ] Project inspected; sources listed in metadata block.
- [ ] Every claim tagged `[observed]`, `[reported]`, `[inferred]`, or `[assumption]`.
- [ ] No fabricated research, metrics, results, or quotes.
- [ ] Output written to the §4 path, or shown in chat if the user asked for chat only.
- [ ] Ends with open questions and one next step.
