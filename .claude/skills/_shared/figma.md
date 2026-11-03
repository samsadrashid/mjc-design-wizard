# Figma output (shared adapter)

Optional. Skills whose Outputs section cites this file may also draw their result as editable objects in the project's Figma design file. The Markdown file is always written first and stays the source of truth. Figma never replaces it, and nothing here is required for a skill to work.

## 1. When Figma output runs

Figma output runs only when all of these hold. Otherwise write Markdown only and end with the matching `Figma: not used` line from §8.

1. `design/figma.json` exists and `publishing.enabled` is `true`. A connected Figma MCP is never permission to write.
2. The Figma MCP write tools (`use_figma`, `create_session`) are available in the session.
3. If `publishing.confirm_each_run` is `true` (the default), the user confirmed this run. Ask once, in one question. No answer means no write; report `Figma: not used (run not confirmed)`.

## 2. Project configuration: `design/figma.json`

Never store tokens, passwords, or account identifiers here. Authentication belongs to the MCP connection.

```json
{
  "schema_version": 1,
  "publishing": { "enabled": false, "confirm_each_run": true },
  "privacy": { "allow_quotes": false, "allow_participant_codes": true },
  "file": { "key": null, "url": null, "created_by_integration": false },
  "pages": {},
  "artifacts": {}
}
```

- `file.key`: the file the project publishes to. Take it from a URL or key the user supplies (`figma.com/design/<key>/...`).
- `pages`: skill name to page ID, filled as pages are created.
- `artifacts`: one entry per artifact key `<skill>/<topic>`: `{ "node_id", "page_id", "fingerprint", "source", "version" }`. `source` is the Markdown path the frame was drawn from.
- Write this file only under `design/`, like any other output. It may be committed, so it must hold no personal data.

## 3. Resolve the file

Use the Figma account the MCP is currently connected with. Never switch accounts. If no account is connected, or the user wants another one, say so and tell them to reconnect the Figma MCP with `/mcp`, then write Markdown only and report `Figma: not used (no Figma account connected)`.

A design file belongs to one project. Never point two projects' configurations at the same file.

1. Use `file.key` from the configuration, or a URL or key the user supplied in this run. Before writing, confirm access with a read-only call (`get_metadata` with the key). An error means the file does not exist or the account cannot edit it; the tool does not say which. Report `Figma: failed (file not found or no edit access)` and write Markdown only.
2. If there is none and publishing is enabled, create one with `create_new_file` (`editorType: "design"`, name `<project> — MJC Design Wizard`). Get plans with `whoami`: one plan, use it; several, ask the user which. Never share or change permissions.
3. Record the returned key, set `created_by_integration: true`, and say in the reply that a file was created.
4. If creation fails or is not possible, write Markdown only and tell the user how to supply an existing file: create a design file in Figma, then put its URL in `file.url` or `file.key`.

## 4. Pages

One design file per project. Each skill draws only on its own page, created the first time it writes. After every write, also create or update the index frame on the `Overview` page: an owned artifact with key `overview/index` that lists every manifest artifact with its page, frame name, and node ID. Create the `Overview` page if it does not exist. Find a page by stored ID, then by exact name; create it only if neither exists. In a file the integration created, the empty default `Page 1` may be renamed `Overview`.

| Skill | Page | Artifact topic (from the Markdown filename) |
|---|---|---|
| product-discovery | Product Discovery | `<topic>` |
| problem-framing | Problem Framing | `<topic>` |
| competitive-analysis | Competitive Analysis | `<scope>` |
| ux-research-planner | UX Research Plans | `<topic>` |
| interview-guide-builder | Interview Guides | `<topic>` |
| usability-test-planner | Usability Testing | `<topic>` |
| persona-builder | Personas | `<topic>` |
| journey-map-builder | Journey Maps | `<actor>-<scope>` |
| user-flow-designer | User Flows | `<task>` |
| information-architect | Information Architecture | `<scope>` |
| ux-audit | UX Audit | `<scope>` |
| design-system-audit | Design System Audit | `main` |
| design-qa | Design QA | `<feature>` |
| design-critique | Design Critiques | `<artifact>` |
| product-metrics | Product Metrics | `<goal>` |
| mvp-planner | MVP Planning | `<topic>` |
| feature-prioritization | Feature Prioritization | `<topic>` |
| design-documentation | Design Documentation | `spec-<feature>`, `component-<name>`, or `adr-<topic>` |
| case-study-writer | Case Studies | `<project>` |

## 5. Ownership, updates, and manual edits

**Artifact key.** `<skill>/<topic>`, where `<topic>` is the part of the Markdown filename named in the §4 table, without the date or a rerun suffix such as `-2`. On a rerun about the same subject, reuse the key already in the manifest for this skill; never invent a new key for the same subject.

An artifact frame is owned by this integration only when both hold:

- a node exists at the `node_id` stored for the artifact key, and
- that node's `getSharedPluginData("mjc", "artifact")` equals the artifact key.

Never identify ownership by name or by tag alone: a copy of a frame keeps the tag but gets a new ID. Do not use `setPluginData` (unsupported in this tool).

| Situation | Action |
|---|---|
| Publishing disabled or configuration missing | Markdown only. Report `Figma: not used (publishing disabled)`. In a project with no `design/figma.json`, the Figma line may be left out |
| Configuration unreadable (invalid JSON or unknown `schema_version`) | Markdown only. Report `Figma: not used (design/figma.json unreadable)` and say what to fix. Do not rewrite the file |
| Figma tools unavailable | Markdown only. Report `Figma: not used (tools unavailable)` |
| No file and creation not possible | Markdown only. Say how to supply a file. Report `Figma: not used (no design file)` |
| No artifact entry, or stored node missing | Create a new frame and record it |
| Owned, stored fingerprint has the `fp1:` prefix and equals the current one | No tracked edit. Update in place, but only within the non-destructive update rules below |
| Owned, fingerprint matches, but the update needs more than the non-destructive rules allow | A replacement. Ask the user to confirm it. Without confirmation, draw a new version from the Markdown |
| Owned but fingerprint differs (edited by hand) | Do not overwrite. Draw a new frame named `... v<n+1>` from the Markdown, never by cloning the edited frame, and record it |
| Stored fingerprint missing or lacks the current `fp1:` prefix | Unknown. Preserve the frame and ask the user to confirm a replacement. Without confirmation, draw a new version from the Markdown |
| Node at stored ID lacks the tag | Treat it as not owned. Create a new frame; leave that node alone |

**Non-destructive update rules.** The fingerprint covers only the properties in the function below, so a matching fingerprint does not prove the frame is unchanged: an edit to corner radius, effects, gradients, stroke weight, constraints, or auto-layout settings is not detected. An in-place update may therefore only change the characters of existing text nodes and append new nodes. It never deletes, recreates, reorders, or restyles existing nodes, and never sets any other property on an existing node, so an undetected manual edit is never overwritten. If the new Markdown needs anything else (for example removing a finding card), that is a replacement: ask first. Every new version is drawn from the Markdown, never cloned from an earlier frame.

Never change, move, or delete anything outside owned frames. Deleting anything, owned or not, needs the user's explicit confirmation.

**Fingerprint.** Compute it with this exact function, pasted unchanged into the `use_figma` script, after every write; store the returned string. Moving the whole frame does not count as an edit; any change inside it does.

```js
// MJC fingerprint fp1. Paste unchanged.
const fp1 = (root) => {
  const r = v => Math.round(v);
  const col = ps => Array.isArray(ps) ? ps.filter(p => p.type === "SOLID" && p.visible !== false).map(p => [p.color.r, p.color.g, p.color.b].map(c => c.toFixed(3)).join(",")).join("|") : "";
  const snap = (n, top) => {
    const o = [n.type, n.name, top ? 0 : r(n.x), top ? 0 : r(n.y), r(n.width), r(n.height), "opacity" in n ? n.opacity.toFixed(2) : "", n.visible ? 1 : 0, col(n.fills), col(n.strokes)];
    if (n.type === "TEXT") o.push(n.characters, typeof n.fontSize === "number" ? n.fontSize : "mixed", n.fontName && n.fontName.family ? n.fontName.family + " " + n.fontName.style : "mixed");
    if ("children" in n) o.push(n.children.map(c => snap(c, false)));
    return o;
  };
  const s = JSON.stringify(snap(root, true));
  let h = 0x811c9dc5;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; }
  return "fp1:" + h.toString(16).padStart(8, "0");
};
```

Properties outside this list (corner radius, effects, gradients, stroke weight, constraints, auto-layout settings) are not tracked. The non-destructive update rules above keep such edits from being overwritten; they do not make them detectable.

## 6. Drawing conventions

- Before any `use_figma` call, load the Figma `figma-use` guidance (the `/figma-use` skill, or the `skill://figma/figma-use/SKILL.md` resource). Call `create_session` once per run with the file key. The `figma-generate-design` guidance is not needed: these frames document findings and do not compose product screens from a design system.
- Wrap each artifact in one frame named `mjc · <skill> · <topic> · <date>`, tagged with `setSharedPluginData("mjc", "artifact", "<skill>/<topic>")`. Place new frames to the right of existing content, never at (0,0).
- Draw the representation the skill's Outputs line names, not a copy of the Markdown as one text block. Keep every evidence tag, confidence level, severity, and label such as `[assumption]`, `Not observed`, `Missing`, `Provisional`, or `[TO VERIFY]` visible on the frame. Never drop uncertainty to make a frame look cleaner.
- Use editable text, frames, and shapes. Never place a screenshot or flattened image of the output. Images cannot be added by this tool; cite evidence by path instead.
- Flows: nodes are shapes with text labels (named `node:<id>`); connections are vectors with an arrow end cap (named `edge:<from>-><to>`). Connector objects are not available in design files.
- Do not create or modify variables, styles, or components in the file.
- Return every created and changed node ID from each call, then read back counts and IDs to confirm before reporting.

## 7. Privacy

Figma files are shared more widely than a repository. Apply the standard's privacy rules (`standard.md` §8) to everything drawn. Use participant codes only if `privacy.allow_participant_codes` is `true`. Draw no verbatim quotes unless `privacy.allow_quotes` is `true`. Never draw names, contact details, or sensitive categories.

## 8. Reporting

When `design/figma.json` exists, make one line the last content of the chat reply, stating only what a tool response confirmed. A closing emoticon from `personality.md` §5, if any, follows it after one blank line:

- `Figma: created <n> frames on <page> (<file URL>)` or `Figma: updated <frame> on <page>`
- `Figma: new version <frame> v<n> created; the earlier frame was edited by hand and left unchanged`
- `Figma: new version <frame> v<n> created; replacement not confirmed, the earlier frame was left unchanged`
- `Figma: not used (publishing disabled)`
- `Figma: not used (design/figma.json unreadable)`
- `Figma: not used (tools unavailable)`
- `Figma: not used (run not confirmed)`
- `Figma: not used (no Figma account connected)`
- `Figma: not used (no design file)`
- `Figma: failed (file not found or no edit access)`
- `Figma: failed after <step>; Markdown written; nodes written before the failure: <IDs or none>`

Copy a `not used` line exactly as written; do not reword the reason in parentheses. Explanations go in a separate sentence before it. Use the first new-version line only when the fingerprint differed; for an unconfirmed replacement or an unknown fingerprint, use the second.

If a `use_figma` call fails, follow its `safeToRetryWithoutCanvasRead` flag. If it still fails, stop the Figma part; the Markdown output is unaffected.

## 9. Capability evidence

All live runs used one dedicated scratch design file and synthetic data. No real project file was used.

| Evidence type | What it covers |
|---|---|
| Automated validator (all 19 skills) | Each skill cites this file, names its mapped page, takes its artifact topic from its output filename, keeps the Markdown-first line, has an adapter quality check, states what it never draws, and calls no Figma tool directly. This file keeps the default-off config, the decision table, the exact `fp1` function, the non-destructive rules, and fixed `not used` lines. These checks read instructions; they do not prove a model follows them. |
| Simulated failures (pilot) | Malformed `design/figma.json`, a placeholder file key (the tool returned an access error), and Figma tools withheld from the run. A real disconnected MCP was not tested. |
| Live, publishing on, with independent read-back (8 skills) | `ux-audit`, `user-flow-designer`, `design-system-audit`, `feature-prioritization`, `persona-builder`, `information-architect`, `competitive-analysis`, `mvp-planner` (after its exclusion rule was added: every candidate traced to the Markdown and roadmap, no invented dates or effort). Each read-back confirmed the page, the tag, a fingerprint equal to the manifest, editable text, frames, and shapes (flows and trees as shapes with arrow vectors), uncertainty labels visible, no image fills, and no variables, styles, or components created. The planted-personal-data check ran on the pilot runs and `persona-builder` only. Every earlier frame's fingerprint was compared and unchanged for every run after `feature-prioritization`; that run was not compared. |
| Live, publishing off (7 skills) | `ux-audit`, `user-flow-designer`, `design-system-audit`, `feature-prioritization`, `persona-builder`, `product-metrics`, `design-critique`: Markdown written, manifest unchanged, no Figma calls. The first `design-critique` reply reworded the reason in its `not used` line; after §8 was fixed, a rerun ended with exactly `Figma: not used (publishing disabled)` and its transcript shows no Figma tool calls. |
| Manual-edit and replacement safety | Rollout (`mvp-planner`): a corner-radius edit left `fp1` unchanged; the rerun took the in-place row, changed one text node, kept all 64 node IDs, and the radius read back unchanged. Pilot skills: A tracked edit was detected and a new version drawn from the Markdown with the edited frame untouched; an untracked corner-radius edit was not detected and survived a rerun; an unconfirmed replacement left the earlier frame intact and drew a new version; a rerun with no edit updated in place with no duplicate. The confirmed-replacement path was not run. |
| Visual checks (2 frames) | Rendered screenshots of the `competitive-analysis` and `mvp-planner` frames: no clipped text, clear hierarchy, uncertainty labels visible and matching the Markdown. Cosmetic issues: uneven panel widths, and slices and risks drawn as plain lines rather than cards. The other frames were not reviewed visually. |

Validator only, never run live: `product-discovery`, `problem-framing`, `usability-test-planner`, `interview-guide-builder`, `ux-research-planner`, `journey-map-builder`, `design-qa`, `design-documentation`, `case-study-writer`.

Not live-tested at all: file creation by the adapter (the README setup describes it, but it has never run), the `run not confirmed`, `no Figma account connected`, and `no design file` reporting lines, a confirmed replacement, reruns and manual edits on 15 of the 16 rollout skills, the exclusion sentences on 6 of the 7 earlier skills, a real disconnected MCP, rate limits, very large artifacts, and concurrent editing.
