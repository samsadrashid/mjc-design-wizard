"""Validate the mjc-design-wizard skills against docs/ARCHITECTURE.md.

Run from repo root: python3 tests/validate_skills.py
Exit 0 when every check passes, 1 otherwise. Standard library only.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / ".claude" / "skills"

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
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

results: list[tuple[bool, str]] = []


def check(ok: bool, label: str) -> None:
    results.append((ok, label))
    print(f"{'PASS' if ok else 'FAIL'}  {label}")


def parse(text: str) -> tuple[dict[str, str] | None, list[str]]:
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


def headings(body: list[str]) -> list[str]:
    """Top-level '## ' headings outside code fences."""
    found, fenced = [], False
    for line in body:
        if line.startswith("```"):
            fenced = not fenced
        elif not fenced and line.startswith("## "):
            found.append(line[3:].strip())
    return found


def section(body: list[str], name: str) -> list[str]:
    out, active, fenced = [], False, False
    for line in body:
        if line.startswith("```"):
            fenced = not fenced
        if not fenced and line.startswith("## "):
            active = line[3:].strip() == name
            continue
        if active:
            out.append(line)
    return out


def validate_skill(d: Path) -> None:
    p = d / "SKILL.md"
    tag = d.name
    if not p.is_file():
        check(False, f"{tag}: SKILL.md exists")
        return
    text = p.read_text(encoding="utf-8")
    meta, body = parse(text)
    check(meta is not None, f"{tag}: frontmatter present")
    meta = meta or {}
    check("name" in meta and "description" in meta, f"{tag}: has name and description")
    name = meta.get("name", "")
    check(name == d.name, f"{tag}: name matches directory")
    check(bool(NAME_RE.match(name)) and len(name) <= 64, f"{tag}: name format")
    desc = meta.get("description", "")
    check(0 < len(desc) <= 1024, f"{tag}: description length")
    check("Use when" in desc, f"{tag}: description has 'Use when'")
    check(headings(body) == SECTIONS, f"{tag}: sections in required order")
    wf = [l for l in section(body, "Workflow") if l.startswith("1.")]
    check(bool(wf) and "Inspect the project" in wf[0], f"{tag}: workflow step 1 inspects project")
    check(any("ARCHITECTURE.md" in l for l in section(body, "Quality checks")),
          f"{tag}: quality checks reference ARCHITECTURE.md")
    refs = set(re.findall(r"`([a-z0-9-]+)`", "\n".join(section(body, "Boundaries"))))
    others = {r for r in refs if r in EXPECTED and r != name}
    check(bool(others), f"{tag}: boundaries reference a sibling skill")
    unknown = {r for r in refs if r not in EXPECTED}
    check(not unknown, f"{tag}: boundaries refs exist {sorted(unknown) or ''}".strip())
    check(40 <= len(body) <= 150, f"{tag}: body length {len(body)} in 40-150")
    check("\t" not in text, f"{tag}: no tabs")


def main() -> int:
    dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()) if SKILLS_DIR.is_dir() else []
    check(len(dirs) == 19, f"repo: 19 skill directories (found {len(dirs)})")
    check({d.name for d in dirs} == EXPECTED, "repo: skill names match expected set")
    for d in dirs:
        validate_skill(d)
    readme = ROOT / "README.md"
    rtext = readme.read_text(encoding="utf-8") if readme.is_file() else ""
    check(readme.is_file(), "repo: README.md exists")
    missing = sorted(n for n in EXPECTED if n not in rtext)
    check(not missing, f"repo: README mentions all skills {missing or ''}".strip())
    check((ROOT / "docs" / "ARCHITECTURE.md").is_file(), "repo: docs/ARCHITECTURE.md exists")
    failed = sum(1 for ok, _ in results if not ok)
    print(f"\n{len(results) - failed} passed, {failed} failed, {len(results)} total")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
