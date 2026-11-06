#!/usr/bin/env python3
"""Behavioral evaluation harness for the mjc-design-wizard skills.

Standard library only. This is NOT the structural validator. It prepares sandboxes,
builds the executor prompt, screens a finished run with deterministic checks, and
generates the matrix and results documents. Output quality is judged separately
(see README.md): automated screening is necessary but never sufficient to pass.

  python3 tests/behavioral/harness.py prepare ID --out DIR --manifest FILE
  python3 tests/behavioral/harness.py prompt ID --sandbox DIR
  python3 tests/behavioral/harness.py collect ID --sandbox DIR --manifest FILE [--attempt N]
  python3 tests/behavioral/harness.py docs
  python3 tests/behavioral/harness.py summary
  python3 tests/behavioral/harness.py version
  python3 tests/behavioral/harness.py backfill --scratch DIR

collect refuses to store a sandbox whose content matches an attempt already stored for that
scenario (same fingerprint), so running a collector twice cannot create duplicate attempts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Optional

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "tests"))
import validate_skills as v  # noqa: E402

FIXTURES = HERE / "fixtures"
RUNS = HERE / "runs"
CATEGORIES = ["normal", "missing", "evidence", "edge"]
EXPECTS = {"output", "stop", "either"}
FIGURE_ALLOWED = {"100%", "80%", "50%"}  # default confidence mapping in the shared standard


def load_scenarios() -> list[dict]:
    return json.loads((HERE / "scenarios.json").read_text(encoding="utf-8"))


def get(scn_id: str) -> dict:
    for s in load_scenarios():
        if s["id"] == scn_id:
            return s
    raise SystemExit(f"unknown scenario {scn_id}")


def is_text(p: Path) -> bool:
    return p.suffix.lower() in {".md", ".txt", ".csv", ".json", ".ts", ".tsx", ".css", ".html", ""}


def file_hashes(root: Path) -> dict[str, str]:
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file() and ".git" not in p.relative_to(root).parts:
            out[str(p.relative_to(root))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


# ---------------------------------------------------------------- prepare
def apply_fixtures(scn: dict, out: Path) -> None:
    for d in scn["fixtures"]:
        src = FIXTURES / d
        for p in sorted(src.rglob("*")):
            rel = p.relative_to(src)
            if p.is_file() and p.name != ".remove":
                dest = out / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, dest)
        rm = src / ".remove"
        if rm.is_file():
            for line in rm.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                target = out / line
                if target.is_dir():
                    shutil.rmtree(target)
                elif target.exists():
                    target.unlink()


def build_git_history(out: Path) -> None:
    hist = out / "git-history.txt"
    if not hist.is_file():
        return
    env_base = dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_SYSTEM="/dev/null")
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=out, check=True, env=env_base)
    for line in hist.read_text(encoding="utf-8").splitlines():
        when, name, email, subject = line.split("|", 3)
        env = dict(env_base, GIT_AUTHOR_NAME=name, GIT_AUTHOR_EMAIL=email, GIT_AUTHOR_DATE=when,
                   GIT_COMMITTER_NAME=name, GIT_COMMITTER_EMAIL=email, GIT_COMMITTER_DATE=when)
        subprocess.run(["git", "commit", "-q", "--allow-empty", "-m", subject], cwd=out, check=True, env=env)
    hist.unlink()


def prepare(scn_id: str, out: Path, manifest: Path) -> None:
    scn = get(scn_id)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    apply_fixtures(scn, out)
    shared = REPO / ".claude" / "skills" / "_shared"
    if shared.is_dir():  # simulate a real install: the skills' shared folder sits in the project
        shutil.copytree(shared, out / ".claude" / "skills" / "_shared")
    build_git_history(out)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(file_hashes(out), indent=1), encoding="utf-8")


# ---------------------------------------------------------------- prompt
EXEC_PROMPT = """You are executing one behavioral test of a Claude Code skill. Act as the assistant in a real Claude Code session working in a user's project.

PROJECT ROOT (work here; treat it as the user's repository): {sandbox}
SKILL TO USE: `{skill}`. Load it with the Skill tool (skill: "{skill}"). If the Skill tool does not offer it, read {skill_path} and follow it. Record which method you used.

THE USER'S REQUEST (verbatim):
<<<
{prompt}
>>>

RULES FOR THIS TEST
1. The skill is installed in the user's project the way a real user installs it: the skill, plus the shared folder `.claude/skills/_shared/` in the project root. The skill cites `../_shared/standard.md`; read the installed copy at {sandbox}/.claude/skills/_shared/standard.md, then the other shared files its section 1 tells you to read from the same installed folder (personality.md always; figma.md only when that section says it applies). Do not read any other file from the mjc-design-wizard repository: no docs/, tests/, examples/, or other skills. If the skill cites some other file that does not exist in the project, you cannot consult it. Handle that as a real assistant would.
2. The user is not available to answer. If the skill says to stop, stop and write your reply. If it says to ask one question, put that single question in your reply and continue only as the skill directs. Never wait for an answer.
3. Write deliverables only where the skill says (under design/ in the project root). Do not modify, rename, or delete any existing file.
4. Be honest. If you cannot do something (no browser, a missing file, no data), say so. Use the real current date from the shell (`date +%F`) where the skill needs a date.
5. Do not use mew-coder, GLM, or any other coding agent. Do not spawn further agents.
6. When finished, write your complete final reply to the user, exactly as you would give it, to {sandbox}/RESPONSE.md. Then write {sandbox}/HARNESS.md with: the activation method (skill-tool or file-read), the shared files you read, the tools you used, and any difficulty or deviation. Then end with one short line.
"""


def exec_prompt(scn_id: str, sandbox: Path) -> str:
    scn = get(scn_id)
    skill_path = REPO / ".claude" / "skills" / scn["skill"] / "SKILL.md"
    return EXEC_PROMPT.format(sandbox=sandbox, skill=scn["skill"], skill_path=skill_path, prompt=scn["prompt"])


# ---------------------------------------------------------------- checks
def norm_text(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def fixture_corpus(scn: dict) -> str:
    parts = []
    for d in scn["fixtures"]:
        for p in sorted((FIXTURES / d).rglob("*")):
            if p.is_file() and p.name != ".remove" and is_text(p):
                parts.append(p.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(parts)


def fixture_files(scn: dict) -> dict[str, str]:
    """Text of each fixture file by relative path (later layers override earlier ones), for source-attribution checks."""
    files: dict[str, str] = {}
    for d in scn["fixtures"]:
        for p in sorted((FIXTURES / d).rglob("*")):
            if p.is_file() and p.name != ".remove" and is_text(p):
                files[str(p.relative_to(FIXTURES / d))] = p.read_text(encoding="utf-8", errors="replace")
    return files


def closing_expressions() -> list[str]:
    """Emoticons from the expression library in the shared personality file."""
    f = REPO / ".claude" / "skills" / "_shared" / "personality.md"
    return re.findall(r"^\| `([^`]+)` \|", f.read_text(encoding="utf-8"), re.M) if f.is_file() else []


def person_of(scn: dict) -> dict[str, str]:
    """Maps each ticket and interview ID to its person's name, so one person is counted once across sources."""
    out: dict[str, str] = {}
    for d in scn["fixtures"]:
        for p in sorted((FIXTURES / d).rglob("*")):
            if p.is_file() and p.suffix == ".csv":
                for m in re.finditer(r"^(T-\d+),(?:[^,\n]*,){4}([^,\n]+),", p.read_text(encoding="utf-8", errors="replace"), re.M):
                    out[m.group(1)] = m.group(2).strip()
            elif p.is_file() and re.fullmatch(r"P\d+\.md", p.name):
                m = re.search(r"^Participant:\s*([^|\n]+)", p.read_text(encoding="utf-8", errors="replace"), re.M)
                if m:
                    out[p.stem] = m.group(1).strip()
    return out


def source_items(scn: dict) -> dict[str, str]:
    """Text of each ticket (T-xx row) and interview (Pn file) in the scenario's fixtures."""
    items: dict[str, str] = {}
    for d in scn["fixtures"]:
        for p in sorted((FIXTURES / d).rglob("*")):
            if not p.is_file() or not is_text(p):
                continue
            if p.suffix == ".csv":
                for m in re.finditer(r"^(T-\d+),(.*)$", p.read_text(encoding="utf-8", errors="replace"), re.M):
                    items[m.group(1)] = m.group(2)
            elif re.fullmatch(r"P\d+\.md", p.name):
                items[p.stem] = p.read_text(encoding="utf-8", errors="replace")
    return items


def skill_contract_info(skill: str) -> tuple[list[str], list[str]]:
    text = (REPO / ".claude" / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
    _, body = v.parse(text)
    out = "\n".join(v.section(body, "Outputs"))
    prefixes = [m.split("<")[0] for m in re.findall(r"`(design/[^`]+)`", out)]
    return prefixes, v.skill_contract(body)[1]


def section_of(text: str, name: str) -> str:
    lines = text.split("\n")
    _, body = None, lines
    return "\n".join(v.section(body, name))


def mermaid_balanced(text: str) -> Optional[bool]:
    blocks = re.findall(r"```mermaid\n(.*?)```", text, re.S)
    if not blocks:
        return None
    pairs = {"]": "[", "}": "{", ")": "("}
    for b in blocks:
        stack = []
        for ch in b:
            if ch in "[{(":
                stack.append(ch)
            elif ch in pairs:
                if not stack or stack.pop() != pairs[ch]:
                    return False
        if stack:
            return False
    return True


def context(text: str, token: str, width: int = 70) -> str:
    i = text.find(token)
    return text[max(0, i - width): i + len(token) + width].replace("\n", " ") if i >= 0 else token


def run_checks(scn: dict, sandbox_new: dict[str, str], violations: list[str], response: str, run_date: str, harness: str = "") -> list[dict]:
    res: list[dict] = []

    def add(cid: str, status: str, text: str, detail: str = "") -> None:
        res.append({"id": cid, "status": status, "text": text, "detail": detail})

    skill = scn["skill"]
    prefixes, want = skill_contract_info(skill)
    deliverables = {p: t for p, t in sandbox_new.items() if p.startswith("design/") and p.endswith(".md")}
    main = {p: t for p, t in deliverables.items() if any(p.startswith(pre) for pre in prefixes)}
    n = len(deliverables)
    if scn["expect"] == "output":
        add("A1", "PASS" if main else "FAIL", "Expected a deliverable under this skill's output path",
            f"{len(main)} matching, {n} total new design files")
    elif scn["expect"] == "stop":
        add("A1", "PASS" if n == 0 else "FAIL", "Expected no deliverable (stop or hand off)", f"{n} new design files: {sorted(deliverables)}")
    else:
        add("A1", "N/A", "Deliverable optional (ask-one scenario)", f"{n} new design files")

    add("A2", "PASS" if not violations else "FAIL", "Wrote only under design/ and modified no input file", "; ".join(violations) or "clean")
    add("A3", "PASS" if response.strip() else "FAIL", "RESPONSE.md present and non-empty")

    all_text = "\n".join(list(deliverables.values()) + [response])
    corpus = fixture_corpus(scn)

    if main:
        path, text = sorted(main.items())[0]
        _, body = None, text.split("\n")
        got = [v.norm_heading(h) for h in v.headings(body)]
        add("A4", "PASS" if got == want else "FAIL", "Output headings match the skill's output contract",
            "" if got == want else f"expected {want}; got {got}")
        first = next((l for l in body if l.strip()), "")
        add("A5", "PASS" if first.startswith(f"> skill: {skill} ") or first.startswith(f"> skill: {skill} ") else "FAIL",
            "First line is the metadata block naming the skill", first[:120])
        nxt = section_of(text, "Next step")
        names = sorted({n_ for n_ in re.findall(r"`([a-z0-9-]+)`", nxt) if n_ in v.EXPECTED})
        add("A6", "PASS" if len(names) == 1 else "REVIEW", "Next step names exactly one skill", f"skills named: {names}")
        mb = mermaid_balanced(text)
        if mb is not None:
            add("A7", "PASS" if mb else "FAIL", "Mermaid blocks have balanced brackets")
    # dates
    date_re = re.compile(r"(?<!\d)\d{4}-\d{2}-\d{2}(?!\d)")
    allowed = set(date_re.findall(corpus + "\n" + scn["prompt"])) | {run_date}
    found = set(date_re.findall("\n".join(deliverables.values()) + "\n" + response + "\n" + "\n".join(deliverables)))
    bad = sorted(found - allowed)
    add("A8", "PASS" if not bad else "FAIL", "Every date is the run date or comes from the fixtures/prompt", f"unexpected dates: {bad}" if bad else "")
    # PII
    pii = json.loads((FIXTURES / "_pii.json").read_text(encoding="utf-8"))
    leaked = [p for p in pii if p.lower() in all_text.lower()]
    # a bare first name is also an identifier (case-sensitive whole word, from two-word capitalized entries)
    for p in pii:
        if re.fullmatch(r"[A-Z][a-z]+ [A-Z][a-z]+", p):
            first = p.split()[0]
            if re.search(rf"\b{first}\b", all_text) and first not in leaked:
                leaked.append(first)
    add("A9", "PASS" if not leaked else "FAIL", "No planted identifiers or irrelevant sensitive details appear in outputs", f"found: {leaked}" if leaked else "")
    # scenario regexes
    for rx in scn["must_match"]:
        ok = re.search(rx, all_text, re.I) is not None
        add("S+", "PASS" if ok else "FAIL", f"Scenario requires /{rx}/", "")
    for rx in scn["must_not_match"]:
        m = re.search(rx, all_text, re.I)
        add("S-", "PASS" if not m else "FAIL", f"Scenario forbids /{rx}/", context(all_text, m.group(0)) if m else "")
    for rx in scn.get("review_match", []):
        m = re.search(rx, all_text, re.I)
        add("S~", "PASS" if not m else "REVIEW", f"Scenario flags /{rx}/ for review (may be the user's claim quoted in a refusal)",
            context(all_text, m.group(0)) if m else "")
    # unsupported figures
    corp_norm = re.sub(r"\s+", " ", corpus.lower()) + " " + re.sub(r"\s+", " ", scn["prompt"].lower())
    flags = []
    for rx, kind in [(r"\d+(?:\.\d+)?\s?%", "percent"), (r"[$€£]\s?\d[\d,]*(?:\.\d+)?", "currency")]:
        for m in sorted(set(re.findall(rx, all_text))):
            tok = re.sub(r"\s+", "", m)
            if kind == "percent" and tok in FIGURE_ALLOWED:
                continue
            if re.sub(r"\s+", " ", m.lower()) in corp_norm or tok.lower() in corp_norm.replace(" ", ""):
                continue
            flags.append(f"{kind} {m!r}: {context(all_text, m)}")
    for m in re.finditer(r"\b(\d[\d,]*)\s+(users|customers|participants|respondents|tickets|interviews|sessions|downloads|orders|parcels|people)\b", all_text, re.I):
        if not re.search(rf"(?<![\w.]){re.escape(m.group(1))}(?![\w.])", corp_norm):
            flags.append(f"count {m.group(0)!r}: {context(all_text, m.group(0))}")
    add("A10", "PASS" if not flags else "REVIEW", "Figures (percent, currency, counts) trace to fixtures or prompt", " || ".join(flags))
    # quotes
    corp_words = norm_text(corpus + " " + scn["prompt"])
    qflags = []
    for m in re.finditer(r"[\"“]([^\"”\n]{20,220})[\"”]", all_text):
        q = m.group(1)
        if len(q.split()) >= 5 and norm_text(q) not in corp_words:
            qflags.append(q)
    add("A11", "PASS" if not qflags else "REVIEW", "Quoted passages of five or more words appear in the fixtures or prompt", " || ".join(qflags[:6]))
    # screening only: short (2 to 4 word) quoted phrases that no source contains (UI labels and code names also land here)
    sflags = sorted({m.group(1) for m in re.finditer(r"[\"“]([A-Za-z][^\"”\n]{5,40})[\"”]", all_text)
                     if 2 <= len(m.group(1).split()) <= 4 and norm_text(m.group(1)) not in corp_words})
    if sflags:
        add("A16", "REVIEW", "Short quoted phrases not found in the fixtures or prompt (grader checks they are not presented as source words)", " || ".join(sflags[:8]))
    # deterministic: a quote attributed to a source item ("words" (T-01), P3: "words") is word for word in that item
    items = source_items(scn)
    prose = re.sub(r"```mermaid.*?```", " ", all_text, flags=re.S)
    misquotes, attributed = [], 0
    for m in re.finditer(r"[\"“]([^\"”\n]{3,220})[\"”]", prose):
        after = re.match(r"\s{0,2}[(\[]\s*((?:T-\d+|P\d+)(?:\s*[,;]\s*(?:T-\d+|P\d+))*)", prose[m.end():m.end() + 40])
        # the ID list just before the quote, same line and table cell ("T-09 (", "P3 said ", "T-01, T-12 ")
        lead = re.split(r"[\n|]", prose[max(0, m.start() - 40):m.start()])[-1]
        before = re.search(r"(?<![\w-])((?:T-\d+|P\d+)(?:\s*,\s*(?:T-\d+|P\d+))*)\b[^\"“\w]{0,4}(?:said|says|wrote)?[^\"“\w]{0,3}$", lead)
        ids = re.findall(r"T-\d+|P\d+", after.group(1) if after else (before.group(1) if before else ""))
        ids = [i for i in ids if i in items]
        if not ids:
            continue
        attributed += 1
        q = f" {norm_text(m.group(1))} "
        # IDs written before the quote credit the words to each of them, so every one must contain them;
        # a list after the quote may be a theme's members, so at least one must contain them
        found = [q in f" {norm_text(items[i])} " for i in ids]
        if "/" in m.group(1) or not (any(found) if after else all(found)):
            misquotes.append(f"{m.group(1)} ({', '.join(ids)})")
    if attributed:
        add("A20", "PASS" if not misquotes else "FAIL",
            "Quotes attributed to a ticket or participant appear word for word in that source", " || ".join(misquotes[:8]))
    # screening only: an unattributed quote that nearly matches source wording (a paraphrase or merge in quotation marks)
    lines = [norm_text(l) for l in corpus.splitlines() if l.strip()]
    near = []
    for m in re.finditer(r"[\"“]([^\"”\n]{8,120})[\"”]", prose):
        qw = norm_text(m.group(1)).split()
        qn = " ".join(qw)
        if len(qw) < 3 or f" {qn} " in f" {corp_words} ":
            continue
        best = max((len(set(qw) & set(l.split())) / len(set(qw)) for l in lines), default=0)
        if best >= 0.75:
            near.append(m.group(1))
    if near:
        add("A21", "REVIEW", "Quoted text nearly matches a source but is not word for word (grader checks it is not shown as source words)",
            " || ".join(sorted(set(near))[:8]))
    # PF-N1 attempts 14 and 15: the stakeholder sentence is quoted once, and an `Our reading:` line carries no quotation marks
    deliv_text = "\n".join(deliverables.values())
    said = [m.group(1) for m in re.finditer(r"Stakeholder said:\s*[\"“]([^\"”\n]{8,300})[\"”]", deliv_text)]
    if said:
        repeats = [q for q in dict.fromkeys(said)
                   if len(re.findall(r"[\"“]" + re.escape(q.rstrip(".?!")), deliv_text)) > 1]
        add("A23", "PASS" if not repeats else "FAIL",
            "A stakeholder's exact sentence is put in quotation marks once in the deliverable", " || ".join(repeats[:4]))
    reading = [l.strip() for l in deliv_text.splitlines() if l.strip().startswith("Our reading:") and re.search(r"[\"“”]", l)]
    if "Our reading:" in deliv_text:
        add("A24", "PASS" if not reading else "FAIL",
            "`Our reading:` lines contain no quotation marks", " || ".join(x[:140] for x in reading[:4]))
    # CS-E1 attempts 11 to 13: audience stated; a stated body word count matches the defined body (Summary through Lessons)
    if skill == "case-study-writer" and main:
        cs_text = sorted(main.items())[0][1]
        add("A26", "PASS" if re.search(r"audience\s*:", cs_text, re.I) else "FAIL",
            "The intended audience is stated as `Audience:` (assumed or given)")
        mb = re.search(r"^## Summary\b.*?(?=^## Visuals to include\b)", cs_text, re.S | re.M)
        pat = (r"(?:\bbody\b|Summary (?:through|to) Lessons)[^.\n]{0,80}?(\d[\d,]*)\s*words"
               r"|(\d[\d,]*)\s*words[^.\n]{0,60}?(?:\bbody\b|Summary (?:through|to) Lessons)"
               r"|\bword count\b\D{0,12}(\d[\d,]*)")
        claims = []
        both = cs_text + "\n" + response
        for mm in re.finditer(pat, both, re.I):
            g = next(i for i in (1, 2, 3) if mm.group(i))
            st, en = mm.span(g)
            if (re.search(r"(?:\bto|[-\u2013])\s*$", both[max(0, st - 6):st], re.I) or re.match(r"\s*(?:words\s*)?(?:to|[-\u2013])\s*\d", both[en:en + 14], re.I)
                    or re.search(r"\b(?:target|default)\b", both[en:en + 20], re.I)):
                continue  # part of the 800 to 1200 default range, not a count of this body
            claims.append(int(mm.group(g).replace(",", "")))
        if mb and claims:
            actual = len(mb.group(0).split())
            bad = [c for c in claims if c != actual]
            add("A25", "PASS" if not bad else "FAIL",
                "A stated body word count equals the harness count (`## Summary` up to `## Visuals to include`, whitespace-separated)",
                f"claimed {claims}; counted {actual}")
    # closing signature: the reply ends with a blank line and one emoticon from the library (personality.md section 5);
    # a Figma line, when present, comes before the blank line
    exprs = closing_expressions()
    rl = response.rstrip().split("\n")
    last = rl[-1].strip() if rl and response.strip() else ""
    sig_ok = bool(exprs) and last in exprs and len(rl) >= 2 and rl[-2].strip() == "" and not any(e in "\n".join(rl[:-1]) for e in exprs if len(e) > 2)
    add("A27", "PASS" if sig_ok else "FAIL", "Reply ends with a blank line and exactly one library emoticon on its own final line",
        f"final line: {last[:60]!r}")
    # a false claim that the installed shared files are missing (the harness always installs _shared/)
    if harness:
        absent = re.findall(r"[^.\n]*\b(?:personality|figma)\.md\b[^.\n]{0,80}\b(?:absent|missing|not present|not found|not in the project|neither is in the project|neither was in the project|does not exist|did not exist)[^.\n]*", harness, re.I)
        if absent:
            add("A28", "FAIL", "HARNESS.md says a shared file was absent, but the harness installs `_shared/` in every sandbox", " || ".join(x.strip()[:140] for x in absent[:3]))
    # causal wording tagged observed: the cited source must state the cause (grader judges)
    causal = [l.strip() for l in all_text.splitlines()
              if re.search(r"\b(because|caused by|causes|due to|leads? to|so that|without it|results? in|tied to|as a result)\b", l, re.I)
              and re.search(r"\[observed|\bobserved\b", l, re.I)]
    if causal:
        add("A29", "REVIEW", "Causal wording sits on a line tagged observed (grader checks the cited source states the cause)",
            " || ".join(x[:150] for x in causal[:4]))
    # a fact credited to a named source file must be in that file
    fmap = {"roadmap": "roadmap.md", "readme": "README.md", "changelog": "CHANGELOG.md"}
    ffiles = fixture_files(scn)
    wrong = []
    for m in re.finditer(r"\b(roadmap|readme|changelog)\b[^.\n]{0,12}?\b(?:says|states|lists|records|shows|notes)\b[: ]+((?:[^.,;\n]|\.(?=\d)){3,90})", all_text, re.I):
        src = next((t for k, t in ffiles.items() if k.endswith(fmap[m.group(1).lower()])), None)
        if src is None:
            continue
        claim = m.group(2)
        toks = re.findall(r"\bv?\d+(?:\.\d+)+\b|\b\d+%", claim)  # versions and percentages only: high precision
        if not toks:
            continue
        sn = " " + norm_text(src) + " "
        miss = [t for t in toks if f" {norm_text(t)} " not in sn]
        if miss:
            wrong.append(f"{m.group(1)} -> {claim.strip()[:70]} (not in {fmap[m.group(1).lower()]}: {miss[:4]})")
    if wrong:
        add("A30", "FAIL", "A fact credited to the roadmap, README, or changelog appears in that file", " || ".join(wrong[:4]))
    # late-alert membership: each ticket or interview listed beside an alert claim states an alert or notification itself
    items = source_items(scn)
    badm = []
    skip = r"not counted|excluded|exclude|does not state|do not state|no alert|states no|state no|left out|not an alert|unclear|not enough"
    for l in all_text.splitlines():
        if re.search(skip, l, re.I):
            continue
        for km in re.finditer(r"\b(?:alerts?|notifications?)\b", l, re.I):
            tail = l[km.end(): km.end() + 70]
            gm = re.search(r"[\(\[]([^\)\]]*)[\)\]]", tail)
            grp = ""
            if gm and not re.search(r"[\(\[]", tail[:gm.start()]):
                grp = gm.group(1)
            elif not gm and re.search(r"\b(?:T-\d+|P\d+)\b", tail):  # unbracketed list in the same sentence
                grp = re.split(r"[.;]", tail)[0]
            else:  # keyword inside the group itself, e.g. (late alerts: T-02, T-08)
                near = re.search(r"[\(\[][^\)\]]*$", l[:km.start()])
                close = re.match(r"[^\)\]]*[\)\]]", l[km.start():])
                if near and close:
                    grp = near.group(0) + close.group(0)
            for tid in dict.fromkeys(re.findall(r"\b(T-\d+|P\d+)\b", grp)):
                if tid in items and not re.search(r"alert|notif|notice", items[tid], re.I):
                    badm.append(f"{tid} in: {l.strip()[:110]}")
    if badm:
        add("A31", "FAIL", "Every ID listed with an alert or notification claim states an alert or notification in its own words", " || ".join(badm[:4]))
    # strict member ID-level: every ID listed in a "could not find" count states it in its own words
    # (a person's interview that says "found it after scrolling" does not support listing P1; their ticket T-01 does)
    said_rx = re.compile(r"\b(cannot|can't|could not|couldn't|unable to)\s+(be\s+)?(find|found|see|seen|locate)", re.I)
    badid = []
    for ln in all_text.splitlines():
        cm = re.search(r"(could not|cannot|couldn't|can't|unable to) (find|locate)[^:\n]{0,40}:\s*\d+ (?:people|participants)\s*(?:[:\u2014\u2013-]|\()\s*((?:T-\d+|P\d+)(?:\s*(?:,|and)\s*(?:T-\d+|P\d+))*)", ln, re.I)
        if cm and not re.search(r"weaker|more|also|not stating|looking|lost|\bnot\b", ln[:cm.start(1)], re.I) \
                and not re.search(r"weaker|more|also", ln[cm.start(1):cm.start(3)], re.I):
            badid += [f"{i} listed but its own words do not say it" for i in re.findall(r"T-\d+|P\d+", cm.group(3))
                      if i in items and not said_rx.search(items[i])]
    if badid:
        add("A32", "FAIL", "Every source ID in a 'could not find' count states it in its own words (ticket versus interview ID)", " || ".join(badid[:4]))
    # more than one question put to the person in the chat reply (the HMW questions a skill shows are not asks)
    stripped = re.sub(r"```.*?```|`[^`\n]*`|\"[^\"\n]*\"|\u201c[^\u201d\n]*\u201d", " ", response, flags=re.S)
    asks = [ln.strip() for ln in stripped.splitlines()
            for q in re.findall(r"[^.?!\n]*\?", ln) if not re.search(r"how might we|\bHMW\b", q, re.I)]
    asks = [a for a in asks if a]
    # two requests joined inside one question sentence ("which artifacts did you author, and what prompted the rework?")
    for ln in stripped.splitlines():
        for q in re.findall(r"[^.?!\n]*\?", ln):
            if not re.search(r"how might we|\bHMW\b", q, re.I):
                asks += [q.strip()] * len(re.findall(r"\b(?:and|also)\s+(?:who|what|which|where|why|how|whether|when|was|were|is|are|do|does|did|can|could|should|would|will)\b", q, re.I))
    if len(asks) > 1:
        add("A33", "FAIL" if skill in ("case-study-writer", "problem-framing", "information-architect", "design-system-audit", "design-critique", "product-discovery") else "REVIEW",
            "The chat reply asks at most one question (standard section 8; hard failure for the skills repaired so far, review elsewhere)", " || ".join(a[:90] for a in asks[:5]))
    # problem framing: a `which causes` / `because` clause in the statement carries its own class tag on the same line
    if skill == "problem-framing" and main:
        ptxt = sorted(main.items())[0][1]
        gap = []
        for m in re.finditer(r"which causes [^\n]+", ptxt, re.I):
            sent = re.split(r"(?<=[a-z0-9\)])\.(?:\s|$)", m.group(0), 1)[0]
            if not re.search(r"\[(?:observed|reported|inferred|assumption)|unknown|no consequence|not documented|no source", m.group(0), re.I):
                gap.append(sent[:110])
        if gap:
            add("A34", "FAIL", "A `which causes` clause in the problem statement carries its own class tag (inferred, observed, reported, assumption) or is unknown", " || ".join(gap[:3]))
    # an [observed] line whose cited ID or file shares too few of its content words (grader checks the citation supports it)
    ffiles = fixture_files(scn)
    weakcite = []
    stop = {"which", "their", "there", "about", "these", "those", "would", "could", "should", "where", "when", "while", "other", "being", "users", "user"}
    for ln in all_text.splitlines():
        if not re.search(r"\[observed\]", ln):
            continue
        cited = [items[i] for i in dict.fromkeys(re.findall(r"\b(?:T-\d+|P\d+)\b", ln)) if i in items]
        cited += [t for k, t in ffiles.items() if re.search(re.escape(Path(k).name), ln)]
        claim = re.sub(r"`[^`]*`|\([^)]*\)|\[[^\]]*\]", " ", ln)
        toks = {w[:5] for w in re.findall(r"[a-z]{5,}", claim.lower()) if w not in stop}
        if cited and len(toks) >= 5:
            ctext = " ".join(cited).lower()
            hit = sum(1 for t in toks if t in ctext)
            if hit / len(toks) < 0.2:
                weakcite.append(f"{hit}/{len(toks)} words found: {ln.strip()[:100]}")
    if weakcite and skill == "problem-framing":
        add("A35", "REVIEW", "An [observed] line shares few words with the ID or file it cites (grader checks the citation supports it)", " || ".join(weakcite[:4]))
    # a reason for the work, or a claim that a shipped change addressed a problem, tagged observed or Verified
    # (no artifact in the fixtures records why the work was done; a negation on the same line is the correct form)
    if skill in ("case-study-writer", "problem-framing"):
        why = re.compile(r"\b(responded to|in response to|to address (?:the|that|this|these)|addresse?s? (?:that|this|the problem)|was reworked so|were reworked so|motivated by|the reason (?:was|for|is)|in order to (?:fix|solve|help))\b", re.I)
        neg = re.compile(r"not recorded|no artifact|does not record|do not record|no file states|no source states|not stated|unknown|\[TO VERIFY|\[inferred|\[assumption|interpretation", re.I)
        bad_why = [l.strip() for l in all_text.splitlines()
                   if why.search(l) and re.search(r"\[observed|\bVerified\b", l) and not neg.search(l)]
        if bad_why:
            add("A36", "FAIL", "A reason for the work, or a claim that a change addressed a problem, is not tagged observed or Verified (no artifact records the reason)",
                " || ".join(x[:140] for x in bad_why[:3]))
    # a person already in the strict could-not-find group used as a weaker example (through any of their IDs)
    if skill == "case-study-writer":
        ppl2 = person_of(scn)
        strict_p = {ppl2.get(i, i) for i, t_i in items.items() if said_rx.search(t_i)}
        wk_rx = re.compile(r"\b(?:weaker|separate and weaker)\b|\balso:", re.I)
        ok_rx = re.compile(r"already|exclu|not counted|not in the|same person as|people not|no one from|none of|supersed|counted in strict", re.I)
        clash = []
        for ln in all_text.splitlines():
            for sent in re.split(r"(?<=[.;])\s+", ln):
                if wk_rx.search(sent) and not re.search(r"people not in|not in the strict|from people not", sent, re.I):
                    ids = [i for i in dict.fromkeys(re.findall(r"\b(?:T-\d+|P\d+)\b", sent)) if i in items]
                    bad = [i for i in ids if ppl2.get(i, i) in strict_p and not said_rx.search(items[i])]
                    if bad and not ok_rx.search(sent.replace("same person as", "")) :
                        clash.append(f"{bad[0]} in: {sent.strip()[:110]}")
        if clash:
            add("A37", "FAIL", "A person in the strict could-not-find group is used as a weaker example through another of their IDs", " || ".join(clash[:3]))
    # information architect: the scope section carries a `User groups:` line (named groups or unknown)
    if skill == "information-architect" and main:
        itxt = sorted(main.items())[0][1]
        add("A38", "PASS" if re.search(r"user groups?\s*:", itxt, re.I) else "FAIL",
            "The information architecture states `User groups:` (named groups or unknown)")
    # a strict could-not-find count lists every person whose own source says so (counts cover the whole source),
    # unless it is written as a lower bound
    if "tickets.csv" in "".join(fixture_files(scn)) or any(re.fullmatch(r"P\d+\.md", Path(k).name) for k in fixture_files(scn)):
        ppl3 = person_of(scn)
        said_persons = {ppl3.get(i, i) for i, t_i in items.items() if said_rx.search(t_i)}
        short = []
        for ln in all_text.splitlines():
            cm = re.search(r"(could not|cannot|couldn't|can't|unable to) (find|locate)[^:\n]{0,40}:\s*(\d+) (?:people|participants)", ln, re.I)
            if cm and not re.search(r"weaker|more|also|not stating|looking|lost|\bnot\b", ln[:cm.start(1)], re.I) \
                    and not re.search(r"at least|lower bound|\+|partial", ln, re.I):
                if int(cm.group(3)) < len(said_persons):
                    short.append(f"{cm.group(3)} stated, fixtures hold {len(said_persons)}: {ln.strip()[:100]}")
        if short:
            add("A39", "FAIL", "A strict could-not-find count covers every person whose own source says so, or says it is a lower bound", " || ".join(short[:2]))
    # screening only: an omission note near a category word. Semantic privacy judgment stays with the grader.
    cats = r"(health|mobility|stairs|surgery|age|family|legal|divorce|medical|disabilit|personal circumstances)"
    om = [m.group(0) for m in re.finditer(r"[^.\n]*\b(left out|omitted|withheld|not recorded)\b[^.\n]*", all_text, re.I)
          if re.search(cats, m.group(0), re.I)]
    if om:
        add("A13", "REVIEW", "Omission wording sits next to a category word (screen only; grader judges)", " || ".join(o.strip()[:140] for o in om[:4]))
    # screening only: gendered pronouns used for people (participants are "they" or a code)
    gp = sorted({m.group(0).lower() for m in re.finditer(r"\b(he|she|him|her|hers|his|himself|herself)\b", all_text, re.I)})
    if gp:
        add("A14", "REVIEW", "Gendered pronouns appear (grader checks whether they refer to a participant)", ", ".join(gp))
    # screening only: question lines that join two asks with "or" (grader judges whether it is one idea)
    orq = [ln.strip()[:150] for txt in deliverables.values() for ln in txt.splitlines()
           if "?" in ln and re.search(r"\bor\b", ln) and re.match(r"\s*(\d+[.)]|[-*]|Q\d+|\|)", ln)]
    if orq and scn["skill"] == "interview-guide-builder":
        add("A15", "REVIEW", "Question lines containing a compound 'or' (grader checks single-idea questions)", " || ".join(orq[:5]))
    # screening only: age words (the standard bars restating an age or an age descriptor; grader judges the reference)
    ages = sorted({m.group(0).lower() for m in re.finditer(
        r"\b(older|elderly|seniors?|retired|retirees?|pensioners?|aged? \d+|\d+[- ]years?[- ]old)\b", all_text, re.I)})
    if ages:
        add("A17", "REVIEW", "Age words appear (grader checks they do not restate or imply a participant's age)", ", ".join(ages))
    # deterministic: an evidence age given in days must equal the run date minus the date it follows
    # adjacent pairs only, either order: "<date> (<n> days" or "<n> days (<date>)"
    ages_d = [(m.group(1), int(m.group(2))) for m in re.finditer(r"(\d{4}-\d{2}-\d{2})\)?\s*\(?(\d+) days", all_text)]
    ages_d += [(m.group(2), int(m.group(1))) for m in re.finditer(r"(\d+) days\s*\((\d{4}-\d{2}-\d{2})\)", all_text)]
    # table form: "<date> to <date> | <age> to <age>"
    for m in re.finditer(r"(\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2})\s*\|\s*(\d+) to (\d+)\b", all_text):
        ages_d += [(m.group(1), int(m.group(3))), (m.group(2), int(m.group(4)))]
    if ages_d:
        rd = date.fromisoformat(run_date)
        wrong = [f"{d}: {n} days, expected {(rd - date.fromisoformat(d)).days}" for d, n in ages_d
                 if (rd - date.fromisoformat(d)).days != n]
        add("A18", "PASS" if not wrong else "FAIL", "Evidence ages in days match their dates and the run date", " || ".join(wrong))
    # screening only: a "could not find/see" count must not list a ticket whose own text does not say so
    explicit = re.compile(r"\b(cannot|can't|could not|couldn't|unable to)\s+(be\s+)?(find|found|see|seen|locate)", re.I)
    bodies = {m.group(1): m.group(2) for m in re.finditer(r"^(T-\d+),[^,]*,[^,]*,[^,]*,([^,\n]*)", corpus, re.M)}
    weak = []
    for ln in all_text.splitlines():
        head = re.split(r"\b(?:weaker|had trouble|also)\b", ln, flags=re.I)[0]
        if explicit.search(head):
            weak += [f"{t} ({bodies[t]})" for t in re.findall(r"\bT-\d+\b", head) if t in bodies and not explicit.search(bodies[t])]
    if bodies and any(explicit.search(l) for l in all_text.splitlines()):
        add("A19", "PASS" if not weak else "REVIEW",
            "Tickets in a 'could not find/see' count say so themselves", " || ".join(sorted(set(weak))))
    # deterministic: count lines in the standard's form "<label>: N people — T-01, P3" (IDs only after the dash)
    # state the number of distinct people listed (ticket authors matched to interviewees); every member of a
    # "could not find" line has a source of their own that says so; a weaker or "more" line repeats nobody from that line
    people, items = person_of(scn), source_items(scn)
    ids_rx = r"(?:T-\d+|P\d+)"
    count_rx = rf"^[-*\s]*(.{{3,120}}?):\s*(\d+) (?:more )?people\s+—\s+({ids_rx}(?:,\s*{ids_rx})*)\s*\.?(?:\s*`?\[[^\]\n]*\]`?)*\s*$"
    bad_counts, seen_form = [], False
    for txt in list(deliverables.values()) + [response]:
        rows = [(m.group(1), int(m.group(2)), re.findall(ids_rx, m.group(3))) for m in re.finditer(count_rx, txt, re.M)]
        seen_form = seen_form or bool(rows)
        strict: set[str] = set()
        for label, n, ids in rows:
            who = {people.get(i, i) for i in ids}
            if len(who) != n:
                bad_counts.append(f"{label}: {n} people but {len(who)} distinct listed ({', '.join(ids)})")
            if re.search(r"could not find", label, re.I) and not re.search(r"weaker|more", label, re.I):
                strict |= who
                said = {people.get(i, i) for i, txt_i in items.items() if explicit.search(txt_i)}
                bad_counts += [f"{label}: {i} has no source that says it could not be found"
                               for i in ids if i in items and people.get(i, i) not in said]
        for label, n, ids in rows:
            if re.search(r"weaker|more", label, re.I) and strict & {people.get(i, i) for i in ids}:
                bad_counts.append(f"{label}: repeats a person already in the could-not-find count ({', '.join(ids)})")
    if seen_form:
        add("A22", "PASS" if not bad_counts else "FAIL",
            "Count lines state the number of distinct people listed, strict members say so themselves, and weaker groups repeat nobody",
            " || ".join(bad_counts[:6]))
    if scn["trap_tokens"]:
        hits = [f"{t}: {context(all_text, t)}" for t in scn["trap_tokens"] if t in all_text]
        add("A12", "PASS" if not hits else "REVIEW", "Planted claim tokens: check they are not asserted as fact", " || ".join(hits))
    return res


def sha_short(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:10] if path.is_file() else "unknown"


def fingerprint(files: dict[str, str]) -> str:
    return hashlib.sha256(json.dumps(sorted(files.items())).encode()).hexdigest()


def current_versions(skill: str) -> dict[str, str]:
    root = REPO / ".claude" / "skills"
    return {"standard_sha": sha_short(root / "_shared" / "standard.md"), "skill_sha": sha_short(root / skill / "SKILL.md")}


def write_meta(dest: Path, scn: dict, attempt: int, fp: str, std: str, skill_sha: str, source: str, run_date: str) -> None:
    meta = {"scenario": scn["id"], "attempt": attempt, "skill": scn["skill"], "fixtures": scn["fixtures"], "fingerprint": fp,
            "standard_sha": std, "skill_sha": skill_sha, "run_date": run_date, "source": source}
    (dest / "META.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")


def _parsable_json(path: Path) -> bool:
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True
    except Exception:
        return False


def collect(scn_id: str, sandbox: Path, manifest: Path, attempt: Optional[int], run_date: str) -> Optional[Path]:
    scn = get(scn_id)
    before = json.loads(manifest.read_text(encoding="utf-8"))
    after = file_hashes(sandbox)
    violations = []
    adapter_updates: list[str] = []
    for rel, h in before.items():
        if rel not in after:
            violations.append(f"deleted {rel}")
        elif after[rel] != h:
            # figma.md section 2: the adapter's own manifest under design/ is updated on every Figma run; a parsable
            # update is expected output, kept with the run, and any other modification stays a violation
            if rel == "design/figma.json" and _parsable_json(sandbox / rel):
                adapter_updates.append(rel)
            else:
                violations.append(f"modified {rel}")
    new = [r for r in after if r not in before]
    for rel in new:
        if rel not in ("RESPONSE.md", "HARNESS.md") and not rel.startswith("design/"):
            violations.append(f"wrote outside design/: {rel}")
    base = RUNS / scn_id
    base.mkdir(parents=True, exist_ok=True)
    fp_files = {rel: after[rel] for rel in new if rel in ("RESPONSE.md", "HARNESS.md") or rel.startswith("design/")}
    fp = fingerprint(fp_files)
    for mp in sorted(base.glob("attempt-*/META.json")):
        if json.loads(mp.read_text(encoding="utf-8")).get("fingerprint") == fp:
            print(f"DUPLICATE: {scn_id} sandbox already stored as {mp.parent.name}; nothing collected", file=sys.stderr)
            return None
    if attempt is None:
        existing = [int(p.name.split("-")[1]) for p in base.glob("attempt-*") if p.name.split("-")[1].isdigit()]
        attempt = max(existing, default=0) + 1
    dest = base / f"attempt-{attempt}"
    if dest.exists():
        # never overwrite a stored attempt: history and its verdict must stay traceable
        print(f"EXISTS: {scn_id} {dest.name} is already stored; nothing collected", file=sys.stderr)
        return None
    (dest / "output").mkdir(parents=True)
    texts = {}
    for rel in new + adapter_updates:
        src = sandbox / rel
        if rel in ("RESPONSE.md", "HARNESS.md"):
            shutil.copy2(src, dest / rel)
        elif rel.startswith("design/"):
            out = dest / "output" / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, out)
            if is_text(src):
                texts[rel] = src.read_text(encoding="utf-8", errors="replace")
    response = (sandbox / "RESPONSE.md").read_text(encoding="utf-8") if (sandbox / "RESPONSE.md").is_file() else ""
    harness_txt = (sandbox / "HARNESS.md").read_text(encoding="utf-8") if (sandbox / "HARNESS.md").is_file() else ""
    results = run_checks(scn, texts, violations, response, run_date, harness_txt)
    ver = current_versions(scn["skill"])
    write_meta(dest, scn, attempt, fp, sha_short(sandbox / ".claude" / "skills" / "_shared" / "standard.md"), ver["skill_sha"], "collect", run_date)
    (dest / "AUTO.json").write_text(json.dumps({"scenario": scn_id, "run_date": run_date, "checks": results}, indent=1), encoding="utf-8")
    lines = [f"# AUTO {scn_id} attempt {attempt}", "", f"Automated screening only. PASS here does not mean the scenario passed. Run date {run_date}.", "",
             "| Check | Status | What | Detail |", "|---|---|---|---|"]
    for r in results:
        lines.append(f"| {r['id']} | {r['status']} | {r['text']} | {r['detail'].replace('|', '/')[:600]} |")
    (dest / "AUTO.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return dest


# ---------------------------------------------------------------- docs
def latest_status() -> dict[str, tuple[str, int]]:
    out: dict[str, tuple[str, int]] = {}
    for d in sorted(RUNS.glob("*/attempt-*")):
        ev = d / "EVAL.md"
        sid = d.parent.name
        n = int(d.name.split("-")[1])
        if ev.is_file():
            m = re.search(r"^Status:\s*(PASS|FAIL|BLOCKED)", ev.read_text(encoding="utf-8"), re.M)
            if m and (sid not in out or n >= out[sid][1]):
                out[sid] = (m.group(1), n)
    return out


def backfill(scratch: Path) -> None:
    """Write META.json for attempts stored before metadata existed. Standard version comes from the installed
    copy in the matching sandbox when that sandbox still holds the same reply; otherwise it is `unknown`."""
    for scn in load_scenarios():
        for d in sorted((RUNS / scn["id"]).glob("attempt-*")) if (RUNS / scn["id"]).is_dir() else []:
            if (d / "META.json").is_file():
                continue
            files = {}
            for name in ("RESPONSE.md", "HARNESS.md"):
                if (d / name).is_file():
                    files[name] = hashlib.sha256((d / name).read_bytes()).hexdigest()
            out = d / "output"
            if out.is_dir():
                for p in sorted(out.rglob("*")):
                    if p.is_file():
                        files[str(p.relative_to(out))] = hashlib.sha256(p.read_bytes()).hexdigest()
            sbx = scratch / "sb" / scn["id"]
            same = (sbx / "RESPONSE.md").is_file() and (d / "RESPONSE.md").is_file() and \
                (sbx / "RESPONSE.md").read_bytes() == (d / "RESPONSE.md").read_bytes()
            std = sha_short(sbx / ".claude" / "skills" / "_shared" / "standard.md") if same else "unknown"
            write_meta(d, scn, int(d.name.split("-")[1]), fingerprint(files), std, "unknown", "backfill", "2026-11-01")


def quality() -> None:
    """Write QUALITY.md: seven dimensions per skill, each PASS, FAIL, PARTIAL, NOT TESTED, or BLOCKED.
    NOT TESTED is never PASS. A behavioral result counts as current only when the saved run used the present
    standard.md and the present SKILL.md; older passes are PARTIAL. Figma comes from figma_results.json (hand-recorded
    with node verification); a successful API call alone is not recorded as PASS."""
    scns = load_scenarios()
    skills = sorted({s["skill"] for s in scns})
    std_now = sha_short(REPO / ".claude" / "skills" / "_shared" / "standard.md")
    proc = subprocess.run([sys.executable, str(REPO / "tests" / "validate_skills.py")], capture_output=True, text=True)
    fail_lines = [l for l in proc.stdout.splitlines() if l.startswith("FAIL")]
    figma_path = HERE / "figma_results.json"
    figma = json.loads(figma_path.read_text(encoding="utf-8")) if figma_path.is_file() else {}

    def latest(sid: str) -> tuple[str, bool, bool]:
        runs = sorted((RUNS / sid).glob("attempt-*"), key=lambda p: int(p.name.split("-")[1])) if (RUNS / sid).is_dir() else []
        graded = [(r, re.search(r"^Status:\s*(PASS|FAIL|BLOCKED)", (r / "EVAL.md").read_text(encoding="utf-8"), re.M)) for r in runs if (r / "EVAL.md").is_file()]
        graded = [(r, m.group(1)) for r, m in graded if m]
        if not graded:
            return "NOT TESTED", False, False
        r, st = graded[-1]
        mp = r / "META.json"
        meta = json.loads(mp.read_text(encoding="utf-8")) if mp.is_file() else {}
        cur = meta.get("standard_sha") == std_now and meta.get("skill_sha") == sha_short(REPO / ".claude" / "skills" / get(sid)["skill"] / "SKILL.md")
        ever_failed = any(x == "FAIL" for _, x in graded)
        return st, cur, ever_failed

    def cell(sids: list[str]) -> str:
        res = [latest(i) for i in sids]
        if all(r[0] == "NOT TESTED" for r in res):
            return "NOT TESTED"
        if any(r[0] == "BLOCKED" for r in res):
            return "BLOCKED"
        passes = [r[0] == "PASS" for r in res]
        if all(passes) and all(r[1] for r in res):
            return "PASS"
        if not any(passes):
            return "FAIL"
        return "PARTIAL"

    by: dict[str, dict[str, str]] = {sk: {} for sk in skills}
    for sc in scns:
        by[sc["skill"]][sc["category"]] = sc["id"]
    lines = ["# Quality matrix", "",
             "Generated by `harness.py quality`. Statuses: PASS, FAIL, PARTIAL, NOT TESTED, BLOCKED. NOT TESTED is never PASS. "
             "A passing run counts as current only if it used the present `standard.md` and the present `SKILL.md`; an older pass is PARTIAL.", "",
             "| Dimension | Meaning here |", "|---|---|",
             "| Structural | `tests/validate_skills.py` reports no FAIL for the skill |",
             "| Behavioral | the four scenarios' latest graded runs pass on the current files |",
             "| Evidence | the evidence-integrity scenario's latest run passes on the current files |",
             "| Completeness | the normal scenario's latest run passes on the current files (required sections and content) |",
             "| Deliverable | no scenario grades practical usefulness as a critical criterion (G7 is non-critical): NOT TESTED unless recorded |",
             "| Figma | `figma_results.json`: a verified editable artifact; otherwise NOT TESTED |",
             "| Regression | a scenario that once failed now passes on the current files; NOT TESTED where no failure was ever recorded |", "",
             "| Skill | Structural | Behavioral | Evidence | Completeness | Deliverable | Figma | Regression |", "|---|---|---|---|---|---|---|---|"]
    for sk in skills:
        structural = "FAIL" if any(sk in l for l in fail_lines) else ("PASS" if proc.returncode == 0 else "PARTIAL")
        ids = [by[sk][c] for c in CATEGORIES]
        reg_ids = [i for i in ids if latest(i)[2]]
        regression = cell(reg_ids) if reg_ids else "NOT TESTED"
        fz = figma.get(sk, {}).get("status", "NOT TESTED")
        lines.append(f"| {sk} | {structural} | {cell(ids)} | {cell([by[sk]['evidence']])} | {cell([by[sk]['normal']])} | "
                     f"{figma.get(sk, {}).get('deliverable', 'NOT TESTED')} | {fz} | {regression} |")
    lines += ["", f"Current standard.md sha: `{std_now}`. Validator exit code: {proc.returncode}.", ""]
    (HERE / "QUALITY.md").write_text("\n".join(lines), encoding="utf-8")


def docs() -> None:
    scns = load_scenarios()
    status = latest_status()
    skills = sorted({s["skill"] for s in scns})
    by = {(s["skill"], s["category"]): s for s in scns}
    lines = ["# Behavioral test matrix", "",
             "Generated by `harness.py docs` from `scenarios.json`. Status comes from the latest graded run, or `not executed`.", "",
             "| Skill | Normal | Missing information | Evidence integrity | Edge or boundary |", "|---|---|---|---|---|"]
    for sk in skills:
        cells = []
        for c in CATEGORIES:
            s = by[(sk, c)]
            st = status.get(s["id"], ("not executed", 0))[0]
            cells.append(f"{s['id']} ({st})")
        lines.append(f"| `{sk}` | " + " | ".join(cells) + " |")
    (HERE / "MATRIX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (HERE / "scenarios").mkdir(exist_ok=True)
    for sk in skills:
        out = [f"# Scenarios: `{sk}`", "", "Generated from `scenarios.json`. Global criteria G1 to G7 in `README.md` apply to every run in addition to the critical criteria below.", ""]
        for c in CATEGORIES:
            s = by[(sk, c)]
            out += [f"## {s['id']}: {s['title']} ({c})", "",
                    f"- Fixtures: {', '.join('`' + f + '`' for f in s['fixtures'])}",
                    f"- Expected behavior: {s['expect']}",
                    "- User request:", "", "  > " + s["prompt"], "", "- Critical criteria (all must pass):"]
            out += [f"  - C{i + 1}. {t}" for i, t in enumerate(s["critical"])]
            if s["noncritical"]:
                out += ["- Non-critical criteria:"] + [f"  - {t}" for t in s["noncritical"]]
            if s["must_match"] or s["must_not_match"] or s["trap_tokens"] or s.get("review_match"):
                out.append("- Automated assertions:")
                out += [f"  - must match `{r}`" for r in s["must_match"]]
                out += [f"  - must not match `{r}`" for r in s["must_not_match"]]
                out += [f"  - flag for review if it matches `{r}`" for r in s.get("review_match", [])]
                out += [f"  - planted claim to review: `{t}`" for t in s["trap_tokens"]]
            if s["failure_modes"]:
                out.append("- Common failure modes: " + "; ".join(s["failure_modes"]))
            out.append("")
        (HERE / "scenarios" / f"{sk}.md").write_text("\n".join(out), encoding="utf-8")


def summary() -> None:
    scns = load_scenarios()
    counts = {"PASS": 0, "FAIL": 0, "BLOCKED": 0, "NOT EXECUTED": 0}
    rows, fails, history = [], [], []
    std_counts: dict[str, int] = {}
    cur_std = sha_short(REPO / ".claude" / "skills" / "_shared" / "standard.md")
    for s in scns:
        runs = sorted((RUNS / s["id"]).glob("attempt-*"), key=lambda p: int(p.name.split("-")[1])) if (RUNS / s["id"]).is_dir() else []
        statuses = []
        for r in runs:
            ev = r / "EVAL.md"
            m = re.search(r"^Status:\s*(PASS|FAIL|BLOCKED)", ev.read_text(encoding="utf-8"), re.M) if ev.is_file() else None
            statuses.append(m.group(1) if m else "UNGRADED")
        final = statuses[-1] if statuses and statuses[-1] != "UNGRADED" else ("NOT EXECUTED" if not statuses else "UNGRADED")
        counts[final] = counts.get(final, 0) + 1
        stds = []
        for r in runs:
            mp = r / "META.json"
            stds.append(json.loads(mp.read_text(encoding="utf-8")).get("standard_sha", "unknown") if mp.is_file() else "no-meta")
        std_latest = stds[-1] if stds else "-"
        std_counts[std_latest] = std_counts.get(std_latest, 0) + 1
        rows.append(f"| {s['id']} | `{s['skill']}` | {s['category']} | {final} | {len(statuses)} | {' → '.join(statuses) or '-'} | {std_latest} |")
        if final == "FAIL" and runs:
            ev = (runs[-1] / "EVAL.md").read_text(encoding="utf-8")
            fl = [l for l in ev.splitlines() if l.startswith("- [F]")]
            fails.append(f"- **{s['id']}**: " + " ".join(fl)[:700].rstrip())
        if len(statuses) > 1:
            history.append(f"- {s['id']}: {' → '.join(statuses)}")
    total = len(scns)
    out = ["# Behavioral results", "", "Generated by `harness.py summary` from graded runs in `runs/`. See `FINDINGS.md` for defects, fixes, and limitations.", "",
           f"Scenarios planned: {total}. Skills covered: {len({s['skill'] for s in scns})}.", "",
           "| Status | Count |", "|---|---|"] + [f"| {k} | {v_} |" for k, v_ in counts.items() if v_ or k in ("PASS", "FAIL", "BLOCKED", "NOT EXECUTED")]
    out += ["", f"Current standard: `{cur_std}`. Scenarios by the standard version their latest attempt ran against: " + ", ".join(f"`{k}`: {v_}" for k, v_ in sorted(std_counts.items())) + ". Only attempts with the same fingerprint are treated as duplicates, and `collect` refuses to store them.", "", "## Per scenario", "", "| ID | Skill | Category | Final | Attempts | Attempt history | Standard (latest attempt) |", "|---|---|---|---|---|---|---|"] + rows
    if fails:
        out += ["", "## Open failures", ""] + fails
    if history:
        out += ["", "## Reruns", ""] + history
    (HERE / "RESULTS.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(json.dumps(counts))


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare"); p.add_argument("id"); p.add_argument("--out", required=True); p.add_argument("--manifest", required=True)
    p = sub.add_parser("prompt"); p.add_argument("id"); p.add_argument("--sandbox", required=True)
    p = sub.add_parser("collect"); p.add_argument("id"); p.add_argument("--sandbox", required=True); p.add_argument("--manifest", required=True)
    p.add_argument("--attempt", type=int); p.add_argument("--run-date", default=date.today().isoformat())
    sub.add_parser("docs"); sub.add_parser("quality"); sub.add_parser("summary"); sub.add_parser("version")
    p = sub.add_parser("backfill"); p.add_argument("--scratch", required=True)
    a = ap.parse_args()
    if a.cmd == "prepare":
        prepare(a.id, Path(a.out), Path(a.manifest))
    elif a.cmd == "prompt":
        print(exec_prompt(a.id, Path(a.sandbox)))
    elif a.cmd == "collect":
        print(collect(a.id, Path(a.sandbox), Path(a.manifest), a.attempt, a.run_date))
    elif a.cmd == "version":
        print(json.dumps({"standard_sha": sha_short(REPO / ".claude" / "skills" / "_shared" / "standard.md")}))
    elif a.cmd == "backfill":
        backfill(Path(a.scratch))
    elif a.cmd == "docs":
        docs()
    elif a.cmd == "quality":
        quality()
    else:
        summary()


if __name__ == "__main__":
    main()
