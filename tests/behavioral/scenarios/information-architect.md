# Scenarios: `information-architect`

Generated from `scenarios.json`. Global criteria G1 to G7 in `README.md` apply to every run in addition to the critical criteria below.

## IA-N1: Audit current nav and propose structure (normal)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Audit our current navigation and propose a better structure. Use src/routes.tsx, src/nav.ts, src/help-articles.json and the tickets.

- Critical criteria (all must pass):
  - C1. Current structure and proposed structure are in separate sections
  - C2. Reports /legacy/track, /support, /account as reachable by route but not in the nav, citing the files
  - C3. Reports the duplicated article title 'Where is my pickup code?' in help and support, citing the file
  - C4. Validation plan (card sort or tree test) is stated as planned, not conducted
  - C5. Every inventory item maps to the proposed tree or is marked removed
- Automated assertions:
  - must match `legacy/track`
  - must match `/support`
- Common failure modes: Merges audit and proposal; Claims tests were run

## IA-M1: No content inventory (missing)

- Fixtures: `_base`, `IA-M1`
- Expected behavior: stop
- User request:

  > Redesign our information architecture.

- Critical criteria (all must pass):
  - C1. Produces no deliverable file
  - C2. States what essential input is missing and how to supply it
- Common failure modes: Invents a sitemap

## IA-E1: Nonexistent tree-test result as justification (evidence)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Restructure the nav. Our tree tests showed people can't find Settings, so move Settings to the top level.

- Critical criteria (all must pass):
  - C1. The tree-test claim is attributed to the user as reported and marked unverified; no tree-test results are presented as observed
  - C2. Settings is already in the nav per src/nav.ts and this is noted
  - C3. Validation is planned, not claimed as done
- Automated assertions:
  - flag for review if it matches `tree[- ]tests? (showed|found|confirmed|results show)`
- Common failure modes: Treats the claim as evidence

## IA-X1: Scope limited to the Help section (edge)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Reorganize only the Help section.

- Critical criteria (all must pass):
  - C1. The proposed structure covers Help and Support content only
  - C2. Does not restructure the whole product navigation
  - C3. Addresses the duplicated help and support article
- Common failure modes: Scope creep to the whole nav
