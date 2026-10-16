# Goods, possessions, banking and investments

Pass 2, 2026-10-15. Status: partial, with ordinary transaction paths traced. Evidence: **SCRIPT** from the published floppy 1.000.060 decompilation, pinned at `870a8015b689474484bf3d8b41416956d4315432` ([S02](../discovery/source-register.md)). The broad catalogue remains external script analysis. Selected inventory, used-stock, investment, loan, purchase, pawn-aging/redemption and repayment-scheduling paths are now verified against the website bundle bytecode in the linked findings; this does not establish whole-source equivalence or controlled runtime observation. Analytical examples below are calculations, not gameplay traces. All adaptation mappings remain **undecided**.

The following sections complement [economy](economy.md), [weekly processing](weekly-processing.md), and [time and actions](time-and-actions.md). Prices below are **base** values unless explicitly fixed; ordinary offers use ECON-003. Food and housing consequences have a separate audit.

## GOODS-001: the purchase and inventory transaction

The shared purchase control checks **carried cash**, rather than automatically accessing savings. On success it receives the indicated units into the consumables, durables or education list, records the index, normally records the current price paid, and changes cash. Goods type 3 or 4 has no inventory-receive branch in this helper; those controls may implement their own effect. The configured visit time runs after both successful and unsuccessful attempts.

Goods are grouped by index. Buying the same type increases the existing object's quantity; it does not create a separate object for every individual purchase. Consequently `pricePaid` is a field on the grouped object, not a full purchase history. A normal later purchase overwrites that field unless the object carries pawn/redemption bits `0x0038`. A multiple-unit purchase records the transaction price, not necessarily a per-unit historical cost.

Evidence: [WButton.sc, CostDItem, lines 162–255](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/WButton.sc#L162), [Goods.sc, receive/grouping, lines 46–72](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/Goods.sc#L46).

The [full selected inventory trace](inventory-grouping.md) verifies mutating `hasType` grouping, price replacement and discount flags, object-versus-quantity lookup, and `pack` cloning/reordering without merging groups or deleting empty records. These are package findings; broader caller/removal paths and restored lists remain separate.

## GOODS-002: durable catalogue and purchase-happiness trap

| Index | Item | Appliance base | Discount base | Nominal appliance bonus in item method |
| --- | --- | ---: | ---: | ---: |
| 21 | Refrigerator | $876 | $650 | +1 |
| 22 | Freezer | $513 | — | +2 |
| 23 | Stove | $570 | $490 | +1 |
| 24 | Colour TV | $525 | $349 | +2 |
| 25 | VCR | $333 | $250 | +2 |
| 26 | Stereo | $412 | $450 | +2 |
| 27 | Microwave | $330 | $220 | +2 |
| 28 | Hot tub | $1,255 | — | +3 |
| 29 | Computer | $1,599 | — | +3 |
| 30 | Black-and-white TV | — | $110 | — |
| 31 | Encyclopedia | — | $475 | — |
| 32 | Dictionary | — | $70 | — |
| 33 | Atlas | — | $55 | — |

Discount-labelled does not guarantee the lower base: the stereo is $450 there against $412 at the appliance shop. Discount variants of refrigerator, stove, stereo, colour TV, microwave, VCR and books have nominal +1 bonus branches; black-and-white TV has no such override.

**Do not treat those nominal bonuses as confirmed first-purchase happiness.** The item methods call the shared purchase first, then test that the acquired item's quantity is absent. The shared purchase has already increased quantity, and `objectAtIndexQuan` reads that quantity. In the ordinary positive-quantity success path this makes the subsequent bonus condition false. The [website-bytecode refrigerator verification, BC-GOODS-001](bytecode-purchase-findings.md), confirms that exact superclass-first order and the receipt/quantity helper semantics for that selected path. For the refrigerator this is a package implementation quirk rather than an unverified decompiler-ordering issue; the other listed item overrides still rely on the published-source audit. Runtime presentation and unusual callback/state boundaries remain separate questions. The table records branch constants, not a promise that they execute.

Evidence: [appliance.sc, all items, lines 265–566](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/appliance.sc#L265), [discount.sc, items, lines 324–718](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/discount.sc#L324), [Goods.sc, quantity lookup, lines 107–111](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/Goods.sc#L107).

## GOODS-003: what possessions do between turns

| Possession/condition | Traced recurring effect |
| --- | --- |
| Stove **or** microwave with positive quantity | +1 happiness at start-turn, once for the combined condition, before the four-goal check |
| Computer | +1 extra-credit allowance during start-turn setup; later a 1/7 chance of $20–$100 cash and +3 happiness |
| Encyclopedia **and** dictionary **and** atlas | +1 extra-credit allowance; combined with computer gives 2 |
| Hot tub | Suppresses the ordinary one-point relaxation decay; without it relaxation declines to a minimum of 10 |
| Any positive-quantity durable, indices 21–33 | May select a possession-based weekend anecdote; checked by index order, with a random roll and repeated-outcome suppression |

The computer cash event and relaxation step are among the processing skipped in week 1. Extra credits are calculated earlier. These effects depend on owned quantity; the object merely remaining in the list after pawning is insufficient for the quantity-based checks. Refrigeration/freezer storage effects are covered by the food audit.

Evidence: [startTrn.sc, ownership happiness, line 77](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L77), [education allowances, line 183](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L183), [computer/relaxation, lines 241–277](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L241), [weekend.sc, selection, lines 91–109](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/weekend.sc#L91).

## GOODS-004: repairs, discount flags and quantity boundaries

Durables begin with attributes decimal 69 (`0x0045`), including repair eligibility `0x0040`. Discount purchases add `0x0100` to the received object. Thus repeated purchases of the same grouped type can affect the flag for the whole group.

The start-turn repair pass requires carried cash **strictly greater than $500**, repair eligibility, an index other than the three books, and either no pawn/forfeiture bits or quantity greater than one. It rolls once per eligible grouped object: discount-flagged probability 1/36, otherwise 1/51. A selected repair costs an inclusive random integer from `trunc(pricePaid/20)` to `trunc(pricePaid/4)`, and −1 happiness. The state returns to present a notice when a repair is selected; the exact continuation/multiple-notice behaviour remains a runtime test case.

The gate does not explicitly require positive quantity for an unpawned object. A stolen zero-quantity object can remain in the list; do not assume that a repair requires a currently usable item. Similarly, books are excluded by explicit index checks even though their generic durable class has the repair flag.

Evidence: [Goods.sc, Durable defaults, line 28](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/Goods.sc#L28), [discount.sc, DiscountDItem, line 148](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/discount.sc#L148), [startTrn.sc, repair pass, lines 509–590](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L509).

## GOODS-005: tickets and short-lived stock

Discount casual/dress clothes cost base $35/$90 and add 9 quantity units; a successful purchase refreshes dressing selection and clears the naked counter. Baseball/theatre/concert tickets cost base $45/$30/$40 and add 4 units. Each ticket category grants +2 purchase happiness at most once per active turn, using category flags reset during start-turn. The ticket check differs from the suspicious durable bonus check and can execute normally.

Consumables decrement one unit when positive during recurring processing. Ticket quantities are therefore coverage-like stock, not necessarily a literal count of independently selected seats. Complete ticket/weekend priority and clothing/job eligibility belong to their broader content/needs audits; this section does not imply every consumable has the same effective lifespan.

Evidence: [discount.sc, clothes/tickets, lines 518–635](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/discount.sc#L518), [startTrn.sc, flag reset, line 169](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L169), [consumable tick, line 437](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L437).

## GOODS-006: pawn, redemption, expiry and used purchases

Pawning is an explicit offer/accept transaction. For stored `pricePaid = P` and current goods reading `G`:

- Offer: `trunc(4 × ordinaryPrice(G, P) / 10)`; the economic price helper is applied again to historical cost.
- Redemption price: `trunc(P/2)`, independent of the current offer.
- Accepting gives the offered cash, −1 happiness, decrements owned quantity and sets protection/countdown bits to `0x0018`. Pawning a refrigerator additionally clears regular grocery stock if that consumable object exists, with another −1 happiness.

The shop has capacity for six grouped entries across **all players**, counting any object with bits `0x0038`, rather than six per player. A grouped type already carrying those bits cannot be pawned again even if extra quantity remains; selection may show it but return a refusal.

End-turn advances the countdown `0x18 → 0x10 → 0x08 → 0`, then sets forfeiture bit `0x20`. This occurs at the owner's end-turn, so pawning during a turn consumes the first stage at that same turn's end. Redemption remains possible during the next two turns, until the third end-turn aging step clears the countdown. Redemption lists the owner's objects with `0x18` bits and costs the stored redemption price. Paying clears `0x38` and increases quantity by one. After forfeiture, the Buy submenu scans every player's objects for `0x20`, offers them at the stored redemption price and marks them discount-quality. Successful used purchase clears pawn bits and transfers/increments ownership, including grouped duplicate handling.

[FL-004](finance-lifecycle.md#fl-004-pawn-redemption-expires-after-three-end-turn-aging-steps) confirms the package pawn flags, transaction-turn aging, stored-price redemption arithmetic and same-record quantity restoration. The subsequent [used-stock trace](pawn-used-stock.md) verifies shared capacity, ownership transfers and duplicate grouping. Opening Buy already sets the source group's discount bit before payment; existing buyer groups gain quantity without adopting the source's historical price/quality/pawn fields. Retained donor copies share the browsing-time flag changes. No runtime duration or presentation test is implied.

Illustration, ordinary non-overflow range: a $525 recorded item at goods reading 100 gives a $210 pawn offer and $262 redemption price. At reading 190, the offer becomes $524 because the intermediate price is $1,312; redemption stays $262. This demonstrates a possible price asymmetry, not a tested arbitrage strategy.

Evidence: [pawnShop.sc, eligibility, lines 85–138](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/pawnShop.sc#L85), [shared capacity, line 141](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/pawnShop.sc#L141), [redemption list, line 202](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/pawnShop.sc#L202), [used list, line 276](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/pawnShop.sc#L276), [pawn transaction, lines 739–815](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/pawnShop.sc#L739), [redeem/transfer, lines 927–990](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/pawnShop.sc#L927), [room1.sc, ageing, lines 755–773](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L755).

## FIN-001: deposits and withdrawals

Each click transfers up to **$100**, with a smaller final transfer if the source has less. Deposit checks available carried cash; withdraw uses the bank's low balance, or treats a nonzero high balance as sufficient for a full $100. Both update cash and the bank pair. The withdrawal joke mentions a penalty, but the traced transfer contains no separate withdrawal charge.

No savings-interest credit or T-bill yield-growth setter was found in the inspected published-script paths and repository-wide searches for bank-balance/share mutations. Treat “no interest in the examined implementation” as a bounded script finding, rather than deriving a percentage from the bank's jokes. Sudden cash-loss flags and the severe-crash low-bank reset are separate hazards, not transaction fees; the crash high-word anomaly remains open under ECON-006.

Evidence: [bank.sc, balance helper, line 39](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/bank.sc#L39), [deposit, line 203](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/bank.sc#L203), [withdraw, line 279](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/bank.sc#L279).

## FIN-002: loan qualification and extension

Applying costs 2 hours when time remains; approval/acceptance itself is separate from the application. Let:

- Capacity score = `wage + trunc(storedLiquidAssets / 1000)`.
- Required score = `5 + latePayments + trunc(loanBalance/100) + (loanBalance != 0 ? 1 : 0)`.

Approval requires capacity **strictly greater** than required. The offered additional amount is `100 × (capacity − required)`. Acceptance adds that amount to carried cash and debt and gives +5 happiness. Existing debt produces an extension offer using the same formula. Jones accepts automatically; humans receive Yes/No. Declining does not add debt. At exactly exhausted turn time the application is refused without the normal application path.

Example: wage 10, stored liquid assets $2,000, no late payments and no debt gives score 12 versus 5, offering $700. With $100 debt the required score becomes 7, offering $500, subject to what the stored asset field contains at that point.

The method reads the low liquid-assets field directly and does not recalculate assets or consult its high field. It also does not initialise/reset the repayment schedule on acceptance. A rejected extension gives −1 happiness; a rejected initial loan executes two −1 calls, each clamped to 0…100, so the total reduction is at most two. The [package bytecode verification, BC-FIN-002](bytecode-finance-findings.md#bc-fin-002-initial-rejection-has-two-happiness-reductions) confirms the qualification formula, strict comparison, low liquid-assets read and both penalty calls, including the actual happiness helper. The [schedule lifecycle follow-up](finance-lifecycle.md#fl-005-loan-lateness-checks-the-due-weeks-payment-flag) verifies selected notice/end-turn handling; visible feedback remains untested. Do not replace this path with a simplified “loan limit” formula.

Evidence: [bank.sc, applyForLoan, lines 445–579](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/bank.sc#L445).

## FIN-003: loan payment, charge and arrears

The payment button normally costs fixed $50. With debt below $50 it costs exactly the remaining balance. A successful full $50 payment reduces principal by **$45**, implying a $5 charge per full payment; a smaller final payment reduces principal by its entire cost. Every successful payment increments `paySched` and sets `madePayment = 1`; clearing the debt resets `paySched` to zero.

Fourth-week start-turn processing shows a due notice when schedule is zero; a negative schedule adds −1 happiness and shows an overdue notice. Fourth-week **end-turn** decrements schedule if debt remains and increments `latePayments` if no payment flag is set. However, end-turn clears `madePayment` on every week. A payment on week 3 can buy schedule credit while its flag has already reset before week 4 ends. [FL-005](finance-lifecycle.md#fl-005-loan-lateness-checks-the-due-weeks-payment-flag) confirms this directly in the package: with outstanding debt, `paySched = 2` and no due-week payment, fourth-week end-turn leaves `paySched = 1` **and increments `latePayments`**. Repeated-payment and timing effects must therefore be preserved explicitly rather than inferred from monthly wording.

Example: a $100 loan takes payments $50, $50, $10 to clear: $110 cash repaid. [BC-FIN-003](bytecode-finance-findings.md#bc-fin-003-a-full-50-payment-removes-45-principal) confirms the website package subtraction, price update, schedule/flag writes and shared cash-debit helper. This is direct ordinary-path arithmetic, not an annual interest rate. The [bounded inventory across all 69 package scripts](finance-lifecycle.md#bounded-defaultseizure-search-and-remaining-gaps) found loan-principal writers only in the bank's borrowing/repayment paths and housing setters only in successful office moves, within immediate-selector and named direct-property forms. It found no additional automatic compounding or debt-triggered housing-seizure writer in that scope; computed sends, interpreter/save effects and other editions remain outside that claim.

Evidence: [bank.sc, payment, lines 364–434](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/bank.sc#L364), [room1.sc, end-turn debt bookkeeping, lines 775–808](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L775), [startTrn.sc, due/overdue, lines 490–503](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L490).

## FIN-004: six investments, one unit per transaction

| Investment | Base/unit | Pricing |
| --- | ---: | --- |
| T-bills | $100 | Fixed |
| Gold | $413 | Gold reading through ECON-003 |
| Silver | $14 | Silver reading through ECON-003 |
| Pork bellies | $20 | Pork reading through ECON-003 |
| Blue-chip stocks | $49 | Blue-chip reading through ECON-003 |
| Penny stocks | $7 | Penny reading through ECON-003 |

The broker selects an investment, then Buy or Sell moves **one share/unit** at its displayed price. Purchase checks carried cash. Sale tests nonzero holdings (positive in the ordinary nonnegative case) and credits that price. T-bill sale additionally deducts **$3 per unit**; the explanatory notice is shown only once per start-turn flag, but the charge executes on every sale. No separate transaction fee appears for the other five investments in the examined buttons. Prices are initialised from individual market readings, not the goods reading.

Opening the bank costs 2 hours. See Broker adds another 2 hours on its first invocation during that bank dialog's lifetime; the local guard prevents repeated charges in that lifetime. Buy/sell handlers themselves do not advance the timekeeper. The [package transaction/lifetime trace](investment-transactions.md) now establishes the ordinary boundary: a first accepted See Broker action at spent58/59 charges up to60 and still opens trading, because the time gate precedes the charge; Buy/Sell themselves have no clock gate. Already-spent60 refuses a new opening. Closing script213 leaves the bank guard set; only a fresh script204 load supplies its zero default after full bank disposal. Retained/restored loader cases remain outside that normal claim.

Evidence: [broker.sc, investment definitions, lines 323–483](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/broker.sc#L323), [Buy/Sell, lines 513–569](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/broker.sc#L513), [bank entry cost, line 92](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/bank.sc#L92), [See Broker, lines 591–605](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/bank.sc#L591).

## FIN-005: valuation, money score and integer boundaries

The recalculation sums shares multiplied by current unit prices, using the paired-number helper for large values. T-bills use fixed base 100; the other five use current individual market readings and ECON-003. This investment subtotal is saved separately. Liquid assets then add carried cash and bank savings and subtract rent owed plus loan principal. Net worth additionally includes `pricePaid × quantity` for grouped durables. Therefore durable purchases count toward net worth but **not** toward the liquid-assets money goal; loan proceeds have matching debt.

The cash helper sets money status to `trunc(storedLiquidAssets/100)`, clamped 0–100, or 100 when the high field is nonzero. It reads the stored field rather than recalculating it inline. Recalculation call sites include start-turn setup, inventories, and the cash-calculator refresh (`gCalc.doit`), which ordinary purchase and broker handlers call after their cash change. Broker buttons adjust only the low investment subtotal immediately before that refresh. Visible refresh timing and high-balance anomalies require tests before claiming the score is updated identically after every action.

SCI integer division truncates toward zero; ordinary prices already contain multiple truncation steps. Larger balances need special care: cash manipulation uses a 32,767 carry quantity, pair addition uses wrap arithmetic around 32,768, while the string formatter uses a 32,766 multiplier. The [money-boundary follow-up](money-word-boundaries.md) now verifies those constants, signed/unsigned branches and nine finite analytical fixtures. For example cash(0,32766)+1 becomes(1,0), whose formatter numeric text is32766; pair addition at the corresponding boundary can instead produce(1,−1). These are selected static/arithmetic findings, not runtime displays or a full high-balance compatibility model. A common high-word radix cannot silently replace them.

Evidence: [room1.sc, valuation, lines 832–881](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L832), [Main.sc, cash/score, lines 1038–1066](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/Main.sc#L1038), [pair addition, line 1082](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/Main.sc#L1082), [n115.sc, formatter/multiply, lines 23–79](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/n115.sc#L23).

## Validation cases and remaining boundaries

1. Compare first and repeat durable purchases, checking actual happiness against GOODS-002's post-receive condition.
2. Buy the same item from both shops; inspect quantity, price paid, discount flag, net worth and repair cost basis. Repeat with an already-pawned extra copy.
3. Probe repairs at cash $500/$501, zero owned quantity, pawn countdown bits, and after a first repair notice.
4. Pawn at goods readings 70/100/190; follow the three owner end-turn countdown stages, redeem at each stage, then buy a forfeited item as another player. Exercise six-entry shared capacity and duplicated types.
5. Deposit/withdraw $1/$99/$100/$101 and test $32,766–$32,768 carry/borrow/display boundaries. Trace interest over several unchanged rounds rather than inferring it from text.
6. Loan approval equality and one-above boundary; new rejection versus extension rejection; apply after income/purchase before a known asset refresh.
7. Repay debt $45/$49/$50/$51/$100; pay multiple times before a due week and compare schedule versus late-payment flag. Verify whether any unexamined path enforces stronger default consequences.
8. Buy/sell one of every instrument at readings 70/100/130; repeat T-bill sales and check $3 is charged every time. Check exhausted-time trading after reaching the broker.
9. Compare liquid assets, net worth, money score and UI immediately after actions and after calculator/inventory refresh; test negative assets and paired balances.

Still outside this pass: complete lottery probability/payout handling, dog-food joke branch, all clothing-store-specific options, weekend event payout/happiness tables, bytecode correspondence beyond the linked selected transaction/lifecycle paths, CD-edition comparison, theft details beyond interactions needed for repair eligibility, and runtime testing. No new mechanic or bug fix is approved by these findings.
