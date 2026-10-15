# Original-game rules audit

**Status:** first script-based pass completed for time/actions, turn/weekly processing, and economy. Coverage remains partial; runtime reproduction and remaining systems are open.

## Pass 1 findings (2026-10-15)

- [Time and action boundaries](time-and-actions.md): TIME-001–007, including partial shifts, final-hour study, zero-time transactions, travel/entry costs, and a garnishment anomaly.
- [Turn and weekly processing](weekly-processing.md): WEEK-001–006, including ordered pre-turn processing, fourth-week obligations, and weekend cash gates.
- [Economy](economy.md): ECON-001–007, including layered market state, exact ordinary pricing, stored contracts, shocks, and floppy/CD differences.
- [Validation backlog](validation-backlog.md): analytical checks completed and runtime scenarios still pending.
- [Design implications](../planning/audit-implications.md): recommendations and compatibility decisions to resolve before building.
- [Sources and provenance](../discovery/source-register.md): permanent references, methods, and limitations.

This pass inspects an existing published decompilation; it does not claim we decompiled the website bundle ourselves or independently matched the script bytes. No controlled gameplay test has been marked OBSERVED.

Provisional reference: the website bundle identifying version **1.000.060**, retrieved 2026-10-15. Confirm the edition before treating it as the sole reference.

## Evidence labels

- **PACKAGE:** directly inspected package or configuration fact.
- **SCRIPT:** supported by an identified script/resource and interpreted control flow; record disassembly uncertainty.
- **OBSERVED:** reproduced in the running reference game; record initial state and exact actions.
- **DOCUMENTED:** stated in a manual or other cited source; may differ from implementation.
- **HYPOTHESIS:** plausible explanation requiring verification.
- **PROPOSAL:** a new-game design choice, not a claim about the original.

A script finding and an observed result can support the same rule. Keep conflicting evidence visible. Do not upgrade a documentary claim to observed behaviour.

For SCRIPT evidence, state whether it is our own bytecode analysis or an externally published decompilation. Pass 1 uses the latter. Domain files group related rule IDs while retaining source links, limitations, and adaptation status.

## Coverage

| Area | Questions | Status |
| --- | --- | --- |
| Setup and goals | Starting resources, player count, goal settings, win timing | Partial: boundary win check; complete goal/setup audit pending |
| Time and travel | Weekly allowance, movement, entry costs, rounding, partial actions | Partial: [TIME-001–007](time-and-actions.md); travel matrix/runtime pending |
| Weekly processing | Order of rent, food, events, economy, income, and victory checks | Partial: [WEEK-001–006](weekly-processing.md); rare branches/runtime pending |
| Economy | State transitions, duration, randomness, price/wage/job effects | Partial: [ECON-001–007](economy.md); bytecode/runtime/long-run validation pending |
| Employment | Vacancies, qualifications, experience, hiring, raises, dismissal, pay | Partial: pay, stored wages, event dismissal; full progression pending |
| Education | Prerequisites, fees, lessons, completion, goal contribution | Partial: enrollment fee and short study; content/prerequisites pending |
| Food and basic needs | Consumption, storage, shortages, penalties | Partial: processing order and time penalties; complete item/probability mapping pending |
| Housing | Rent schedule, upgrades, access, possessions, consequences of nonpayment | Partial: stored rent, cadence, garnishment; extensions/moving pending |
| Goods and happiness | Purchase effects, recurring effects, duplicates, relaxation | Not audited |
| Banking and investments | Interest, loans, repayment, shares, valuation, rounding | Partial: market inputs and cash gates; full transaction/high-value audit pending |
| Random events | Triggers, eligibility, probabilities, ordering, recovery | Partial: economic shocks and ordering; remaining event catalogue pending |
| Computer opponent | Policy, information, difficulty, special treatment | Not audited |
| Multiplayer and saves | Turn order, public/private information, persistence | Partial: rotation and per-player economy; removal, visibility, saves pending |

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
