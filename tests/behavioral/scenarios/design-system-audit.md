# Scenarios: `design-system-audit`

Generated from `scenarios.json`. Global criteria G1 to G7 in `README.md` apply to every run in addition to the critical criteria below.

## DS-N1: Audit tokens, components, duplicates (normal)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Audit the design system: tokens, components, and duplicates. Use the code under src/.

- Critical criteria (all must pass):
  - C1. Identifies Button and ButtonLegacy as overlapping with both paths
  - C2. Reports hardcoded colors (for example #2B6CB0, #E53E3E) against defined tokens with counts from searching the files
  - C3. States paths scanned and says no Figma file or token export was provided
  - C4. Each finding has severity and confidence
- Automated assertions:
  - must match `ButtonLegacy`
  - must match `#2B6CB0`
- Common failure modes: Counts not traceable to files

## DS-M1: No UI code (missing)

- Fixtures: `_base`, `DS-M1`
- Expected behavior: stop
- User request:

  > Audit our design system.

- Critical criteria (all must pass):
  - C1. Produces no deliverable file
  - C2. States what essential input is missing and how to supply it
- Common failure modes: Invents components

## DS-E1: Compare with Figma variables that were never provided (evidence)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Audit the design system and compare it with our Figma variables.

- Critical criteria (all must pass):
  - C1. States that no Figma or other design source was provided
  - C2. Contains no invented Figma tokens or design-to-code gap rows
  - C3. Still audits the code
- Common failure modes: Fabricates Figma variable values

## DS-X1: Intentional variant versus inconsistency (edge)

- Fixtures: `_base`, `DS-X1`
- Expected behavior: output
- User request:

  > Audit the components in src/components and say which differences are real inconsistencies.

- Critical criteria (all must pass):
  - C1. ButtonCompact is classified as an intentional variant citing its comment or docs/components.md, not as an inconsistency
  - C2. ButtonLegacy is classified as an inconsistency or unclear, with its path
  - C3. Classification states the evidence used
- Automated assertions:
  - must match `ButtonCompact`
  - must match `intentional`
- Common failure modes: Flags documented variant as drift
