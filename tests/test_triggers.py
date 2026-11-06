"""Static trigger checks for the 19 skill descriptions.

Claude picks a skill from its description, so these tests check the descriptions themselves:
every quoted trigger phrase belongs to exactly one skill, and requests that are easy to confuse
are named by the intended skill and by no sibling. This is a proxy: it does not run a model.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parent.parent / ".claude" / "skills"

# Requests that sit near a boundary between two skills, and the skill that should own each.
CONFUSABLE = {
    "map the flow": "user-flow-designer",
    "journey map": "journey-map-builder",
    "site map": "information-architect",
    "UX audit": "ux-audit",
    "critique this": "design-critique",
    "design QA": "design-qa",
    "frame the problem": "problem-framing",
    "plan research": "ux-research-planner",
    "interview guide": "interview-guide-builder",
    "usability test": "usability-test-planner",
}


def triggers() -> dict[str, list[str]]:
    out = {}
    for d in sorted(p for p in SKILLS.iterdir() if p.is_dir() and not p.name.startswith("_")):
        desc = re.search(r"^description:\s*(.+)$", (d / "SKILL.md").read_text(encoding="utf-8"), re.M).group(1)
        use_when = desc.split("Use when", 1)[-1].split("Not for", 1)[0]
        out[d.name] = [q.lower() for q in re.findall(r'"([^"]+)"', use_when)]
    return out


class Triggers(unittest.TestCase):
    def test_every_skill_lists_trigger_phrases(self) -> None:
        t = triggers()
        self.assertEqual(len(t), 19)
        for skill, phrases in t.items():
            self.assertGreaterEqual(len(phrases), 3, f"{skill}: fewer than three trigger phrases")

    def test_no_phrase_is_shared_by_two_skills(self) -> None:
        owners: dict[str, list[str]] = {}
        for skill, phrases in triggers().items():
            for p in phrases:
                owners.setdefault(p, []).append(skill)
        shared = {p: s for p, s in owners.items() if len(s) > 1}
        self.assertEqual(shared, {}, f"trigger phrases claimed by several skills: {shared}")

    def test_confusable_requests_route_to_one_skill(self) -> None:
        t = triggers()
        for request, want in CONFUSABLE.items():
            hits = [s for s, phrases in t.items() if any(request.lower() in p or p in request.lower() for p in phrases)]
            self.assertEqual(hits, [want], f"'{request}' should trigger only {want}, matched {hits}")


if __name__ == "__main__":
    unittest.main()
