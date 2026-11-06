"""Self-check for an MJC deliverable before it is saved. Read-only; prints problems and exits 1 if any.

Usage (from the project root):
    python3 .claude/skills/_shared/check_evidence.py <deliverable.md> [--reply <reply.md>]

Checks, against the project's own sources (ticket CSVs whose first column is an ID such as T-01,
and interview files named like P1.md):
  Q1  a quote credited to a ticket or interview ("words" (T-01), P3: "words") is in that source word for word;
      IDs written before a quote must each contain it.
  C1  a count line "<label>: N people — ID, ID" lists N distinct people (a ticket author who was also
      interviewed is one person); only IDs follow the dash.
  C2  every member of a "could not find" count has a source of their own that says it could not be found.
  C3  a weaker or "more" count line repeats nobody from the could-not-find line.
  R1  with --reply: the chat reply asks at most one question (one "?" and no second request joined by "and").
Names and contact details found in the sources are used only to match people and are never printed.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

SKIP = {".claude", ".git", "design", "node_modules"}
IDS = r"(?:T-\d+|P\d+)"
EXPLICIT = re.compile(r"\b(cannot|can't|could not|couldn't|unable to)\s+(be\s+)?(find|found|see|seen|locate)", re.I)


def norm(s: str) -> str:
    return " " + re.sub(r"[^a-z0-9]+", " ", s.lower()).strip() + " "


def sources(root: Path) -> tuple[dict[str, str], dict[str, str]]:
    """Text of each ticket and interview, and the person each belongs to (internal only)."""
    text: dict[str, str] = {}
    person: dict[str, str] = {}
    for p in root.rglob("*"):
        if not p.is_file() or SKIP & set(p.relative_to(root).parts):
            continue
        if p.suffix == ".csv":
            with p.open(encoding="utf-8", errors="replace", newline="") as f:
                rows = list(csv.reader(f))
            if not rows:
                continue
            head = [h.strip().lower() for h in rows[0]]
            who = next((i for i, h in enumerate(head) if h in ("customer_name", "name", "author", "customer", "user")), None)
            for r in rows[1:]:
                if r and re.fullmatch(r"T-\d+", r[0].strip()):
                    text[r[0].strip()] = ",".join(r[1:])
                    if who is not None and who < len(r):
                        person[r[0].strip()] = r[who].strip().lower()
        elif re.fullmatch(r"P\d+\.md", p.name):
            body = p.read_text(encoding="utf-8", errors="replace")
            text[p.stem] = body
            m = re.search(r"^Participant:\s*([^|\n]+)", body, re.M)
            if m:
                person[p.stem] = m.group(1).strip().lower()
    return text, person


def check(doc: str, text: dict[str, str], person: dict[str, str]) -> list[str]:
    out = []
    prose = re.sub(r"```.*?```", " ", doc, flags=re.S)
    for m in re.finditer(r"[\"“]([^\"”\n]{3,220})[\"”]", prose):
        after = re.match(rf"\s{{0,2}}[(\[]\s*({IDS}(?:\s*[,;]\s*{IDS})*)", prose[m.end():m.end() + 40])
        lead = re.split(r"[\n|]", prose[max(0, m.start() - 40):m.start()])[-1]
        before = re.search(rf"(?<![\w-])({IDS}(?:\s*,\s*{IDS})*)\b[^\"“\w]{{0,4}}(?:said|says|wrote)?[^\"“\w]{{0,3}}$", lead)
        ids = [i for i in re.findall(IDS, after.group(1) if after else (before.group(1) if before else "")) if i in text]
        if not ids:
            continue
        found = [norm(m.group(1)) in norm(text[i]) for i in ids]
        if "/" in m.group(1) or not (any(found) if after else all(found)):
            out.append(f'Q1 "{m.group(1)}" is not word for word in {", ".join(ids)}')
    # a quote credited to a file path ("words" (docs/request.md)) is in that file word for word
    for m in re.finditer(r"[\"“]([^\"”\n]{3,220})[\"”]\s{0,2}\(`?([\w./-]+\.(?:md|txt|csv))`?\)", prose):
        path = Path.cwd() / m.group(2)
        if path.is_file() and norm(m.group(1)) not in norm(path.read_text(encoding="utf-8", errors="replace")):
            out.append(f'Q2 "{m.group(1)}" is not word for word in {m.group(2)}')
    who = lambda i: person.get(i, i)
    said = {who(i) for i, t in text.items() if EXPLICIT.search(t)}
    rx = rf"^[-*\s]*(.{{3,120}}?):\s*(\d+) (?:more )?people\s+—\s+({IDS}(?:,\s*{IDS})*)\s*\.?(?:\s*`?\[[^\]\n]*\]`?)*\s*$"
    rows = [(m.group(1), int(m.group(2)), re.findall(IDS, m.group(3))) for m in re.finditer(rx, doc, re.M)]
    strict: set[str] = set()
    for label, n, ids in rows:
        people = {who(i) for i in ids}
        if len(people) != n:
            out.append(f"C1 {label}: says {n} people but lists {len(people)} distinct ({', '.join(ids)})")
        if re.search(r"could not find", label, re.I) and not re.search(r"weaker|more", label, re.I):
            strict |= people
            out += [f"C2 {label}: {i} has no source that says it could not be found" for i in ids if i in text and who(i) not in said]
    for label, n, ids in rows:
        if re.search(r"weaker|more", label, re.I) and strict & {who(i) for i in ids}:
            out.append(f"C3 {label}: repeats someone already in the could-not-find count ({', '.join(ids)})")
    return out


def reply_questions(reply: str) -> list[str]:
    asks = [s for s in re.findall(r"[^.?!\n]*\?", reply) if s.strip()]
    if len(asks) > 1 or (asks and re.search(r"\b(and|also)\b.*\b(or|who|what|which|whether|how|when|where)\b", asks[0], re.I)):
        return [f"R1 the reply asks more than one question: {' | '.join(a.strip() for a in asks)[:200]}"]
    return []


def main(argv: list[str]) -> int:
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    doc_path = Path(argv[0])
    text, person = sources(Path.cwd())
    problems = check(doc_path.read_text(encoding="utf-8"), text, person)
    if "--reply" in argv:
        problems += reply_questions(Path(argv[argv.index("--reply") + 1]).read_text(encoding="utf-8"))
    for p in problems:
        print(p)
    print(f"{len(problems)} problem(s); checked against {len(text)} ticket and interview sources")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
