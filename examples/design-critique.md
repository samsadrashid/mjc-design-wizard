# Example: design-critique

> **Illustrative example.** All inputs and outputs below use invented sample data to show the output shape. Kettle is a fictional meal-kit subscription app; the mockup and feedback are hypothetical.

## Prompt

```
/design-critique Feedback on design/screens/deliveries-mockup.md. Goal: subscribers can skip next week without help. Direction first, please.
```

## Sample input (invented)

`design/screens/deliveries-mockup.md` describes one mobile screen:

- Header "Deliveries", then a full-width promo banner "Try our new desserts" (about a third of the screen height).
- A list of four upcoming weeks. Each row: week label, three recipe thumbnails, and a text link "Skip" aligned right in grey.
- Under the list, a line of small grey text: "Changes close at the weekly cutoff."
- A primary button at the bottom: "Add extras".
- No error, loading, past-cutoff, or empty state is described.

Repo: `src/styles/tokens.css` defines `--color-action-primary` and `--color-text-muted`. The persona doc names Persona A, a week-by-week skipper who cannot find skip today.

## What the skill does

1. Reads the persona and tokens and uses them as the baseline.
2. Describes the mockup before judging it, including what it does not show.
3. Writes each item about a named element: risks get a severity and a separate confidence; preferences are marked as opinion.
4. Suggests directions with trade-offs, without redesigning the screen.

## Output shape (`design/audits/design-critique-deliveries-mockup-<YYYY-MM-DD>.md`)

```markdown
> skill: design-critique · date: <YYYY-MM-DD> · scope: deliveries mockup (description only) · sources: design/screens/deliveries-mockup.md, src/styles/tokens.css, design/research/personas-kettle-subscribers-<YYYY-MM-DD>.md

## Goal, audience, and basis
Goal: subscribers can skip next week without help [reported: user]. Audience: Persona A, week-by-week skipper [observed: persona doc]. Basis: the written mockup description only; no image, so sizes and contrast are not measurable. Feedback wanted: direction first [reported: user].

## What the design shows
A Deliveries header, a promo banner, a list of four weeks with a grey "Skip" text link on each row, a small grey cutoff note under the list, and an "Add extras" primary button [observed: mockup]. Not shown: past-cutoff, skipped, loading, error, and empty states.

## What works
- Skip sits on each week, where the week is shown; this matches the persona's pain of not finding skip [observed: persona doc] [inferred].

## Findings: usability and accessibility risks
| Element | Risk | Why it matters | Severity | Confidence | Direction and trade-off |
|---|---|---|---|---|---|
| "Skip" text link | Low visual weight for the screen's main task | The goal is skipping; a grey text link competes with the primary "Add extras" button (hierarchy) | Major | Medium: inferred from the description | Give Skip a visible control style; trade-off: adds weight to every row |
| Cutoff note | Cutoff time not stated and placed after the list | Persona A was charged after missing the cutoff [observed: persona doc, P2]; users read rows before the note | Major | Medium | Show the cutoff time on each row; trade-off: more text per row |
| Promo banner | Pushes the week list down on a small screen | The task content starts below a third of the screen [observed: mockup] | Minor | Low: no measured height | Shrink or move the banner below the list; trade-off: lower promo visibility |
| Grey text (link and note) | Possible low contrast | `--color-text-muted` is used for both [inferred: tokens.css]; ratio not computed, values not given | Minor | Low | Check the ratio against 4.5:1 before build |

## Observations: preference
- Opinion: three recipe thumbnails per row may be more than needed to recognize a week. No severity; a matter of taste.

## Missing states and edge cases
- Past cutoff: what Skip does after the cutoff.
- Skipped week: how a skipped row looks and how to undo it.
- Loading and error when skipping.
- No upcoming weeks (empty list).

## Open questions / to validate
- Is the banner required by marketing on this screen?
- What is the cutoff rule per week?

## Next step
Run `usability-test-planner` to test whether subscribers find and complete Skip on this screen.
```
