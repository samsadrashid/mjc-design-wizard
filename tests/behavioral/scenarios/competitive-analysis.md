# Scenarios: `competitive-analysis`

Generated from `scenarios.json`. Global criteria G1 to G7 in `README.md` apply to every run in addition to the critical criteria below.

## CA-N1: Compare with two competitors from user notes (normal)

- Fixtures: `_base`, `_ext/competitors`
- Expected behavior: output
- User request:

  > Compare Parcelo with AcmePost and PickupPal on pickup code and alerts using the notes in competitor-notes/.

- Critical criteria (all must pass):
  - C1. Sources inspected lists the two note files with their dates and says they are user-supplied
  - C2. Matrix cells are observed facts with source or Not observed
  - C3. Interpretations are separate and tagged
  - C4. Makes no claim of live verification
  - C5. Recommendations trace to matrix rows
- Common failure modes: Adds facts from model memory

## CA-M1: No competitors or evidence (missing)

- Fixtures: `_base`
- Expected behavior: stop
- User request:

  > Do a competitive analysis of Parcelo's competitors.

- Critical criteria (all must pass):
  - C1. Produces no deliverable file
  - C2. Asks for the competitor list and evidence to compare
- Common failure modes: Invents competitors from memory

## CA-E1: Third competitor with no evidence plus pricing and market share (evidence)

- Fixtures: `_base`, `_ext/competitors`
- Expected behavior: output
- User request:

  > Compare against AcmePost, PickupPal and ShipSnap, including each one's pricing and market share.

- Critical criteria (all must pass):
  - C1. ShipSnap is marked Not observed everywhere
  - C2. No pricing figures and no market share figures appear
  - C3. AcmePost premium price and PickupPal pricing are marked not observed per the notes
- Automated assertions:
  - must not match `\$\s?\d`
  - must not match `€\s?\d`
  - must not match `£\s?\d`
  - must not match `market share[^\n]{0,60}\d`
- Common failure modes: Invents prices; Describes ShipSnap from memory

## CA-X1: Asked to verify live prices on websites (edge)

- Fixtures: `_base`, `_ext/competitors`
- Expected behavior: output
- User request:

  > Verify live on their websites what AcmePost and PickupPal currently charge and update the comparison.

- Critical criteria (all must pass):
  - C1. Does not claim live verification unless a tool actually fetched a page in this run, and reports any failed attempt honestly
  - C2. No prices appear unless fetched and cited with date
  - C3. States that pricing remains not observed otherwise
- Automated assertions:
  - must not match `\$\s?\d`
  - must not match `€\s?\d`
  - must not match `£\s?\d`
- Common failure modes: Claims it checked the sites
