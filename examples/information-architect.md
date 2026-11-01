# Example: information-architect

> **Illustrative example.** All inputs and outputs below use invented sample data to show the output shape. Kettle is a fictional meal-kit subscription app; the routes, navigation, and tickets are hypothetical.

## Prompt

```
/information-architect Restructure Kettle's account area. Routes are in src/routes.ts and navigation in src/nav.ts.
```

## Sample input (invented)

`src/routes.ts`:

```
/menu
/account
/account/profile
/account/plan
/account/plan/deliveries
/account/payment
/account/referrals
/help
/help/skip
/help/faq
```

`src/nav.ts`: top navigation Menu, Account, Help. Account sub-navigation: Profile, Plan, Payment. The Plan page links to Deliveries. Nothing links to `/account/referrals`. `/help/faq` contains a section titled "How to skip" with the same text as `/help/skip`.

Evidence of user vocabulary: ticket subjects T-01 "How do I skip next week?", T-03 "Where is the skip button", T-05 "Can I pause for a month?", T-08 "How to skip a week" (date unknown). No card sort, tree test, or search logs exist.

## What the skill does

1. Builds the inventory from routes and navigation, with how each item is reached.
2. Audits the current structure only from the inventory, and reports orphaned, duplicate, and hard-to-find items with sources.
3. Takes user vocabulary from the tickets, then proposes a tree with change markers and maps every inventory item into it.
4. Plans a card sort and tree test, marked planned, not conducted.

## Output shape (`design/architecture/information-architect-account-area-<YYYY-MM-DD>.md`)

```markdown
> skill: information-architect · date: <YYYY-MM-DD> · scope: account area · sources: src/routes.ts, src/nav.ts, support/tickets.csv (4 subjects, date unknown)

## Scope and evidence base
Scope: the account area plus the help pages it links to [reported: user]. Evidence: routes and navigation [observed]; four ticket subjects [observed]. No findability study exists.

## Content inventory
| Item | Type | Location | How it is reached | Source |
|---|---|---|---|---|
| Menu | Page | /menu | Top nav | routes.ts, nav.ts |
| Account | Hub page | /account | Top nav | routes.ts, nav.ts |
| Profile | Page | /account/profile | Account sub-nav | routes.ts, nav.ts |
| Plan | Page | /account/plan | Account sub-nav | routes.ts, nav.ts |
| Deliveries | Page | /account/plan/deliveries | Link on Plan page only | routes.ts, nav.ts |
| Payment | Page | /account/payment | Account sub-nav | routes.ts, nav.ts |
| Referrals | Page | /account/referrals | No link; URL only | routes.ts, nav.ts |
| Help | Hub page | /help | Top nav | routes.ts, nav.ts |
| How to skip | Article | /help/skip | Help hub | routes.ts |
| FAQ | Article | /help/faq | Help hub | routes.ts |

## Current structure (audited)
Depth 3 at most (Account > Plan > Deliveries); breadth 3 at the top level. Organizing scheme: top level by type of content (catalog, account, help); account level by object (profile, plan, payment) [observed: nav.ts].

## Findings on the current structure (evidence and confidence)
| Finding | Type | Evidence | Confidence |
|---|---|---|---|
| Deliveries sits three levels deep and is reached only through Plan | Hard to find | Path count 3 [observed: nav.ts]; T-01, T-03, T-08 ask how or where to skip [observed] | Medium |
| Referrals has no navigation link | Orphaned | Route exists, nothing links to it [observed: routes.ts, nav.ts] | High |
| Skip instructions appear in two places | Duplicate | /help/skip and the "How to skip" section of /help/faq [observed] | High |
| Users say "skip" and "pause"; no nav label uses either | Ambiguous | T-01, T-03, T-05, T-08 [observed]; nav labels [observed: nav.ts] | Medium |
| Whether "Plan" is understood as the place for deliveries | Unverified | No evidence either way | — |

## Top tasks and user vocabulary
- Skip a week: "skip" in T-01, T-03, T-08 [observed].
- Pause for longer: "pause" in T-05 [observed].
- Other tasks are not in the evidence; top tasks beyond these are [assumption].

## Proposed structure (tree, change markers, inventory mapping)
- Menu [unchanged]
- Deliveries [moved: from Account > Plan > Deliveries to top level] — holds the per-week skip
- Account [unchanged]
  - Profile [unchanged]
  - Plan [unchanged]
  - Payment [unchanged]
  - Referrals [moved: now linked from Account sub-nav; was orphaned]
- Help [unchanged]
  - How to skip [unchanged]
  - FAQ [unchanged; its "How to skip" section replaced by a link to /help/skip]
Depth 2 at most; breadth 4 at the top level, within the default maximum of three levels.
Inventory mapping: all 10 inventory items appear above; none removed.
URL impact: /account/plan/deliveries moves to /deliveries; a redirect is needed.

## Labeling decisions
| Label | Decision | Rejected alternative and reason |
|---|---|---|
| Deliveries | Keep; matches the page title [observed: nav.ts] | "Skip" as a top label: names one action, not the place |
| Pause | Not added: no pause feature exists [observed: routes.ts] | — |
"Deliveries" as a top-level label is a guess and should be tested.

## Content model
Delivery week: week identifier, delivery date, cutoff time, status (scheduled, skipped), recipes (reference to Menu items). Required: week identifier, cutoff time, status [inferred: from the route and the skip task]. Reused by Deliveries and by any reminder email.

## Validation plan (planned, not conducted)
- Tree test with tasks: "Skip next week's box", "Find where to update your card", "Find how to invite a friend". Measures: success and first click. Planned, not conducted; study design goes to `ux-research-planner`.
- An open card sort was considered and not planned: the inventory is small and the main question is findability.

## Open questions / to validate
- Is a top-level Deliveries label understood by subscribers?
- Should Referrals stay at all? Usage is unknown.

## Next step
Run `ux-research-planner` to design the tree test for the proposed structure.
```
