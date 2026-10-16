# Wealth score and asset refresh contract

Audited 2026-10-16 against the website DOS **1.000.060** package, downloaded 2026-10-15. Evidence: **BYTECODE**, static package analysis; no new gameplay or runtime score observations. [Verification metadata](../../artifacts/rules-audit/score-refresh-verification.json) contains the package identity, resource hashes, complete literal-selector and cash-helper call inventories across all 69 decoded scripts, and transaction witnesses. Original listings and comparison source remain ignored locally. This extends [SCORE-001](bytecode-flow-and-persistence.md#score-001-stored-goals-liquid-assets-and-net-worth-are-different).

## The contract

There are three separate states: actual money/holdings/debts, cached asset totals, and stored Wealth (`monStat`, selector375). **Refreshing asset totals does not refresh Wealth.** The package's only identified executable Wealth setters are in Main export10: the initial setter at `0:0x050d`, then upper/lower clamps at `0x0528` and `0x0542`. Its cash write is at `0x04e5`; its score reads the already stored liquid-assets pair at `0x04f2/0x0503`. There is no intervening asset calculation.

For ordinary low-word amounts, this writes `clamp(trunc(cachedLiquidAssets / 100), 0, 100)`. The nonzero-high-word branch writes100 regardless of the high word's sign; this is the actual condition, not a general signed big-integer interpretation. Carry/borrow uses32767 in the shared cash helper and asset addition helper. This pass does not claim all overflow/negative-high-word cases have been reproduced.

`Player.calcNetWorth` (`1:0x0fb3–0x1011`) first calls `calcLiquidAssets` at `0x0fb9`. The latter (`0x1012–0x10d2`) values holdings, caches investment assets, adds cash and savings, and subtracts rent owed plus loan balance. Net worth then adds durable purchase price × quantity. Neither method writes Wealth. The literal-selector inventory finds only three external `calcNetWorth` sends: board cash panel `1:0x2462`, start-turn `111:0x03e2`, and Statistics `231:0x0015`. The only literal `calcLiquidAssets` invocation is the self call within `calcNetWorth`.

The cash panel's `doit` (`1:0x23c6–0x2464`) always refreshes assets after its conditional cash-number redraw. Its `draw` calls `doit` at `0x23c3`. Therefore an unchanged cash amount does not suppress this refresh. The conclusion is **a cache sampled at each cash-helper invocation**, not a proven universal one-action or one-turn lag.

## Ordinary action order

In this table, **C** means cash mutation followed by stored Wealth assignment from the cache; **A** means recalculation of cached liquid assets and net worth. Optional notices, animation and other callbacks are discussed separately below. Each order describes the successful direct action path, not every instruction in the method.

| Action | Proved direct order | Consequence |
| --- | --- | --- |
| Ordinary goods/course purchase, shared `CostDItem` | Receive item and set purchase price → C (`104:0x04a5`) → superclass `doit` → A (`0x04b6`) → item/purchase callbacks → charge visit time | The explicit final A incorporates the cash expense; it leaves the just-written Wealth untouched. Callbacks after A may mutate more state. |
| Work pay | Garnishment may reduce rent owed and display a notice → C (`108:0x032c`) → A (`0x0339`) → time charge | The pre-C notice is a possible callback boundary; the direct final A does not recalculate Wealth. |
| Pay rent | Receive prepaid-rent consumable → C (`201:0x063c`) → A (`0x064f`) → optional notice | No direct Wealth update follows A. This does not equate prepaid rent with immediate debt cancellation. |
| Deposit | C (`204:0x050a`) → start pig animation → A (`0x0522`) → optional notice → savings increase via local helper (`0x059a` → `0x0113`) | The explicit A runs **before** the savings credit. Until another refresh, this cache temporarily counts the cash debit without its savings counterpart. |
| Withdraw | C (`204:0x06ce`) → start pig animation → A (`0x06e7`) → optional notice → savings decrease (`0x072c` → `0x0113`) | The explicit A runs **before** the savings debit. Until another refresh, this cache temporarily counts both the withdrawn cash and its savings counterpart. |
| Take loan | Confirmation/notices → C (`204:0x0b1b`) → increase loan balance (`0x0b33`) → A (`0x0b3b`) | The direct A includes the new debt. Wealth still samples the cache that existed before C. |
| Make loan payment | Inherited `CostDItem.doit` performs C and A → subclass records payment and reduces principal (`204:0x0896`) → notice | The inherited A precedes principal reduction. The subsequent full refresh is a separate call, not part of this principal setter. |
| Buy investment | Increase shares → C (`213:0x0c9b`) → adjust investment subtotal → local holding display helper → A (`0x0cdd`) | Final A derives holdings afresh. The manually adjusted subtotal does not itself set Wealth. |
| Sell investment | Decrease shares → C (`213:0x0dae`) → adjust investment subtotal → holding display helper → optional Treasury-bill fee C (`0x0dea`) → A (`0x0e15`) | Both cash-helper calls sample the cache then present; the fee call is not automatically a score from the completed sale. |
| Pawn possession | Mark pawn state, reduce quantity and rebuild selector → C (`212:0x138c`) → A (`0x1395`) | Final A follows both quantity and cash changes; Wealth remains the cash-helper sample. |
| Redeem possession | C (`212:0x16ac`) → A (`0x16b5`) → item/purchase callbacks → clear pawn flags and other completion work | Do not assume all redemption work precedes A. The later durable-state handling is distinct from Wealth. |

The full cash-helper inventory also includes five start-turn callsites and the weekend expense procedure. It contains **17 callsites in eight scripts**, including the two broker sale calls. Those are not seventeen independent player actions. See the metadata for exact locations.

## Draws, callbacks, screens and turn boundaries

Location initialization and each location's `draw` frequently send the cash panel `setSize/value/draw`; the metadata inventories these sends, including bank and broker. Thus a later redraw can repair a temporarily incomplete cache. Statistics explicitly calls A before composing its figures (`231:0x0015`). Goals overview and locked goal details read stored Wealth (`238:0x0014`, `236:0x09ff`); they contain no direct asset-refresh or Wealth-set call. Reading Statistics can affect the cache sampled by a **later** cash-helper call without directly changing the stored goal score.

The callback audit prevents treating nearby source lines as the whole execution:

- Main export1 (`0:0x0276–0x0283`) calls Animate with flag0. It is not an alias for cash-helper10 or asset refresh.
- The board's cash panel is a `DIcon` added to room controls (`1:0x2043–0x204c`), not an actor in the cast. The inherited item `cycle` is an empty return (`255:0x042a`). `Controls.draw` explicitly draws its members (`255:0x1558–0x1565`), and `Controls.handleEvent` can invoke a matched control's `doit` (`0x1566–0x159b`); neither is a perpetual all-controls score update.
- The modal loop (`255:0x0d68–0x0e85`) cycles its own items, cycles/calls its window's animation object, dispatches script/event handlers, and runs checks. The pig icon's `doit` only installs a cycler (`204:0x0f5b–0x0f74`). Its DCIcon cycle path (`967:0x000c–0x0037`) advances the cycler and redraws on cel/loop change; it does not transfer bank balances. The savings helper runs at the explicit deposit/withdraw callsites above.
- The outer game loop (`994:0x046d–0x04c7`) checks sounds, animates cast with flag1, dispatches pending motion cues, scripts, room and User. `Rm.doit` (`0x06c1–0x06cd`) only invokes its script when present. The board room has its own movement/player work. None introduces an unconditional Wealth setter. Presentation-driven callbacks can still cause explicit draws, action calls or handover.

At start turn, `Player.startTurn` initializes the clock, calls export1, sets location/readiness state, updates the economy, and initializes startTrn (`1:0x0d6b–0x0d9a`). StartTrn compares stored Wealth at `111:0x00cc` and `0x0174` in its two completion gates; its explicit A is later at `0x03e2`. Any intervening draw can change cached assets, but cannot change stored Wealth without reaching a cash-helper call. The inspected winner presentation calls export1 but no cash-helper10 or Wealth setter. Victory therefore consumes stored scores; neither the visible cash redraw nor the start-turn A is an immediate victory trigger.

## Coverage and the remaining experiment

The inventory scans all 69 decoded package scripts, resolves selectors375/461/462 from vocabulary997, enumerates Main exports1/10 calls, checks direct property access to Player's Wealth slot22, and records cash-panel target sends. It finds no direct Player property write to that slot. Default class and four player-instance Wealth values are zero. Literal-selector and property-slot searches are static coverage, not proof against arbitrary reflection, restored VM state or unexamined interpreter internals. Conservative pseudocode supplied navigation; raw decoded instructions settled argument counts, targets and order.

The subsequent [bank modal-continuation trace](bank-refresh-continuation.md) now establishes a selected ordinary path where the incomplete cache survives to the next transaction. The modal loop does not invoke an outer board redraw; ordinary Print notices restore pixels and clerk animation without a blanket asset calculation. Statistics explicitly repairs the cache. Goals alone returns through bank.draw, whose gCalc refresh is gated by restoration flag518 and skipped after normal initialization.

The remaining experiment is visible corroboration: log consecutive deposit/withdraw/payment sequences with messages on/off, Statistics or Goals between them, and log every cash helper, asset calculation, savings/principal setter and Wealth write. No such runtime result is claimed. Restored/dynamic callback and extreme-balance paths remain separate.

For 2.0 planning, keeping stored score, cached assets and balances separate is the faithful static contract. Continuously deriving Wealth after every transaction, or choosing a different score-refresh policy remains an explicit compatibility decision; the selected static sequence is now documented while displayed lag remains unobserved. No implementation is approved by this audit.

Sources: [website archive](https://jonesinthefastlane.com/bundle.jsdos), [source register](../discovery/source-register.md), and [published comparison source at pinned revision](https://github.com/sluicebox/sci-scripts/tree/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src). Package resource hashes and witnesses are in the accompanying metadata; no game code or assets are included.
