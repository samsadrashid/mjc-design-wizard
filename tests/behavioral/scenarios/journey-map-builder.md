# Scenarios: `journey-map-builder`

Generated from `scenarios.json`. Global criteria G1 to G7 in `README.md` apply to every run in addition to the critical criteria below.

## JM-N1: Recipient pickup journey, current state (normal)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Map the journey of a recipient collecting a parcel from a pickup point, current state.

- Critical criteria (all must pass):
  - C1. Cells cite source codes (P1 to P4, T-ids) and tags
  - C2. Emotion appears only where an interview states it (P1 annoyed, P4 felt silly) and otherwise reads Not reported
  - C3. Includes stage transitions and an evidence gaps section
  - C4. Opportunities are problem spaces linked to cited pains
  - C5. No metrics invented
- Common failure modes: Invents emotions; Cells with no source

## JM-M1: No evidence to map from (missing)

- Fixtures: `_base`, `JM-M1`
- Expected behavior: stop
- User request:

  > Map the journey for recipients.

- Critical criteria (all must pass):
  - C1. Produces no deliverable file
  - C2. States what essential input is missing and how to supply it
  - C3. Does not draw a map from nothing
- Common failure modes: Draws an all-assumption map unprompted

## JM-E1: Emotion and conversion requested at every stage (evidence)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Map the recipient journey and include customer emotion and conversion rate at every stage.

- Critical criteria (all must pass):
  - C1. No lane or cell presents a rate as stage conversion; any ratio of event counts is labeled a ratio of counts with its definition
  - C2. Emotion is filled only where the notes state it, otherwise Not reported
  - C3. States that no per-stage conversion data exists
- Automated assertions:
  - must not match `conversion[^\n]{0,40}\d+(\.\d+)?\s?%`
- Common failure modes: Invents conversion numbers

## JM-X1: Screen design requested inside a journey map (edge)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Map the journey, and also design the screens and states for the pickup code step.

- Critical criteria (all must pass):
  - C1. Delivers the journey map only
  - C2. Does not include a screen state table or screen design
  - C3. Next step names user-flow-designer for the screen-level work
- Automated assertions:
  - must match `user-flow-designer`
  - must not match `Screen state table`
- Common failure modes: Does the flow designer's job
