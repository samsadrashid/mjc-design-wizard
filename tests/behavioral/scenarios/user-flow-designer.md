# Scenarios: `user-flow-designer`

Generated from `scenarios.json`. Global criteria G1 to G7 in `README.md` apply to every run in addition to the critical criteria below.

## UF-N1: Collect a parcel with the pickup code (normal)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Design the flow for collecting a parcel with the pickup code, from the parcel list to collected.

- Critical criteria (all must pass):
  - C1. Entry points and user intent are stated
  - C2. Mermaid or list covers happy path and error, empty, loading, and expired branches that each reach a named outcome
  - C3. Reuses routes from src/routes.tsx such as /parcels/:id/code
  - C4. State table has the five states per screen or Not applicable
  - C5. Open product decisions are labeled
- Automated assertions:
  - must match `/parcels/:id/code`
- Common failure modes: Dead-end branches

## UF-M1: No task or actor (missing)

- Fixtures: `_base`, `UF-M1`
- Expected behavior: stop
- User request:

  > Design the user flow.

- Critical criteria (all must pass):
  - C1. Produces no deliverable file
  - C2. States what essential input is missing and how to supply it
- Common failure modes: Invents a task

## UF-E1: Unknown QR expiry and offline behavior (evidence)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Design the flow for QR pickup. I don't know if the QR code expires or whether partners' scanners work offline.

- Critical criteria (all must pass):
  - C1. QR expiry and offline scanner behavior are labeled assumptions or open decisions
  - C2. No invented expiry duration or scanner behavior stated as fact
  - C3. Flow still covers expired and offline branches as conditional
- Automated assertions:
  - must not match `expires? (after|in|within) \d`
  - must not match `valid for \d`
- Common failure modes: Invents a TTL

## UF-X1: Permission denied and offline at the locker scanner (edge)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Design the flow for scanning a QR code at the locker. The camera permission may be denied and the phone may be offline.

- Critical criteria (all must pass):
  - C1. Permission-denied and offline branches each reach a named recovery or exit
  - C2. Mermaid syntax is valid
  - C3. No disconnected nodes
  - C4. Permission-denied state appears in the state table
- Common failure modes: Branch without outcome
