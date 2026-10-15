# Original-game rules audit

**Status:** two script-based passes now cover time/actions, turn/weekly processing, economy, computer policy, food/housing and ordinary goods/finance. Coverage remains partial; runtime reproduction and remaining systems are open.

The subsequent [original-game baseline](../original-game/README.md) adds source-based setup, town/layout, all destination actions, course/job/product catalogues, progress views, saves, and finish. It describes the original for later iteration; it does not close all numerical/runtime/visual gaps.

## Pass 1 findings (2026-10-15)

- [Time and action boundaries](time-and-actions.md): TIME-001–007, including partial shifts, final-hour study, zero-time transactions, travel/entry costs, and a garnishment anomaly.
- [Turn and weekly processing](weekly-processing.md): WEEK-001–006, including ordered pre-turn processing, fourth-week obligations, and weekend cash gates.
- [Economy](economy.md): ECON-001–007, including layered market state, exact ordinary pricing, stored contracts, shocks, and floppy/CD differences.
- [Validation backlog](validation-backlog.md): analytical checks completed and runtime scenarios still pending.
- [Design implications](../planning/audit-implications.md): recommendations and compatibility decisions to resolve before building.
- [Sources and provenance](../discovery/source-register.md): permanent references, methods, and limitations.

This pass inspects an existing published decompilation; it does not claim we decompiled the website bundle ourselves or independently matched the script bytes. No controlled gameplay test has been marked OBSERVED.

Provisional reference: the website bundle identifying version **1.000.060**, retrieved 2026-10-15. Confirm the edition before treating it as the sole reference.

## Pass 2 findings (2026-10-15)

- [Computer opponent](computer-opponent.md): AI-001–009; ordered destination/action policy, goal-based difficulty, shared action execution and internal market information.
- [Food and housing](food-and-housing.md): NEED-001–004 and HOME-001–005; food coverage/storage/illness, rent, extensions, arrears, moving, rest and apartment theft.
- [Goods and finance](goods-and-finance.md): GOODS-001–006 and FIN-001–005; grouped possessions, purchase effects, repairs, pawning, banking, loans, investments and valuation.
- [Screen reconstruction](../original-game/screen-reconstruction.md): 18 local analytical composites plus town/victory component studies, with state and presentation limits.
- [Pass 2 source metadata](../../artifacts/rules-audit/2026-10-15-pass2-source-inputs.json) records the 25 cited source inputs; no original source payloads are included.

All adaptation mappings remain undecided. Apparent bugs and information differences are findings to verify, not approved changes.

## Evidence labels

- **PACKAGE:** directly inspected package or configuration fact.
- **DECODED:** pixels, text or events exported from the hash-pinned package; not necessarily final runtime composition or behaviour.
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
| Setup and goals | Starting resources, player count, goal settings, win timing | Source baseline: [setup](../original-game/setup-multiplayer.md), [scores/finish](../original-game/progression-and-finish.md); runtime and edge paths pending |
| Time and travel | Weekly allowance, movement, entry costs, rounding, partial actions | Partial: [TIME-001–007](time-and-actions.md); travel matrix/runtime pending |
| Weekly processing | Order of rent, food, events, economy, income, and victory checks | Partial: [WEEK-001–006](weekly-processing.md); rare branches/runtime pending |
| Economy | State transitions, duration, randomness, price/wage/job effects | Partial: [ECON-001–007](economy.md); bytecode/runtime/long-run validation pending |
| Employment | Vacancies, qualifications, experience, hiring, raises, dismissal, pay | Partial: [all 37 original job rows and thresholds](../original-game/content-progression.md); rejection/raise edge cases/runtime pending |
| Education | Prerequisites, fees, lessons, completion, goal contribution | Source baseline: [11-course graph and credits](../original-game/content-progression.md); [book labels decoded](../original-game/asset-catalogue-notes.md#precise-course-label-transcription-targets); runtime pending |
| Food and basic needs | Consumption, storage, shortages, penalties | Detailed SCRIPT: [NEED-001–004](food-and-housing.md); food IDs, storage, spoilage sentinel, hunger and illness; runtime/object cleanup pending |
| Housing | Rent schedule, upgrades, access, possessions, consequences of nonpayment | Detailed SCRIPT: [HOME-001–005](food-and-housing.md); payment/extension/debt/moving/rest/theft; runtime/edge paths pending |
| Goods and happiness | Purchase effects, recurring effects, duplicates, relaxation | Detailed SCRIPT: [GOODS-001–006](goods-and-finance.md); grouped inventory, purchase bonus anomaly, recurring effects/repairs/pawn; joke products and weekend tables pending |
| Banking and investments | Interest, loans, repayment, shares, valuation, rounding | Detailed SCRIPT: [FIN-001–005](goods-and-finance.md); transfer/loan/trade/valuation paths; high-value anomalies and runtime pending |
| Random events | Triggers, eligibility, probabilities, ordering, recovery | Partial: economic shocks and ordering; remaining event catalogue pending |
| Asset presentation | Resource inventory, decompression, graphics/text/audio coverage | [266 unique resources catalogued](../original-game/asset-catalogue-notes.md); 108 graphics resources rendered, sound events/MIDI exported; [18 screen composites](../original-game/screen-reconstruction.md); full text/animation/role transcription and runtime comparison pending |
| Computer opponent | Policy, information, difficulty, special treatment | Detailed SCRIPT: [AI-001–009](computer-opponent.md); runtime, demo/CD comparison and exhaustive privilege scan pending |
| Multiplayer and saves | Turn order, public/private information, persistence | Source baseline: [supported combinations, visibility, handover, fixed-slot saves](../original-game/setup-multiplayer.md); runtime/emulator persistence pending |

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
