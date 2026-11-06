# Shared standard

Installed with the skills. Every skill cites this file as `../_shared/standard.md`, so it must be copied next to them. Section numbers (1, 2, 3, 4, 7, 8) are stable and are referenced by the skills.

## 1. Shared files to load

Read these from this folder before you work, in addition to this file:

- `personality.md`: always. Every skill that writes a chat reply ends it with the closing signature in its §5.
- `figma.md`: only when `design/figma.json` exists or the user asks for Figma output. It decides whether anything is drawn and sets the `Figma:` reporting line. When neither holds, do not load it.

- `check_evidence.py`: run it before saving any deliverable when the project has support tickets or interview notes, from the project root: `python3 .claude/skills/_shared/check_evidence.py <deliverable> --reply <draft reply>`, with the full text of the draft chat reply (never a placeholder) saved outside the project, for example under `/tmp`. Fix every problem it reports and run it again; mention in the reply only that it passed or what it could not check. It checks quotes credited to a source, `N people — IDs` count lines, and the one-question rule; it does not judge whether a claim is right.

Skills cite these files and do not repeat their rules.

## 2. Evidence-first rule

No skill invents data. Every claim in an output carries a tag:

| Tag | Meaning |
|---|---|
| `[observed]` | Seen directly in repo, files, screenshots, or user-provided material. Cite the path or source. |
| `[reported]` | Stated by the user or a stakeholder. Name who said it. |
| `[inferred]` | Reasoned from observed or reported facts. State the reasoning. |
| `[assumption]` | Not yet validated. Must appear in an "Open questions / to validate" list. |

Forbidden: fabricated user quotes, personas, analytics, conversion rates, test results, NPS, revenue, dates, or competitor facts. When data is missing, the output says `No data available` and proposes how to obtain it.

### Claim-level evidence

Applies to every skill that states findings, counts, reasons, or causes.

1. **Split first.** A sentence with several factual or causal clauses is several claims ("they could not find the code, which caused missed pickups" is two). Class and source each clause on its own.
2. **Ledger row.** Each claim that matters has: the claim, its source reference, the exact words that support it, its class, and a limit where one applies.
3. **Four classes.** `[observed]` (the cited source states it in so many words), `[reported]` (a named person or stakeholder states it), `[inferred]` (your reading, with the reasoning), unknown (no available source settles it; say so). A claim never becomes observed because it sounds reasonable.
4. **A source supports only what it states.** A source for a problem is not a source for its consequence. A source for an outcome is not a source for its cause. A shipped change is not a reason for the change. A reason for doing the work is observed only when an artifact records that reason. A source naming the subject, or one part of a claim, supports that part; the rest is `[inferred]` or unknown.
5. **Four kinds of ID stay apart.** A participant (a person), an interview (P1), a ticket (T-01), and a file path are different things. Name the source that states the claim, with its kind. If the person is the same across sources, say so beside the claim (`T-01, same person as P1`); do not list one source's ID for a statement another source makes.
6. **No forced content.** A template slot for a consequence, cause, motivation, impact, or number stays empty (write unknown) when no source supports it; drop the clause instead of filling it.
7. **Counts cover the whole source.** Compute a count over every row or file it ranges over (open the full table, not its first lines). If you read only part, say which part and write the figure as "at least N".
8. **One account per fact.** The same evidence carries the same class and the same IDs in the narrative, tables, and appendices.
9. **Use the source's words, one source per line.** Describe a claim with the words the source uses ("hard to see" is not "cannot see"; "found it after scrolling" is not "could not find it"). Give each source ID its own line; never lump several people or sources under one class. Context you supply (who the users are, where they act, what screen) is `[observed]` only if a cited source states it; otherwise `[inferred]` or dropped. A person counted in the strict group appears in no weaker group, list, ledger row, or example, through any of their sources; an exclusion note ("P1, also T-01, is already counted") is fine. A source that supports a finding is never also listed as counter-evidence to it.

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

Filename: use the pattern in the skill's Outputs section. If a skill gives none, use `<skill>-<topic>-<YYYY-MM-DD>.md`. Each file starts with a metadata block:

```markdown
> skill: <name> · date: <date> · scope: <what was examined> · sources: <paths or "none">
```

## 7. Quality checks (global)

Every skill's final checklist includes these, plus its own:

- [ ] Project inspected; sources listed in metadata block.
- [ ] Every claim tagged `[observed]`, `[reported]`, `[inferred]`, or `[assumption]`.
- [ ] No fabricated research, metrics, results, or quotes.
- [ ] Output written to the §4 path, or shown in chat if the user asked for chat only.
- [ ] Ends with open questions and one next step. Headings match the template exactly, and `## Next step` names one skill.
- [ ] Every derived count lists what was counted or the command used.
- [ ] `check_evidence.py` (§1) reported no problems, when the project has tickets or interview notes.
- [ ] Omission notes name no detail or category of what was withheld.
- [ ] Missing information handled per §8 (stop, one question, or labeled assumption).
- [ ] No personal identifiers copied from research inputs (§8 privacy).
- [ ] Date from a reliable source or left as `<YYYY-MM-DD>`; no existing file overwritten (§8).

## 8. Shared quality standard

Applies to every skill where relevant. It does not impose one workflow; each skill keeps its own purpose. Where a skill's text and this section disagree, this section wins.

### Activation and routing

- A description states what the skill produces and when to use it, with `Use when` triggers.
- Where a sibling could be confused for it, the description adds a `Not for X (use sibling)` clause.
- Output headings are a contract. Never add, rename, shorten, or reorder them. If the user asks for something the template has no section for, put it under the nearest existing heading and say so there. Answer a direct question from the user in the first section.
- `## Next step` is one sentence that names one skill and why. No sequences ("then"), no alternatives, and no pointing back to the skill that ran just before. A stop or hand-back reply in chat follows the same rule: one skill, never "rerun", "come back to this skill", or "or". A job you decline because it belongs to another skill goes on its own line outside Next step: "Not done here: <job>, which belongs to `<skill>`."
- If a request spans skills, run the one that matches the primary deliverable, then name the next skill in `## Next step`. Never do a sibling's job inline.

### Missing information

| Situation | Action |
|---|---|
| An essential input is absent and the deliverable cannot be produced without it | Stop. Say what is missing, how to supply it, and which skill can create it. If no skill can create it (only the user can supply it, such as application code or a build), name no skill and write "Next step: supply <the input>." Do no part of the deliverable. |
| A non-essential input is absent and the answer would materially change the output | Ask one question. State the default you will use if it goes unanswered. |
| Anything else | Proceed. Tag the gap `[assumption]` and list it under `## Open questions / to validate`. |

Never fill a gap with invented data. Write `No data available` and how to obtain it.

The chat reply asks the person at most one question in total, and that question is the one "Ask one question" row allows, not a list of the file's open questions. Every other gap is stated in the reply as a sentence (what is unknown and the default used) and kept in `## Open questions / to validate` in the file. A reply that has no question to ask does not invent one. One question is one request for one piece of information in one sentence. Two requests joined by "and", "also", or a list, or a sentence with two question marks, are two questions. Pick the one whose answer changes the output most.

### Severity scale

For evaluative skills (audits, QA, usability findings). Severity measures impact on the user's task, not fix effort or taste.

| Level | Meaning |
|---|---|
| Blocker | Prevents a core task, or causes data loss, harm, or a legal or accessibility failure, with no workaround |
| Major | Task completes only with significant difficulty, error, or a workaround |
| Minor | Noticeable friction; task completes easily |
| Cosmetic | No effect on the task; polish or consistency |

Priority labels (for example must-fix, should-fix, consider) rank work and must not be presented as severity.

### Confidence scale

Separate from severity. It rates how well the evidence supports a claim.

| Level | Meaning |
|---|---|
| High | Directly observed, or several independent sources agree |
| Medium | One solid source, or a consistent inference from several weak ones |
| Low | One weak source, or an assumption |

Scoring frameworks that need a number may map High, Medium, Low to 100%, 80%, 50% as a default. State the mapping in the output.

### Evidence and traceability

Tags from §2 apply everywhere. The form of traceability depends on the deliverable:

| Deliverable | Required traceability |
|---|---|
| Findings tables (audit, QA, critique) | Evidence column with source path or screen, plus a tag |
| Matrices (competitive, journey, scoring) | Source and tag per cell, or `Not observed` |
| Narrative (case study, framing) | Inline tag on each factual claim |
| Plans and specs | Sources in the metadata block; unvalidated items in open questions |

Derived numbers (counts, sums, ratios, percentages) must be computed with a command or by listing the items counted. Never write a tally from memory, including a summary of earlier research: list each counted member beside the count (for example P1, T-01). Attribute a detail only to the source that contains it. Compute the age of evidence from its dates with a command; for a date range give the age of each end, and copy each age from the command output. Place evidence before or after a release only if a source dates that release; otherwise say the order is unknown. Quotation marks surround only words a source contains verbatim. Before writing, copy each passage you will quote from its source; write a source quote as `"exact words" (ID)`, never join, shorten, or reword quoted words, and never put a label or summary of your own in quotation marks. A count tagged `[observed]` names the sources counted. An item that does not state a cause is not evidence for that cause; at most it supports an `[inferred]` link. Count only items that state the category. Label every count with its exact category and list its members. A count labelled "could not find" holds only statements that themselves say the person cannot or could not find or see it; "looking for", "hard to see", or "where is" are weaker statements, not members of that count. A count labelled "had trouble with the code" may add weaker statements (found it only after scrolling, lost it), each listed as such. Count each person once across interviews and tickets: match ticket authors to interviewees by identity, internally and without printing the identifiers, and list the members beside every count. Write each person count on its own line in the form `<label>: N people — ID, ID` with only source IDs after the dash, so N equals the distinct people listed; a weaker-statements line lists only people not already in the strict count. When items are grouped into themes, put each item's ID and its own words beside the theme, for example `T-05 "Arrived and the point was closed"`, and file an item only under a theme its own words state. Name a channel, tool, or decision status (push, email, rejected, approved, shipped) only as a source names it.

### Thresholds and defaults

Numeric limits in skills (participants per segment, items per critique, metrics per tree) are defaults that keep outputs focused. Each skill states them as defaults with a one-line reason. Apply a user or project override and record it in the metadata block. Never present a default as research-backed unless a source is cited.

### Privacy and anonymization

Research inputs (interview notes, tickets, recordings, survey text) may contain personal data.

- Do not copy names, emails, phone numbers, account IDs, or other identifiers into outputs. Use participant codes (P1, P2) or roles.
- Quote minimally and strip identifying details. Mark paraphrase as paraphrase.
- Do not record sensitive categories (health, finances, beliefs, and similar) beyond what the research question requires. Flag them instead.
- Do not infer protected attributes such as age, gender, or ethnicity for personas or segments. Refer to participants by code or as "they". Never infer gender from a name, never restate an age or an age descriptor (such as "older" or "retired"), including in a segment hypothesis or an `[assumption]`, and never write a first name, even to explain that a ticket and an interview come from the same person: use codes.
- When you explain an omission, name nothing about what was left out: not the detail, not its category (for example health or family), and not whom it concerned. Do not state, in any section including bias, ethics, and sensitivity checks, that the sources contain a sensitive category; generic guidance not tied to the sources is fine. Collect accessibility or health needs only as far as the task requires, say sharing is optional, and cover it in the consent text. Say only "Some personal details in the sources were left out for privacy." This applies to the chat reply as well as the file. Wrong: "Stairs difficulty was left out for privacy." A product-relevant fact may appear as a finding under a participant code; the sensitive reason behind it stays out and is not announced. When you decline a request that contains names or identifiers, do not repeat them; say "the names you listed".
- `design/` may be committed or published. When outputs derive from personal data, say so and note whether `design/` is gitignored.

### Date handling

Use the current date from a reliable source: a date provided in the session context, or the shell `date` command when available. If none is available, leave `<YYYY-MM-DD>` in the metadata block and filename and say so. Never guess a date. Dates of evidence come from the source itself, or are `date unknown`.

### Output paths and reruns

- Write only under `design/<area>/` as §4, unless the user names another path.
- List the target directory first. Never overwrite a file that lacks a `> skill:` metadata line, since the toolkit did not create it.
- Topic slugs are lowercase, hyphenated, and at most 40 characters.
- Rerun on the same skill and topic: update the existing toolkit file in place if the user asked to revise it. Otherwise write a new file with a numeric suffix (`-2`) and never overwrite silently.
- A later-dated rerun writes a new file and adds `supersedes: <path>` to the metadata block.

### Validation tiers

| Tier | What it proves | How |
|---|---|---|
| Structural (automated) | Files, frontmatter, section order, cross-references, example contracts, links | `bash tests/run.sh` |
| Behavioral (manual) | Output quality on a realistic scenario | Run the skill in Claude Code, grade against a rubric, record the date and the person who ran it |

The structural tier says nothing about output quality. A skill's behavior is unverified until a behavioral run is recorded.
