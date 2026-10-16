# Travel clock: bounded cycle-order result

Audited 2026-10-16 against the actual website bundle, DOS version **1.000.060**, SHA-256 `c08f3310f4f9cf47316bc32745507ae065bba7741430f7c3620602f534c46180`. The [metadata](../../artifacts/rules-audit/travel-timing-verification.json) records provenance and checks. This note extends [FLOW-004](bytecode-flow-and-persistence.md#flow-004-clock-and-route-are-separate-state).

**Result:** the package establishes the movement and clock instructions. With the pinned ScummVM cast-update semantics, an ordinary uninterrupted trip between distinct locations makes `(distance − 1) × moveSpeed` no-argument clock calls. The arrival update does **not** charge another travel tick. This is a conditional analytical result, not a measurement of the original DOS interpreter or a fixed hours-per-building rule.

## Evidence and reproduction

**BYTECODE:** actual scripts0, 1, 101, 992, 994, 997 and998; method/landmark offsets and payload hashes are in the metadata. Decoded listings and original resource bytes remain ignored under `work/`. Published comparison sources are [room1.sc](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc), [marblePath.sc](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/marblePath.sc), Actor.sc, Motion.sc, Game.sc and Menu.sc in that same directory. The numerical result comes from the package trace plus the reference engine, rather than accepting decompiled source as proof.

**REFERENCE-ENGINE:** [ScummVM `animate.cpp`, commit2b5f9b5d95f267c87889746906148db6088130f8](https://github.com/scummvm/scummvm/blob/2b5f9b5d95f267c87889746906148db6088130f8/engines/sci/graphics/animate.cpp#L135), retrieved2026-10-16. `kernelAnimate` calls `invoke` when its cycle argument is nonzero; `invoke` synchronously calls each eligible cast object's `doit`. This pins the dependency formerly left unresolved by the script-only audit. It does not establish the corresponding implementation of Sierra's original executable.

**ANALYTICAL_CHECK:** after the local package decode and retrieval of the pinned `animate.cpp`/`animate.h` into `work/audit/scummvm-engine-animate.cpp`/`.h`, run `python3 tools/research/check_travel_timing.py`. The original research checker independently advances movement phase and step count, then compares the observed nonarrival clock-call count with the closed form for all85 positive shortest-route distances, all6 menu speeds, and every normal initial residual at each speed: **25,500 cases, zero disagreements**. Explicit boundary fixtures check immediate adjacent arrival and an oversized residue after reducing speed. It also derives a13×13 route-step matrix from the already tracked analytical location-index metadata and verifies seven decoded payload hashes against actual local resources. These are mathematical checks under stated assumptions, not SCI execution or a new gameplay implementation. The matrix diagonal is an endpoint identity marker, not a zero-step mover contract.

## Movement, completion and board clock order

The actual `Game.doit` in script994 calls kernel11 (`Animate`) with cast elements and cycle flag1 at `0x0481`. It then handles completion flag58 through the cast's `motionCue` at `0x0495`, calls the room's `doit` at `0x04a9`, and only then calls User's `doit` at `0x04b0`. Therefore ordinary user input starts a mover after that iteration's board clock; an AI mover created in the board's nonmoving branch likewise receives its first normal cast update on the following iteration.

The clock view itself is in the cast, but **does not receive an automatic `doit` from this normal animation pass**. Actual `timeKeep` has signal257 (`0x0101`); actual marble has signal0. Pinned [animate.h](https://github.com/scummvm/scummvm/blob/2b5f9b5d95f267c87889746906148db6088130f8/engines/sci/graphics/animate.h#L30) defines frozen as`0x0100`, and `invoke` skips objects with that bit. `View.init` preserves it while registering the clock in the cast. The explicit board clock call therefore is not doubled by automatic cast dispatch. This exclusion is essential to the calculation.

Within that cast update, actual script998 `Act.doit` calls the marble mover at `0x04cc`. Script101 `MarblePath.init` sets movement counter to `s−1`, sets `firstMove`, and calls `next`. This initialization call consumes `firstMove` without advancing the ring index. The **first subsequent mover `doit` advances one ring step**, because its counter reaches `s` immediately. Later ring steps occur every `s` mover updates, where `s=marble.moveSpeed`.

On reaching the destination, `MarblePath.doit` calls inherited `moveDone` at `101:0x00a2`. Script992 records completion and sets flag58; the cast completion pass invokes `Act.motionCue`, which invokes `Motion.motionCue`. That clears the marble's mover before calling `marbleMoved.cue`. The cue stores the arrival index and marks room-local flag0.

Next, `room1.doit` processes that flag at `1:0x2267–0x227d`, disposes script101 and invokes the destination cue **before** its mover test/clock call at `0x2285–0x2290`. Thus an ordinary arrival has no mover when that clock branch is reached. The destination's two-hour entry charge is separate. If a modal destination runs synchronously inside that cue, its duration is not extra board travel ticks. Main export1's redraw helper calls `Animate` with cycle flag0, so those redraw calls do not themselves supply extra mover updates under the pinned engine.

## Formula and its limits

For distinct route indices `a` and `b`, let `d=min(|a−b|,170−|a−b|)`, `s` be a constant speed1…6, and `r` the initial residual in0…14s. Assume an ordinary active marble, uninterrupted shortest-route movement, no turn exhaustion, and one normal cast update followed by a board update per counted cycle.

| Quantity | Derived result |
| --- | --- |
| First step | Mover update1 |
| Arrival update | `1+(d−1)s` |
| Travel clock calls before arrival | `N=(d−1)s` |
| Travel hours charged | `floor((r+N)/(14s+1))` |
| Residual after travel | `(r+N) mod (14s+1)` |
| Ordinary location entry | Add2 spent hours separately; preserve residual; cap total at60 |

The denominator is `14s+1`, because the clock compares the **incremented** residue with `14s` using strict greater-than, then resets residue to0. A supplied argument adds whole hours without clearing residue; the next journey therefore inherits fractional progress. The formula does not include action costs inside the destination.

Zero residue is a mathematical input, not an assumed turn-start invariant. `marble.cue` resets323/324/460 and immediately sends the no-argument clock call at `1:0x190c`, ordinarily advancing the freshly reset residue to1. Further explicit calls and prior journeys determine the actual starting value.

Animation speed is not perfectly neutral in this conditional model. Apartments(index1) to employment(index99) has shortest distance72. At zero residual, speed1 gives71 clock calls, four travel hours and residual11; speed6 gives426 calls, five travel hours and residual1. Both then add the ordinary two-hour entry charge. This is a concrete package/reference-engine consequence, **not observed original-DOS behaviour** or an approved adaptation rule. Speed1 is the marble's package default; the menu's “Faster” value6 maps to movement speed1, while menu value1 maps to movement speed6.

## Reroutes, speed changes and exhaustion

The closed form must not be applied across these state transitions:

- **Reroute:** `Place.handleEvent` can replace an active mover. `Act.setMotion` disposes the previous mover, then initializes the replacement. Current ring index/position is retained during active motion; the replacement chooses direction from the current position, consumes `firstMove`, and resets its movement phase to`s−1`. The clock residue is preserved. Time already charged is not refunded. The shortened first-step phase can change subsequent tick counts relative to keeping one mover.
- **Speed change:** script997 menu772 sets `ticksToDo` and `moveSpeed` to`7−slider`, resets an existing mover's `b-moveCnt` to0, updates its cycler and sets threshold475 to`14s`. It does **not** reset residue324. The next movement step therefore waits the new full movement interval, unlike a newly initialized mover's immediate first step. If lowering the threshold leaves residue above it, the next clock call charges **one** hour and resets residue to0; it does not convert all excess using division. Use the per-call recurrence across changes, not the constant-speed formula.
- **Exhaustion:** a whole-hour update reaching60 while an ordinary mover remains active and flag460 is clear invokes export9. That performs turn handling and replaces normal travel with the home-return `MoveTo` path. An arrival iteration clears the normal mover first; a two-hour entry charge can reach60 while the destination is opening. The destination exit then handles exhaustion. The normal-route formula is consequently only valid for journeys that reach the intended destination before an earlier exhaustion branch intervenes.
- **Same destination:** a stationary human selection can call the place cue directly and pay entry without normal travel. Explicitly initializing `MarblePath` at its own destination is different: initialization does not test completion; the first mover update steps away and its destination test follows that step. The ring instructions imply a full circuit for that constructed state, absent interruption/exhaustion. AI board code has a same-destination `setMotion` branch, but reachable ordinary AI examples and original-runtime effects are not demonstrated here. Do not implement matrix diagonal0 as a claim that every same-destination mover completes immediately.

## Remaining boundary for2.0 planning

The ordinary tick count and arrival ordering are now specified **for the actual package with pinned reference-engine semantics**. Original DOS cast timing, possible frozen/update-suppressed actor states, restored mid-motion states, and visible effects of menu/reroute edge cases still need narrow reproduction if exact compatibility is desired. No elapsed-seconds-to-hours claim is made.

A deterministic distance-based travel cost, normalization across animation speeds, or removal of phase/residue dependence would be explicit adaptation proposals. This audit does not approve any of them or start application implementation.
