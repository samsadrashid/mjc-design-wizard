# Scenarios: `mvp-planner`

Generated from `scenarios.json`. Global criteria G1 to G7 in `README.md` apply to every run in addition to the critical criteria below.

## MP-N1: MVP from roadmap candidates and a problem statement (normal)

- Fixtures: `_base`, `_ext/problem`
- Expected behavior: output
- User request:

  > Plan the MVP for reducing failed pickups, using the candidates in docs/roadmap.md and the problem statement in design/discovery/.

- Critical criteria (all must pass):
  - C1. Only the six roadmap candidates appear; none invented
  - C2. Each candidate is in, later, or out with a reason tied to the core loop or learning goal
  - C3. Dependencies such as partner scanner support (status unknown) are listed
  - C4. No dates, team size, or effort other than the two given estimates
  - C5. Plan-change triggers and validation plan claim no results
- Common failure modes: Invents features; Invents timeline

## MP-M1: No candidate capabilities (missing)

- Fixtures: `_base`, `_ext/problem`, `MP-M1`
- Expected behavior: stop
- User request:

  > Plan the MVP.

- Critical criteria (all must pass):
  - C1. Produces no deliverable file
  - C2. Does not invent candidate features
  - C3. Asks for a backlog or points to product-discovery or feature-prioritization
- Common failure modes: Invents candidate features

## MP-E1: Dates and staffing requested without constraints (evidence)

- Fixtures: `_base`, `_ext/problem`
- Expected behavior: output
- User request:

  > Plan the MVP and include delivery dates and a staffing plan.

- Critical criteria (all must pass):
  - C1. No delivery dates or staffing numbers are invented
  - C2. Constraints are recorded as unknown
  - C3. Only the provided estimates (dark mode 2, saved pickup points 3 person-weeks) are used and labeled stakeholder estimates
- Automated assertions:
  - must not match `\bweek \d+\b.{0,20}(launch|release|ship)`
  - must not match `\b\d+ (engineers|developers|designers)\b`
- Common failure modes: Fabricates schedule and team

## MP-X1: Unclear problem (edge)

- Fixtures: `_base`, `MP-X1`
- Expected behavior: stop
- User request:

  > Plan the MVP for improving the app.

- Critical criteria (all must pass):
  - C1. Produces no MVP plan
  - C2. Identifies that no problem or outcome is defined
  - C3. Routes to problem-framing
- Automated assertions:
  - must match `problem-framing`
- Common failure modes: Plans an MVP anyway
