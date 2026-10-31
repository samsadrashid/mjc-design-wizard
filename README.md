# mjc-design-wizard

Nineteen reusable [Claude Code](https://claude.com/claude-code) skills for product designers. Each skill is a structured workflow that Claude follows inside your project: it inspects what already exists, works only from evidence, and writes a Markdown artifact under `design/`.

No external AI APIs. No network calls. Plain Markdown skills plus a stdlib Python validator.

## What is a skill

A skill is a `SKILL.md` file with YAML frontmatter that Claude Code loads on demand. When your request matches a skill's description, Claude follows its workflow. You can also invoke one directly with `/skill-name`.

```
.claude/skills/ux-audit/SKILL.md
```

## The 19 skills

| Phase | Skill | Produces |
|---|---|---|
| Discover | `product-discovery` | Opportunity brief, hypotheses, discovery plan |
| Discover | `problem-framing` | Problem statement, HMW questions, success definition |
| Discover | `competitive-analysis` | Comparison matrix from observed sources |
| Research | `ux-research-planner` | Research questions, method, participants, timeline |
| Research | `interview-guide-builder` | Timed discussion guide and note template |
| Research | `usability-test-planner` | Tasks, measures, script, results template |
| Research | `persona-builder` | Evidence-backed personas or labeled proto-personas |
| Model | `journey-map-builder` | Stage-by-stage journey map with moments of truth |
| Model | `user-flow-designer` | Mermaid flow plus screen state table |
| Model | `information-architect` | Content inventory, navigation tree, labels, content model |
| Evaluate | `ux-audit` | Heuristic and accessibility findings with severity |
| Evaluate | `design-system-audit` | Token, component, pattern inventory and drift |
| Evaluate | `design-qa` | Build-vs-design defect log with repro steps |
| Evaluate | `design-critique` | Ranked, element-specific feedback |
| Measure | `product-metrics` | Metric tree, instrumentation spec, baseline status |
| Plan | `mvp-planner` | Core loop, scope table, release slices |
| Plan | `feature-prioritization` | Scored ranking with sources and sensitivity |
| Communicate | `design-documentation` | Feature spec, component doc, or decision record |
| Communicate | `case-study-writer` | Evidence-backed project narrative |

Responsibilities do not overlap. Each skill's `Boundaries` section names the sibling that owns adjacent work. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) §5.

## Principles

1. **Evidence first.** Every claim is tagged `[observed]`, `[reported]`, `[inferred]`, or `[assumption]`. Skills never fabricate research, metrics, test results, quotes, or outcomes. Missing data is stated as missing.
2. **Project aware.** Step 1 of every workflow reads the repo and prior `design/` outputs before writing.
3. **Actionable.** Outputs are checklists, tables, and specs someone can act on, not essays.
4. **Token efficient.** Skills are 50 to 130 lines. Clarifying questions are capped at three.

## Installation

### Option A: copy into a project

```bash
git clone https://github.com/samsadrashid/mjc-design-wizard.git
```

```bash
cp -r mjc-design-wizard/.claude/skills/. your-project/.claude/skills/
```

Open Claude Code in `your-project`. Skills load automatically.

### Option B: install globally for all projects

```bash
cp -r mjc-design-wizard/.claude/skills/. ~/.claude/skills/
```

### Option C: use this repo as the workspace

Clone it, drop your design files or notes in, and run skills here.

Verify with `/ux-audit` or by asking "which skills are available".

## Usage

Describe what you need in natural language, or call a skill by name.

```
/product-discovery Should we add shared shopping lists to the grocery app?
```

```
Audit the checkout flow in staging for usability and accessibility issues.
```

Claude inspects the project, runs the workflow, writes to `design/<area>/`, and summarizes in chat. Every output ends with open questions and one next step, which often names the next skill to run.

Typical chains:

- New idea: `product-discovery` → `problem-framing` → `ux-research-planner` → `interview-guide-builder` → `persona-builder`
- Define a feature: `journey-map-builder` → `user-flow-designer` → `information-architect` → `design-documentation`
- Ship: `mvp-planner` → `feature-prioritization` → `product-metrics` → `design-qa`
- Review: `ux-audit`, `design-critique`, `design-system-audit`
- Tell the story: `case-study-writer`

Worked examples live in [examples/](examples/).

## Output layout

```
design/
  discovery/   research/   journeys/   architecture/
  audits/      metrics/    planning/   docs/
```

Filenames: `<skill>-<topic>-<YYYY-MM-DD>.md`. Each file opens with a metadata line naming the skill, date, scope, and sources.

## Validation

```bash
python3 tests/validate_skills.py
```

Checks frontmatter, naming, required sections and order, evidence rules, boundary cross-references, and README coverage. Stdlib only, exits non-zero on failure. Run it after editing any skill.

### Automated validation

GitHub Actions runs the same validator on every push to `main` and every pull request targeting `main` ([workflow](.github/workflows/validate.yml)). It uses Python 3.12, installs no dependencies, and has read-only token permissions. The job runs `bash tests/run.sh`, so a failing check fails the build. Run that command locally for the same result.

## Writing or editing a skill

Follow [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): format, section order, evidence tags, output paths, boundary table, global quality checks. Then run the validator.

## Limitations

- Skills guide reasoning; they do not fetch analytics, open design tools, or run tests by themselves. They use whatever Claude Code can read in the repo or what you paste in.
- Browser-based inspection (live audits, competitor pages) requires a Claude Code setup with browser access; otherwise provide screenshots.
- Quality of output tracks quality of evidence in the project. With no research, skills produce proto-artifacts labeled `[assumption]` rather than refusing.

## License

MIT
