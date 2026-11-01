# Example: design-system-audit

> **Illustrative example.** All inputs and outputs below use invented sample data to show the output shape. Kettle is a fictional meal-kit subscription app; the files, values, and counts are hypothetical.

## Prompt

```
/design-system-audit Audit colors and buttons in src/. No Figma file.
```

## Sample input (invented)

`src/styles/tokens.css`:

```css
:root {
  --color-action-primary: #1E4FD8;
  --color-text: #1A1A1A;
  --color-text-muted: #6B7280;
  --color-surface: #FFFFFF;
}
```

Search results (`grep -rnoE "#[0-9A-Fa-f]{6}" src --include=*.tsx`):

```
src/components/Button.tsx:12:#1E4FD8
src/components/LinkButton.tsx:8:#1E4FD8
src/components/SkipWeek.tsx:21:#9AA0A6
src/components/SkipWeek.tsx:34:#9AA0A6
src/pages/Menu.tsx:47:#E53E3E
```

Search for token use (`grep -rnc "var(--color-" src --include=*.tsx`, non-zero lines): `Button.tsx:2`, `Banner.tsx:3`, `Deliveries.tsx:4`.

Components: `Button.tsx` (props `variant: "primary" | "secondary"`, `disabled`) and `LinkButton.tsx` (props `href`, renders an `<a>` styled like a primary button, comment: "for navigation, not actions"). No Storybook or usage docs.

## What the skill does

1. Locates tokens and components and records the paths scanned, excluded, and the commit (`version unknown` in this sample).
2. Counts tokenized and hardcoded color values from the recorded searches.
3. Classifies each difference: inconsistency, intentional variant (rationale found), or unclear.
4. Prioritizes recommendations with a severity and a separate confidence.

## Output shape (`design/audits/design-system-audit-<YYYY-MM-DD>.md`)

```markdown
> skill: design-system-audit · date: <YYYY-MM-DD> · scope: colors and buttons · paths scanned: src/styles/tokens.css, src/**/*.tsx · excluded: tests, node_modules · commit: version unknown · design source: none

## Scope and coverage
Colors and button components in `src/` [reported: user]. Covered: `.css` and `.tsx`. Not reached: inline styles built at runtime, third-party components. No design source, so design-to-code comparison is skipped.

## Token inventory and drift
| Token or value | Defined | Occurrences in .tsx | Files |
|---|---|---|---|
| `--color-action-primary` (#1E4FD8) | tokens.css | hardcoded 2 times | Button.tsx:12, LinkButton.tsx:8 |
| #9AA0A6 | Not a token | 2 | SkipWeek.tsx:21, SkipWeek.tsx:34 |
| #E53E3E | Not a token | 1 | Menu.tsx:47 |
Drift: #9AA0A6 is close to, but not equal to, `--color-text-muted` (#6B7280) [observed]. No error or danger token exists [observed: tokens.css].

## Component inventory and variants
| Component | Path | Variants and props | States | Usage docs |
|---|---|---|---|---|
| Button | src/components/Button.tsx | variant primary, secondary; disabled | disabled | none |
| LinkButton | src/components/LinkButton.tsx | href | none in code | comment only |

## Pattern inventory
Not in scope for this request (colors and buttons only).

## Design-to-code gaps
No design source supplied; comparison not done.

## Findings (classification, severity, confidence)
| id | Finding | Classification | Severity | Confidence |
|---|---|---|---|---|
| F1 | `--color-action-primary`'s value is hardcoded in Button.tsx and LinkButton.tsx instead of the token | Inconsistency: no rationale in code or docs | Cosmetic: same color today, no task impact | High |
| F2 | SkipWeek.tsx uses #9AA0A6 twice, near but not equal to `--color-text-muted` | Unclear: no comment explains it; question for the owner | Minor: lighter grey text may be harder to read [inferred; contrast not computed here] | High (value), Low (intent) |
| F3 | Menu.tsx uses #E53E3E with no error token | Inconsistency: no token covers the role | Cosmetic | Medium |
| F4 | LinkButton duplicates the primary Button's look | Intentional variant: the comment says it is for navigation, not actions | Cosmetic | Medium |

## Measures (counts with method)
- Hardcoded hex colors in .tsx: 5 occurrences, 3 distinct values (first search above).
- Lines using a color token in .tsx: 9 (2 + 3 + 4, second search above).
These are counts, not a score.

## Recommendations (prioritized)
1. Replace the hardcoded #1E4FD8 with `--color-action-primary` (F1). Low effort; prevents drift.
2. Ask the SkipWeek owner whether #9AA0A6 should be `--color-text-muted` or a new token (F2).
3. Add an error color token and use it in Menu.tsx (F3).
4. Document when to use LinkButton versus Button (F4).

## Open questions / to validate
- Is #9AA0A6 deliberate? (F2)
- Is an error color defined anywhere outside `src/`?

## Next step
Run `design-documentation` to document Button and LinkButton usage, since the only rationale today is a code comment.
```
