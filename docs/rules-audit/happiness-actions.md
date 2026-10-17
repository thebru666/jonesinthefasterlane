# Happiness from purchases and deliberate actions

Audited 2026-10-16; consolidated 2026-10-17 against website DOS **1.000.060**. Evidence **BYTECODE**, all47 identified literal Main export13 calls in action scripts200…213, with selected inherited purchase/work/reset support. No runtime score observations or full dynamic-call absence proof. [Verification metadata](../../artifacts/rules-audit/happiness-actions-verification.json) gives every site, attempted amount, latch and selected method hashes. Original code and payloads stay ignored.

This completes the action side of the [Happiness catalogue](happiness-catalogue.md). [Event contributions](happiness-events.md) account for the other29 identified sites. Main's helper clamps each change to0…100; rewards and penalties below can be smaller at those bounds. The allocated starting score is0, not an implied bonus from starting possessions or cash.

## Shared active-turn latches

These are separate opportunities. The first successful qualifying purchase/action sets its category flag before applying the modifier. Repeats can still cost money/receive stock while giving no further category bonus. The ordinary active-player start-turn resets them; a same-turn location return does not. This is active-turn scope, not a shared week-long allowance across all players.

| Category / flag | Attempted Happiness | Identified action site(s) |
| --- | --- | --- |
| Rest,465 | +2 for first eligible rest across either home | Low-cost `200:0x02c4`; security `202:0x031c` |
| Baseball,466 | +2 first successful ticket purchase | `211:0x0e36` |
| Theatre,467 | +2 first successful ticket purchase | `211:0x0ec6` |
| Concert,468 | +2 first successful ticket purchase | `211:0x0f56` |
| Lottery,469 | +2 first successful lottery-ticket purchase | `203:0x096b` |
| Groceries,470 | One/two/four-week packs give +1/+2/+4, sharing one opportunity | `203:0x0744/0x0804/0x08c5` |
| Drinks,471 | Shake+2 or Cola+1, sharing one opportunity | `210:0x08fe/0x098e` |
| Enhanced meal,472 | Cheeseburger+1 or Chicken+2, sharing one opportunity | `210:0x077a/0x080a` |

Groceries therefore add another purchase-order effect beside the [fast-food categories](fast-food-bonuses.md): buying the one-week pack before the four-week pack yields only+1 through these handlers, while buying four weeks first yields+4. This does not change the separately granted stock. Hamburgers/Fries have no such Happiness override and consume neither enhanced-meal nor drink opportunity.

Eligible rest requires resident access and old spent time not equal60. Its time charge and relaxation increase are separate effects; a final partial six-unit rest can still give the full ordinary effect. A second rest increases relaxation again but not this score through the latched branch. Buying while already at Happiness100 still consumes a successful qualifying purchase's latch. Failed generic affordability does not consume the item latch; intentional refusal penalties below are different branches.

## Rewards that repeat on successful actions

| Action | Attempted modifier and condition | Sites |
| --- | --- | --- |
| QT business suit / dress clothes | +2 / +1 on **every** successful purchase; no first-purchase or per-turn latch | `209:0x05a4/0x0645` |
| New job / granted raise | +3 / +3 after the appropriate successful employment mutation | `206:0x047a/0x057f` |
| Course graduation | +5 on completion; ordinary lesson/enrollment has no direct modifier | `207:0x044a` |
| Accepted new loan or extension | +5 when the loan is accepted; merely qualifying/declining does not award it | `204:0x0ae6` |
| First rent-extension request accepted | +1 on initial approval | `201:0x07e9` |

The QT rewards differ from Z-Mart clothing, which has no Happiness call in its successful clothing handlers. The [clothing lifecycle](clothing-lifecycle.md), [employment](employment.md), [education](education.md) and [loan/extension rules](goods-and-finance.md) provide the associated eligibility, prices, stock and time effects. A table entry is not a promise that a repeat remains eligible without those checks.

## Refusals, joke products and pawning

| Action branch | Attempted modifier | Sites / order |
| --- | --- | --- |
| Refused new-job application feedback | −1 | `206:0x00e6`; refusal feedback bridge, not an automatic loss on every Work or raise attempt |
| Refused rent extension, first request | −1 | `201:0x0849`; repeated request dialogue does not repeat this call |
| Loan refusal | Extension−1; initial application two separate−1 calls | `204:0x0b9f`, plus initial-only `0x0bd7`; both independently clamp |
| Dog food / eight-track / Truman Capote joke purchases | −1 / −1 / −2 on each successful purchase | `211:0x1233/0x12b9/0x133f` |
| Accepted pawn | −1 | `212:0x130f` |
| Pawning refrigerator with a grocery record | Another−1, with grocery stock cleared | `212:0x1370`; presence of the grocery record, not a new food-purchase reward |

The joke products use type3: the shared purchase does not add them as food/durable inventory. They do not become useful food because of their names. Their negative changes repeat on successful purchases; unaffordable purchases skip them. Pawning's additional refrigerator branch can see a retained empty grocery record because [packing does not remove empty records](inventory-grouping.md).

## All18 nominal durable-purchase branches

Actual methods in both durable shops call their superclass first and then require success **and no post-receipt quantity** for the relevant item. Shared receipt already increases that quantity. Thus, with ordinary nonnegative initial quantities and a successful positive receipt, the condition is false for all18 listed overrides. These are recorded branch constants, not functioning first-purchase rewards.

| Socket City item | Nominal value | Z-Mart item | Nominal value |
| --- | ---: | --- | ---: |
| Refrigerator |1 | Refrigerator |1 |
| Freezer |2 | Stove |1 |
| Stove |1 | Stereo |1 |
| Colour TV |2 | Colour TV |1 |
| VCR |2 | Microwave |1 |
| Stereo |2 | VCR |1 |
| Microwave |2 | Encyclopedia |1 |
| Hot tub |3 | Dictionary |1 |
| Computer |3 | Atlas |1 |

The metadata identifies all18 call addresses and their containing methods. Z-Mart's black-and-white TV has no corresponding override. This extends the earlier refrigerator-only package check to the complete identified override set. It does **not** prove the branches unreachable under negative/wrapped quantities, restored corruption or arbitrary callback mutation. The legitimate recurring stove/microwave/computer effects are separate event paths and are not disabled by this purchase-order issue.

## Zero additional Happiness is also part of the contract

In the selected action paths, plain rent payment, arrears payment, moving, deposits, withdrawals, loan payment, investment Buy/Sell, redemption/used purchase, ordinary lesson/enrollment, casual-clothes purchase, Z-Mart clothing and ordinary work pay have no additional helper13 reward or penalty. Work and other cash mutations do not imply a Happiness change. Housing/finance events and successful hiring/graduation can have separate calls elsewhere.

This is a bounded inventory of known literal action calls and selected inherited handlers, not a proof against arbitrary computed sends, native memory changes or every possible callback. Exact visible message timing, unusual balances/inventories, restored flow and future keep/change decisions remain separate. No new-game rule is approved by this catalogue.
