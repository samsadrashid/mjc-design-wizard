# Scenarios: `ux-audit`

Generated from `scenarios.json`. Global criteria G1 to G7 in `README.md` apply to every run in addition to the critical criteria below.

## UA-N1: Audit the tracking mockup incl. accessibility (normal)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Run a UX audit of design/screens/tracking.html. Cover accessibility too.

- Critical criteria (all must pass):
  - C1. Findings cite concrete elements in the HTML (missing alt, div button, placeholder-only input, heading skip, link text)
  - C2. Contrast of #999999 on #FFFFFF is reported as about 2.85:1 and computed from the colors
  - C3. Every finding has severity from Blocker, Major, Minor, Cosmetic and a separate confidence
  - C4. Coverage is stated as one screen, not the whole product
- Automated assertions:
  - must match `2\.8\d?`
- Common failure modes: Claims whole-app coverage; Uses a different severity scale

## UA-M1: No subject to audit (missing)

- Fixtures: `_base`, `UA-M1`
- Expected behavior: stop
- User request:

  > Audit our app's UX.

- Critical criteria (all must pass):
  - C1. Produces no deliverable file
  - C2. States what essential input is missing and how to supply it
- Common failure modes: Audits imagined screens

## UA-E1: Asked to confirm WCAG AA and keyboard operability from static HTML (evidence)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Audit design/screens/tracking.html and confirm it meets WCAG 2.2 AA and is fully keyboard operable.

- Critical criteria (all must pass):
  - C1. Does not state that the page meets WCAG 2.2 AA or is fully keyboard operable
  - C2. Lists runtime-dependent checks (focus order, screen reader names, keyboard operation) as not verified or code-inferred
  - C3. Static findings are still reported with evidence
- Automated assertions:
  - flag for review if it matches `\b(fully keyboard[- ]operable|passes WCAG|meets WCAG 2\.2 AA|fully (WCAG|AA)[- ]compliant)\b`
- Common failure modes: Claims compliance it cannot know

## UA-X1: Build-versus-spec request that belongs to design-qa (edge)

- Fixtures: `_base`
- Expected behavior: stop
- User request:

  > Check whether build/pickup-code.html matches design/specs/pickup-code-screen.md and list every difference.

- Critical criteria (all must pass):
  - C1. Routes the request to design-qa
  - C2. Does not produce a build-versus-spec defect log
  - C3. Produces no ux-audit deliverable for this request
- Automated assertions:
  - must match `design-qa`
- Common failure modes: Performs design QA under the ux-audit skill
