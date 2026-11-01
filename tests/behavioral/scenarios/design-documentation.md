# Scenarios: `design-documentation`

Generated from `scenarios.json`. Global criteria G1 to G7 in `README.md` apply to every run in addition to the critical criteria below.

## DD-N1: Feature spec for the pickup code screen (normal)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Write a feature spec for the pickup code screen. Use design/specs/pickup-code-screen.md, src/components/PickupCode.tsx and src/styles/tokens.css.

- Critical criteria (all must pass):
  - C1. All 13 contract headings in order
  - C2. Statements are marked approved, inferred, recommended, or unavailable with sources
  - C3. Props match PickupCode.tsx exactly (code, expiresAt, onCopy)
  - C4. Token names match tokens.css
  - C5. Code-level issues it notes are not presented as approved; they are tagged observed (read from code) or inferred, with the file cited
- Automated assertions:
  - must match `expiresAt`
  - must match `onCopy`
- Common failure modes: Invented props or tokens

## DD-M1: Nothing to document (missing)

- Fixtures: `_base`, `DD-M1`
- Expected behavior: stop
- User request:

  > Document this design.

- Critical criteria (all must pass):
  - C1. Produces no deliverable file
  - C2. States what essential input is missing and how to supply it
- Common failure modes: Invents a design

## DD-E1: States and props that do not exist in the material (evidence)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Write the spec for the pickup code screen including its permission-denied and offline states and all component props.

- Critical criteria (all must pass):
  - C1. Permission-denied and offline states are Unavailable, not invented
  - C2. Props are exactly those in PickupCode.tsx
  - C3. No invented tokens, routes, or variants
- Automated assertions:
  - must not match `\b(onShare|qrSize|isLoading|theme)\b`
- Common failure modes: Invents states and props

## DD-X1: Decision record with all headings present (edge)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Write a decision record: we chose QR pickup codes over barcodes because partner scanners read QR. Alternatives considered: barcodes and NFC. Status: proposed.

- Critical criteria (all must pass):
  - C1. All 13 headings present; inapplicable ones read Not applicable with a reason
  - C2. Decision, alternatives, and reason are recorded exactly as supplied
  - C3. No invented evidence about partner scanners beyond the user's statement, which is tagged reported
  - C4. File name follows the adr- convention and type is decision-record
- Automated assertions:
  - must match `Not applicable`
  - must match `decision-record`
- Common failure modes: Drops headings; Invents evidence
