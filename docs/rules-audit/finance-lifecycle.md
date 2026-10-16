# Package verification: rent, pawns and loan scheduling

Verified 2026-10-16. Evidence: **BYTECODE**, selected arithmetic and control flow from the actual website package, version 1.000.060. No gameplay was used. This advances the earlier **SCRIPT** findings in [housing](food-and-housing.md) and [goods/finance](goods-and-finance.md); it does not approve implementation or changes to original mechanics.

The [website bundle](https://jonesinthefastlane.com/bundle.jsdos) was retrieved 2026-10-15, SHA-256 `c08f3310f4f9cf47316bc32745507ae065bba7741430f7c3620602f534c46180`; see the [original retrieval record](../../artifacts/discovery/2026-10-15-bundle-inventory.json). [Verification metadata](../../artifacts/rules-audit/bytecode-finance-lifecycle-verification.json) records resource hashes, selected range hashes and a bounded inventory across all 69 decoded scripts. Original resources, disassembly and source comparison stay ignored under `work/`. Offsets below are hexadecimal, zero-based positions in decompressed SCI resource payloads, including block headers. Names come from package object records and vocabulary997 selectors; global302 is the active player and global372 the week counter.

## FL-001: ordinary payment buys the remainder of the four-week cycle

Script201 `rentOffice.init`, `0x028f–0x02bc`, selects goods40 for low-cost housing (`livesAt=0`), otherwise41, and sets `payRent.price` from the player's stored `curRent`. The transaction controls become available when `week % 4 == 0` or `leaveOpen` is true (`0x0275–0x028d`). Employment at the office separately enables work controls.

`payRent.doit` (`0x0602–0x06bb`) requires carried cash at least the price, calls consumables `recieve(indexNum, 4−week%4)` at `0x0633`, then debits `theSign×price` at `0x063c`. The object sign is −1 and its price is fixed. Script106 `ListOfGoods.recieve/hasType`, `0x00dd–0x0171`, creates a record if missing or adds to the existing quantity; this is additive stock, not an assignment.

| Week remainder | Rent units added | Cash charge |
| --- | ---: | --- |
| 0 | 4 | Full stored current rent |
| 1 | 3 | Full stored current rent |
| 2 | 2 | Full stored current rent |
| 3 | 1 | Full stored current rent |

No paid-stock cap or extension-history reset appears inside this payment method. That establishes the transaction behavior; repeated-payment reachability through every UI state remains untested.

## FL-002: extension approval and arrears form a flag-based lifecycle

Script201 `moreTime.doit`, `0x0728–0x0ae3`, first requires zero current-housing paid quantity and `triedExt=0`. It selects the following initial outcome at `0x0764–0x07bb`:

| `rentExt` history | Approval predicate | Analytical chance under inclusive uniform SCI Random |
| --- | --- | ---: |
| −1 | False | 0 |
| 0 | True | 1 |
| 1 | Random(1,12)>3 | 3/4 |
| 2 | Random(1,12)>6 | 1/2 |
| Other | Random(1,12)>9 | 1/4 |

Acceptance increments history, calls the happiness helper with +1, then sets `triedExt=1` (`0x07d0–0x0841`). Refusal calls that helper with −1 and sets `triedExt=2` (`0x0846–0x08a1`). Repeats branch directly to `0x08a6`, bypassing approval draws and these happiness calls. An already accepted request remains1; refused-repeat states2…5 advance by one for escalating replies and eventually remain6. No prepaid rent is awarded.

Script1 `Player.endTurn`, `0x0e9a–0x0f5b`, chooses goods40/41 and accrues `curRent` to `rentOwed` only if an actual current-rent record exists with zero quantity, `triedExt!=1`, and `turnedOver=0`. On non-fourth weeks it additionally requires existing `rentOwed=0`; on fourth weeks it can add another month's debt. Accrual sets `turnedOver=1`. Both week branches copy `(triedExt==1)` to `leaveOpen` and then reset `triedExt=0`. Thus an accepted extension grants next-turn office access and prevents that end-turn accrual; it does not erase debt. Script111 `0x0983–0x0a0d` decrements consumables, then on fourth weeks checks for a zero-quantity rent record, dispatches the rent notice and resets `turnedOver=0` at `0x0a0b`. This permits the new month's later accrual.

The separate arrears control uses the shared affordability transaction and, on success, writes only `rentOwed=0` in this debt family (`script201:0x0fd0–0x1052`). It buys no current rent units and does not reset `rentExt`. Wage garnishment and its partial-shift overwrite were already [verified separately](bytecode-finance-findings.md#bc-fin-001-garnishment-really-overwrites-partial-shift-pay).

## FL-003: moving forfeits prepaid stock and preserves arrears

Script201 `rentLowCost.doit` (`0x0b3c–0x0d19`) and `rentSecurity.doit` (`0x0d86–0x0f63`) reject the current destination. With enough cash, if the old housing record has positive quantity, a human confirmation is required: decline returns before purchasing; accept zeroes that old quantity. Jones (`playing=29`) directly takes the zeroing path. There is no refund call in these paths.

Both then call superclass55 `CostDItem.doit`. Their package object properties specify consumables type1, goods40/41, four units, sign−1 and base price325/475. Script104 `CostDItem.init`, `0x0344–0x0374`, uses the economy-price helper when `fixedPrice=0`; `doit`, `0x03cf–0x0403` and `0x049e–0x04a8`, receives those four units and debits the price. After success the move updates the ordinary rent control's goods ID/price and the player's `curRent`/`livesAt` (`0x0cb5–0x0cdb`, `0x0eff–0x0f25`). These handlers contain no `rentOwed` write, so moving does not discharge arrears. Existing destination stock is incremented through the same goods receipt rule.

## FL-004: pawn redemption expires after three end-turn aging steps

On an accepted pawn, script212 `0x1302–0x1347` sets attribute bits`0x18`, stores `trunc(pricePaid/2)` as `redemptionPrice`, and subtracts one quantity. Cash proceeds are a separate economy-scaled offer: `trunc(priceHelper(economy,pricePaid)×4/10)` (`0x1283–0x129c`), paid at `0x138c`. Redemption is therefore based on half the original recorded purchase price, not half the cash received from pawning.

Script1 `Player.endTurn`, `0x0df7–0x0e99`, loops durables and replaces masked bits`attributes&0x18` as follows, preserving unrelated bits:

| Before an end turn | After it | Redeemable? |
| --- | --- | --- |
| `0x18` | `0x10` | Yes |
| `0x10` | `0x08` | Yes |
| `0x08` | `0`, with `0x20` set | No; forfeited stock |

The end of the pawn transaction's own turn already performs the first step. The player can redeem during either of the next two turns before the third end turn expires the pawn. This is a control-flow timing deduction, not a measured runtime duration.

Script212's redemption list requires nonzero`attributes&0x18` (`0x06de–0x06e4`) and uses stored `redemptionPrice` as fixed price. Its buy-stock list instead requires`attributes&0x20` (`0x093d–0x0943`) across players' inventories. On successful redemption, `aRedeemableItem.doit` checks cash, debits the price, clears bits`0x38` with mask`0xffc7`, and, for redemption mode`local0=2`, increments the same durable's quantity (`0x1687–0x17ad`). Buying forfeited stock was outside this redemption pass; the subsequent [used-stock audit](pawn-used-stock.md) now traces the selected ownership/duplicate branches, browsing-time quality changes and shared capacity.

## FL-005: loan lateness checks the due week's payment flag

Script1 `Player.endTurn`, `0x0eab–0x0ec3`, enters loan scheduling only when `week%4==0` and `loanBal!=0`. It decrements `paySched`; if `madePayment=0`, it also increments `latePayments`. Both fourth-week and other-week exits reset `madePayment=0` (`0x0f07`, `0x0f57`). Consequently a payment made in week3 does not preserve the flag through week4, even though its schedule credit persists. A player with `paySched=2`, debt outstanding and no payment in the due week ends that week at schedule1 **and still gains one late-payment count**. This distinction matters because late payments reduce later loan qualification.

Script111's fourth-week recurring notice (`0x0af3–0x0b53`) requires debt. Schedule0 dispatches notice5; negative schedule calls happiness−1 and dispatches notice4; positive schedule skips these notices. No principal change or automatic debit is present in this inspected notice/scheduling path. Each successful payment increments the schedule and marks the flag; clearing principal resets schedule0, as already [package-verified](bytecode-finance-findings.md#bc-fin-003-a-full-50-payment-removes-45-principal). The recurring finance charge demonstrated there is the $50 payment removing $45 principal; it is not evidence for periodically compounding principal.

## Bounded default/seizure search and remaining gaps

All69 resource hashes and every listed instruction byte span were checked against the local decompressed payloads. This confirms listing-to-payload consistency, not an independent disassembler or execution test. The metadata inventories all69 decoded scripts for immediate selector candidates for `loanBal`, `paySched`, `latePayments`, `madePayment`, `rentOwed` and `livesAt`, plus named direct property writes/increments/decrements. Setter candidates were checked in their surrounding control flow. In those forms, loan principal writers occur only in bank script204's borrowing and repayment methods; housing setters occur only in rentOffice script201's successful moves. Rent debt writers occur in rentOffice, work garnishment and Player end-turn accounting. The search found no additional principal-compounding or debt-triggered housing-seizure writer in that bounded inventory.

This is stronger evidence than looking at one missed-payment branch, but is **not** a universal proof of absence: computed-selector sends, interpreter effects, save/restore mutations, patches and other editions are not established by this immediate-selector inventory. No default termination or forced eviction should be invented from the loan notices alone. Exact text/presentation, callbacks, unusual restored inventories and UI repeat-payment limits remain runtime or further analysis gaps. [Money word boundaries](money-word-boundaries.md) now supply selected carry/display fixtures, without settling all overflow cases. All preservation/correction choices remain undecided.
