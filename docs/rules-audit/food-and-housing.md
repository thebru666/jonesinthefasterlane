# Food, housing and basic needs

Pass 2, 2026-10-15. Evidence: **SCRIPT**, an interpretation of the externally published floppy DOS 1.000.060 decompilation, [S02](../discovery/source-register.md), pinned to `870a8015b689474484bf3d8b41416956d4315432`. Most sections retain that published-source evidence. HOME-003’s garnishment calculation now also has direct website-bytecode verification, linked below. Runtime observations are recorded separately and do not establish every precision scenario here; CD and other editions may differ. Adaptation mapping for every rule is **undecided**.

The subsequent [package needs/event trace](bytecode-needs-events.md) confirms selected food coverage/storage, hunger sentinel, illness predicates/bills/notice time and apartment-theft paths directly. The later [package finance lifecycle trace](finance-lifecycle.md) also verifies selected ordinary-rent, extension, arrears and moving paths in HOME-001–004. Object-lifetime/restored-state limits and unlinked rules retain their previous evidence scope; neither follow-up establishes complete runtime behavior.

This fills in [WEEK-004/005](weekly-processing.md) and cross-references [TIME-006](time-and-actions.md#time-006-rent-garnishment-appears-to-overwrite-partial-shift-pay). The order is significant: relaxation decay/theft → food detection → grocery spoilage → fast-food expiry/hunger → illness → consumable decrement → rent notice. Week 1 skips the recurring path. These are turn-start calculations for the active player, not simultaneous round-wide consumption.

## NEED-001: coverage is an inventory test, not a nutrition meter

At a normal recurring turn start, the script scans consumable IDs 5 down to 1 and records the highest ID with nonzero quantity. This records whether any qualifying food existed **before** spoilage and expiry. It does not choose a meal and subtract only that item's quantity. Later, every nonzero consumable quantity decreases by one, including unused groceries and chicken.

| Source/item | Goods ID | Purchase quantity | Base price input | Coverage / persistence |
| --- | --- | --- | --- | --- |
| Market groceries, one week | 1 | 1 | 55 | Storage-dependent; decrement once each recurring start |
| Market groceries, two weeks | 1 | 2 | 100 | Added to existing quantity |
| Market groceries, four weeks | 1 | 4 | 190 | Added to existing quantity |
| Astro Chicken | 2 | 1 | 124 | Not cleared with the other fast food; ordinary decrement |
| Hamburgers | 3 | 1 | 79 | Counts for coverage, then all stock cleared |
| Cheeseburger | 4 | 1 | 89 | Counts for coverage, then all stock cleared |
| Fries | 5 | 1 | 65 | Counts for coverage, then all stock cleared |
| Shakes / colas | 6 / 7 | No inventory addition | 102 / 69 | Purchase type 3; outside the food scan |

Prices above are economy-scaling inputs, not fixed checkout prices and not cents. The shared purchase handler adds inventory for types 0, 1 and 2, but type 3 simply pays without adding goods. Therefore buying a drink is not food coverage in this script path. Multiple food types do not preserve each other: groceries and chicken still decrement even when a higher-index fast food supplied the coverage marker.

Evidence: [market.sc, food controls, line 270](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/market.sc#L270), [fastFood.sc, item definitions, line 260](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/fastFood.sc#L260), [WButton.sc, CostDItem, line 161](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/WButton.sc#L161), [Goods.sc, decrement/addition, line 16](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/Goods.sc#L16), [startTrn.sc, state 8, line 328](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L328).

## NEED-002: refrigerators and freezers bound grocery stocks

Only grocery ID 1 takes this storage branch:

- With no refrigerator object (durable 21), all groceries become zero, with −2 happiness and a spoilage notice. If groceries were the only qualifying food, the food marker becomes −1.
- With a refrigerator but no freezer object (durable 22), stock above six is capped at six, with −1 happiness and an excess-stock notice.
- With both objects, stock above twelve is capped at twelve, with −1 happiness and that notice.

After the later universal decrement, those capped amounts become five and eleven. A freezer alone does not bypass the refrigerator requirement. The storage checks use **object presence**, not the `objectAtIndexQuan` quantity check used elsewhere. A zero-quantity object can therefore still count. The [package pack/pawn/storage trace](bytecode-needs-events.md#ne-b05-packing-does-not-discard-empty-inventory-records) now establishes a selected retention chain: pack does not generically discard empty records, and an accepted pawn action can leave the indexed record at quantity0. Exact visible scenarios and every removal/expiry route remain unverified; this is not an approved compatibility decision.

Evidence: [startTrn.sc, state 10, line 347](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L347), [appliance.sc, IDs 21/22, line 265](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/appliance.sc#L265), [Goods.sc, lookup methods, line 93](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/Goods.sc#L93).

## NEED-003: hunger and spoilage are different paths

The next stage clears all quantities for IDs 3–5. Their earlier food marker still counts for that turn. If the food marker is **zero**, the player loses 2 happiness, receives a hunger notice, and spends 20 hours. With groceries spoiled and marker −1, the player instead takes the spoilage consequences from NEED-002: −1 is truthy, so it avoids this separate hunger notice and 20-hour charge.

The script does not kill, eliminate, or evict the player in these inspected hunger/illness paths. Do not introduce a health or death system as part of a faithful reconstruction.

Evidence: [startTrn.sc, states 12–14, line 388](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L388), [moveNotice, time costs, line 967](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L967).

## NEED-004: illness requires both a random gate and carried cash

Ignoring the minimum-relaxation override, the illness gate is:

| Food marker | Random gate that permits illness | Chance of gate |
| --- | --- | --- |
| Positive, usable food detected | Initialized to safe | 0 |
| Zero, no food detected | Uniform draw 0–3 equals zero | 1/4 |
| −1, groceries were sole food and spoiled | Uniform draw 0–1 equals zero | 1/2 |

If relaxation is exactly 10, an additional independent draw 0–4 equal to zero forces the gate open. Under the standard inclusive, uniform SCI `Random` interpretation, combined gate probabilities at relaxation 10 are 1/5 for usable food, 2/5 for no food and 3/5 for sole-food spoilage. These are analytical probabilities from the source, not measured runtime frequencies. The extra draw occurs after the food draw; preserve draw order if reproducing saved/random sequences.

Even with the gate open, cash must be positive. Define bill ceiling `C`: start at 200; if carried cash is below 500 use 50; then clamp C to carried cash. Charge a uniform integer in 30…C when C > 30, otherwise charge C. The player also loses 4 happiness and spends 10 hours. Savings are not automatically withdrawn. Thus cash 499 permits a bill up to 50, while cash 500 permits up to 200; cash 1…30 can be exhausted, but zero cash suppresses the doctor outcome entirely.

Hunger followed by illness can consume 30 of the 60 turn hours before normal controls return. Spoilage followed by illness consumes 10 through these branches. Happiness adjustments use the common 0…100 clamp, so arithmetic totals are subject to that clamp.

Evidence: [startTrn.sc, state 14, line 405](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L405), [notice handler, line 967](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L967), [Main.sc, happiness clamp, line 1100](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/Main.sc#L1100).

## HOME-001: starting housing, rent contract and office availability

The standard player template starts at low-cost housing (`livesAt = 0`), current rent 325, no arrears and three prepaid rent units (consumable 40). Security housing uses `livesAt = 2` and consumable 41. These rent units count down on recurring turn starts with other consumables. Initial week 1 does not run that decrement.

The office exposes rent, extension and moving controls when `week mod 4 == 0` or `leaveOpen` is set. Being employed there can also expose its workplace controls on otherwise closed weeks; it does not by itself expose the full rent transaction set. Entering costs two hours. The fourth-week due notice occurs **after** that turn's consumable decrement and clears `turnedOver` so later end-turn accounting can recognise the unpaid obligation.

Ordinary rent payment uses the stored `curRent` contract rather than recomputing the economic price. It requires enough carried cash, debits the full current rent, and **adds** `4 − (week mod 4)` units to the current housing's rent stock. At a normal due week this adds four; in an extension week it may add three, two or one for the same full payment. This is not a proportional rent discount. Repeated payment adds again rather than replacing the stock; verify intended prepayment limits through the UI at runtime. [FL-001](finance-lifecycle.md#fl-001-ordinary-payment-buys-the-remainder-of-the-four-week-cycle) confirms the stored contract price, cash charge and additive remainder-of-cycle stock directly from package bytecode.

Evidence: [room1.sc, defaults/init, line 604](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L604), [rentOffice.sc, availability, line 84](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/rentOffice.sc#L84), [payment, line 247](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/rentOffice.sc#L247), [startTrn.sc, rent notice, line 437](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L437).

## HOME-002: requesting an extension

The player must have no paid rent units and must not already have tried this turn. The `rentExt` history value controls the first request:

| History value | Success condition | Analytical chance |
| --- | --- | --- |
| −1 | Always refused | 0 |
| 0 | Always accepted | 1 |
| 1 | Draw 1…12 greater than 3 | 3/4 |
| 2 | Draw 1…12 greater than 6 | 1/2 |
| Any other value | Draw 1…12 greater than 9 | 1/4 |

Success increments `rentExt`, adds 1 happiness and sets `triedExt = 1`. Failure loses 1 happiness and sets `triedExt = 2`. Repeated requests that turn produce escalating dialogue rather than another independent approval draw; the inspected repeat branches do not repeat the initial happiness deduction. At end turn, `leaveOpen` records whether `triedExt` was exactly 1, then `triedExt` resets. This extends access into the next turn; it does not grant prepaid rent units. [FL-002](finance-lifecycle.md#fl-002-extension-approval-and-arrears-form-a-flag-based-lifecycle) verifies these approval branches, repeat handling and end-turn flags in the package, together with the arrears conditions and due-notice reset described below. The stated probabilities remain analytical consequences of inclusive uniform Random, not measured frequencies.

Evidence: [rentOffice.sc, extension, line 295](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/rentOffice.sc#L295), [room1.sc, endTurn, line 775](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L775).

## HOME-003: unpaid rent becomes garnishment debt

At end turn, an existing current-housing rent object with zero quantity can create arrears. On fourth weeks, add `curRent` if there was no successful extension and `turnedOver` is false; set that flag when adding. On other weeks, the same checks also require existing arrears to be zero. The flag prevents the same unpaid obligation from repeatedly accruing, while the fourth-week notice resets it for a new obligation. Missing rent objects are a distinct edge: the accounting explicitly requires an object to exist.

Arrears do not force a move in these handlers. The inspected `livesAt` writes change housing only on successful moving purchases. The office offers a full-balance payment when its transaction controls are open and debt is nonzero; this uses the shared affordability handler, clears `rentOwed`, and removes that control. It does not buy current rent units or reset the extension history.

At work, rent debt garnishes wages. Let F = 8 × displayed hourly wage and D = arrears. If trunc(F/2) > D, cash is F − D and debt clears. Otherwise cash is trunc(F/2) − 2 and debt falls by trunc(F/2); equality takes this second branch and still charges the extra 2. Either branch sets `rentExt = −1`, so later extension requests are refused. This overwrites prorated partial-shift pay: see TIME-006 and the [direct package verification](bytecode-finance-findings.md#bc-fin-001-garnishment-really-overwrites-partial-shift-pay) for the confirmed branch order and precision examples. The pay overwrite and equality arithmetic are package-confirmed; their visible feedback has not been reproduced in controlled gameplay. No automatic savings debit is present in this path.

Evidence: [room1.sc, endTurn rent accounting, line 775](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L775), [rentOffice.sc, balance payment, line 725](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/rentOffice.sc#L725), [n108.sc, garnishment, line 127](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/n108.sc#L127).

## HOME-004: moving replaces the housing contract

Moving to low-cost or security housing uses economy-scaled base inputs 325 or 475. The destination purchase adds four prepaid units, charges the full destination price, sets `curRent` to that transaction price, and updates `livesAt`. The ordinary rent button is then updated to the new housing ID and contract price. These moves do not clear `rentOwed` in their inspected handlers.

Already living at the destination is refused. With sufficient cash and positive prepaid rent at the old destination, a human must confirm losing those units; declining cancels the move. Accepting zeroes old prepaid stock with no refund. Jones automatically accepts this confirmation. The destination stock is added through the common goods handler, so a pre-existing destination object is incremented rather than replaced; test round-trip moves at runtime. No separate moving-time charge is specified by these controls (the shared default `visitTime` is zero); the office entry still costs time. [FL-003](finance-lifecycle.md#fl-003-moving-forfeits-prepaid-stock-and-preserves-arrears) confirms the selected package confirmation/forfeiture, purchase and contract-update paths, including preservation of arrears. UI and restored-state boundaries remain untested.

Evidence: [rentOffice.sc, low-cost move, line 481](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/rentOffice.sc#L481), [security move, line 603](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/rentOffice.sc#L603), [Goods.sc, additive receipt, line 42](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/Goods.sc#L42).

## HOME-005: rest and apartment theft connect housing to needs

Both resident relaxation controls cost six hours if any time remained when pressed. Each use adds three relaxation, capped at 50; the first such relaxation action in a turn also adds two happiness. With zero time remaining the effect is refused. The recurring pre-turn stage reduces relaxation by one, with a floor of 10, unless the player has positive quantity of durable 28 (hot tub).

Apartment theft is tested only for low-cost housing, before food storage. With any durable objects and a zero result from `Random(0, relaxation)`, iterate all durables; except for IDs 21/22/23, each independently loses its entire quantity on a nonzero `Random(0,3)` result. If anything takes that branch, lose four happiness and show theft news. As written the inner test does not require the target's current quantity to be positive, so retained zero-quantity objects could affect notices. The refrigerator, freezer and stove are excluded. Security housing bypasses this apartment-theft branch; that does not establish immunity from every other theft/random event in the game.

Evidence: [lowcost.sc, relaxation, line 114](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/lowcost.sc#L114), [security.sc, relaxation, line 122](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/security.sc#L122), [startTrn.sc, decay/theft, line 265](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L265).

## Pending runtime scenarios and gaps

| Case | Controlled starting state / action | Script prediction or question |
| --- | --- | --- |
| N01 | Groceries only, no fridge, positive cash; normal recurring start | Spoilage −2, zero groceries; no 20-hour hunger charge; illness gate 1/2 before relaxation override |
| N02 | No food, no carried cash, positive savings | Hunger −2 and 20 hours; no doctor bill or automatic savings withdrawal |
| N03 | Food present, relaxation 10, compare with 11 across seeded runs | 1/5 override only at exactly 10; decay can make 11 become 10 before test |
| N04 | Groceries 7 with fridge, then groceries 13 with fridge/freezer | Cap then decrement: five / eleven left; −1 happiness |
| N05 | Freezer alone; retained zero-quantity refrigerator object | Freezer alone fails; object-presence behaviour needs reproduction and object-lifetime check |
| N06 | Buy three chickens versus three hamburgers; buy only drinks | Chicken stock decrements across starts; hamburgers expire together; drinks give no food coverage |
| N07 | Force doctor gate; carried cash 0, 1, 30, 31, 499, 500 | Suppression/bill ceilings and 499→500 discontinuity; no backend/random sampling claimed |
| H01 | Due-week rent quantity 1 before recurring start; leave unpaid | Decrement→notice→end-turn debt once; next non-due turn does not double-charge |
| H02 | First accepted extension; fail or omit payment the next week | `leaveOpen` access, no free rent units, then arrears; verify notice/flag sequencing |
| H03 | Extension histories −1,0,1,2,3 and repeated clicks | Approval odds and no reroll on repeat; history after paying rent/garnishment remains distinct |
| H04 | Pay full rent in weeks 4 and 5; repeat payment | Adds four versus three units for same stored price; confirm any UI prevention of repeated prepayment |
| H05 | Move both directions while prepaid; cancel once; keep debt | No refund on accept, cancel preserves state; new contract from economy; arrears remain |
| H06 | Full/one-hour work shifts with arrears below/equal/above half-shift | TIME-006 anomaly and $2 equality handling; subsequent extension permanently refused in inspected path |
| H07 | Low-cost/security rest at 0,1,6 hours left; repeat within turn | Partial final rest still full effect, happiness once, relaxation each successful action |

Remaining gaps: use narrow runtime cases for unresolved UI/presentation and restored-state questions, verify SCI random semantics and integer boundaries against runtime, trace object cleanup after breakage/theft, inspect any script patches outside the selected verified package paths, and audit street theft/repairs/durable purchase happiness separately. These findings clarify original mechanics; they do not approve extra meters, eviction, nutrition systems, gentler penalties, or bug fixes for the adaptation.


The [fresh-game package state](initial-player-state.md) includes no food, six casual-clothing units and three prepaid low-rent units; week1 skips the later recurring needs path. [Fast-food bonuses](fast-food-bonuses.md) now verifies all six controls, food versus drink receipt types and the shared once-per-turn meal/drink latches. That purchase-order rule is distinct from coverage, spoilage and illness above.
