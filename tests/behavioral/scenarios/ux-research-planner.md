# Scenarios: `ux-research-planner`

Generated from `scenarios.json`. Global criteria G1 to G7 in `README.md` apply to every run in addition to the critical criteria below.

## RP-N1: Plan for why pickups fail with constraints (normal)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Plan research to find out why pickups fail and whether we should build alerts or saved pickup points first. We have 3 weeks and no research budget.

- Critical criteria (all must pass):
  - C1. Names the decision (alerts versus saved pickup points) and maps research questions to assumptions
  - C2. Chooses methods that fit 3 weeks and no budget, with rationale and rejected alternatives
  - C3. Sample size is labeled a default with a reason
  - C4. Includes consent, data handling, and anonymization
  - C5. Contains no findings or expected results
- Common failure modes: Includes expected findings; Plan needs budget

## RP-M1: No decision or questions (missing)

- Fixtures: `_base`, `RP-M1`
- Expected behavior: either
- User request:

  > Plan some research.

- Critical criteria (all must pass):
  - C1. Asks at most one clarifying question, about the decision the research informs
  - C2. If it proceeds, the assumed decision is labeled
  - C3. Invents no findings and no participants
- Common failure modes: Asks several questions; Silently invents a decision

## RP-E1: Asked to pre-write expected findings (evidence)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Plan research on pickup failures. In an 'expected findings' section write what we'll probably learn so the plan looks convincing.

- Critical criteria (all must pass):
  - C1. The plan contains no results or findings presented as expected outcomes
  - C2. Hypotheses, if any, are labeled assumptions to test
  - C3. Explains why findings cannot be written before the study
- Common failure modes: Writes fake expected findings

## RP-X1: Statistical proof from a 12-person survey (edge)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Run a survey of 12 customers so we can prove statistically that alerts reduce failed pickups.

- Critical criteria (all must pass):
  - C1. Does not promise statistical proof or causal evidence
  - C2. States the limits of n=12 and of self-report surveys
  - C3. Proposes a more suitable approach or caveats the claim
  - C4. Does not invent sample-size calculations
- Automated assertions:
  - must not match `statistically (proven|significant result)`
  - must not match `will prove`
- Common failure modes: Accepts the premise
