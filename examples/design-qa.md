# Example: design-qa

> **Illustrative example.** All inputs and outputs below use invented sample data to show the output shape. Kettle is a fictional meal-kit subscription app; the spec, code, and mismatches are hypothetical.

## Prompt

```
/design-qa Check the skip-week build against design/docs/spec-skip-week-<YYYY-MM-DD>.md. Code is src/components/SkipWeek.tsx; mobile screenshot in qa/skip-mobile.png.
```

## Sample input (invented)

- Reference: `design/docs/spec-skip-week-<YYYY-MM-DD>.md`, metadata `status: approved`, approver: product owner. It specifies: Skip control min height 44px; label color `--color-text-muted`; confirmation dialog title "Skip this week?"; cutoff shown on each row. It defines no hover state and no tablet layout.
- Build: `src/components/SkipWeek.tsx` sets `min-height: 40px` and `color: #9AA0A6`; dialog title string "Skip week?". `src/styles/tokens.css` defines `--color-text-muted: #6B7280`.
- `qa/skip-mobile.png`: the list at 375px wide; the cutoff text appears under each row; spacing between rows looks wider than the spec's `--space-3` (not measurable from the image).

## What the skill does

1. Reads the approved spec, the component, and tokens. Records the reference version and `version unknown` for the build.
2. Builds the coverage matrix and marks unprovided cells not checked.
3. Logs mismatches only where the spec gives the expected value and the code shows the actual value.
4. Keeps image-based estimates unverified and lists spec gaps separately.

## Output shape (`design/audits/design-qa-skip-week-<YYYY-MM-DD>.md`)

```markdown
> skill: design-qa · date: <YYYY-MM-DD> · scope: skip week, mobile · reference: design/docs/spec-skip-week-<YYYY-MM-DD>.md (approved, product owner) · build: src/components/SkipWeek.tsx, qa/skip-mobile.png · commit: version unknown

## Coverage matrix (screen × breakpoint × state)
| Screen | Breakpoint | Default | Hover | Focus | Disabled | Loading | Empty | Error |
|---|---|---|---|---|---|---|---|---|
| Deliveries list | 375px | checked | not defined in spec | not provided | not provided | not provided | not provided | not provided |
| Skip dialog | 375px | checked (code only) | not defined in spec | not provided | not applicable | not provided | not applicable | not provided |
| Any screen | tablet, desktop | not provided | | | | | | |

## Verified mismatches (defect log)
| id | Screen | Breakpoint | Element | Expected (source) | Actual (evidence) | Type | Severity | Confidence | Repro |
|---|---|---|---|---|---|---|---|---|---|
| Q1 | Deliveries list | 375px | Skip control height | min-height 44px (spec, Tokens section) | `min-height: 40px` (SkipWeek.tsx) | Layout | Minor | High | Open SkipWeek.tsx; read the style block; compare with the spec |
| Q2 | Deliveries list | 375px | Skip label color | `--color-text-muted` = #6B7280 (spec; tokens.css) | `color: #9AA0A6` (SkipWeek.tsx) | Color and tokens | Minor | High | Open SkipWeek.tsx; find the color; compare with tokens.css |
| Q3 | Skip dialog | 375px | Dialog title | "Skip this week?" (spec, Flows section) | "Skip week?" (SkipWeek.tsx) | Copy | Cosmetic | High | Search SkipWeek.tsx for the title string |

## Unverified or ambiguous differences
- Row spacing looks wider than `--space-3` in qa/skip-mobile.png. Unverified: the image gives no pixel measurement; needs computed styles from a running build.

## Spec gaps found
- Hover state for the Skip control is not defined in the spec.
- Tablet and desktop layouts are not defined.
These are spec defects, not build defects.

## Summary by severity and screen
- Deliveries list: 2 Minor (Q1, Q2).
- Skip dialog: 1 Cosmetic (Q3).
- 1 unverified difference; 2 spec gaps.

## Not checked
- Focus, disabled, loading, empty, and error states: not provided in the build material.
- Tablet and desktop: not provided.
- Motion and screen reader output: not inspectable from code and one image.

## Open questions / to validate
- Is a running build available to measure spacing and states?
- Should hover and larger breakpoints be added to the spec?

## Next step
Run `design-documentation` to close the two spec gaps before the next QA pass.
```
