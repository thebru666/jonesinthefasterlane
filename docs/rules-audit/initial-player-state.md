# Fresh-game player state

Audited2026-10-16 against the actual website DOS1.000.060 package. **BYTECODE** covers the class/instance property tables, selected setup setters and common initialization paths below. No new runtime session was performed. The [verification artifact](../../artifacts/rules-audit/initial-player-state-verification.json) records eight resource hashes, property-block/range hashes, four instance comparisons and2,132 selected instruction/payload comparisons. Original property tables and listings remain ignored.

This closes the consolidated fresh-state gap for ordinary human setup and the optional Jones rival. It does not define restored/interrupted-state initialization or approve a new starting balance for2.0.

## INIT-001: distinguish template, allocated game and prepared turn

There are three different boundaries:

1. **Loaded player records:** script1's Player class and four player instances contain numeric defaults, but inventory-list fields are still zero references. Setup chooses participants, bodies and targets.
2. **Common allocation after setup:** `room1.init` calls `players.init` at`1:0x1f88`. That method removes nonplaying entries, assigns participant markers, invokes each remaining player's `init`, records the list size and selects its first entry as active. The common `Player.init`, `0x0ad0–0x0bf3`, is guarded by nonzero `playing`; it creates each player's lists and starting items. The tables below describe this allocated fresh-game state **before turn preparation**.
3. **Incoming turn preparation:** `Player.startTurn`, `0x0d6b–0x0d9a`, initializes the clock, copies housing into current-location state, updates the economy and initializes script111. Preparation resets flags, calculates credits/assets and follows its week-specific event sequence. These later mutations must not be confused with the template or setup choices.

The four actual player instances match the selected resource, progression and score defaults in the artifact. `player1` initially has `playing=1`; other slots have`playing=0` until setup enables them. Unselected slots are removed rather than allocated as extra competitors.

## INIT-002: common resources and progression

| State after common allocation | Human | Optional Jones |
| --- | --- | --- |
| Carried cash | $200, high word0 | Same |
| Bank savings | $0, high word0 | Same |
| Rent owed; loan principal | $0; $0 | Same |
| Loan schedule, late count, payment flag | All0 | Same |
| Housing | Low-cost apartments, place0 | Same |
| Stored current rent | $325 | Same |
| Prepaid rent |3 units of low-cost rent, index40; stored pricePaid325 | Same |
| Clothing |6 units of casual clothes, index36; stored pricePaid30 | Same |
| Uniform requirement; wearing field |36;36 | Same |
| Food and lottery tickets | No records initially | Same |
| Durable possessions; education records | Empty lists | Same |
| Investments | Six investment records, all shares0 | Same |
| Employer; occupation; wage; base wage | All0: unemployed | Same |
| Stored job identifier `jobT` |−1 | Same |
| Experience; experience ceiling |10;10 | Same |
| Dependability; minimum dependability |20;0 | Same |
| Relaxation |25 | Same |
| Enrollment count; completed courses |0;0 | Same |
| Equipment study credits; education/experience credits | All0 | Same |
| Rent-extension history/attempt/open flags | All0 | Same |

The casual clothes and prepaid rent are starting allocations. The selected initializer does not debit their stored prices from cash: it explicitly writes cash200/high0, creates empty lists, then receives those two items. It creates no groceries, fast food, degrees, durable goods or lottery tickets.

Actual receipt frames are`1:0x0bd5` for rent `(index40, quantity3)` and`0x0bef` for clothes `(index36, quantity6)`. The subsequent sends write their stored prices and indices. Item meanings and duration behaviour join the [food/housing](food-and-housing.md) and [grouped inventory](inventory-grouping.md) contracts. Quantity6 is a clothing stock/duration, not six independently priced outfits.

The investment list contains distinct zero-share records for the six instruments. `I.init` adds each new record to that player's list; `I.shares` defaults0. The stored base-price inputs are not free holdings, cash or guaranteed initial market quotes. Likewise the initial rent contract325 is distinct from a newly calculated moving quote. The first turn updates the economy, so the full town price list must not be initialized by assuming every economic reading is100.

## INIT-003: zero stored scores despite cash and asset caches

| Field | Allocated fresh value |
| --- | --- |
| Wealth / `monStat` |0 |
| Happiness / `hapStat` |0 |
| Education / `eduStat` |0 |
| Career / `carStat` |0 |
| Net-worth cache |200, high word0 |
| Liquid-assets cache |200, high word0 |
| Investment-assets cache |0, high word0 |
| Finish status and goal-progress ratio fields |0 |

The default cash and cached assets do **not** imply an initial stored Wealth score of2. The common initializer writes cash through a direct property send, rather than Main's score-writing cash helper. These are separate stored fields. Later cash-helper calls sample the cached assets as explained in [score refresh](score-refresh.md); the panel's asset recalculation alone does not write Wealth.

Similarly dependability20 does not imply an initial Career score20: the stored score is0 and the player is unemployed. No starting degrees are inferred from experience10 or its ceiling10.

## INIT-004: human choices versus Jones overrides

The ordinary human-count helper in actual script239 `0x000c–0x0034` sets`playing=1` for the selected leading slots. Human appearance buttons in script235 set only the selected body's `whichBody` in their relevant player-mutation paths. They do not change the starting resources in INIT-002. The four body choices are setup choices, not evidence of a resource handicap.

Human goal configuration is separate from starting scores. Actual script236 initializes the first player's four sliders to50 (`0x01eb–0x020c`). Later players' initial slider values come from the preceding player's configured targets (`0x0171–0x01dd`). The four slider overrides write the selected player's target fields at`0x0784`, `0x07f6`, `0x0868` and`0x08da`. Thus every human can choose targets10…100 in steps of10; later inheritance is an editable default, not a requirement for equal goals. The scores in INIT-003 remain separate.

On the one-human optional-rival path, actual script237's Yes handler sets the second slot's `playing=29` at`0x06c6`. Its allocator sets `playingAsJones=1` at`0x0055`; `players.init` assigns computer marker4. The common Player initializer is then used for this slot just as for human slots. No extra cash, job, education, experience, clothing or food grant occurs in these inspected rival setup paths.

Jones's difficulty changes **targets**, using the allocator called with offset+10/0/−10 for Take It Easy/Play Fair/Go For Broke at`237:0x0819`, `0x087c` and`0x08e1`. The intended total is the human's total plus four times that offset, bounded40…400. The allocator initially sets Wealth from the human's Wealth plus the offset, bounded10…100, draws Happiness/Education and obtains Career from the remainder. Its redistribution can subsequently change the initial Wealth assignment. Therefore do not prescribe the human's same four targets for Play Fair or treat the initial Wealth assignment as an immutable final category value. The [opponent allocation audit](computer-opponent.md) and existing analytical checker detail the distribution.

The startup demonstration is distinct: script233 sets the first slot to`playing=29`; it is not the optional second-slot Jones setup. This document does not turn that demonstration route into an additional supported multiplayer combination.

## INIT-005: what changes before the first ordinary action

Start-turn processing follows the [ordered lifecycle](bytecode-weekly-opponent.md). The fresh lists mean no ownership-happiness award, no equipment study credits and no ticket prize on the first ordinary preparation. The asset refresh runs, but does not by itself rewrite the four zero starting scores. Script111's week1 branch at`0x0515–0x052f` skips the later recurring states: no initial clothing/rent-stock decay, hunger/doctor event, repair or emergency grant is inferred simply from the fresh record lacking food.

Week1 does **not** skip the economy update, goal checks or earlier preparation logic. For optional Jones, player1 can already act before Jones's first turn; economy and cross-player state must consequently be considered when discussing the rival's first visible screen. The common post-allocation snapshot is the clean comparison boundary, not an arbitrarily observed later screen.

Clock initialization also has distinct entry routes. The room initializer calls the first active player's `startTurn` directly; later `marble.cue` handovers reset counters and immediately call the no-argument clock, ordinarily yielding residue1. This document does not import that later handover residue as a universal fresh-game clock invariant. See [travel timing](travel-timing.md).

## Evidence and limits

The earlier [runtime observations](runtime-observations.md), OBS-004 and OBS-007, independently report two human players with cash200, savings0, rent owed0, loan0, durable goods0, and initial unemployment. Those observations support that visible subset; they do not inspect hidden experience, dependability, credits, all scores or Jones initialization. The present broader table comes from actual property tables and initialization instructions, not extrapolation from those screenshots.

Published [room1.sc](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc) and setup scripts were used for comparison. Selected instruction/payload checks establish framing and provenance, not whole-source equivalence or execution. Restore overrides, edited saves, complete demonstration behaviour and other releases remain outside this fresh-game contract. Choosing different modern starting resources or automatic score derivation would be explicit adaptation decisions.
