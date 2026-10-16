# Package trace: turn lifecycle and computer execution

Audited 2026-10-16 against the website DOS **1.000.060** package. Evidence tier **BYTECODE** applies to the bounded anchors below; previously published SCRIPT findings remain separately labelled. No original-game runtime experiment was performed for this pass. Adaptation mapping is **undecided**.

The [verification manifest](../../artifacts/rules-audit/bytecode-weekly-opponent-verification.json) records resource hashes, methods and instruction ranges. Rebuild the ignored local listings using the [decompilation guide](../discovery/decompile-original-scripts.md). The published sources were used to identify candidate paths, then the package's method/property tables and decoded instructions were inspected. This is a control-flow trace, not proof of equivalence between the entire published source and every package instruction.

## WEEK-B01: rotation, round count and the pre-turn entry

The package has separate operations for choosing the next player, starting a round and preparing that player's turn.

| Package anchor | Verified operation |
| --- | --- |
| Script 1, `players.init` 0x138e; 0x1416–1426 | Initialise remaining players, store list size in global 374 and select its first entry as active player (global 302). This stored size is not recomputed by the inspected normal rotation method. |
| Script 1, `players.doit` 0x1427–144b | Normally call active player's `endTurn`. If global 448 indicates a just-finished player, clear that flag and mark `playing=3` instead; do not apply ordinary end-turn penalties to that completed turn. |
| Script 1, 0x1490–151b | Advance cyclically through the list; skip entries with `playing=3`. A separate removal marker (global 521) can delete the previous player. If deletion occurred before the old last list position, set suppression flag 523 to avoid an extra round increment. |
| Script 1, `marble.cue` 0x18f0–1903 | Reset elapsed hours (323), residual movement ticks (324) and movement state (460). |
| Script 1, 0x1990–19f6 | Scan from the list head, ignoring inactive entries. Increment week 372 when the selected player is the first eligible entry and suppression flag 523 is clear; otherwise clear suppression. This is more precise than incrementing on an unconditional array-index wrap. |
| Script 1, `Player.startTurn` 0x0d6b–0d9a | Initialise the time display, refresh the panel, copy housing into 457, disable normal-turn readiness (473=0), invoke script 107's economy `doit`, then initialise script 111 on this player. |

If rotation finds no eligible player, its later path presents Restart/Quit (script 1, following 0x151d). Retirement and completion are distinct: normal completion marks an entry inactive; physical removal uses a separate marker. The normal menu deletion entry point is traced in WEEK-B05 below.

## WEEK-B02: outgoing-turn bookkeeping

Script 1 `Player.endTurn`, 0x0d9b–0f5b, confirms the following ordered mutation:

1. Dependability loses 3, floored at zero. Career becomes `min(100, 10 × trunc(dependability/8))` if employed, otherwise zero. Career is therefore a discrete boundary recalculation, not merely an increasing lifetime work total.
2. For each durable, the attribute mask 0x0018 ages through 24 → 16 → 8 → 0. At zero, set attribute 0x0020. Other bits are preserved.
3. Select the current housing consumable (40 or 41). On fourth weeks, a nonzero loan decrements the payment schedule; if no payment was made, increment late-payment count.
4. If that housing consumable exists with zero quantity, no successful extension is recorded (`triedExt != 1`) and rent has not already been turned over, add stored current rent to arrears and mark it turned over. Outside fourth weeks, this branch additionally requires existing rent owed to be zero. Do not collapse these into identical weekly charges.
5. Preserve whether an extension was granted in `leaveOpen`, then clear extension-attempt and payment-made flags. These resets occur on both modulo branches.

The quarter-period test is the outgoing player's current week, before the next player's round-selection step. No cash debit is performed by this bookkeeping itself: rent payment and work garnishment remain separate actions.

## WEEK-B03: completion is checked twice before recurring consequences

Actual script 111 performs four threshold comparisons in state 0, with their failure branches at: money **0x00d9**, happiness **0x00f0**, education **0x0107**, career **0x011e**. A nonzero `finishStatus` bypasses them. The gates compare stored score properties; the explicit `calcNetWorth` refresh at 0x03e2 occurs later. First, ownership of positive quantity of durable 23 or 27 grants happiness +1 (0x008c–00a9). If all goals pass, launch winner script 234 and return (0x012a–0130).

State 1 clears/disposes the winner script and advances. State 2 repeats all four comparisons, with failure branches at **0x0181, 0x0198, 0x01af, 0x01c6**. On success it sets the just-finished flags 448/505, stamps `finishStatus` with the current week, and clears the player's script. When more than one non-inactive player remains, it offers Continue, Restart or Quit (0x0249–02b5). It then schedules state 35 rather than processing the ordinary weekend/needs sequence. On the subsequent rotation, the special path described above marks this player inactive.

This proves two checks in the start-turn flow and their ordering relative to economy, ownership and needs. It does not prove the absence of other finish-related checks elsewhere. Winner script 234's placement and continuation handling are traced in WEEK-B05 below.

## WEEK-B04: pre-turn state sequence and interruption contract

The table records actual outer state dispatch ranges in script 111. Paired odd states mostly schedule a one-cycle delay; they are presentation ticks, not game hours. Within effect states, a notice or child script can suspend processing via `setScript` and `return`, then resume through the script/cue mechanism. A port must preserve that order even if notices are collected into a different presentation.

| State | Package range | Ordered role |
| --- | --- | --- |
| 0–1 | 0x0024–0158 | Reset flags, ownership happiness, first win gate, winner presentation continuation. |
| 2 | 0x0159–0514 | Second win gate; otherwise reset per-turn policy/action flags and visited-place flags, recalculate education bonuses/net worth, run weekend except week 1, then resolve lottery item 9 and consume tickets. |
| 3 | 0x0515–052f | On week 1, set state to 35, thereby skipping recurring states 4–34. Economy and the earlier ownership/win/lottery paths have already run. |
| 4–7 | 0x0530–0701 | Computer-item income opportunity; relaxation decay and cheap-apartment theft. |
| 8–15 | 0x0702–097b | Determine food coverage; spoil/cap groceries; expire food; hunger notice; doctor eligibility, cost and notice. |
| 16–17 | 0x097c–0a24 | Decrement consumables; fourth-week rent notice; reset turned-over marker on the notice path. |
| 18–21 | 0x0a25–0b63 | Update clothing presentation/warning; fourth-week loan schedule warning and overdue happiness loss. |
| 22–23 | 0x0b64–0d1e | Eligible durable repair draw, cash cost and notice. |
| 24–25 | 0x0d1f–0e5a | Economic news, active-player happiness effect and investment-exposure adjustment. |
| 26–33 | 0x0e5b–120c | For each of up to four list entries, apply eligible crash `doScandal` effects if unfinished; give dismissal/pay-cut notice and happiness effect. Clear event after the fourth slot, then clear target marker. |
| 34–35 | 0x120d–135d | Emergency donation eligibility/counter, possible cash award/notice, then delay. |
| 36 | 0x135e–13bf | If not quitting, detach/dispose notice and pre-turn scripts, clear event 373, set readiness flags 473/474, call Main export 8. |

Only outer dispatch/order and selected effects were promoted here. Exact random odds, complete item behaviour, repair eligibility and notice text continue to use their dedicated [needs](food-and-housing.md), [events](random-events.md) and [finance](goods-and-finance.md) evidence tiers. Decoding a stage does not independently validate every arithmetic expression inside it.

Consequences for a faithful simulation: the economy can change once **per player's turn**, crash effects can touch other players before their turns, completion can precede hunger/repair consequences, and the first week skips only part of preparation. A single undifferentiated end-of-round callback would change these behaviours.

## WEEK-B05: placement, winner acknowledgement and game controls

Actual script 234 `winnerScript.changeState` starts at 0x000c. State 0 hides the board walker, prepares the winner/podium/star scene, disables statistics, goals and deletion menu entries, and calls `pedistal.init(1)` at **0x01b6**. That method (entry 0x09be) assigns the active player to the **first empty placement slot**: winner global 461 at **0x09d4**, second global 462 at **0x09f3**, third global 463 at **0x0a12**, fourth global 464 at **0x0a31**. It selects corresponding text resources 234:0…3. Placement is therefore reserved during the presentation, **before** script 111's state-2 completion stamp and Continue prompt. Neither placement allocation nor the inspected winner methods recompute or award goal scores.

The scene's controller handles an unclaimed nonzero event only after state ≥2 (0x03d6–03fd). That records an acknowledgement; `cue` at 0x033a–0356 uses it to break the animation loop. End states 5/6 dispose the scene, clear the parent's child-script slot, set global 532 and restore menu state (0x02cd–0335). Script 111 `doit` at 0x000c–0023 notices 532, clears it and cues its continuation: state 1 disposes script 234, then state 2 runs the second goal gate. The normal winner methods do not change the compared scores, so their own animation does not invalidate the second gate. However, the second test is a real conditional recheck, and a changed/restored state could in principle fail it; no blanket invariant across all menu/restore/debug interactions is claimed. Placement is not rolled back by that failure branch in the inspected state-2 code.

The winner's moving character/staging uses ordinary `Random` kernel calls while its scene repeats. A future deterministic implementation must explicitly decide how cosmetic draws relate to simulation randomness; moving them to a separate generator would be a proposed departure from that call sequence, not an established original rule.

Actual script 997 `MenuBar.handleEvent` (entry 0x00b8) provides these game-control routes:

| Control | Package anchors | State consequence |
| --- | --- | --- |
| Restart, menu ID 518 | 0x026a–02b8 | Confirm Yes/No; Yes sets request flag 528 at 0x029f. Main script 0 `jones.doit` processes it only when no location dialog (502) is active: clear request at 0x0178 and call restart at 0x0181. |
| Quit, menu ID 517 | 0x02be–02f9 | Confirm Yes/No; copy answer into quit flag 4 at 0x02e4. This leaves quit handling to the engine/game loop. |
| Delete current player, menu ID 771 | 0x0460–0576 | Count list players whose `finishStatus` is zero. Allow the confirmation only if more than one remains (0x04b0). On Yes, store current player in removal marker 521 at 0x0548 and set elapsed time to 60 at 0x054d. If outside a location dialog, immediately call board export 1:9 at 0x0558; otherwise defer until leaving that location. |

Deletion does not directly splice the player list or assign a finishing place. Rotation later runs outgoing bookkeeping, chooses the next active player, increments removal counter 522, deletes the marked old entry and applies the round-suppression flag described in WEEK-B01. If exactly two unfinished players existed at the confirmation, the menu's deletion option is disabled before setting the marker. Finished players are excluded from this menu count by `finishStatus`, whereas rotation skips players using `playing=3`; preserve those distinct representations.

This closes the normal menu retirement/restart/quit entry points and winner-return chain. Whole-engine event precedence, interrupted restores and all error paths remain outside this bounded verification.

## AI-B01: policy, location controller and shared action are separate layers

Actual script 300 object `WhereShouldIGo` has `doit` at 0x0047. It derives completion flags from the supplied player's goals (0x0047–00bc), then chooses ordered destinations and writes plan fields. That is policy state, rather than direct mutation of wages or inventory.

Actual script 110 class `DialogScript.handleEvent` starts at 0x0004:

- State 1 checks time <60, plan code 1, positive remaining count, matching workplace and the caller's work-enabled argument. It writes event message **119 (`w`)** at 0x0055 and decrements the plan count.
- State 10 clears the earlier primary plan, then may schedule incidental work at the current workplace if no successful work has occurred this turn and clothing permits it: three attempts, or four if only money remains (0x006f–00bc). The event is again `w` at 0x00d5.
- State 19 invokes script 300 (0x00f8–00fd). If the selected location is still current and time remains, reset state to zero so another local plan can run.
- State 20 writes event **120 (`x`)** at 0x0128 to leave. `cue` advances controller state and sets its register, 0x012c–0132.

This verifies the shared event-execution bridge for work and exit; it does not by itself verify every location's consumer. Existing AI-005–009 tables retain SCRIPT status for their unexamined individual shopping/hiring branches. Human/computer rules parity remains a bounded finding, not a blanket fairness claim.

## AI-B02: difficulty changes goals; hidden market state is available

Actual script 237 difficulty buttons invoke allocator entry 0x000c with **+10 / 0 / −10** at **0x0819 / 0x087c / 0x08e1**. Its beginning reads all four human goals, applies a wealth offset with 10…100 limits and adjusts total by four times that offset with 40…400 limits (0x000c–00cc). This confirms the difficulty mechanism's entry and bounds. The existing allocation checker covers the independently transcribed full formula; this pass does not re-prove each redistribution-loop instruction.

Actual script 300 reads main market trend 315 and investment reading 308 at 0x150f–151f, and main trend again for sales at 0x1598. Actual broker controller (script 213, `computerScript.handleEvent` 0x0f70) reads indexed internal individual trends starting at global 318 in the selection/sale paths: **0x0fe2–0ff5**, **0x1125–113e**, **0x121d**. Thus privileged current economic inputs are package-confirmed. These are not evidence of knowledge of future random draws or future prices.

## AI-B03: two suspicious policy branches are real package logic

**Relaxation route check:** script 300 at **0x1391** calls feasibility helper **0x17f5** with two arguments: current place number and housing destination. The helper reads only `param1` and computes `elapsed + trunc((residualTicks + param1)/ticksPerHour) < 60`; it does not read param2 or call the route-distance helper. This is an actual argument/units mismatch. The branch can select home while disregarding the actual route distance. Actual travel still uses shared board time; this does not grant free travel.

**Shadowed clothes branch 222:** normal execution reaches the later cash test at **0x0b18** only after failing an earlier **identical `cashProxy >= clothingBudget`** test at **0x0a6c**, whose true branch returns clothes destination 9 at 0x0a7b. The intervening regular checks do not change cash or clothing budget; if they succeed they return bank or pawn instead. Package branch targets do not provide an alternate entry past the first comparison. Therefore diagnostic branch 222 at **0x0b1e** is unreachable in ordinary uninterrupted execution with stable player state. Conditional development `SetDebug` hooks exist between checks; debugger intervention is excluded from this claim.

Both issues should be explicit compatibility decisions for 2.0. Neither has been silently corrected or promoted into a design requirement.

## Remaining lifecycle gates before a 2.0 rules specification

- Verify interrupted restore/event precedence during a pending notice or winner scene; normal winner/menu retirement routes are now package-traced.
- Independently verify the remaining random-state arithmetic and every child-script resume path, including donation and crash branches.
- Package-check every location's AI action consumer, all financing proxies, and the complete goal redistribution loop. Policy and normal-action bridge are established; exhaustive shared-rule parity is not.
- Decide whether to preserve the two AI bugs, goal-based difficulty and privileged market information. These are proposals requiring an adaptation decision.
- Use narrow runtime experiments only for interpreter/presentation uncertainties; no broad manual game session is required to establish the verified control flow above.
