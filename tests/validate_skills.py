"""Structural validator for the mjc-design-wizard skills, docs, and examples.

Run from repo root: python3 tests/validate_skills.py
Exit 0 when every check passes, 1 otherwise. Standard library only.

These checks prove structure and conventions. They say nothing about the
quality of a skill's output; see .claude/skills/_shared/standard.md section 8.
"""
from __future__ import annotations

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

    validate_links(root, report)
    return report


def main() -> int:
    report = validate()
    failed = len(report.failed)
    print(f"\n{len(report.results) - failed} passed, {failed} failed, {len(report.results)} total")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
