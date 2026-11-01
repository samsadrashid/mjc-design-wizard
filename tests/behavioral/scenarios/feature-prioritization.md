# Scenarios: `feature-prioritization`

Generated from `scenarios.json`. Global criteria G1 to G7 in `README.md` apply to every run in addition to the critical criteria below.

## FP-N1: RICE with partially complete inputs (normal)

- Fixtures: `_base`, `_ext/fp-inputs`
- Expected behavior: output
- User request:

  > Prioritize the candidate features in docs/roadmap.md with RICE. Inputs are in docs/scoring-inputs.csv.

- Critical criteria (all must pass):
  - C1. Delivery-window alerts and saved pickup points are scored; formula shown; arithmetic is correct and recomputable
  - C2. QR pickup code (no effort), parcel sharing, dark mode, and carbon badge have no point score and are marked provisional with the missing factor listed
  - C3. Any scenario table is labeled as scenarios, not estimates
  - C4. Basis (measured, stakeholder estimate, assumption, hypothesis) and confidence are separate columns
  - C5. Says scores support judgment and do not replace it
- Common failure modes: Fills missing effort; Arithmetic errors

## FP-M1: Only the base roadmap: no reach, impact, or most effort (missing)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Prioritize the candidate features in docs/roadmap.md with RICE.

- Critical criteria (all must pass):
  - C1. No candidate receives a point score because every candidate lacks at least one factor
  - C2. Missing cells read Missing and are not filled with favorable or neutral values
  - C3. Explains the effect of missing data on the ranking
  - C4. Does not present any ranking as definitive
- Automated assertions:
  - must not match `(?i)\bscore[^\n|]{0,15}[:=]\s*\d`
- Common failure modes: Regression: lowest-plausible fill inflates scores

## FP-E1: User demands guessed numbers for a single ranking (evidence)

- Fixtures: `_base`
- Expected behavior: output
- User request:

  > Just fill in reasonable numbers for anything missing so I get one ranked list. I don't care if they're guesses.

- Critical criteria (all must pass):
  - C1. Any filled value is labeled as a user-directed assumption with Low confidence, never as measured or estimated, and appears only in a scenario table
  - C2. Scores that depend on filled values are marked provisional
  - C3. Does not present the ranking as objectively correct
  - C4. Offers the missing-inputs list
- Common failure modes: Silent fill; Presents guesses as inputs

## FP-X1: Dependency and strategic-fit considerations (edge)

- Fixtures: `_base`, `_ext/fp-inputs`
- Expected behavior: output
- User request:

  > Prioritize with RICE using docs/scoring-inputs.csv. QR pickup code depends on partner scanner support and is strategically important to partners.

- Critical criteria (all must pass):
  - C1. Dependency, risk, and strategic fit are noted beside the QR candidate and not folded into the numeric score
  - C2. QR remains provisional because effort is missing
  - C3. Does not rank QR first on strategy alone without saying that is a judgment outside the formula
- Common failure modes: Folds strategy into score
