# Package trace: food, illness and selected events

Verified 2026-10-16 against website DOS1.000.060. **BYTECODE** applies to the selected instructions and constants below; earlier domain findings retain their own evidence labels. [Metadata](../../artifacts/rules-audit/bytecode-needs-events-verification.json) records resource hashes/ranges: 1,654 selected instruction records matched their raw payload spans, with ten independently read constant/comparison landmarks. This is not a second interpreter or a runtime experiment. Original listings remain local.

## NE-B01: food coverage is sampled before food changes

Actual script111 states8–14 (`0x0702–0x096d`) establish this sequence:

1. Scan consumables5 down to1; retain the first nonzero quantity found (positive for ordinary stock) as a food marker (`0x0709–0x0744`). It is a coverage test, not selection of the only item to consume.
2. Inspect grocery item1. If stock exists but durable lookup21 returns no refrigerator object, clear all grocery quantity, apply happiness−2, and set the marker to−1 **only if it was1** (`0x0783–0x07bf`). A higher fast-food marker is preserved.
3. With a refrigerator, lookup22 determines freezer presence; cap grocery quantity above6 without a freezer or above12 with one, applying−1 happiness (`0x07c5–0x0838`). These are **object** lookups, not positive-quantity tests on the appliances.
4. Clear all stock of food IDs5,4,3, without clearing the earlier coverage marker (`0x0857–0x0882`). Chicken2 does not take this explicit clearing loop.
5. Marker0 applies happiness−2, records a Random(0,3) result and launches hunger notice0 (`0x0885–0x08ab`). Marker−1 is nonzero and therefore bypasses that separate hunger notice.
6. Later state16 calls every consumable's `doit` (`0x0991`). Actual script106 `Consumable.doit`, `0x0034–0x003b`, decrements a nonzero quantity once. Thus capped groceries6/12 become5/11, and other nonzero consumables also age.

This directly confirms [NEED-001–003](food-and-housing.md). Sole grocery spoilage avoids the separate twenty-hour hunger charge in this package; that is not merely a published-decompiler suspicion. Whether a zero-quantity appliance object can survive long enough to affect the presence checks remains an object-lifetime question. No new health/death subsystem is implied.

## NE-B02: illness and notice time costs

Script111 initializes the safety value to1. No food supplies Random(0,3); sole-food spoilage replaces it with Random(0,1) (`0x08ca–0x08d8`). If relaxation is exactly10, a later Random(0,4)==0 sets it to0 (`0x08da–0x08f7`). Only safety0 **and available carried cash>0** reach the doctor outcome (`0x091f–0x092d`). These actual draw order/branches confirm the analytical gates:

| Food marker | Relaxation above10 | Relaxation exactly10 |
| --- | ---: | ---: |
| Usable food | 0 | 1/5 |
| No food | 1/4 | 2/5 |
| Sole groceries spoiled | 1/2 | 3/5 |

Fractions assume inclusive uniform reference `Random`, not measured DOS frequencies. The extra relaxation draw is taken after the relevant food draw; even an eventual cash refusal can have consumed those random values.

Bill ceiling starts200, becomes50 when available cash<500, and is capped by that cash (`0x08f9–0x091d`). If ceiling>30, draw30…ceiling; otherwise charge the ceiling. The outcome applies happiness−4, debits cash through Main export10 and launches doctor notice3 (`0x0930–0x0964`). It does not withdraw savings automatically.

The **notice continuation** carries the time cost: register3 calls `timeKeep.doit(10)` at `0x1675`; register0 calls `doit(20)` at `0x169a`. Thus food/doctor mutations and time/acknowledgement are separate stages. Hunger plus doctor can spend30 of60 before control returns. The original ordering must not be replaced by one generic immediate “needs penalty” without an explicit change.

## NE-B03: apartment theft and repair eligibility

Theft in actual script111 `0x0595–0x06f3` follows relaxation decay. Without positive hot-tub quantity, relaxation drops1 but is floored10. Only low-cost housing0 proceeds to Random(0,relax)==0 and a nonempty durable list. Each durable except IDs21,22,23 gets a Random(0,3) check; nonzero clears its **whole quantity**. If any selected entry triggers the stolen flag, apply happiness−4 and open the theft/news presentation. Security housing does not take this branch. The quantity/lifetime of retained empty objects is not independently resolved here.

Repairs at `0x0b64–0x0d10` test **cash>500**, exclude book IDs31,32,33, require attribute0x0040, and use the original protection/pawn mask0x0038 plus quantity condition. The eligibility expression is not simply “all owned items may break.” Attribute0x0100 selects denominator35 instead of50; the actual draw is inclusive Random(0,denominator)==0, hence nominal1/36 or1/51 per eligible tested candidate. The bill draws from trunc(pricePaid/20)…trunc(pricePaid/4), applies happiness−1, debits cash and suspends through a repair notice. Inventory protection/quantity cleanup and every resume/candidate interaction remain bounded by the [goods audit](goods-and-finance.md).

## NE-B05: packing does not discard empty inventory records

Actual script106 `ListOfGoods.pack`, `0x0172–0x023f`, is **not a zero-quantity cleanup**. It checks attribute bit0x0001, clones/replaces entries with that bit while clearing it, then adds replacements back to the list. An entry without that bit is left alone regardless of quantity. There is no quantity selector read in this method. Location return invokes pack on all three inventory lists (`1:0x061d–0x0648`). Thus “quantity0 means remove the record at exit” is not the original contract.

An accepted pawn action sets attributes OR0x0018 and subtracts1 quantity (`212:0x131a–0x1347`), preserving other bits. Given an already packed one-unit record with bit0x0001 clear, that action leaves a retained quantity0 record, and the inspected exit pack leaves it alone. For a refrigerator, the pawn handler additionally clears existing groceries and happiness−1 (`0x134d–0x137a`). At a later storage test, lookup21 checks object presence rather than quantity. These inspected paths therefore permit a refrigerator record to satisfy the presence test after its usable quantity is exhausted; they do not support silently treating presence and positive ownership as identical.

This narrows the earlier object-lifetime uncertainty: the selected pack/pawn/storage chain does not delete the record. It is not a full audit of every inventory-removal method, interpreter clone implementation, pawn-expiry path or restored state, and no ordinary-play scenario is claimed. Quantity-based equipment/ownership effects remain different from object-presence storage checks.

## EV-B01: weekends prioritize tickets; redraw really calls the debit helper

Actual script232 `weekendText.draw`, `0x0722–0x08b7`, checks ticket37, then38, then39; the first positive category is selected and its **entire quantity** is cleared. Otherwise it calls the possession selector at `0x07fb`; failing that it draws general outcome17…60, rerolling the shared previous index. Possession selection `0x0360–0x03d0` scans IDs21…33, checks positive quantity and uses the full durable-list size in its draw. These branches agree with [EVENT-001/002](random-events.md).

Fresh weekend initialization (`0x0488–0x0507`) chooses low expense5…20 only with carried cash, then medium15…55 and high50…100. The outcome/debit helper `0x03d1–0x0467` caps spending to available cash and calls Main export10; it does not draw from savings.

The suspected [EVENT-003 redraw anomaly](random-events.md#event-003-weekend-redraw-can-debit-cash-again) is present in actual bytes: when remembered outcome local8 is not−1 (`0x072a–0x072f`), `draw` draws a fresh1…20 expense (`0x0736`) and calls that same debit helper (`0x073f`). This is not a pure text repaint. **Which ordinary UI redraws reach it, and how often, remains unproved.** The package confirmation must not be presented as an observed repeat-charge exploit.

## EV-B02: lottery thresholds and ticket consumption

Script111 `0x046d–0x0514` looks up ticket object9, then draws **one** Random(0,500), even if a retained object has quantity0. A win requires **quantity>draw** (`0x0485–0x0486`). It then tests draw≤trunc(quantity/20) for5000, otherwise draw≤trunc(quantity/5) for500, otherwise200. Prize constants at `0x049b/0x04b3/0x04b9` and comparison directions were independently read from the raw bytes. Happiness is10 for5000 and5 for the other prizes. Both win and loss clear all ticket quantity (`0x0500/0x050a`).

This upgrades the selected resolution formula in [EVENT-004](random-events.md) to BYTECODE. The existing [1,503-case enumeration](../../artifacts/rules-audit/lottery-probability-check.json) now corresponds to these actual ordinary-range thresholds. It remains an analytical enumeration, not original-game execution, measured RNG odds, extreme-quantity validation or verification of every ticket purchase path.

## EV-B03: mugging is selected at entry and clears cash at exit

Actual market script203 draws Random(0,50) at `0x0552`, then checks positive available cash and sets flag446=1. Bank script204 similarly draws Random(0,30) at `0x02f8`, then checks cash and sets446=2. The order matters: cash0 can still consume the entry draw. Normal eligibility probabilities are1/51 and1/31 under uniform inclusive draws.

After each dialog's ordinary `doit` returns, the pending flag causes **both carried-cash words to be cleared** at `203:0x05b4` or `204:0x035a`. The amount lost is therefore cash held at exit, not a captured entry balance. Savings are not cleared by these calls. Board continuation separately handles happiness and animation, as already traced in [location flow](bytecode-flow-and-persistence.md#flow-002-travel-entry-and-return). Restored initializations and removal/quit boundaries retain their limits.

## EV-B04: computer ownership windfall

Actual script111 `0x0530–0x0586` checks positive computer quantity29, draws Random(0,6)==0, applies happiness+3 and draws cash20…100, then launches its notice. This occurs after lottery and before apartment theft; week1 skips it. It confirms the ordinary selected branch of [EVENT-007](random-events.md), not a separate second computer reward.

## Scope before adaptation

These are package confirmations of selected needs/event predicates, amounts and operation order. Other rent/moving/pawn/default/crash/emergency/joke paths retain their existing evidence unless independently linked elsewhere. Random uniformity, exact DOS draw state, every notice resume, empty-object lifetime, graphical redraw reachability and high-value overflow remain explicit research boundaries. No quirk has been approved for copying or correction in2.0.
