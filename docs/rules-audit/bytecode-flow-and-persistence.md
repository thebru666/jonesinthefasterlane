# Package trace: location flow, time, scores and persistence

Audited 2026-10-16 against website DOS 1.000.060. Evidence **BYTECODE** is scoped to the identified paths. [Verification metadata](../../artifacts/rules-audit/bytecode-flow-verification.json) records hashes, thirteen entry-call frames, ten additional instruction landmarks and method ranges. No runtime execution or save roundtrip is claimed. Original listings stay local.

## FLOW-001: setup dispatch

Actual script 1 `room1.init`, `0x1d6e–0x1e0f`, opens startup script233, conditionally player-count script239, then character/goal selection script235. The equality test at `0x1dce` permits Jones configuration script237 only when the configured human count is one. If the second player is computer code29, it opens read-only goals via script236. Calls and dispatch order agree with the [setup baseline](../original-game/setup-multiplayer.md); every slider and cancellation branch is not re-proved here.

## FLOW-002: travel, entry and return

Script1 `Place.handleEvent`, `0x022e–0x0364`, requires an unclaimed event, enabled controls, board-readiness flag474, a matching hit rectangle and its clock/motion gate. A different destination starts motion; selecting the stationary current destination can call `cue` directly. Input during interrupted motion is handled through the saved route index. This is not a teleport-and-open interface.

`Place.cue`, `0x0365–0x0540`, calculates door presentation: homes open for their resident; rental-office doors depend on employment, fourth-week timing or `leaveOpen`; ordinary destinations open normally. It stops motion, hides the walker, disables normal control, invokes that place's script `init(room1)` at `0x046c–0x0472`, then resumes the board. A closed-door visual does not by itself prove no location dialog ran: the actual `init` call follows the door branch. Conditional street events can suspend the return path before `endCue`.

`Place.endCue`, `0x0541–0x0662`, updates the walker, calls exhausted-turn export9 at `0x060d`, conditionally closes the door, and packs consumable/durable/education lists. Do not assume the close-animation or inventory cleanup itself is the only handover gate. Export9 at `0x0082` first tests spent time ==60, then calls `players.doit` at `0x00ab`; if time remains it returns without rotation.

## FLOW-003: all thirteen destination entries cost two

The actual entry methods for scripts200–212 each send `timeKeep.doit(2)`. Calls are listed in the metadata. This includes both apartment types, the employment agency, pawn shop and factory as well as staffed shops. The charge is **per location initialization**, in addition to travel. Employer job lists and other child screens are not additional town destinations; do not add a blanket two-unit charge to every modal.

The location entry charge can exhaust the clock while the dialog is opening. Because motion has already stopped, the shared clock need not immediately rotate: permitted free transactions can still finish, and the location's return then invokes the exhaustion gate. Timed actions have their own checks; see [employment](employment.md), [education](education.md) and [time/actions](time-and-actions.md).

## FLOW-004: clock and route are separate state

Actual script1 `timeKeep.doit`, `0x24f8–0x25dc`, has two modes:

| Invocation | Mutation |
| --- | --- |
| An argument is supplied and nonzero | Add it to spent-hours global323; preserve residual ticks324 |
| Argument supplied as zero | Do not advance either counter |
| No argument | Increment residual ticks324; if **strictly greater** than threshold475, add one spent hour and reset residue to0 |

The handler caps spent hours at60. It emits its time-up sound once using a latch. When an update reaches60 during normal ongoing motion, it calls export9; otherwise an exhausted location can remain open until its own exit flow. Normal board-loop motion calls the no-argument clock at `0x2290`. The separate handover resets counters, as documented in [the lifecycle trace](bytecode-weekly-opponent.md).

Initial threshold475 is `14 × marble.moveSpeed` (`1:0x216d–0x2177`). Script101 uses a 170-point ring: `at`, `0x0112–0x013b`, wraps 0→170 and171→1; `setDirection`, `0x013c–0x01c1`, selects direction using distance against85; `doit`, `0x0067–0x00a4`, gates stepping on movement speed. The actual destination indices are recorded in the metadata.

**Do not replace this with a proven fixed hours-per-building table.** Exact travel cost depends on residual ticks, speed, first-step handling and interpreter update order. The bytecode establishes the mechanism and separate counters; numerical route/hour equivalence and speed invariance remain narrowly unresolved. A new deterministic distance-based travel rule would be an explicit adaptation choice.

## SCORE-001: stored goals, liquid assets and net worth are different

The actual scoring path supports the ordinary liquid-assets interpretation of Wealth, while exposing an important refresh-order boundary:

- Main export10 mutates cash and then sets `monStat` from stored `lqAssHi/lqAss`, clamping the score to0…100 (`0:0x04dc–0x0544`). It does not calculate that score directly from the just-written cash.
- `Player.calcLiquidAssets`, `1:0x1012–0x10d2`, values investments, adds cash and savings, then subtracts rent owed and loan balance. `invAss` is the investment subtotal. `calcNetWorth`, `0x0fb3–0x1011`, adds durable `pricePaid × quantity` separately.
- Board panel `calc.doit` always calls `calcNetWorth` at `0x2462`, after its conditional cash redraw. It does **not** write `monStat` in this method.
- Start-turn goal checks compare stored scores before the explicit asset refresh at `111:0x03e2`. Therefore it is unsafe to silently implement all displayed/stored scores as continuously fresh derived values and claim exact original timing.

The ordinary formula is Wealth = clamp(trunc(liquidAssets/100),0,100); durable goods contribute to net worth, not this direct Wealth calculation. Nonzero high words take a special scoring branch. Full high-word/sign correctness, every caller's refresh sequence and observable stale-score effects remain open. This pass establishes concrete ordering, not a universal claim of a one-action or one-turn lag.

Script238 procedure `0x000c–0x00e7` confirms the Goals overview caps each category at its own target, sums those capped values, then computes a truncated total-target percentage. A larger target carries greater weight. Reaching100% on the display is not a separate immediate action-time finish trigger; the [two start-turn gates](bytecode-weekly-opponent.md#week-b03-completion-is-checked-twice-before-recurring-consequences) determine completion on this path.

## SAVE-001: fixed-slot kernel boundary

Script990 export0 (`0x0012`) calls SCI kernel41, SaveGame, at `0x0077`, with game name, **slot1**, game name and version. Failure and success have separate notices. Export1 (`0x00ed`) lists saves via kernel93 at `0x014e`, checks slot1/version via kernel101 at `0x016c`, then calls RestoreGame kernel42 with **slot1** and version at `0x017f`. No multiple-slot chooser is present in these methods. They preserve/restore cursor, sound pause and controls around normal return paths.

Script997's menu dispatch asks before overwrite, then calls the game object's `save` selector at `0x0337–0x033c`. Restore confirmation sets flag529 at `0x039b` for the outer game flow. Restart and Quit set their flags at `0x029f` and `0x02e4`. Menu deletion sets marker521 to the current player (`0x0548`), sets spent time60 (`0x054d`) and invokes export9 immediately only when no location dialog is active. Rotation handles removal separately from normal completion.

Kernel names are resolved using the pinned [SCI16 kernel table](https://github.com/scummvm/scummvm/blob/2b5f9b5d95f267c87889746906148db6088130f8/engines/sci/engine/kernel_tables.h#L1099). The actual DOS serialization format, restoration during a suspended notice/finish animation, RNG-state persistence and website filesystem persistence are **not** established by these calls. The original save contains interpreter state; that does not prescribe the future TypeScript save schema.

## FINISH-001: placement is assigned during presentation

Script234 calls `pedistal.init(1)` at `0x01b6`. That method checks placement slots461…464 and stores the current player in the first empty one at `0x09d4`, `0x09f3`, `0x0a12` or `0x0a31`, selecting the corresponding label. These placements are allocated before the start-turn continuation stamps the finishing week. Winner exits set532 at `0x02da`/`0x0316`; start-turn processing uses that continuation, then its second goal check.

The ordinary winner animation initializes actors, plays sound and consumes Random kernel calls. Its inspected paths do not write the four scores. Player input is accepted only once the winner script state is at least2 (`0x03d6–0x03ff`). The scene's own normal continuation therefore supplies no score mutation that would invalidate the second check; this does not settle restored/re-entered state behaviour.

Random calls inside presentation mean a faithful replay specification must account for more than rule-labelled draws. This proves those calls exist, without claiming the DOS RNG state or every animation tick has been reproduced. Separating visual and simulation randomness in 2.0 remains a deliberate technical choice.
