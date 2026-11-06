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
| Model | `user-flow-designer` | One complete flow plus a diagram per individual flow, a sourced transition inventory, gaps, and integrity check |
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

### Option A: install as a Claude Code plugin (recommended)

Inside Claude Code, run:

```text
/plugin marketplace add https://github.com/samsadrashid/mjc-design-wizard
```

```text
/plugin install mjc-design-wizard@mjc-design-wizard
```

Choose **project** scope to keep the skills inside one project, or **user** for every project. The plugin carries the skills and their `_shared/` folder together, so nothing collides with other skill packs. Plugin skills are namespaced, for example `/mjc-design-wizard:ux-audit`.

### Option B: copy into a project

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

### Option C: copy globally for all projects

Run these from the folder that contains the clone.

```bash
mkdir -p ~/.claude/skills
```

```bash
cp -r mjc-design-wizard/.claude/skills/. ~/.claude/skills/
```

A global install puts `_shared/` directly in `~/.claude/skills/`. If another skill pack also uses a `_shared/` folder there, one overwrites the other. In that case, use Option A or B so the skills and their `_shared/` folder stay together.

### Option D: use this repo as the workspace

Clone it, drop your design files or notes in, and run skills here.

Verify with `/ux-audit` or by asking "which skills are available".

### Update and uninstall

- **Plugin:** `/plugin marketplace update mjc-design-wizard` and then reinstall to update; `/plugin uninstall mjc-design-wizard@mjc-design-wizard` to remove.
- **Copied skills:** pull the repository again and repeat the copy command; it overwrites the 19 skill folders and `_shared/`. To remove, delete those 19 folders and `_shared/` from the `.claude/skills/` folder you copied into. Your `design/` outputs are never touched.

Changes between versions are listed in [CHANGELOG.md](CHANGELOG.md).

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

## Figma output (optional)

All 19 skills can also draw their result as editable objects in a Figma design file. Each draws on its own page (see the page map in `figma.md` §4). The Markdown file is always written and stays the source of truth. The rules live in [.claude/skills/_shared/figma.md](.claude/skills/_shared/figma.md).

**Setup**

1. Connect the Figma MCP server in Claude Code and sign in. To use a different Figma account, sign out and reconnect it with `/mcp`; the skills never switch accounts.
2. Create `design/figma.json` in your project and set `publishing.enabled` to `true`. Publishing is off by default, and a connected Figma account alone is not permission to write.
3. Optionally put an existing design file's URL in `file.url`. Without one, the adapter is instructed to create a project file and record its key; this path has not been tested live, so supplying an existing file is the tested route.

```json
{
  "schema_version": 1,
  "publishing": { "enabled": true, "confirm_each_run": true },
  "privacy": { "allow_quotes": false, "allow_participant_codes": true },
  "file": { "url": "https://www.figma.com/design/<file-key>/..." },
  "pages": {},
  "artifacts": {}
}
```

**What it does.** One file per project, an `Overview` page, and one page per skill created on first use (for example `UX Audit`, `User Flows`, `Design System Audit`). With `confirm_each_run` on (the default), each run asks before writing. Each result is one tagged frame. A rerun updates that frame in place by changing text and adding content only. If a hand edit changed a property the fingerprint tracks (text, size, position, fill), the rerun leaves the frame alone and adds a new version. Edits the fingerprint cannot see, such as corner radius, are not detected; they survive because in-place updates never restyle. Any update that would remove or restyle content is a replacement and needs your confirmation; without it, a new version is drawn and the old frame is kept. Nothing outside the integration's own frames is changed, and deleting anything needs confirmation. Flows are drawn as shapes with labels and arrow lines on the `User Flows` page. Design system audits are documentation only: they never create or change variables, styles, or components.

**Limitations.** Tested live only in a scratch file with synthetic data (see `figma.md` §9), not on real projects. Edits to properties the fingerprint does not track, such as corner radius or effects, are not detected; reruns therefore only change text and add content in place, and anything more asks before replacing. No images or screenshots are placed. Figma rate limits depend on your seat. Research skills draw plans, guides, and personas only: never study results, participant names, or quotes (quotes only if `privacy.allow_quotes` is `true`). Every skill draws only what its Markdown contains: no invented pages, emotions, defects, competitor capabilities, outcomes, screenshots, or numbers. Case studies never draw their author-only appendix sections. Publishing was live-tested on 8 of 19 skills and the disabled path on 7 (two of them not in the first group), so 10 skills have some live run; the other 9 are covered only by validator checks of their instructions. Manual-edit safety was live-tested on the pilot skills and `mvp-planner`, and two frames were reviewed visually (see `figma.md` §9).

**Troubleshooting.** When `design/figma.json` exists, the reply ends with a `Figma:` line; projects without it get no Figma line. `not used (publishing disabled)`: set `publishing.enabled`. `not used (design/figma.json unreadable)`: fix the JSON or `schema_version`. `not used (tools unavailable)` or `not used (no Figma account connected)`: connect the Figma MCP with `/mcp`. `not used (run not confirmed)`: confirm the run when asked. `not used (no design file)`: put a design file URL in `file.url`. File access errors: check that your account can edit the file. A failed run still writes the Markdown file.

## MJC Emotional Layer

MJC talks in chat with a calm, curious, design-obsessed voice and signs each completed reply with one text emoticon, such as `-_-`, `o_o`, `ಠ_ಠ`, or `^_^`, alone on the last line after a blank line (never pictographic emoji, and no other emoticon in the reply). Replies that are only JSON, code, or another strict format get no signature. The rules and the expression library live in one file, [.claude/skills/_shared/personality.md](.claude/skills/_shared/personality.md); each of the 19 skills cites it with one quality-check line instead of copying it. Expressions follow the moment the skill is in (gathering, analyzing, a finding, an error, verified completion) and never appear in written files, metadata, tables, JSON, or Figma text. Personality never changes a skill's steps, approval gates, or evidence rules, and `^_^` is used only after checks pass. Ask for no emoticons and MJC stops for the session; a future setting can switch the layer off in that one file. New skills adopt it by adding the same quality-check line.

## Validation

```bash
bash tests/run.sh
```

Runs the structural validator and its unit tests. It checks frontmatter, naming, required sections and order, boundary cross-references, README coverage, example contracts, and relative links. Standard library only, exits non-zero on failure. Run it after editing any skill or example.

These are structural checks. They do not measure output quality. Behavioral evaluation is manual and is described in [the shared standard](.claude/skills/_shared/standard.md) §8 and [tests/behavioral](tests/behavioral/README.md).

The behavioral results ([RESULTS.md](tests/behavioral/RESULTS.md), [FINDINGS.md](tests/behavioral/FINDINGS.md), [QUALITY.md](tests/behavioral/QUALITY.md)) summarize graded runs whose raw evidence (`tests/behavioral/runs/`) is kept on the maintainer's machine and is not published, so those summaries cannot be re-checked from this repository alone. Trigger phrases are checked statically by `tests/test_triggers.py`; that test reads the descriptions and does not run a model.

### Automated validation

GitHub Actions runs the same validator on every push to `main` and every pull request targeting `main` ([workflow](.github/workflows/validate.yml)). It uses Python 3.12, installs no dependencies, and has read-only token permissions. The job runs `bash tests/run.sh`, so a failing check fails the build. Run that command locally for the same result.

## Writing or editing a skill

Follow [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) (format, section order, boundary table) and [the shared standard](.claude/skills/_shared/standard.md) (evidence tags, output paths, quality standard). See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow, then run the validator.

## Limitations

- Skills guide reasoning; they do not fetch analytics, open design tools, or run tests by themselves. They use whatever Claude Code can read in the repo or what you paste in.
- Browser-based inspection (live audits, competitor pages) requires a Claude Code setup with browser access; otherwise provide screenshots.
- Quality of output tracks quality of evidence in the project. Each skill's Inputs table sets what happens when something is missing. In general, a skill stops and says what to supply when an essential input or evidence is missing, may ask one focused question when a less important input is missing, and otherwise proceeds with gaps labeled `[assumption]` instead of presenting them as fact. The exact rules differ by skill.
- Behavioral evaluation is limited. The latest attempts show 75 of 76 scenarios passing, but under a stricter rule (three attempts in a row) PF-N1, CS-E1, CS-N1, DS-X1 and UF-N1 are not yet reliable; see [tests/behavioral/FINDINGS.md](tests/behavioral/FINDINGS.md). Figma output is verified by read-back for only some skills (see [tests/behavioral/QUALITY.md](tests/behavioral/QUALITY.md)); the rest are covered by the validator alone.

## License

MIT
