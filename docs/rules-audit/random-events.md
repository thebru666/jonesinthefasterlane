# Weekends, tickets and personal events

Pass 3, 2026-10-15. Evidence: **SCRIPT**, external published floppy 1.000.060 decompilation at revision `870a8015b689474484bf3d8b41416956d4315432` ([S02](../discovery/source-register.md)). No outcomes below are runtime-confirmed. Adaptation mappings remain **undecided**. [Inspected source hashes](../../artifacts/rules-audit/2026-10-15-events-source-inputs.json) support reproduction of this analysis, not independent bytecode matching.

A subsequent [direct package trace](bytecode-needs-events.md) confirms selected weekend priority/debit/redraw, lottery resolution, mugging entry/exit and computer-windfall paths. The redraw branch is real, but its ordinary repeated invocation remains unproved; this is not an observed exploit. Other event paths retain their earlier evidence labels.

Probabilities assume inclusive, uniform `Random(a,b)` draws and ordinary non-overflow quantities. Arithmetic divisions below truncate. Cosmetic animation draws also consume randomness; a faithful deterministic replay would need their actual call order, not just outcome percentages. [Weekly processing](weekly-processing.md) records the overall order; economic shocks, illness, apartment theft and repairs retain their existing [economy](economy.md), [food/housing](food-and-housing.md) and [goods](goods-and-finance.md) records.

## EVENT-001: weekend selection and spending tiers

After week 1, the start-turn sequence opens a weekend dialog before lottery, computer income, food and clothing processing. Its **first text draw** chooses the first applicable branch:

1. Positive baseball ticket stock (consumable 37).
2. Positive theatre ticket stock (38).
3. Positive concert ticket stock (39).
4. Successful possession-based selection (EVENT-002).
5. General anecdote pool: uniformly draw text index 17–60, rerolling the immediately preceding shared weekend index.

The ticket outcome sets that category's **entire quantity to zero**, even though a purchase adds four units. Thus four units do not buy four selected weekends. If multiple ticket categories are held, only the first is selected; the ordinary later consumable tick ages the remaining categories by one. Positive stock is tested, not the category's purchase-happiness flag.

On fresh dialog initialisation the script draws a low expense of $5–$20 only if carried cash is positive, a medium expense of $15–$55, and a high expense of $50–$100. Tickets use medium expense; possessions use low. General indices 17–44 use low, 45–52 medium, and 53–60 high. The debit is capped to `proc0_11` available carried cash; savings are untouched. No cash means no debit or expense line. No explicit game-hour debit occurs in this weekend script. Most anecdotes have no additional mechanical effect, regardless of what their prose implies; for example, the beauty-contest reference at index 36 does **not** grant $10.

General outcomes 58–60 additionally grant a random **+2–+4 happiness**. Other ordinary weekend anecdotes have no direct happiness adjustment in this path. Happiness uses the shared 0–100 clamp.

Evidence: [startTrn.sc, state 2](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L201), [weekend.sc, spending helper and initialisation](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/weekend.sc#L111), [first-draw priority and tier selection](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/weekend.sc#L244), [consumable tick](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L437).

## EVENT-002: possessions bias weekend opportunities by index order

Let `N` be the durable list's **object count**, including retained zero-quantity entries. The script scans indices 21–33 in ascending order. For each existing object with nonzero quantity it rolls `Random(0,4N) == 0`: probability **1/(4N+1)** for that candidate. Its weekend text index is `durable index − 20`. The first successful candidate whose text index differs from `global421` wins; a candidate matching that remembered index is rejected and scanning continues. This is not a uniform draw among possessions. Earlier eligible indices have a larger chance of selection, and retained empty entries dilute every candidate's odds.

| Durable index | Possession | Weekend text index |
| --- | --- | ---: |
| 21–23 | Refrigerator, freezer, stove | 1–3 |
| 24–27 | Colour TV, VCR, stereo, microwave | 4–7 |
| 28–30 | Hot tub, computer, black-and-white TV | 8–10 |
| 31–33 | Encyclopedia, dictionary, atlas | 11–13 |

With one owned durable and no excluded repeat, its selection probability is 1/5; with two eligible objects and `N=2`, the first has 1/9 and the second 8/81, leaving 64/81 for the general pool. These are analytical examples. `global421` is shared state rather than a field on the player, so the examined suppression can couple successive players' weekend selections. Ticket selection does not update it. With no possession selection and a previous remembered index inside 17–60, each remaining general outcome has probability 1/43; otherwise each has 1/44.

Evidence: [weekend.sc, localproc_1](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/weekend.sc#L91), [general pool](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/weekend.sc#L286), [Goods.sc, grouped objects](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/Goods.sc#L46).

## EVENT-003: weekend redraw can debit cash again

After selecting an outcome, the dialog retains its text index in `local8`. A subsequent `weekendText.draw` enters a separate first branch: draw a fresh $1–$20 expense and call the **same cash-debit helper** again for that remembered outcome. It does not merely repaint the first result. Tickets are not consumed again and the general pool's happiness award is not repeated in this branch.

This is a bounded script anomaly, not a confirmed user-triggerable exploit or normal repeated charge. Determine which runtime redraw operations actually invoke this element's `draw`, whether restoring a dialog or repainting a covered window does so, and how that reachability affects compatibility; the branch itself is now [package-confirmed](bytecode-needs-events.md#ev-b01-weekends-prioritize-tickets-redraw-really-calls-the-debit-helper).

Evidence: [weekend.sc, redraw branch](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/weekend.sc#L244), [debit helper](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/weekend.sc#L111).

## EVENT-004: lottery uses one draw for all held tickets

The market sells ten tickets for fixed **$10**, consumable index 9, adding ten quantity. Successful purchase gives +2 happiness once per active turn through `global469`; extra purchases that turn add tickets but no repeated bonus. The shared purchase costs no extra action hours beyond the market visit (the item retains zero `visitTime`).

After weekend processing the start-turn path checks whether the ticket object exists and draws `r = Random(0,500)`. With held quantity `Q`, a win requires **Q > r**. On a win:

| Additional condition, in this order | Cash prize | Happiness |
| --- | ---: | ---: |
| `r <= trunc(Q/20)` | $5,000 | +10 |
| Otherwise `r <= trunc(Q/5)` | $500 | +5 |
| Otherwise | $200 | +5 |

The whole ticket quantity is then set to zero, on a win **or** loss. One player receives at most one prize for that draw; there is no independent draw per ticket and no matching-number simulation. The path is before the week-1 skip, although ordinary new-game players have no ticket stock yet. Existence rather than positive quantity gates the draw, so an exhausted retained ticket object can still consume a random draw with no chance to win.

Analytical examples (outcomes out of 501):

| Tickets held | $5,000 outcomes | $500 outcomes | $200 outcomes | Total winning probability |
| --- | ---: | ---: | ---: | ---: |
| 10 | 1 | 2 | 7 | 10/501, about 2.00% |
| 20 | 2 | 3 | 15 | 20/501, about 3.99% |
| 100 | 6 | 15 | 79 | 100/501, about 19.96% |

The original [stdlib-only analytical checker](../../tools/research/check_lottery_probabilities.py) enumerates all 501 possible draws for each row (1,503 cases) and records exact rational expected values in [tracked metadata](../../artifacts/rules-audit/lottery-probability-check.json). From the repository root, verify the committed result with:

```sh
python3 tools/research/check_lottery_probabilities.py --check
```

Run the same command without `--check` to regenerate the metadata; neither mode runs the game or reads original resource payloads.

For ten tickets the expected cash prize is $7,400/501, about **$14.77**, against $10 purchase cost, ignoring travel/opportunity costs and happiness. This positive nominal expectation is a script calculation, not an observed strategy recommendation. Very large quantities, signed integer overflow, UI purchase limits and any edition differences remain unvalidated.

Evidence: [market.sc, lottery item](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/market.sc#L367), [startTrn.sc, lottery resolution](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L214), [turn flags](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L169).

## EVENT-005: street mugging is selected on market/bank entry

On fresh market initialisation, a roll `Random(0,50) == 0` with positive available carried cash sets `global446 = 1`: **1/51**, conditional on cash at that moment. Bank initialisation uses `Random(0,30) == 0`, flag 2: **1/31**. These are per eligible fresh dialog initialisation, not per town movement or elapsed hour. The random roll precedes the cash gate in the short-circuit expression, so a zero-cash entry still consumes a random draw despite being ineligible for mugging. A restored dialog's `global518` branch bypasses this initialisation block.

The shop remains usable after the flag is set. Upon dialog exit, either handler clears **both cash words**, regardless of the remaining cash amount. Thus the removed amount is the cash held on exit; entering with money, depositing it all, or withdrawing more after a trigger can change the loss. Entering with no cash then withdrawing does not satisfy the positive-cash entry gate. Bank savings are not directly zeroed by this mugging path. Compare the unrelated crash reset under ECON-006.

Normal room continuation processes the flag: −3 happiness, player control suspended, Willy's location-specific animation, then newspaper event 16; it clears the flag. No extra game-hour debit is found in these animation handlers. The room's `global521` guard can suppress that normal continuation; exact end-of-time/quit interruption behaviour needs runtime checking. Cash clearing occurs earlier in the shop handler.

Evidence: [market.sc, selection and cash reset](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/market.sc#L215), [bank.sc](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/bank.sc#L149), [room1.sc, continuation](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L211), [muggedByMarket.sc, both animation paths](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/muggedByMarket.sc#L22).

## EVENT-006: joke purchases have a cost and negative happiness

| Discount item | Base price | Successful purchase happiness |
| --- | ---: | ---: |
| Dog food | $18 | −1 |
| 8-track player | $75 | −1 |
| Works of Capote | $100 | −2 |

These use goods type **3**, which the shared purchase helper does not receive into consumables, durables or education. A successful transaction deducts the current economy-adjusted price and then applies the item's negative happiness; there is no stored possession or food-coverage effect in these handlers. The items keep default zero extra visit time. Repeated successful purchases repeat the penalty; failed purchases do not. The rotating discount stock means each need not be offered on a given turn. Shelf selection is separate from these purchase effects.

Evidence: [discount.sc, joke item handlers](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/discount.sc#L722), [stock selection](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/discount.sc#L197), [WButton.sc, shared transaction](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/WButton.sc#L162).

## EVENT-007: computer windfall follows weekend and lottery

Owning positive computer quantity (durable 29) gives a **1/7** start-turn chance of an inclusive **$20–$100** cash award plus **+3 happiness**, followed by a notice. This executes after lottery and before relaxation decay/apartment theft; week 1 skips it. It is independent of whether the computer supplied that weekend's anecdote. This expands the timing/probability already noted in GOODS-003 rather than defining a second award.

Evidence: [startTrn.sc, state 4](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L247).

## EVENT-008: emergency cash is gated recovery, not a random weekly grant

At late start-turn state 34, the script sums grouped durable quantity times recorded price paid, subtracting one quantity for an object with pawn/forfeiture bits `0x0038`. It checks cash high word zero, cash low word at most zero, no `weeksOfClothing`, and that durable sum **below $200**. Savings are not checked in this eligibility expression.

For each qualifying visit to this branch it increments `nakedCount`; when the count exceeds one it resets the count and grants cash. The base depends on the current uniform: index 34 → $295; 35 → $125; 36 → $73; other → $50. The award is the ordinary goods-price helper applied to that base, **plus Random(1,100)**, and then a notice. There is no probability gate once the counter condition is met. Clothing and other code can reset the counter, so this is two qualifying checks without an intervening reset, not a guaranteed payment every second calendar week. Week 1 skips this recovery path. No direct happiness change is present in this branch.

Evidence: [startTrn.sc, state 34](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L787), [clothes purchase resets](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/discount.sc#L534).

## Focused reproduction backlog

- **EVENT-001/002:** hold all three ticket categories and a computer; record selected event, exact stock after consumption/tick, carried cash, bank balance and happiness. Repeat across two humans to test shared repetition suppression.
- **EVENT-003:** capture first weekend draw; open/close any available overlay or restore a saved dialog; compare cash before and after repaint. Do not infer charge duplication from a static screenshot alone.
- **EVENT-004:** controlled quantities 0, 10, 20 and 100, with known lottery draw values at threshold boundaries. Separate developer instrumentation from ordinary play and preserve input-state provenance.
- **EVENT-005:** trigger flag with positive cash, then deposit all; compare entering with zero cash then withdrawing. Capture cash and happiness at entry, transaction, exit and animation. Repeat at the time limit and save/restore boundaries.
- **EVENT-006:** purchase each joke item twice; inspect cash, happiness, durable list and food coverage. Verify failed purchase has no penalty.
- **EVENT-007/008:** computer award before possible theft; recovery with savings present but zero cash, pawned stock, each uniform and an intervening clothing purchase.

Still outside this bounded event pass: exhaustive flavour-text transcription, random clerk chatter/animation schedules, runtime RNG distribution/seeding, demo/CD comparisons, all shared-state save boundaries, and source-to-package correspondence beyond the selected [verified paths](bytecode-needs-events.md). Apartment burglary, food illness and repairs remain covered by their existing rule IDs rather than duplicated here.
