# Happiness from weekly processing and events

Audited 2026-10-16 against website DOS **1.000.060**. Evidence **BYTECODE**, selected event predicates, recipients, ordered score calls and resets; no runtime observation or measured random frequencies. Actual resources covered are1,111,114 and232, with Main's common helper in0. [Verification metadata](../../artifacts/rules-audit/happiness-events-verification.json) records all29 helper callsites in those event resources, field-access checks and reviewed range hashes. Shop/action contributions are consolidated separately.

## Score helper, coverage and turn order

Main export13 (`0:0x05ea–0x062b`) selects current player global302 when fewer than two arguments are supplied; otherwise it uses the explicit second argument. It adds the signed amount to that player's stored hapStat, clamps the result to0…100 and writes it immediately. Each call clamps separately; listed negative amounts describe attempted changes and can be smaller at the zero floor. The Player class and four original player instances default hapStat to0.

The covered event resources contain26 helper calls in startTrn111, two in Place.cue in1, and one in weekend232. Script114's mugging animations and `Player.doScandal` contain no direct Happiness setter or helper call. The literal hapStat reads in111 belong to the two goal gates, not another score calculation. Direct Player property-slot access and literal-selector scans find no bypassing score writer in the covered event paths. This is bounded static coverage, not an absence proof against computed addressing, restored VM memory or other editions.

At active start turn, the stove/microwave bonus precedes **both stored-score completion gates**. The subsequent weekend/lottery and ordinary recurring penalties happen later. State3 skips states4…34 in week1; the earlier ownership bonus and lottery test are not covered by that skip. Once an already eligible participant finishes through the earlier gates, later ordinary penalties should not be silently moved ahead of those gates in a purported reproduction. [Ordered turn reference](bytecode-weekly-opponent.md).

## Current-player weekly calls

All calls in this table omit the recipient argument and therefore affect current global302. State numbers are startTrn.changeState branches; addresses are script111 helper13 calls.

| State / event | Exact amount and call PC | Trigger and order |
| --- | --- | --- |
| 0: stove or microwave | +1; `0x00a9` | At least one positive-quantity durable index23 or27; combined OR gives one call, not one per appliance. Before the first goal gate. |
| 2: lottery | +10 for prize5000, otherwise +5; `0x04cf` | Ticket quantity q must be strictly greater than Random(0,500). Prize is5000 if draw≤trunc(q/20),500 if draw≤trunc(q/5), otherwise200. Happiness precedes cash credit and the lottery presentation; ticket quantity is cleared on winning continuation or immediate nonwinning path. |
| 4: computer income | +3; `0x055b` | Positive-quantity computer index29 and Random(0,6)==0. Happiness precedes Random(20,100) cash income and notice. |
| 6: theft | −4 once; `0x06c6` | Low-cost housing, Random(0,relax)==0 and nonempty durable list; for each record except indices21/22/23, nonzero Random(0,3) sets its quantity0 and global414=1. The penalty occurs once if that flag became1. No positive-quantity test precedes those individual record rolls; a retained zero record is not automatically excluded. |
| 10: groceries without refrigerator record | −2; `0x07b0` | Grocery index1 has nonzero quantity and objectAtIndex(21) returns no object. Groceries become0; if selected food category was1, local6 becomes−1 for later illness handling. Storage tests here use object presence, not positive appliance quantity. |
| 10: groceries above six without freezer record | −1; `0x07ec` | Refrigerator object exists, freezer object does not, groceries>6; clamp groceries to6, then notice. |
| 10: groceries above twelve with freezer record | −1; `0x0827` | Both storage objects exist and groceries>12; clamp quantity to12. Mutually exclusive with the earlier two storage branches. |
| 12: no selected food | −2; `0x0892` | local6=0 after scanning food indices5 down to1. Before this call, food records3…5 are cleared. Sets later illness control local4=Random(0,3) and displays hunger notice. |
| 14: illness | −4; `0x0933` | Positive carried-cash proxy and illness control local4=0 after the spoiled-food and minimum-relaxation tests. The penalty precedes medical cash cost and ambulance/notice handling. |
| 20: overdue loan | −1; `0x0b3b` | Week divisible by4, outstanding loan balance, paySched<0. paySched==0 produces a due notice without this penalty; positive schedule skips both branches. |
| 22: repair | −1; `0x0ce7` | Cash proxy>500; record is not a reference book, has repair bit0x40, and has no pawn bits0x38 or quantity>1; Random(0,35)==0 for discount bit0x100, otherwise Random(0,50)==0. Repair amount draws trunc(pricePaid/20)…trunc(pricePaid/4). Happiness precedes cash debit and child notice; the branch returns from this state invocation. |
| 24: crash severity1 | −3; `0x0d54`, then investor −5; `0x0d5f` | global373==1; the extra call requires nonzero invAssHi OR invAss>1000. Ordinary combined attempt−8 for an investor, −3 otherwise. |
| 24: crash severity2 | −2; `0x0d96`, then investor −2; `0x0da1` | Same investment test, global373==2; ordinary combined attempt−4 or−2. |
| 24: crash severity3 | −1; `0x0dd8`, then investor −1; `0x0de3` | Same investment test, global373==3; ordinary combined attempt−2 or−1. |
| 24: boom | investor +5; `0x0e19` | No severity1…3 branch, global444 truthy, and the same investment test. Non-investors get its presentation without this helper call. |

There are18 syntactic helper sites in that table, including the three separate storage penalties and seven crash/boom sites. The investor predicate uses a strict low-word threshold>1000 and a truth test on the high word; it is not a newly verified arbitrary-precision comparison.

## Illness and relaxation are conditional mechanisms

Before theft, state6 reduces relaxation by1 to a floor10 unless the player has a positive-quantity hot tub. That relaxation change is not itself a Happiness call. State8 chooses the highest nonzero food category among5…1. State12 initially sets illness control local4=1, replacing it with Random(0,3) only when no food was selected. State14 replaces it with Random(0,1) if local6 was marked−1 by the grocery-spoil branch. If current relaxation equals10, a zero Random(0,4) overrides it to0. Illness finally requires positive cash as well as local4=0; an unaffordable medical charge does not independently add another Happiness penalty here.

Under **independent inclusive-uniform reference draws only**, computer eligibility would yield1/7, the outer theft gate1/(relax+1), each eligible theft record3/4, and a repair roll1/36 or1/51. Without the minimum-relaxation override, no-food and spoiled-food illness controls would be zero with1/4 and1/2 respectively; the override changes those combined probabilities. These are conditional analytical assumptions, not measured DOS probabilities. The [native generator and scaling](dos-randomness.md) do not establish independent uniform outcomes. No unconditional weekly illness/theft/repair frequency follows from these numbers alone.

## Crash job consequences explicitly target every eligible participant

States26,28,30,32 visit players[0],players[1],players[2],players[3] respectively, checking list size for the later entries, finishStatus==0 and global373 in1…2. They store that participant in global480 for the notice and call **that player's** `doScandal(global373)`:

| Recipient | Job-loss return1: −7 | Pay-cut return−1: −3 |
| --- | --- | --- |
| players[0] | `111:0x0ec3` | `0x0ef9` |
| players[1] | `0x0fb0` | `0x0fe6` |
| players[2] | `0x109d` | `0x10d3` |
| players[3] | `0x118e` | `0x11c5` |

All eight calls supply the recipient as the second argument to helper13. These penalties are additional to the current player's state24 crash mood penalty; they are not accidentally all written to current global302. A zero return from doScandal adds neither penalty.

`Player.doScandal` (`1:0x0f5c–0x0fb2`) first requires playing truthy. Severity1 clears the low bank-balance field. For a nonzero wage it tests zero Random(0,severity−1): success clears wage/workplace/occupation and returns1; otherwise a remaining wage is scaled by trunc(wage×(4+2×severity)/10), floored to1, and returns−1. No wage means return0 even if savings were affected. On the inspected severity1 path an employed player loses the job deterministically because the draw interval is0…0. Severity2's job-loss/pay-cut split would be1/2 each only under the uniform-reference assumption. State26…32 do not call this method for severity3.

After the final participant branch, global373 is cleared; state33 clears global480, and final cleanup clears the crash code again. The event code's global lifetime therefore joins the earlier current-player mood branch to this participant sweep. It is not four fresh independent crash selections or a per-person redraw of the severity.

## Mugging belongs to the location-return boundary

After a location dialog returns, `Place.cue` checks that deletion flag521 is absent, then dispatches global446. Value1 calls helper13(−3) at `1:0x04d8` before installing script114's market mugging animation; value2 calls−3 at `0x050f` before its bank animation. Both clear446, disable ordinary control, mark readiness473 false and return into the animation path. They are two mutually exclusive event branches, not a combined−6 penalty.

Script114 moves actors and eventually opens the newspaper/returns control, but contains no helper13 call or direct Happiness write. Replaying or redrawing an animation state is therefore not evidence of another penalty from114 itself. Shop-side cash-loss flags and their selection predicates remain separate action/event boundaries; this consolidation does not add another Happiness charge for the cash setter.

## Weekend bonus and repeated draws

The actual weekend resource is232. Its only helper13 call is at `0x0842`, taking Random(2,4), when the **generic fallback** anecdote chosen by weekendText.draw has identifier≥58. The fallback selects17…60 and rejects immediate equality with global421. Ticket branches and possession-based anecdotes precede it and do not pass through this bonus branch. Spending and the wording of an anecdote are not independent evidence of a score change.

Normal weekend initialization sets local8=−1. After its first selected anecdote, a redraw follows the earlier local8!=−1 branch: it draws another spending amount and reuses the anecdote instead of entering the generic-selection/bonus branch again. Thus an ordinary redraw does not automatically repeat the +2…4 call. Fresh initialization, restored local state and interrupted notices remain distinct call shapes.

Global421 is shared last-anecdote suppression state, updated by successful possession selection and generic fallback; ticket presentation does not update it in the inspected branches. Its prior value changes which generic IDs survive rejection. Consequently even an idealized generic-bonus probability needs its prior-state condition;3/44 is not a universal weekend rate. The exact package facts are the branch bounds, repeat test, one helper call and amount range. Native random correlations and all presentation draws are separate from an iid model.

## Reset, absence and remaining scope

Shared active-turn processing resets event/action latches, including theft flag414 at its state6 start and ticket bonus flags466/467/468 during early setup. Happiness itself is **not reset every turn**. Subsequent clothing loss, charity cash, relaxation decay, plain rent due notices, no-wage scandal results and script114 presentation do not introduce extra helper13 calls in these covered methods. A current cash change also does not imply an inferred Happiness change.

The metadata inventories every literal helper13 call in these four resources, validates Main recipient/clamp logic and searches Player's hapStat property slot24 for direct writes. It records the exact eight explicit-recipient frames. Remaining questions are unusual inventory/high-word states, child-script/re-entry/restoration behavior beyond the reviewed ordinary continuations, complete native random call ordering and visual timing. No adaptation balance or implementation change is approved by this catalogue.

Sources: [website package](https://jonesinthefastlane.com/bundle.jsdos), [pinned comparison scripts](https://github.com/sluicebox/sci-scripts/tree/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src), [needs/event package findings](bytecode-needs-events.md), [inventory semantics](inventory-grouping.md), and [source register](../discovery/source-register.md). Original code and listings are not included.
