# Bank transactions: modal continuation and cached Wealth

Audited 2026-10-16 against website DOS **1.000.060**. Evidence **BYTECODE**, selected normal human dialog paths and callbacks. No new gameplay, instrumented score trace or high-balance execution is claimed. This extends the [score-refresh inventory](score-refresh.md), rather than asserting a universal one-action lag. [Verification metadata](../../artifacts/rules-audit/bank-refresh-continuation.json) identifies five resources, selected method hashes and 3,018 instruction spans checked against their raw payloads. Original listings remain ignored.

## Result and scope

For consecutive successful transactions while the normal bank dialog stays open, the modal loop does **not** automatically refresh the board cash panel between actions. Deposit/withdraw therefore can leave the incomplete asset cache identified in the earlier trace available to the next cash-helper call. The inherited loan-payment cache also precedes principal reduction. Opening Statistics explicitly recalculates assets; opening Goals alone does not repair this cache through the normal bank-return path.

These are selected static path findings, not measurements of visible score lag. They assume ordinary low-word balances, normal initialization with restoration flag518 cleared, and no intervening action that explicitly refreshes assets. They do not establish every possible callback or restored state.

## Why the ordinary loop does not repair it

Script255 `Dialog.doit`, `0x0d68–0x0e85`, runs an inner modal loop. After its `handleEvent` call at `0x0e46`, it disposes the event, calls its timer check, handles exit conditions, waits and loops. It does not return to the outer `Game.doit` between two bank actions. On the next iteration it cycles its own items and the window's animation object. The bank's cash panel belongs to the board controls, rather than this modal item list or the cast.

`Dialog.check` (`0x0e86–0x0eaa`) handles its seconds/cue timer. Item selection and the deposit/withdraw hilite methods change highlighting, ports and short waits; these methods do not send the board cash panel a draw. The prior [callback inventory](score-refresh.md#draws-callbacks-screens-and-turn-boundaries) records the pig cycler, empty item cycle and board panel distinctions. A changing pig cel is not a savings mutation or a general asset refresh.

Thus the sequence is not implicitly “transaction, outer board redraw, next transaction.” A valid selected path is “transaction, modal housekeeping, next transaction.”

## Notices and message settings

The ordinary successful bank notices call Print, script255 export0. It creates a fresh Dialog at `0x1648–0x1651`, assigning its window/name. The Dialog class defaults include `menuBarOK=0` and `client=0`; this Print procedure has no literal menuBarOK setter, and the inspected bank notice arguments do not enable it. `Dialog.handleEvent` gates MenuBar dispatch behind that property at `0x0f9a–0x0fa6`. The ordinary notice therefore does not introduce an F4/F6 menu opportunity inside that nested dialog.

`BubbleWindow.dispose`, script113 `0x056f–0x05d0`, resets/redraws its animation object, restores saved pixel boxes, updates those boxes and disposes the window. It does not send bank or gCalc a draw. Restoring pixels is different from recalculating financial state. The inspected clerk/icon callbacks likewise do not transfer balances or refresh the board asset cache.

With nonessential notices suppressed, that nested path is skipped. With the selected ordinary notices enabled, it adds the traced window/clerk work, without an unconditional cache repair. This does not prove the absence of all dynamic or error callbacks; visible behavior remains suitable for a narrow corroborating experiment.

## Statistics and Goals differ

Both menu routines eventually redraw the current location, but that is not enough to infer an asset refresh:

| User path | Static order and consequence |
| --- | --- |
| F4 Statistics | Script997 export1 loads231 at `0x0827`; script231 calls `calcNetWorth` at `0x0015`, refreshing cached assets before displaying statistics. It does not itself write stored Wealth. |
| F6 Goals | Script997 export2 loads238 at `0x090f`; goal views read stored scores. On return it calls the current location's draw at `0x091d`. |
| Normal bank redraw | Script204 `bank.draw`, `0x03d8–0x0401`, calls its superclass, then redraws gCalc only if global518 is nonzero. Normal bank initialization clears518 before entering the modal loop. Thus a normal Goals return alone does not execute that extra gCalc refresh. |

A restoration path with518 set is a different case. Bank exit/re-entry, a broker visit, Statistics or another explicitly refreshing action must be traced on its own terms, rather than folded into a claim that every bank action has the same lag.

## Analytical example

Assume carried cash200, savings800, no debt/holdings, and a fresh cached liquid-assets total1000. A deposit100 debits cash and writes Wealth from the old1000 cache, then explicitly refreshes assets **before** crediting savings. That refresh sees cash100+savings800=900; after the savings credit the true total is again1000, but the cache remains900 on the selected continuation. A second deposit can therefore write Wealth9 from that cache. Opening Statistics between deposits refreshes the cache to1000, so the later cash helper instead samples10. These are derived ordinary-range values, not captured screen results.

Withdrawal has the opposite transient double-counting shape; principal repayment has its own debt-ordering shape. The full transaction order remains in [the score contract](score-refresh.md#ordinary-action-order). A modern authoritative Wealth calculation after every transaction would be an explicit departure from these stored/cache semantics. No implementation or compatibility choice is approved here.
