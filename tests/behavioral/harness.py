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
1. The skill is installed in the user's project the way a real user installs it: the skill, plus the shared folder `.claude/skills/_shared/` in the project root. The skill cites `../_shared/standard.md`; read the installed copy at {sandbox}/.claude/skills/_shared/standard.md. Do not read any other file from the mjc-design-wizard repository: no docs/, tests/, examples/, or other skills. If the skill cites some other file that does not exist in the project, you cannot consult it. Handle that as a real assistant would.
2. The user is not available to answer. If the skill says to stop, stop and write your reply. If it says to ask one question, put that single question in your reply and continue only as the skill directs. Never wait for an answer.
3. Write deliverables only where the skill says (under design/ in the project root). Do not modify, rename, or delete any existing file.
4. Be honest. If you cannot do something (no browser, a missing file, no data), say so. Use the real current date from the shell (`date +%F`) where the skill needs a date.
5. Do not use mew-coder, GLM, or any other coding agent. Do not spawn further agents.
6. When finished, write your complete final reply to the user, exactly as you would give it, to {sandbox}/RESPONSE.md. Then write {sandbox}/HARNESS.md with: the activation method (skill-tool or file-read), the tools you used, and any difficulty or deviation. Then end with one short line.
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


def run_checks(scn: dict, sandbox_new: dict[str, str], violations: list[str], response: str, run_date: str) -> list[dict]:
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


def collect(scn_id: str, sandbox: Path, manifest: Path, attempt: Optional[int], run_date: str) -> Optional[Path]:
    scn = get(scn_id)
    before = json.loads(manifest.read_text(encoding="utf-8"))
    after = file_hashes(sandbox)
    violations = []
    for rel, h in before.items():
        if rel not in after:
            violations.append(f"deleted {rel}")
        elif after[rel] != h:
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
    for rel in new:
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
    results = run_checks(scn, texts, violations, response, run_date)
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
    sub.add_parser("docs"); sub.add_parser("summary"); sub.add_parser("version")
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
    else:
        summary()


if __name__ == "__main__":
    main()
