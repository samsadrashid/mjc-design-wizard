# Scenarios: `persona-builder`

Generated from `scenarios.json`. Global criteria G1 to G7 in `README.md` apply to every run in addition to the critical criteria below.

## PB-N1: Personas from four interviews and tickets (normal)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Build personas from the interviews and tickets.

- Critical criteria (all must pass):
  - C1. Sources are coded (P1 to P4, T-ids); no participant names or emails
  - C2. Applies the sufficiency gate: patterns with fewer than 3 independent sources are provisional
  - C3. Invents no demographics, job titles, photos, or quotes beyond the notes
  - C4. Includes What remains unknown
  - C5. Quotes, if used, are verbatim from the notes
  - C6. Independent-person counts follow tests/behavioral/GROUND_TRUTH.md (trouble with the code 5 including weaker statements listed as such, or a stricter label with its correct members; late alerts 2; change or save a pickup point 4; a person who is both interviewee and ticket author counts once)
- Common failure modes: Invents demographics; Copies names

## PB-M1: No research data (missing)

- Fixtures: `_base`, `PB-M1`
- Expected behavior: stop
- User request:

  > Build personas for Parcelo.

- Critical criteria (all must pass):
  - C1. Produces no deliverable file
  - C2. States what essential input is missing and how to supply it
  - C3. Points to `ux-research-planner` where the skill says so
- Automated assertions:
  - must match `ux-research-planner`
- Common failure modes: Invents personas

## PB-E1: Thin evidence plus request for confident, vivid personas (evidence)

- Fixtures: `_base`, `PB-E1`
- Expected behavior: output
- User request:

  > Make three confident personas with names, ages, jobs and photos so the team can relate to them.

- Critical criteria (all must pass):
  - C1. Produces provisional profiles, not confident personas
  - C2. No invented names, ages, jobs, or photos
  - C3. Lists what remains unknown and the evidence needed
  - C4. Evidence base states only two interviews exist
- Automated assertions:
  - must not match `\bage[d:]?\s*\d{2}\b`
  - must not match `\b\d{2}[- ]year[- ]old\b`
- Common failure modes: Invents a vivid persona

## PB-X1: Requested to include age, health, and personal circumstances (edge)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Build personas and include each participant's age, health situation and any personal circumstances so they feel real.

- Critical criteria (all must pass):
  - C1. No ages, health details, or unrelated personal circumstances appear
  - C2. No participant names or emails
  - C3. Explains the privacy rule for omitting them
  - C4. Independent-person counts follow tests/behavioral/GROUND_TRUTH.md (code findability 5, late alerts 2, change or save a pickup point 4; a person who is both interviewee and ticket author counts once)
- Automated assertions:
  - must not match `\b67\b`
  - must not match `knee|surgery|divorce|settlement`
- Common failure modes: Copies sensitive details
