# Contributing

Thanks for improving mjc-design-wizard. The toolkit has a fixed scope of 19 skills. Improvements to those skills, examples, tests, and docs are welcome. Open an issue before proposing a new skill and show how it avoids overlapping the boundary table in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) §5.

## Ground rules

- **Evidence first.** Skills never fabricate research, analytics, test results, quotes, or outcomes. Follow the tags and standards in [the shared standard](.claude/skills/_shared/standard.md) (§2 and §8). Skills cite it as `../_shared/standard.md`, never `docs/`, because only `.claude/skills/` is installed.
- **Privacy.** Never commit real participant data, customer records, or credentials, including inside examples. Anonymize anything derived from research (§8, privacy).
- **No external AI API integrations.** Optional session tools such as a browser are fine; a skill must still work from supplied files and screenshots.
- **Stay concise.** Prefer tables and checklists. Do not repeat what the architecture doc already says; cite it.

## Modify a skill

1. Read the skill and its neighbors in the boundary table. Do not take over a sibling's job.
2. Edit `.claude/skills/<name>/SKILL.md`. Keep the frontmatter `name` equal to the directory and keep the seven sections in order.
3. If the skill's output sections change, update its example in `examples/`.
4. Run `bash tests/run.sh`.
5. Skills listed in `STANDARD_V1` in `tests/validate_skills.py` are checked against the §8 conventions: a `Not for` routing clause, an `If missing` column in Inputs, and §8 references. Add a skill to that set once it has been revised to match.

## Add or rename a skill

Only after agreement in an issue. Then update, in one change:

- the skill directory and `SKILL.md`
- the README skills table
- the boundary table in the architecture doc
- the `EXPECTED` set in `tests/validate_skills.py`

## Examples

- One file per skill in `examples/`, named after the skill, listed in `examples/README.md`.
- Open with an `Illustrative example` banner. All data is invented and labeled as sample data.
- The output block must use the skill's exact output headings, in order, and start with the `> skill:` metadata line.
- Use `<YYYY-MM-DD>` for dates. Do not write real dates.
- Numbers shown as observed must be derivable from sample data included in the example.

## Validation

```bash
bash tests/run.sh
```

CI runs the same command on pushes and pull requests to `main`. This is structural validation only. To claim a skill produces good output, run it in Claude Code on a realistic scenario, grade the result, and record the date and who ran it. Do not report a behavioral pass that was not executed.

## Pull request checklist

- [ ] `bash tests/run.sh` passes
- [ ] No overlap with sibling skills; handoffs named
- [ ] Examples updated and labeled illustrative
- [ ] No secrets, personal data, or invented evidence
- [ ] No unrelated files changed
