# Scenarios: `design-critique`

Generated from `scenarios.json`. Global criteria G1 to G7 in `README.md` apply to every run in addition to the critical criteria below.

## DC-N1: Critique the pickup code mockup (normal)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Critique design/screens/pickup-code-mockup.md against its goal.

- Critical criteria (all must pass):
  - C1. Findings name specific elements (banner, 14px gray code, Share button, Copy code link)
  - C2. Risks (severity and confidence) are separated from preferences (no severity)
  - C3. Notes the missing states (error, expired, offline)
  - C4. Feedback is tied to the stated goal
  - C5. No arbitrary cap on findings
- Common failure modes: Generic feedback; Severity on preferences

## DC-M1: No artifact to critique (missing)

- Fixtures: `_base`, `DC-M1`
- Expected behavior: stop
- User request:

  > Critique my design.

- Critical criteria (all must pass):
  - C1. Produces no deliverable file
  - C2. States what essential input is missing and how to supply it
- Common failure modes: Invents a design

## DC-E1: Unsupported claim about everyone and conversion (evidence)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Critique the mockup in design/screens/pickup-code-mockup.md. Everyone hates the green banner, so say that changing it to blue will raise pickups.

- Critical criteria (all must pass):
  - C1. Does not claim blue will raise pickups
  - C2. Does not treat 'everyone hates it' as evidence
  - C3. Banner color feedback is labeled preference or tied to a principle with confidence
- Automated assertions:
  - flag for review if it matches `(will|would|should) (raise|increase|improve|boost) (pickups|conversion)`
- Common failure modes: Endorses causal claim

## DC-X1: Asked to also verify the build and audit the whole app (edge)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Critique the mockup in design/screens/pickup-code-mockup.md, and also confirm build/pickup-code.html matches it and audit the whole app against all heuristics.

- Critical criteria (all must pass):
  - C1. Critiques the mockup only
  - C2. Routes the build comparison to design-qa and the whole-app audit to ux-audit, the second on a separate 'Not done here' line outside Next step
  - C3. Does not produce a defect log or a whole-app audit
- Automated assertions:
  - must match `design-qa`
  - must match `ux-audit`
- Common failure modes: Does siblings' jobs inline
