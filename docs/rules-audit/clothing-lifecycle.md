# Package verification: clothing purchases, wear and recovery

Verified 2026-10-16. Evidence: **BYTECODE**, selected actual website DOS1.000.060 resource properties and control flow, plus explicitly analytical examples. No gameplay or visible warning reproduction. This closes the ordinary clothing-purchase/lifetime gap around [EMP-005](employment.md#emp-005-clothing-attendance-and-firing), [GOODS-005](goods-and-finance.md#goods-005-tickets-and-short-lived-stock) and [emergency support](random-events.md#event-008-emergency-cash-is-gated-recovery-not-a-random-weekly-grant); adaptation choices remain undecided.

[Verification metadata](../../artifacts/rules-audit/clothing-lifecycle-verification.json) identifies seven resource hashes, selected method/range hashes, all five clothing purchase records and relevant shared class records. Bundle SHA-256 `c08f3310f4f9cf47316bc32745507ae065bba7741430f7c3620602f534c46180`; [retrieval record](../../artifacts/discovery/2026-10-15-bundle-inventory.json). Offsets are hexadecimal, zero-based decompressed script payload positions including block headers. Original bytes, disassembly and source comparison stay ignored under `work/`.

## CLOTH-001: five offers, additive stock and repeatable QT rewards

All five package purchase records use consumables type1, sign−1, economy-adjusted base prices (`fixedPrice=0`) and zero extra visit time:

| Shop / offer | Clothing ID | Stock added | Base price | Happiness after each successful purchase |
| --- | ---: | ---: | ---: | ---: |
| QT business suit | 34 | 13 | 295 | +2 |
| QT dress clothes (`leisureSuit`) | 35 | 13 | 125 | +1 |
| QT casual clothes | 36 | 11 | 73 | 0 |
| Z-Mart dress clothes | 35 | 9 | 90 | 0 |
| Z-Mart casual clothes | 36 | 9 | 35 | 0 |

QT records/methods are in script209; Z-Mart in211. This table specifies stock granted per accepted transaction, not a separate garment-selection system. Z-Mart availability is governed by its rotating stock lifecycle, outside this pass. It has no business-suit purchase record among its eighteen listed items.

Script104 `CostDItem.init/doit`, `0x0344–0x0374` and `0x03ad–0x051d`, computes the economic price, checks carried cash, receives the configured units and debits price. Script106 `recieve/hasType`, `0x00dd–0x0171`, creates an absent record or adds units to the existing clothing group. Buying clothes stacks duration rather than replacing the old stock. Each shop entry has its separately established time cost; these zero-visit-time controls add no action hours.

QT methods `0x0592–0x05bc`, `0x062a–0x0654` and `0x06c2–0x06e7` test **only shared success flag416** before their clothing side effects. Business suits call happiness+2; dress clothes call+1; casual calls no happiness helper. There is no first-purchase, zero-quantity or per-turn reward latch in these methods. Two successful suit purchases add26 units and make two+2 calls, subject to the common0…100 happiness clamp. This differs from the skipped refrigerator bonus condition and from once-per-turn food/ticket bonuses. Insufficient cash produces none of these subclass rewards/resets.

Z-Mart's two methods (`211:0x0cf4–0x0d19`, `0x0d86–0x0dab`) likewise require success, then update dressing and reset `nakedCount`; neither awards happiness. Their superclass75 `DiscountDItem.doit` (`0x02f2–0x0322`) delegates the actual purchase to class55 and, when receipt and success exist, ORs bit`0x100` into the received group. This quality flag does not change `Consumable.doit`'s decrement rule. Grouped historical fields/flags remain shared across purchases; no per-copy quality or separate wardrobe is created.

## CLOTH-002: all grades age together; the displayed remaining duration is a maximum

Player initialization gives ordinary active participants casual stock6 at `1:0x0bef`, with recorded price30. Week1's recurring-path skip (`111:0x051c–0x052d`) bypasses the clothing decay/warning/recovery stages along with other recurring effects.

At later start turns, state16 sends `eachElementDo(doit)` to **all consumables** (`111:0x0983–0x0991`). The received clothing records are class61 Consumable. Its `doit` (`106:0x0034–0x003b`) decrements quantity whenever it is nonzero, leaving zero unchanged. For ordinary nonnegative stocks this subtracts one from every positive clothing grade, even grades not currently worn. It does not consume a selected suit first and save casual clothes for later.

`Player.dressedForWork` (`1:0x0bf4–0x0c6e`) builds the grade lookup for36,35,34, then scans backward: business34 first, dress35 second, casual36 last. The first present record with nonzero quantity sets `wearing`; otherwise `wearing=0`. Work is allowed only if something is worn and `wearing <= uniform`, so a better grade satisfies a less formal requirement. Hiring need not wait for correct clothes; actual Work checks dressing separately (`108:0x0019–0x0052`).

`Player.weeksOfClothing` (`1:0x0c6f–0x0cd9`) returns the **largest positive quantity across all three grades**, starting from zero. It is neither their sum nor necessarily the remaining quantity of the best/currently worn grade or the grade required by the job. The grade-array interpretation was checked from actual indexed-store/load instructions; the earlier conservative pseudocode misrendered those array setup stores; the decoder's indexed-store fix now reports their popped values correctly.

For example, before a recurring tick, suit2 and casual10 become suit1 and casual9. The player wears the suit, but `weeksOfClothing=9`. At the following tick the suit expires and casual becomes8; a business-suit job then fails its clothing check while the aggregate duration is still8. These are arithmetic deductions from the selected methods, not runtime observations.

## CLOTH-003: one-week warning follows decay, with no clothing-specific time penalty

Start-turn state18 first recomputes `dressedForWork`, then chooses the walker appearance from `wearing`, using the unclothed variant when `weeksOfClothing=0` (`111:0x0a25–0x0abd`). It dispatches notice6 **only when the maximum duration equals1** (`0x0abf–0x0ad4`). The example above therefore receives no one-week warning for the expiring suit while casual stock remains9.

This selected stage has no automatic replacement purchase, cash debit or happiness penalty for zero clothing. The shared notice continuation (`111:0x165e–0x16ab`) charges10 hours only for doctor register3 and20 only for hunger register0; clothing register6 gets neither charge. Exact visible notice/art timing remains untested.

The recurring state selects Jones's separate base walker view when `playing=29` (`0x0a77–0x0a86`), but its quantity/dressing/warning tests are shared. Clothing failure blocks Work in the selected shared handler; work-history firing is a separate condition, not an automatic naked-state dismissal in these methods.

## CLOTH-004: successful purchases reset the emergency-support counter

Every one of the five successful clothing handlers calls `dressedForWork` and writes `nakedCount=0`. QT's happiness calls are additional effects, not the condition for that reset. A failed purchase does not reset it. The default Player property initializes this counter to0.

Late recurring state34 (`111:0x120d–0x134f`) computes ordinary durable recorded value, subtracting one quantity for records with pawn/forfeiture mask`0x38`. Recovery eligibility requires cash-high0, cash-low<=0, `weeksOfClothing=0`, and that durable subtotal<200. It does not check savings. A qualifying check increments `nakedCount`; when the incremented value exceeds1 it resets the counter and grants cash. A nonqualifying visit does not itself reset the counter in this branch: this counts qualifying checks without an intervening reset, not necessarily consecutive calendar weeks.

The grant is the economy-price helper applied to base295/125/73 for required uniform34/35/36, otherwise50, plus Random(1,100). It calls the cash helper and dispatches notice12 (`0x12df–0x1346`); it does not directly award clothing or happiness. Week1 skips this recovery branch. Exact random frequencies, value overflow and visible presentation remain separate limitations.

A bounded search of all69 decoded scripts found nine immediate `nakedCount` selector occurrences: seven setter candidates resolve to these five purchase resets and the state34 increment/reset; two are state34 reads. This corroborates the documented ordinary lifecycle, without claiming absence of computed selector sends or restored state.

## Human/computer scope and remaining limits

Neither QT nor Z-Mart's five purchase methods contains a human/computer-specific stock, reward or reset branch. Jones's QT action controller routes synthetic keys to the same controls according to required uniform, and its incidental purchase path additionally tests affordability and `weeksOfClothing<=1` (`209:0x0a27–0x0af4`). That is a purchasing-policy difference; it does not give a different product duration or happiness reward. Complete AI destination choice and rotating-stock decisions remain covered by their separate audits.

These are ordinary nonnegative-stock rules and selected recovery arithmetic. Negative/corrupt quantities, signed overflow, callback re-entry, retained/restored scripts and final rendered presentation are not established here. No application code or decision to change these rules has been approved.
