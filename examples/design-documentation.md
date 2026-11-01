# Example: design-documentation

> **Illustrative example.** All inputs and outputs below use invented sample data to show the output shape. Kettle is a fictional meal-kit subscription app; the files, props, tokens, and decisions are hypothetical.

## Prompt

```
/design-documentation Write the spec for skipping a delivery week. The flow is design/journeys/user-flow-skip-week-<YYYY-MM-DD>.md and the component is src/components/SkipWeek.tsx. We chose a confirmation dialog over an undo toast because billing runs at the cutoff.
```

## Sample input (invented)

- Flow doc (approved by the product owner, per its metadata): Deliveries list → Skip week → confirm dialog → week shows "Skipped". Branches: past cutoff, network error.
- `src/components/SkipWeek.tsx`:

```tsx
type SkipWeekProps = {
  weekId: string;
  cutoffAt: string;      // ISO timestamp
  onSkip: (weekId: string) => Promise<void>;
  disabled?: boolean;
};
```

- `src/styles/tokens.css` defines `--color-action-primary`, `--color-text-muted`, `--space-2`, `--space-3`, `--radius-md`, `--font-body`. No token exists for a danger or warning color.
- The component sets `min-height: 40px` as a raw value.
- No loading copy, no rule for household members, and no responsive layout are defined anywhere.

## What the skill does

1. Reads the flow, the component props, and `tokens.css`. Records the commit as `version unknown` (no git metadata in this sample).
2. Chooses type `spec` from the request and fills all 13 headings, marking each statement approved, inferred, recommended, or unavailable.
3. Uses token names from the repo and flags the one raw value.
4. Records the decision and reason the user gave, with approver unknown.

## Output shape (`design/docs/spec-skip-week-<YYYY-MM-DD>.md`)

```markdown
> skill: design-documentation · date: <YYYY-MM-DD> · type: spec · status: draft · scope: skip a delivery week · sources: design/journeys/user-flow-skip-week-<YYYY-MM-DD>.md (approved, product owner), src/components/SkipWeek.tsx, src/styles/tokens.css · version: unknown

## Purpose and status
Lets a subscriber skip one upcoming delivery before its billing cutoff. Status: draft; not yet reviewed by engineering. [Approved: flow doc, product owner]

## Context
Subscribers skip single weeks from the Deliveries list [Approved: flow doc]. Whether skip findability is a problem today is not established in this spec [Unavailable: no linked research]. No usability claim is made here.

## Scope and out of scope
- In scope: skipping one upcoming week; the past-cutoff and network-error branches [Approved: flow doc].
- Out of scope: pausing for several weeks, recipe changes, refunds [Inferred: not in the flow doc].

## Flows and expected behavior
Flow: see the linked flow doc; not redrawn here.
1. Trigger: the subscriber selects "Skip week" on an upcoming week [Approved: flow doc].
2. A confirmation dialog states the week and the cutoff time [Approved: flow doc; the decision is recorded below].
3. On confirm, `onSkip(weekId)` is called [Inferred: SkipWeek.tsx]. On success the week shows "Skipped" [Approved: flow doc].
4. Past the cutoff, the control is unavailable and the cutoff is explained [Approved: flow doc]. Exact copy: Unavailable: no copy supplied.
5. Network error: the dialog stays open with a retry [Approved: flow doc]. Copy: Unavailable: no copy supplied.

## Components, variants, and props
| Component | Prop | Type | Required | Source |
|---|---|---|---|---|
| SkipWeek | `weekId` | string | yes | [Inferred: SkipWeek.tsx] |
| SkipWeek | `cutoffAt` | ISO timestamp string | yes | [Inferred: SkipWeek.tsx] |
| SkipWeek | `onSkip` | `(weekId) => Promise<void>` | yes | [Inferred: SkipWeek.tsx] |
| SkipWeek | `disabled` | boolean | no | [Inferred: SkipWeek.tsx] |
Variants: none defined in code [Inferred: SkipWeek.tsx]. A confirmation dialog component: Unavailable: no shared dialog found in the repo.

## Tokens and references
- Action color `--color-action-primary`; helper and cutoff text `--color-text-muted`; spacing `--space-2`, `--space-3`; corner radius `--radius-md`; type `--font-body` [Inferred: tokens.css].
- Control height `40px` is a raw value with no token [Inferred: SkipWeek.tsx]. Flagged.
- Warning color for the past-cutoff message: Unavailable: no token exists.

## States (interaction, loading, empty, error, permission)
| State | Behavior | Mark |
|---|---|---|
| Default | "Skip week" enabled before cutoff | [Approved: flow doc] |
| Hover, focus | Unavailable: not specified | — |
| Disabled | Past cutoff; `disabled` prop | [Inferred: SkipWeek.tsx] |
| Loading | While `onSkip` resolves; copy and indicator Unavailable | — |
| Empty | No upcoming weeks: Unavailable: not specified in the flow | — |
| Error | Network error keeps the dialog open with retry | [Approved: flow doc] |
| Permission | Unavailable: whether household members can skip is not defined | — |

## Accessibility and responsive requirements
- Target: WCAG 2.2 AA [Recommended: default; no requirement supplied].
- The dialog moves focus into itself and returns it to the trigger on close [Recommended].
- Control height of 40px meets the 24px minimum of 2.5.8 [Inferred: raw value in code].
- Responsive layout: Unavailable: no breakpoints defined.

## Implementation notes and sources
- `onSkip` returns a promise; the UI waits for it before showing "Skipped" [Inferred: SkipWeek.tsx type].
- `cutoffAt` is an ISO timestamp; its time zone handling is unknown [Unavailable: no source].
- Sources: listed in the metadata block.

## Decisions, assumptions, and dependencies
| Decision | Alternatives | Reason | Evidence | Status |
|---|---|---|---|---|
| Confirm with a dialog before skipping | Undo toast after skipping | Billing runs at the cutoff, so an undo could fail after billing | [reported: user, in the request] | Approved, approver unknown |
Assumptions: the cutoff is enforced server side [assumption].
Dependencies: billing service cutoff behavior; a shared dialog component.

## Handoff checklist
- [x] Props match `SkipWeek.tsx`
- [x] Token names match `tokens.css`; one raw value flagged
- [ ] Copy for past-cutoff, loading, and error states supplied
- [ ] Household-member permission rule decided
- [ ] Hover and focus styles specified
- [ ] Responsive layout defined

## Open questions / to validate
- Can household members skip a week?
- What time zone does `cutoffAt` use in the UI?
- Who approved the dialog decision?
- Should 40px become a token?

## Next step
Run `design-qa` to verify the build against this spec once the open copy and permission items are filled.
```

## Same contract, other document types

A decision record (`design/docs/adr-<topic>-<YYYY-MM-DD>.md`, `type: decision-record`) keeps all 13 headings. It fills Purpose and status, Context, and Decisions in depth and writes, for example:

```markdown
## Components, variants, and props
Not applicable: a decision record documents a choice, not a component.
```

A component doc fills components, tokens, states, and accessibility in depth and writes `Not applicable: <reason>` under Flows and expected behavior.
