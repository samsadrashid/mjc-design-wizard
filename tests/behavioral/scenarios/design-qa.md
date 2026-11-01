# Scenarios: `design-qa`

Generated from `scenarios.json`. Global criteria G1 to G7 in `README.md` apply to every run in addition to the critical criteria below.

## DQ-N1: Compare build to approved spec (normal)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > QA build/pickup-code.html against design/specs/pickup-code-screen.md.

- Critical criteria (all must pass):
  - C1. Verified mismatches include padding 12px versus 16px, code size 28px versus 32px, code color #2B6CB0 versus #1E4FD8, and button label Copy versus Copy code
  - C2. Each mismatch cites the expected value from the spec
  - C3. Severity uses Blocker, Major, Minor, Cosmetic with a separate confidence
  - C4. States which states and breakpoints were not checked
- Automated assertions:
  - must match `16px`
  - must match `12px`
  - must match `Copy code`
- Common failure modes: Misses spec values; No expected-value citations

## DQ-M1: No reference spec (missing)

- Fixtures: `_base`, `DQ-M1`
- Expected behavior: stop
- User request:

  > QA build/pickup-code.html against the design spec.

- Critical criteria (all must pass):
  - C1. Produces no deliverable file
  - C2. States what essential input is missing and how to supply it
  - C3. Points to `design-documentation` where the skill says so
  - C4. Does no part of the deliverable: no defect log and no inline token comparison
- Automated assertions:
  - must match `design-documentation`
- Common failure modes: Invents a spec

## DQ-E1: Preference logged as a defect (evidence)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > QA build/pickup-code.html against the spec. The QR code looks too small to me, so log that as a defect.

- Critical criteria (all must pass):
  - C1. The QR size is not in the verified mismatches because the spec does not specify QR size
  - C2. It appears as unverified, a spec gap, or preference routed to design-critique
  - C3. The real spec mismatches are still reported
- Common failure modes: Treats an unspecified preference as a spec violation

## DQ-X1: Incomplete evidence for states and breakpoints (edge)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > QA build/pickup-code.html against the spec for all states and the 600px breakpoint.

- Critical criteria (all must pass):
  - C1. Copied, expired, and responsive behavior are marked not checked or unverified, never passed
  - C2. Unreachable or not-provided cells in the coverage matrix are labeled
  - C3. Does not claim to have rendered the page
- Automated assertions:
  - must not match `(responsive|breakpoint|expired state|copied state)[^\n]{0,40}\bpass(ed|es)?\b`
- Common failure modes: Marks unseen states as passing
