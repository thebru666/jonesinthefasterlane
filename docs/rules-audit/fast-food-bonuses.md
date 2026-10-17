# Fast food: purchases, food stock and shared Happiness bonuses

Audited 2026-10-16 against website DOS **1.000.060**. Evidence **BYTECODE**, selected actual records and purchase/reset paths; no new runtime price, animation or Happiness observation. [Verification metadata](../../artifacts/rules-audit/fast-food-bonuses-verification.json) records four resource hashes, six product records, selected method hashes and a bounded direct latch-writer inventory across69 script hashes. This extends [the food baseline](food-and-housing.md) and the [original product catalogue](../original-game/content-progression.md#purchases-original-menu-pools).

## FOOD-B01: six controls, two different receipt types

The actual script210 records inherit `CostDItem`, class55. All six have units1, fixedPrice0 and visitTime0. Their package properties are:

| Product | Index | Type | Base price | Inventory effect | Own Happiness override |
| --- | ---: | ---: | ---: | --- | --- |
| Hamburgers |3 |1 |79 | One consumable unit | None |
| Cheeseburger |4 |1 |89 | One consumable unit | +1, shared meal latch |
| Astro Chicken |2 |1 |124 | One consumable unit | +2, shared meal latch |
| Fries |5 |1 |65 | One consumable unit | None |
| Shakes |6 |3 |102 | No consumable receipt in shared purchase | +2, shared drink latch |
| Colas |7 |3 |69 | No consumable receipt in shared purchase | +1, shared drink latch |

The base values are the actual integer price inputs, not an inferred modern cents conversion. The shared initializer uses the goods economy reading and [ordinary price helper](economy.md#econ-003-exact-ordinary-price-calculation); the shared purchase debits its resulting price from carried cash. At ordinary goods reading100 the debit equals the listed base. Exact menu formatting is separate from the verified record/cash pipeline.

All four food controls route into the consumable list through shared receipt. The drink controls use type3, which has no inventory-receive branch in this helper. Buying a drink therefore must not be treated as buying a week of stored food from these instructions. Coverage, spoilage and recurring consumption retain the separate [needs trace](bytecode-needs-events.md).

The location entry costs2 time. These six controls add no per-purchase time because their visitTime is0; the shared purchase has no spent60 rejection gate. Affordability remains required. This is distinct from Work at the same location, whose normal time/clothing rules still apply.

## FOOD-B02: the first successful eligible product wins its category bonus

The four overrides call the superclass purchase **first**, retain its return, then require success flag416 and a clear shared latch. The selected method entries and latch stores are:

| Method entry | Bonus/latch store |
| --- | --- |
| Cheeseburger `210:0x075c` | Set global472=1 at `0x0775`, then Happiness+1 |
| Chicken `210:0x07ec` | Set global472=1 at `0x0805`, then Happiness+2 |
| Shakes `210:0x08e0` | Set global471=1 at `0x08f9`, then Happiness+2 |
| Colas `210:0x0970` | Set global471=1 at `0x0989`, then Happiness+1 |

The latch is consumed **before** calling the Happiness helper. That helper clamps each call to0…100; at the cap, a successful qualifying purchase still consumes its latch. An unaffordable attempt does not pass success flag416 and therefore does not consume either category bonus. Hamburgers and Fries have no corresponding override, so buying them does not consume either latch through these item methods.

Cheeseburger and Chicken share one meal opportunity; Shakes and Colas share one drink opportunity. These are not four separate item bonuses. Repeated purchases remain legal and continue receiving/debiting normally, but the later item in an already used category gives no additional bonus through these overrides.

Assuming enough cash, no clamp and initially clear latches:

| Successful order | Total category Happiness |
| --- | ---: |
| Cheeseburger, then Chicken |1 |
| Chicken, then Cheeseburger |2 |
| Cola, then Shake |1 |
| Shake, then Cola |2 |

Thus a Chicken-first and Shake-first sequence can yield4 total from these two categories, whereas Cheeseburger-first and Cola-first yields2. This is an analytical consequence of branch order, not an observed play strategy or a rule saying every food purchase yields happiness.

## FOOD-B03: the reset is the active player's next ordinary turn

Actual start-turn script111 writes global472=0 at `0x02f4` and global471=0 at `0x02f7` during ordinary preparation, after the completion-gate branch. That reset occurs before the later week1 skip of recurring needs. The latches are shared active-turn globals, not separate lifetime fields on each food record.

The bounded inventory across all69 scripts finds only those two direct reset writes and the four direct item writes listed above. No fast-food entry/exit reset occurs in that inventory. Leaving and returning to the restaurant during the same ordinary turn therefore does not replenish these bonuses along the selected paths. The next ordinary active-player preparation clears them for that player's turn. Indexed/computed writes, interpreter restore mutations and arbitrary callback re-entry remain outside the direct-writer absence claim.

Jones's controller selects ordinary purchase events, so these shared item handlers do not establish a different reward formula for the computer. Its menu-selection policy is documented separately in [computer action routing](bytecode-ai-actions.md).

## Planning boundary

This supplies missing everyday Happiness and shopping rules without adding a nutrition meter or a new bonus system. Per-item bonuses, stackable drink food coverage, reset-on-visit or a new cents/dollars scale would be explicit departures. Exact UI text, callbacks, every possible restored state and all dynamic Happiness mutation paths are not established by this selected trace. The subsequent [whole-package catalogue](happiness-catalogue.md) consolidates the identified ordinary action/event sites.
