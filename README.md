# mjc-design-wizard

Nineteen reusable [Claude Code](https://claude.com/claude-code) skills for product designers. Each skill is a structured workflow that Claude follows inside your project: it inspects what already exists, works only from evidence, and writes a Markdown artifact under `design/`.

No external AI API integrations: the toolkit never calls a model API itself, and the skills run inside your Claude Code session. Some skills can use tools that session already has, such as a browser to inspect a page you name or design-tool connectors. That use is optional and limited to targets you provide. Without those tools, supply screenshots or files instead. The repo is plain Markdown skills plus a standard-library Python validator.

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

Copy the whole `.claude/skills` folder, including `_shared/`. Every skill cites `../_shared/standard.md`, which holds the evidence tags, output rules, and quality standard.

### Option A: copy into a project

Run these from the folder that contains `your-project`. The clone lands next to it.

```bash
git clone https://github.com/samsadrashid/mjc-design-wizard.git
```

```bash
mkdir -p your-project/.claude/skills
```

```bash
cp -r mjc-design-wizard/.claude/skills/. your-project/.claude/skills/
```

Open Claude Code in `your-project`. Skills load automatically.

### Option B: install globally for all projects

Run these from the folder that contains the clone.

```bash
mkdir -p ~/.claude/skills
```

```bash
cp -r mjc-design-wizard/.claude/skills/. ~/.claude/skills/
```

A global install puts `_shared/` directly in `~/.claude/skills/`. If another skill pack also uses a `_shared/` folder there, one overwrites the other. In that case, use Option A so the skills and their `_shared/` folder stay inside the project.

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
- Ship: `feature-prioritization` → `mvp-planner` → `product-metrics`
- Review: `ux-audit`, `design-critique`, `design-system-audit`, `design-qa`
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
bash tests/run.sh
```

Runs the structural validator and its unit tests. It checks frontmatter, naming, required sections and order, boundary cross-references, README coverage, example contracts, and relative links. Standard library only, exits non-zero on failure. Run it after editing any skill or example.

These are structural checks. They do not measure output quality. Behavioral evaluation is manual and is described in [the shared standard](.claude/skills/_shared/standard.md) §8 and [tests/behavioral](tests/behavioral/README.md).

### Automated validation

GitHub Actions runs the same validator on every push to `main` and every pull request targeting `main` ([workflow](.github/workflows/validate.yml)). It uses Python 3.12, installs no dependencies, and has read-only token permissions. The job runs `bash tests/run.sh`, so a failing check fails the build. Run that command locally for the same result.

## Writing or editing a skill

Follow [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) (format, section order, boundary table) and [the shared standard](.claude/skills/_shared/standard.md) (evidence tags, output paths, quality standard). See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow, then run the validator.

## Limitations

- Skills guide reasoning; they do not fetch analytics, open design tools, or run tests by themselves. They use whatever Claude Code can read in the repo or what you paste in.
- Browser-based inspection (live audits, competitor pages) requires a Claude Code setup with browser access; otherwise provide screenshots.
- Quality of output tracks quality of evidence in the project. Each skill's Inputs table sets what happens when something is missing. In general, a skill stops and says what to supply when an essential input or evidence is missing, may ask one focused question when a less important input is missing, and otherwise proceeds with gaps labeled `[assumption]` instead of presenting them as fact. The exact rules differ by skill.
- Behavioral evaluation is limited. In the current run, 3 of 76 scenarios fail: PF-N1, RP-M1, and CS-E1 (see [tests/behavioral/RESULTS.md](tests/behavioral/RESULTS.md)). These are single-sample scenario results on a synthetic project, not a statistical estimate of reliability.

## License

MIT
