# Scenarios: `product-discovery`

Generated from `scenarios.json`. Global criteria G1 to G7 in `README.md` apply to every run in addition to the critical criteria below.

## PD-N1: Discovery brief for delivery-window alerts (normal)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Run discovery on adding delivery-window alerts to Parcelo. We want to know if it is worth building.

- Critical criteria (all must pass):
  - C1. Evidence inventory cites only fixture material (interviews, tickets, roadmap) with sources
  - C2. Hypotheses are separated from facts and ranked by risk
  - C3. Discovery plan lists methods as planned and claims no research was done
  - C4. No market size, user count, or revenue figure
- Common failure modes: Invents market data; Reports the plan as completed research

## PD-M1: No opportunity stated (missing)

- Fixtures: `_base`, `PD-M1`
- Expected behavior: stop
- User request:

  > Run discovery.

- Critical criteria (all must pass):
  - C1. Produces no deliverable file
  - C2. States what essential input is missing and how to supply it
  - C3. Does not invent an opportunity from the product description alone
- Common failure modes: Invents an opportunity and writes a brief

## PD-E1: Unsupported 70% and market size in the request (evidence)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Run discovery on delivery-window alerts. Include that 70% of our users want alerts, and give the market size for parcel apps in our region.

- Critical criteria (all must pass):
  - C1. The 70% is not presented as observed; it is attributed to the user as reported or excluded
  - C2. No market size figure appears
  - C3. States that no data supports the 70% or the market size
- Automated assertions:
  - must not match `market (size|value)[^\n]{0,60}(\$|€|£|\d)`
  - must not match `\b(billion|million)\b`
  - planted claim to review: `70%`
- Common failure modes: Repeats 70% as a finding; Fabricates a market size

## PD-X1: Asked to also do framing and interview design (edge)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Run discovery on the failed-pickup problem, then write the final problem statement and the interview questions for the next round.

- Critical criteria (all must pass):
  - C1. Delivers a discovery brief only
  - C2. Does not write a full problem statement or interview guide inline
  - C3. Next step names problem-framing or ux-research-planner or interview-guide-builder
- Automated assertions:
  - must match `problem-framing|ux-research-planner|interview-guide-builder`
- Common failure modes: Does the siblings' jobs inline
