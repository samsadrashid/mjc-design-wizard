# Scenarios: `problem-framing`

Generated from `scenarios.json`. Global criteria G1 to G7 in `README.md` apply to every run in addition to the critical criteria below.

## PF-N1: Frame the problem behind a dashboard request (normal)

- Fixtures: `_base`, `_ext/stakeholder`
- Expected behavior: output
- User request:

  > Frame the problem behind this stakeholder request: docs/stakeholder-request.md. Evidence is in support/ and research/.

- Critical criteria (all must pass):
  - C1. One problem statement with no solution words such as dashboard
  - C2. Supporting evidence and assumptions are listed with tags and confidence
  - C3. Evidence cited matches the fixtures (code findability, late alerts, pickup point changes)
  - C4. Success definition says Baseline none where no baseline exists
  - C5. Includes what would falsify the framing
- Common failure modes: Solution wording; Invented counts

## PF-M1: Request only, no evidence (missing)

- Fixtures: `_base`, `_ext/stakeholder`, `PF-M1`
- Expected behavior: output
- User request:

  > Frame the problem behind this stakeholder request: docs/stakeholder-request.md.

- Critical criteria (all must pass):
  - C1. Statement is labeled Provisional with Low confidence
  - C2. No evidence is invented to support it
  - C3. Next step recommends research planning or gathering evidence
- Automated assertions:
  - must match `provisional`
- Common failure modes: Fabricates supporting evidence

## PF-E1: Claimed problem that the evidence does not support (evidence)

- Fixtures: `_base`, `_ext/stakeholder`
- Expected behavior: output
- User request:

  > Frame the problem as: users can't find their orders on the home screen. Cite the support evidence.

- Critical criteria (all must pass):
  - C1. Does not claim the tickets support 'can't find orders on the home screen'
  - C2. Reports what the tickets and interviews actually say
  - C3. Labels the claim as reported or assumption
- Common failure modes: Cites tickets that do not say this

## PF-X1: Solution disguised as the problem (edge)

- Fixtures: `_base`, `_ext/stakeholder`
- Expected behavior: output
- User request:

  > The problem is that we need a home dashboard. Write that up as the problem statement.

- Critical criteria (all must pass):
  - C1. The statement does not name a dashboard or any solution
  - C2. Explains why the request is a solution and reframes to the user need
  - C3. Keeps the dashboard as a proposed solution in the split table
- Common failure modes: Writes 'need a dashboard' as the problem
