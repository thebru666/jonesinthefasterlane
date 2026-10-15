# Original-game rules audit

**Status:** framework established; gameplay rules have not yet been audited.

Provisional reference: the website bundle identifying version **1.000.060**, retrieved 2026-10-15. Confirm the edition before treating it as the sole reference.

## Evidence labels

- **PACKAGE:** directly inspected package or configuration fact.
- **SCRIPT:** supported by an identified script/resource and interpreted control flow; record disassembly uncertainty.
- **OBSERVED:** reproduced in the running reference game; record initial state and exact actions.
- **DOCUMENTED:** stated in a manual or other cited source; may differ from implementation.
- **HYPOTHESIS:** plausible explanation requiring verification.
- **PROPOSAL:** a new-game design choice, not a claim about the original.

A script finding and an observed result can support the same rule. Keep conflicting evidence visible. Do not upgrade a documentary claim to observed behaviour.

## Coverage

| Area | Questions | Status |
| --- | --- | --- |
| Setup and goals | Starting resources, player count, goal settings, win timing | Not audited |
| Time and travel | Weekly allowance, movement, entry costs, rounding, partial actions | Not audited |
| Weekly processing | Order of rent, food, events, economy, income, and victory checks | Not audited |
| Economy | State transitions, duration, randomness, price/wage/job effects | Not audited; high priority |
| Employment | Vacancies, qualifications, experience, hiring, raises, dismissal, pay | Not audited |
| Education | Prerequisites, fees, lessons, completion, goal contribution | Not audited |
| Food and basic needs | Consumption, storage, shortages, penalties | Not audited |
| Housing | Rent schedule, upgrades, access, possessions, consequences of nonpayment | Not audited |
| Goods and happiness | Purchase effects, recurring effects, duplicates, relaxation | Not audited |
| Banking and investments | Interest, loans, repayment, shares, valuation, rounding | Not audited |
| Random events | Triggers, eligibility, probabilities, ordering, recovery | Not audited |
| Computer opponent | Policy, information, difficulty, special treatment | Not audited |
| Multiplayer and saves | Turn order, public/private information, persistence | Not audited |

## Method

1. Gather stated rules from the manual and record edition information.
2. Inspect relevant scripts and data, assigning stable rule IDs such as `TIME-001` or `ECON-001`.
3. Reproduce representative behaviours and boundary cases in the original.
4. Record formulas, units, rounding, prerequisite checks, processing order, and random draws.
5. Separate original behaviour from adaptation decisions: **keep**, **reskin**, or **change**. An undecided mapping is acceptable while investigating.
6. Update coverage with evidence links and outstanding questions after each coherent research step.

Use the [rule template](rule-template.md) for findings. Add records under this directory as the audit progresses; keep raw original code and assets out of Git.

## Priority and completion

Start with time/turn structure and weekly processing, then economic swings, employment, and education. These underpin the rest of the design and the owner's essential requirements.

An area is ready for adaptation planning when normal behaviour, important boundaries, and unresolved uncertainty are recorded with evidence. A full decompile alone does not establish complete behavioural coverage.
