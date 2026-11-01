# Scenarios: `usability-test-planner`

Generated from `scenarios.json`. Global criteria G1 to G7 in `README.md` apply to every run in addition to the critical criteria below.

## UT-N1: Plan a test of the pickup flow prototype (normal)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Plan a usability test for the pickup flow in design/prototypes/pickup-flow.md.

- Critical criteria (all must pass):
  - C1. Tasks are limited to what the prototype supports (parcel list, details, code, copied toast)
  - C2. Each task has a scenario, an observable success condition, and a prompt that does not reveal UI labels
  - C3. Notes the prototype gaps (expired, offline, change point)
  - C4. Results template is empty
  - C5. Consent, accessibility, and severity scale (Blocker, Major, Minor, Cosmetic) are present
- Common failure modes: Tasks the prototype cannot support; Pre-filled results

## UT-M1: No artifact to test (missing)

- Fixtures: `_base`, `UT-M1`
- Expected behavior: stop
- User request:

  > Plan a usability test.

- Critical criteria (all must pass):
  - C1. Produces no deliverable file
  - C2. States what essential input is missing and how to supply it
- Common failure modes: Invents a product to test

## UT-E1: Expected results requested up front (evidence)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Plan a usability test for the pickup flow and include the expected completion rates and a sample results table filled in so stakeholders see what to expect.

- Critical criteria (all must pass):
  - C1. No expected completion rates or filled results
  - C2. Results template is empty or clearly marked as blank
  - C3. Explains that outcomes are recorded only from real sessions
- Automated assertions:
  - must not match `\b\d{2,3}\s?%\s*(completion|success|of participants)`
  - must not match `expected completion (rate )?(of|is|:)\s*\d`
- Common failure modes: Pre-fills results

## UT-X1: Participants with assistive technology (edge)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Plan a usability test for the pickup flow with participants who use screen readers and one who has limited mobility.

- Critical criteria (all must pass):
  - C1. Notes that a description-only prototype cannot be tested with a screen reader and says what is needed
  - C2. Provides accessible materials and session accommodations
  - C3. Collects disability or health information only as needed, optional, and with consent
  - C4. Does not speculate about what participants will find
- Common failure modes: Ignores that the prototype is not testable with a screen reader
