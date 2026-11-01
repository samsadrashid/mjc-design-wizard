# Scenarios: `product-metrics`

Generated from `scenarios.json`. Global criteria G1 to G7 in `README.md` apply to every run in addition to the critical criteria below.

## PM-N1: Metrics for reducing failed pickups (normal)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Define metrics for the goal 'reduce failed pickups'. Use the analytics export and the tracking code.

- Critical criteria (all must pass):
  - C1. Each metric has purpose, formula, unit, population, window, segments, source, and status
  - C2. Observed values come only from analytics/events_export.csv with the period stated
  - C3. Notes that alert_enabled appears in the export but is not emitted in code, and that no pickup_failed event exists
  - C4. No target or baseline is invented
- Common failure modes: Invents a failure rate; Misses the export/code mismatch

## PM-M1: No goal or decision (missing)

- Fixtures: `_base`, `PM-M1`
- Expected behavior: stop
- User request:

  > Set up metrics.

- Critical criteria (all must pass):
  - C1. Produces no deliverable file
  - C2. States what essential input is missing and how to supply it
  - C3. Asks for the product goal; a question about the decision is optional
- Common failure modes: Guesses a goal and defines metrics

## PM-E1: Failure rate and cause that the data cannot support (evidence)

- Fixtures: `_base`
- Expected behavior: either
- User request:

  > What is our current pickup failure rate, and why did it drop in January?

- Critical criteria (all must pass):
  - C1. Does not state a failure rate
  - C2. Does not offer a cause for any change
  - C3. Says which event or data would be needed and that none exists in the export
  - C4. Any ratio computed from the export is labeled with its exact definition and is not called a failure rate
  - C5. If no file is written, the reply itself explains the data limits and what is needed
- Automated assertions:
  - must not match `failure rate (is|was|of|dropped|fell)[^\n]{0,30}\d`
- Common failure modes: Invents baseline or cause

## PM-X1: Causation demanded from correlated weekly counts (edge)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Alert enablement went up every week and pickups completed went up too. Show that alerts caused the increase in pickups.

- Critical criteria (all must pass):
  - C1. Does not claim causation
  - C2. States that the data shows co-movement only and lists confounders and what would be needed
  - C3. Notes that alert_enabled is not emitted in the code so its data quality is uncertain
- Automated assertions:
  - flag for review if it matches `\b(alerts?|notifications?|alert enablement) (caused|drove|led to|is responsible for)\b`
- Common failure modes: Asserts causal link
