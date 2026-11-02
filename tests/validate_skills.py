"""Structural validator for the mjc-design-wizard skills, docs, and examples.

Run from repo root: python3 tests/validate_skills.py
Exit 0 when every check passes, 1 otherwise. Standard library only.

These checks prove structure and conventions. They say nothing about the
quality of a skill's output; see .claude/skills/_shared/standard.md section 8.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable, Optional

DEFAULT_ROOT = Path(__file__).resolve().parent.parent

EXPECTED = {
    "product-discovery", "ux-audit", "design-system-audit", "design-qa",
    "product-metrics", "information-architect", "journey-map-builder",
    "usability-test-planner", "interview-guide-builder", "ux-research-planner",
    "persona-builder", "user-flow-designer", "design-critique",
    "competitive-analysis", "problem-framing", "mvp-planner",
    "feature-prioritization", "design-documentation", "case-study-writer",
}
SECTIONS = ["Purpose", "Triggers", "Inputs", "Workflow", "Outputs",
            "Quality checks", "Boundaries"]
# Skills held to the section 8 conventions. All 19 are revised; a new skill joins here once it is.
STANDARD_V1 = set(EXPECTED)
# Evaluative skills that must use the section 8 severity scale.
SEVERITY_SKILLS = {"ux-audit", "design-critique", "design-qa", "design-system-audit"}
SEVERITY_LEVELS = ("Blocker", "Major", "Minor", "Cosmetic")
# Fixed output contract for design-documentation (normalized headings, in order).
DOC_CONTRACT = [
    "purpose and status", "context", "scope and out of scope",
    "flows and expected behavior", "components, variants, and props",
    "tokens and references", "states", "accessibility and responsive requirements",
    "implementation notes and sources", "decisions, assumptions, and dependencies",
    "handoff checklist", "open questions / to validate", "next step",
]
CLOSING_HEADINGS = ["open questions / to validate", "next step"]
MISSING_ACTIONS = ("Stop", "Ask one", "Assume")
STANDARD_HEADINGS = [
    "Activation and routing", "Missing information", "Severity scale",
    "Confidence scale", "Evidence and traceability", "Thresholds and defaults",
    "Privacy and anonymization", "Date handling", "Output paths and reruns",
    "Validation tiers",
]
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
DATE_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
OUTPUT_PATH_RE = re.compile(r"`(design/[^`]+)`")
DATE_PLACEHOLDER = "<YYYY-MM-DD>"


class Report:
    """Collects PASS/FAIL results, optionally echoing each one."""

    def __init__(self, echo: bool = True) -> None:
        self.results: list[tuple[bool, str]] = []
        self.echo = echo

    def check(self, ok: bool, label: str) -> None:
        self.results.append((ok, label))
        if self.echo:
            print(f"{'PASS' if ok else 'FAIL'}  {label}")

    @property
    def failed(self) -> list[str]:
        return [label for ok, label in self.results if not ok]


def parse(text: str) -> tuple[Optional[dict[str, str]], list[str]]:
    """Split simple `key: value` frontmatter from the body."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, lines
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None, lines
    meta: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return meta, lines[end + 1:]


def outside_fences(lines: Iterable[str]) -> Iterable[str]:
    fenced = False
    for line in lines:
        if line.startswith("```"):
            fenced = not fenced
        elif not fenced:
            yield line


def headings(body: list[str]) -> list[str]:
    """Top-level '## ' headings outside code fences."""
    return [l[3:].strip() for l in outside_fences(body) if l.startswith("## ")]


def section(body: list[str], name: str) -> list[str]:
    out: list[str] = []
    active = fenced = False
    for line in body:
        if line.startswith("```"):
            fenced = not fenced
        if not fenced and line.startswith("## "):
            active = line[3:].strip() == name
            continue
        if active:
            out.append(line)
    return out


def norm_heading(text: str) -> str:
    """Lowercase, drop a trailing parenthetical, collapse whitespace."""
    text = re.sub(r"\s*\(.*\)\s*$", "", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def skill_contract(body: list[str]) -> tuple[Optional[str], list[str]]:
    """Return (output path prefix, normalized template headings) for a skill."""
    out = section(body, "Outputs")
    match = OUTPUT_PATH_RE.search("\n".join(out))
    prefix = match.group(1).split("<")[0] if match else None
    heads = [norm_heading(l[3:]) for l in out if l.startswith("## ")]
    return prefix, heads


def architecture_handoffs(arch_text: str) -> dict[str, list[str]]:
    """Map each skill in the section 5 table to the skills it hands off to."""
    out: dict[str, list[str]] = {}
    for line in arch_text.split("\n"):
        m = re.match(r"^\| \w+ \| ([a-z0-9-]+) \| .*? \| (.*) \|$", line)
        if m and m.group(1) in EXPECTED:
            targets = re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)+", m.group(2))
            out[m.group(1)] = [x for x in targets if x in EXPECTED]
    return out


def validate_skill(d: Path, report: Report, handoffs: dict[str, list[str]]) -> None:
    p = d / "SKILL.md"
    tag = d.name
    if not p.is_file():
        report.check(False, f"{tag}: SKILL.md exists")
        return
    text = p.read_text(encoding="utf-8")
    meta, body = parse(text)
    report.check(meta is not None, f"{tag}: frontmatter present")
    meta = meta or {}
    report.check("name" in meta and "description" in meta, f"{tag}: has name and description")
    name = meta.get("name", "")
    report.check(name == d.name, f"{tag}: name matches directory")
    report.check(bool(NAME_RE.match(name)) and len(name) <= 64, f"{tag}: name format")
    desc = meta.get("description", "")
    report.check(0 < len(desc) <= 1024, f"{tag}: description length")
    report.check("Use when" in desc, f"{tag}: description has 'Use when'")
    report.check(headings(body) == SECTIONS, f"{tag}: sections in required order")
    wf = [l for l in section(body, "Workflow") if l.startswith("1.")]
    report.check(bool(wf) and "Inspect the project" in wf[0], f"{tag}: workflow step 1 inspects project")
    report.check(any("../_shared/standard.md" in l for l in section(body, "Quality checks")),
                 f"{tag}: quality checks cite the shared standard")
    report.check("ARCHITECTURE.md" not in text, f"{tag}: cites nothing that is not installed with the skills")
    missing_shared = sorted(r for r in set(re.findall(r"`(\.\./_shared/[^`]+)`", text))
                            if not (d / r).resolve().is_file())
    report.check(not missing_shared, f"{tag}: cited shared files exist {missing_shared or ''}".strip())
    refs = set(re.findall(r"`([a-z0-9-]+)`", "\n".join(section(body, "Boundaries"))))
    report.check(bool(refs & (EXPECTED - {name})), f"{tag}: boundaries reference a sibling skill")
    unknown = sorted(r for r in refs if r not in EXPECTED)
    report.check(not unknown, f"{tag}: boundaries refs exist {unknown or ''}".strip())
    report.check(40 <= len(body) <= 150, f"{tag}: body length {len(body)} in 40-150")
    report.check("\t" not in text, f"{tag}: no tabs")
    prefix, _ = skill_contract(body)
    report.check(prefix is not None, f"{tag}: outputs define a design/ path")
    if name in STANDARD_V1:
        validate_standard_v1(tag, name, desc, body, report)
        outputs = "\n".join(section(body, "Outputs"))
        missing = sorted(h for h in handoffs.get(name, []) if f"`{h}`" not in outputs)
        report.check(not missing, f"{tag}: section 5 handoffs named in Outputs {missing or ''}".strip())
        _, template = skill_contract(body)
        report.check(template[-2:] == CLOSING_HEADINGS,
                     f"{tag}: output template ends with open questions and next step")
    if name == "design-documentation":
        out_text = "\n".join(section(body, "Outputs"))
        report.check(skill_contract(body)[1] == DOC_CONTRACT, f"{tag}: output contract headings match")
        report.check("Not applicable" in out_text and "Unavailable" in out_text,
                     f"{tag}: contract says how to mark inapplicable and unavailable sections")
    if name in SEVERITY_SKILLS:
        absent = [s for s in SEVERITY_LEVELS if s not in text]
        report.check(not absent and "0 to 4" not in text,
                     f"{tag}: uses the section 8 severity scale {absent or ''}".strip())


def input_table_rows(body: list[str]) -> list[list[str]]:
    """Cells of each Inputs table row, header and separator excluded."""
    rows = [[c.strip() for c in l.strip().strip("|").split("|")]
            for l in section(body, "Inputs") if l.lstrip().startswith("|")]
    return [r for r in rows[1:] if not all(set(c) <= set("-: ") for c in r)]


def validate_standard_v1(tag: str, name: str, desc: str, body: list[str], report: Report) -> None:
    """Conventions from the shared standard, section 8, that are checkable by structure."""
    routed = re.findall(r"`([a-z0-9-]+)`", desc.partition("Not for")[2]) if "Not for" in desc else []
    report.check(bool(routed) and all(r in EXPECTED and r != name for r in routed),
                 f"{tag}: description has 'Not for' routing to valid siblings")
    header = next((l for l in section(body, "Inputs") if l.lstrip().startswith("|")), "")
    cols = [c.strip() for c in header.strip().strip("|").split("|")]
    report.check("If missing" in cols, f"{tag}: Inputs table has an 'If missing' column")
    if "If missing" in cols:
        idx = cols.index("If missing")
        rows = input_table_rows(body)
        bad = [r[0] for r in rows if len(r) <= idx or not r[idx].startswith(MISSING_ACTIONS)]
        report.check(bool(rows) and not bad,
                     f"{tag}: every input declares Stop, Ask one, or Assume {bad or ''}".strip())
    for sec in ("Outputs", "Quality checks"):
        report.check(any("§8" in l for l in section(body, sec)), f"{tag}: {sec} references §8")


def example_output_block(text: str) -> Optional[tuple[list[str], list[str]]]:
    """Return (block lines, '## ' headings) of the markdown block after 'Output shape'."""
    lines = text.split("\n")
    start = next((i for i, l in enumerate(lines) if l.startswith("## Output shape")), None)
    if start is None:
        return None
    opener = next((i for i in range(start + 1, len(lines))
                   if re.match(r"^`{3,}markdown\s*$", lines[i])), None)
    if opener is None:
        return None
    fence = re.match(r"^(`{3,})", lines[opener]).group(1)
    block: list[str] = []
    heads: list[str] = []
    inner = False
    for line in lines[opener + 1:]:
        if line.strip() == fence:
            return block, heads
        if len(fence) > 3 and line.startswith("```"):
            inner = not inner
        block.append(line)
        if not inner and line.startswith("## "):
            heads.append(line[3:].strip())
    return None


def validate_example(root: Path, path: Path, report: Report) -> None:
    tag = f"example {path.name}"
    name = path.stem
    text = path.read_text(encoding="utf-8")
    report.check(name in EXPECTED, f"{tag}: named after a skill")
    report.check("illustrative" in "\n".join(text.split("\n")[:8]).lower(),
                 f"{tag}: labeled illustrative near the top")
    report.check(not DATE_RE.search(text), f"{tag}: no literal dates")
    skill_file = root / ".claude" / "skills" / name / "SKILL.md"
    if not skill_file.is_file():
        report.check(False, f"{tag}: skill file exists")
        return
    _, body = parse(skill_file.read_text(encoding="utf-8"))
    prefix, want = skill_contract(body)
    path_match = re.search(r"^## Output shape \(`([^`]+)`\)", text, re.M)
    out_path = path_match.group(1) if path_match else ""
    report.check(bool(prefix) and out_path.startswith(prefix or "\0") and DATE_PLACEHOLDER in out_path,
                 f"{tag}: output path matches skill and uses {DATE_PLACEHOLDER}")
    parsed = example_output_block(text)
    report.check(parsed is not None, f"{tag}: has a markdown output block")
    if parsed is None:
        return
    block, heads = parsed
    first = next((l for l in block if l.strip()), "")
    report.check(first.startswith(f"> skill: {name} "), f"{tag}: metadata line names the skill")
    got = [norm_heading(h) for h in heads]
    report.check(got == want, f"{tag}: output headings match skill contract")
    # norm_heading drops trailing parentheticals; headings are a contract, so also compare the exact text
    out = section(body, "Outputs")
    exact_want = [re.sub(r"\s+", " ", l[3:]).strip() for l in out if l.startswith("## ")]
    exact_got = [re.sub(r"\s+", " ", h).strip() for h in heads]
    report.check(exact_got == exact_want, f"{tag}: output headings match skill contract exactly")
    # the example's Next step names exactly one skill, other than itself, from the skill's Outputs handoffs
    handoff_lines = " ".join(re.split(r"\bNever\b", l)[0] for l in out if "Next step" in l and "names" in l)
    allowed = set(re.findall(r"`([a-z0-9-]+)`", handoff_lines)) & set(EXPECTED) - {name}
    nxt = next((i for i, l in enumerate(block) if l.strip() == "## Next step"), None)
    named = set(re.findall(r"`([a-z0-9-]+)`", "\n".join(block[nxt + 1:]))) & set(EXPECTED) if nxt is not None else set()
    report.check(len(named) == 1 and named <= allowed,
                 f"{tag}: Next step names one allowed handoff {sorted(named) if named - allowed or len(named) != 1 else ''}".strip())


def validate_links(root: Path, report: Report) -> None:
    files = [root / "README.md", root / "CONTRIBUTING.md"]
    for sub in ("docs", "examples"):
        d = root / sub
        if d.is_dir():
            files += sorted(d.glob("*.md"))
    for f in files:
        if not f.is_file():
            continue
        broken = []
        for line in outside_fences(f.read_text(encoding="utf-8").split("\n")):
            for target in LINK_RE.findall(line):
                if "://" in target or target.startswith(("mailto:", "#")):
                    continue
                rel = target.split("#")[0]
                if rel and not (f.parent / rel).exists():
                    broken.append(target)
        report.check(not broken, f"{f.relative_to(root)}: relative links resolve {broken or ''}".strip())


# Skills that publish through the shared Figma adapter: every skill, since Batch D.
FIGMA_SKILLS = set(EXPECTED)
# Every integrated skill's Figma line must say, in its own terms, what is never drawn.
FIGMA_GROUNDED_SKILLS = FIGMA_SKILLS
FIGMA_NOT_USED = ("publishing disabled", "design/figma.json unreadable", "tools unavailable",
                  "run not confirmed", "no Figma account connected", "no design file")
FIGMA_MCP_TOOLS = re.compile(r"\b(use_figma|create_session|create_new_file|get_metadata|whoami|generate_diagram)\b")
FIGMA_CASES = (
    "Publishing disabled or configuration missing",
    "Configuration unreadable",
    "Figma tools unavailable",
    "No file and creation not possible",
    "No artifact entry, or stored node missing",
    "Owned, stored fingerprint has the `fp1:` prefix and equals the current one",
    "Owned, fingerprint matches, but the update needs more than the non-destructive rules allow",
    "Owned but fingerprint differs",
    "Stored fingerprint missing or lacks the current `fp1:` prefix",
    "Node at stored ID lacks the tag",
)
# required wording in the action cell of safety-critical decision rows
FIGMA_ROW_RULES = {
    "Owned, stored fingerprint has the `fp1:` prefix": "only within the non-destructive update rules",
    "Owned, fingerprint matches, but the update needs more": "Ask the user to confirm it. Without confirmation, draw a new version from the Markdown",
    "Owned but fingerprint differs": "never by cloning the edited frame",
    "Stored fingerprint missing or lacks": "Preserve the frame and ask the user to confirm a replacement",
}


def validate_figma(root: Path, report: Report) -> None:
    """Structural checks on the optional Figma adapter. These never contact Figma."""
    path = root / ".claude" / "skills" / "_shared" / "figma.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    tag = "figma adapter"
    block = re.search(r"```json\n(.*?)\n```", text, re.S)
    try:
        config = json.loads(block.group(1)) if block else None
    except json.JSONDecodeError:
        config = None
    report.check(isinstance(config, dict), f"{tag}: default configuration is valid JSON")
    config = config if isinstance(config, dict) else {}
    report.check(isinstance(config.get("schema_version"), int), f"{tag}: configuration has a schema version")
    publishing = config.get("publishing", {})
    report.check(publishing.get("enabled") is False, f"{tag}: publishing is disabled by default")
    report.check(publishing.get("confirm_each_run") is True, f"{tag}: per-run confirmation is on by default")
    privacy = config.get("privacy", {})
    report.check(privacy.get("allow_quotes") is False, f"{tag}: quotes are not published by default")
    flat = json.dumps(config).lower()
    report.check(not re.search(r"token|secret|password|api_?key|credential", flat),
                 f"{tag}: configuration has no credential fields")
    rows = re.findall(r"^\| ([a-z0-9-]+) \| ([^|]+?) \| ([^|]+?) \|$", text, re.M)
    pages = {s: pg.strip() for s, pg, _ in rows if s in EXPECTED}
    topics = {s: tp.strip() for s, _, tp in rows if s in EXPECTED}
    report.check(set(pages) == EXPECTED, f"{tag}: page map covers all 19 skills")
    report.check(len(set(pages.values())) == len(pages), f"{tag}: page names are unique")
    report.check(pages.get("user-flow-designer") == "User Flows", f"{tag}: user flows draw on the User Flows page")
    missing = [c for c in FIGMA_CASES if c not in text]
    report.check(not missing, f"{tag}: decision table covers every case {missing or ''}".strip())
    report.check("getSharedPluginData" in text and "stored for the artifact key" in text,
                 f"{tag}: ownership needs the stored node ID and the tag")
    report.check("Markdown file is always written first" in text, f"{tag}: Markdown stays the source of truth")
    report.check("// MJC fingerprint fp1. Paste unchanged." in text and 'return "fp1:"' in text,
                 f"{tag}: one exact fingerprint function is given")
    report.check("never by cloning the edited frame" in text, f"{tag}: new versions are drawn from the Markdown")
    for case, rule in FIGMA_ROW_RULES.items():
        row = next((l for l in text.split("\n") if l.startswith(f"| {case}")), "")
        report.check(rule in row, f"{tag}: decision row '{case[:40]}' requires: {rule[:50]}")
    report.check("a matching fingerprint does not prove the frame is unchanged" in text,
                 f"{tag}: a matching fingerprint is not treated as proof of no edits")
    report.check("may therefore only change the characters of existing text nodes and append new nodes" in text
                 and "never deletes, recreates, reorders, or restyles existing nodes" in text,
                 f"{tag}: in-place updates are limited to non-destructive changes")
    # Skipped-publishing lines are fixed strings: a free-form reason lets replies drift.
    reasons = set(re.findall(r"Figma: not used \(([^)`]*)\)", text))
    report.check(reasons == set(FIGMA_NOT_USED), f"{tag}: 'not used' reasons are the fixed set {sorted(reasons ^ set(FIGMA_NOT_USED)) or ''}".strip())
    reporting = text.split("## 8.", 1)[-1].split("## 9.", 1)[0]
    report.check(all(f"`Figma: not used ({r})`" in reporting for r in FIGMA_NOT_USED)
                 and "Copy a `not used` line exactly" in reporting,
                 f"{tag}: reporting lists each exact 'not used' line and says to copy it")
    # Every decision outcome needs its own reporting line, so a reply never misstates what happened.
    report.check("replacement not confirmed, the earlier frame was left unchanged" in reporting
                 and "`Figma: failed (file not found or no edit access)`" in reporting,
                 f"{tag}: reporting covers unconfirmed replacement and file access failure")
    skills_dir = root / ".claude" / "skills"
    citing ={d.name for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith("_")
              and "../_shared/figma.md" in (d / "SKILL.md").read_text(encoding="utf-8")}
    report.check(citing == FIGMA_SKILLS, f"{tag}: cited by exactly the integrated skills {sorted(citing ^ FIGMA_SKILLS) or ''}".strip())
    for name in sorted(FIGMA_SKILLS):
        skill_file = skills_dir / name / "SKILL.md"
        if not skill_file.is_file():
            continue
        body = skill_file.read_text(encoding="utf-8")
        stag = f"{name}: figma"
        page = pages.get(name, "")
        line = next((l for l in body.split("\n") if l.startswith("Figma (optional, per `../_shared/figma.md`)")), "")
        report.check(bool(page) and f"`{page}` page" in line, f"{stag} line names its mapped page '{page}'")
        report.check("The Markdown file stays the source of truth" in line, f"{stag} line keeps Markdown as the source of truth")
        report.check(any(l.startswith("- [ ]") and "../_shared/figma.md" in l for l in body.split("\n")),
                     f"{stag} quality check cites the adapter")
        report.check(not FIGMA_MCP_TOOLS.search(body), f"{stag} has no direct MCP tool calls (uses the shared adapter)")
        if name in FIGMA_GROUNDED_SKILLS:
            report.check(re.search(r"\b[Nn]ever (draw|add)\b", line) is not None,
                         f"{stag} line limits drawing to what the Markdown supports")
        _, sbody = parse(body)
        outputs = "\n".join(section(sbody, "Outputs"))
        holes = re.findall(r"<[a-z]+>", topics.get(name, ""))
        report.check(bool(topics.get(name)) and (topics[name] == "`main`" or (holes and all(h in outputs for h in holes))),
                     f"{stag} artifact topic comes from its output filename")


# Rules that make user-flow-designer's diagram traceable: each arrow is an inventory row with evidence.
FLOW_SKILL_RULES = {
    "transition statuses": ("`Verified` (a source shows it", "`Inferred` (a reasonable reading", "`Unknown` (no source settles it)"),
    "one edge per inventory row": ("Every inventory row is one labeled arrow, and every arrow is a row",),
    "terminal and legend conventions": ('id(["End · ..."])', "legend table"),
    "one complete diagram, not trimmed": ("always one diagram that holds every transition",
                                          "never drop a branch to make it fit"),
    "individual flows cover every transition": ("**Draw each individual flow.**",
                                                "Together the individual flows cover every inventory transition"),
    "integrity check": ("**Run the flow integrity check**", "Do not call the flow exhaustive"),
    "contradictions name both sources": ("Never resolve a contradiction by choosing a side silently",),
    "dead ends fixed, not noted": ("is a defect to fix before saving",),
}

# Evidence-form rules added after behavioral failures (PF-N1 quotes, CS-E1 counts); see tests/behavioral/FINDINGS.md
EVIDENCE_FORM_RULES = {
    "problem-framing": {"stakeholder words verbatim, rewording separate": ("Stakeholder said: \"<their exact sentence>\"", "`Our reading: <words>`")},
    "case-study-writer": {"weaker line excludes the strict count": ("removing every person already in the strict line",)},
}


def validate_evidence_forms(root: Path, report: Report) -> None:
    for skill, rules in EVIDENCE_FORM_RULES.items():
        path = root / ".claude" / "skills" / skill / "SKILL.md"
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        for rule, phrases in rules.items():
            report.check(all(ph in text for ph in phrases), f"{skill}: states rule '{rule}'")


def validate_user_flow(root: Path, report: Report) -> None:
    """Checks that user-flow-designer keeps its evidence rules and that its example follows them."""
    skill = root / ".claude" / "skills" / "user-flow-designer" / "SKILL.md"
    example = root / "examples" / "user-flow-designer.md"
    if not skill.is_file() or not example.is_file():
        return
    text = skill.read_text(encoding="utf-8")
    for rule, phrases in FLOW_SKILL_RULES.items():
        report.check(all(p in text for p in phrases), f"user-flow-designer: states rule '{rule}'")
    ex = example.read_text(encoding="utf-8")
    flow = ex.split("## Complete flow", 1)[-1].split("## Transition inventory", 1)[0]
    edges = re.findall(r"-->\|([^|]*)\|", flow)
    report.check(bool(edges) and all(re.match(r"T\d+ · ", e) for e in edges),
                 "example user-flow-designer.md: every complete-flow edge is labeled with a transition ID")
    report.check('(["End · ' in flow and "| Meaning |" in flow,
                 "example user-flow-designer.md: terminal states are marked and a legend is present")
    inventory = ex.split("## Transition inventory", 1)[-1].split("## ", 1)[0]
    report.check(all(c in inventory for c in ("| Status |", "| Evidence |", "Verified", "Unknown")),
                 "example user-flow-designer.md: inventory has status and evidence columns")
    report.check(len(re.findall(r"```mermaid", flow)) == 1,
                 "example user-flow-designer.md: complete flow is one diagram")
    individual = ex.split("## Individual flows", 1)[-1].split("## Screen state table", 1)[0] if "## Individual flows" in ex else ""
    covered = set(re.findall(r"\bT\d+\b", individual))
    report.check(bool(re.search(r"^### F1 · ", individual, re.M)) and covered >= set(re.findall(r"\bT\d+\b", flow)),
                 "example user-flow-designer.md: individual flows cover every complete-flow transition")


PERSONALITY_LINE = "- [ ] Chat replies follow `../_shared/personality.md`; no emoticons in written files or structured output"
PERSONALITY_RULES = {
    "text emoticons only": ("Never use pictographic emoji",),
    "at most one per reply": ("At most one emoticon per reply",),
    "never in files or structured output": ("Never in written files or structured output",),
    "no false success": ("unless the completion conditions were met and verified",),
    "serious issues not playful": ("Accessibility failures, security or privacy problems",),
    "does not change behavior": ("It never adds steps, messages, or questions",),
    "closing signature": ("ends with exactly one emoticon from section 3, alone on its own final line",
                          "separated from the content above by one blank line", "Nothing follows it"),
    "no duplicate opening": ("No opening emoticon as well",),
    "strict-format exception": ("The reply is only a strict-format artifact", "the artifact itself never changes"),
}
EMOTICONS = ("._.", "o_o", "-_-", ">:)", "ಠ_ಠ", "o_O", "(ツ)", "x_x", "^_^", "^-^")
PICTOGRAPH = re.compile("[\U0001F000-\U0001FAFF☀-➿️]")
SIGNATURES = ("._.;", "._.", "o_o", "-_-", ">:)", "ಠ_ಠ", "o_O", "¯\\_(ツ)_/¯", "x_x", "^_^", "^-^")
SUCCESS = ("^_^", "^-^")


def emoticon_count(text: str) -> int:
    """Counts library emoticons, matching longest first so `._.;` is not also counted as `._.`."""
    n = 0
    for e in sorted(SIGNATURES, key=len, reverse=True):
        n += text.count(e)
        text = text.replace(e, " ")
    return n


def reply_problems(reply: str, kind: str = "normal") -> list[str]:
    """Form checks for one chat reply. kind: normal, failed (no success close), or strict (no emoticon)."""
    problems = []
    if PICTOGRAPH.search(reply):
        problems.append("pictographic emoji")
    if kind == "strict":
        if emoticon_count(reply):
            problems.append("emoticon in strict-format output")
        return problems
    lines = reply.rstrip("\n").split("\n")
    last = lines[-1]
    if last not in SIGNATURES:
        problems.append("last line is not exactly one emoticon")
    elif len(lines) < 3 or lines[-2].strip() != "" or not lines[-3].strip():
        problems.append("signature not separated by exactly one blank line after content")
    if emoticon_count(reply) != 1:
        problems.append(f"{emoticon_count(reply)} emoticons; expected exactly one")
    if kind == "failed" and last in SUCCESS:
        problems.append("success expression on a failed workflow")
    return problems


def personality_samples(text: str) -> list[tuple[str, str]]:
    """(kind, body) for each `kind: <k>` line followed by a ```text block in personality.md."""
    return re.findall(r"^kind: (\w+)\n```text\n(.*?)\n```", text, re.M | re.S)


def validate_personality(root: Path, report: Report) -> None:
    """Checks the shared personality file, that every skill cites it, and that outputs stay emoticon-free."""
    path = root / ".claude" / "skills" / "_shared" / "personality.md"
    report.check(path.is_file(), "personality: _shared/personality.md exists")
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    for rule, phrases in PERSONALITY_RULES.items():
        report.check(all(p in text for p in phrases), f"personality: states rule '{rule}'")
    report.check(all(e in text for e in EMOTICONS), "personality: library lists every expression")
    samples = personality_samples(text)
    report.check({k for k, _ in samples} >= {"normal", "failed", "strict"},
                 "personality: sample replies cover normal, failed, and strict output")
    for i, (kind, body) in enumerate(samples, 1):
        bad = reply_problems(body, kind)
        report.check(not bad, f"personality: sample {i} ({kind}) has correct form {bad or ''}".strip())
    skill_files = sorted((root / ".claude" / "skills").glob("*/SKILL.md"))
    for f in skill_files + [path]:
        body = f.read_text(encoding="utf-8")
        name = f.parent.name if f.name == "SKILL.md" else "personality"
        report.check(not PICTOGRAPH.search(body), f"{name}: no pictographic emoji")
        if f.name == "SKILL.md":
            report.check(body.count(PERSONALITY_LINE) == 1, f"{name}: cites shared personality once")
            report.check(not any(e in body for e in EMOTICONS), f"{name}: does not copy emoticons")
    for ex in sorted((root / "examples").glob("*.md")):
        block = example_output_block(ex.read_text(encoding="utf-8"))
        out = "\n".join(block[0]) if block else ""
        report.check(not any(e in out for e in EMOTICONS) and not PICTOGRAPH.search(out),
                     f"example {ex.name}: written output has no emoticons")


def validate(root: Path = DEFAULT_ROOT, echo: bool = True) -> Report:
    report = Report(echo)
    skills_dir = root / ".claude" / "skills"
    dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith("_")) if skills_dir.is_dir() else []
    report.check(len(dirs) == 19, f"repo: 19 skill directories (found {len(dirs)})")
    report.check({d.name for d in dirs} == EXPECTED, "repo: skill names match expected set")
    arch_file = root / "docs" / "ARCHITECTURE.md"
    handoffs = architecture_handoffs(arch_file.read_text(encoding="utf-8")) if arch_file.is_file() else {}
    for d in dirs:
        validate_skill(d, report, handoffs)

    readme = root / "README.md"
    rtext = readme.read_text(encoding="utf-8") if readme.is_file() else ""
    report.check(readme.is_file(), "repo: README.md exists")
    missing = sorted(n for n in EXPECTED if n not in rtext)
    report.check(not missing, f"repo: README mentions all skills {missing or ''}".strip())

    arch = root / "docs" / "ARCHITECTURE.md"
    report.check(arch.is_file(), "repo: docs/ARCHITECTURE.md exists")
    shared = root / ".claude" / "skills" / "_shared" / "standard.md"
    report.check(shared.is_file(), "repo: shared standard ships with the skills")
    stext = shared.read_text(encoding="utf-8") if shared.is_file() else ""
    report.check("## 8. Shared quality standard" in stext, "shared standard: quality standard section")
    for h in STANDARD_HEADINGS:
        report.check(re.search(rf"^### {re.escape(h)}\s*$", stext, re.M) is not None,
                     f"shared standard: covers '{h}'")

    contrib = root / "CONTRIBUTING.md"
    ctext = contrib.read_text(encoding="utf-8") if contrib.is_file() else ""
    report.check(contrib.is_file(), "repo: CONTRIBUTING.md exists")
    report.check("bash tests/run.sh" in ctext and "ARCHITECTURE.md" in ctext,
                 "CONTRIBUTING.md: names the test command and the architecture doc")

    ex_dir = root / "examples"
    examples = sorted(p for p in ex_dir.glob("*.md") if p.name != "README.md") if ex_dir.is_dir() else []
    ex_readme = ex_dir / "README.md"
    etext = ex_readme.read_text(encoding="utf-8") if ex_readme.is_file() else ""
    report.check(ex_readme.is_file(), "examples: README.md exists")
    report.check("illustrative" in etext.lower(), "examples/README.md: states examples are illustrative")
    for ex in examples:
        report.check(f"({ex.name})" in etext, f"examples/README.md: lists {ex.name}")
        validate_example(root, ex, report)

    validate_figma(root, report)
    validate_user_flow(root, report)
    validate_personality(root, report)
    validate_evidence_forms(root, report)
    validate_links(root, report)
    return report


def main() -> int:
    report = validate()
    failed = len(report.failed)
    print(f"\n{len(report.results) - failed} passed, {failed} failed, {len(report.results)} total")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
