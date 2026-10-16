# Original DOS randomness: native static findings

Investigated 2026-10-16 in the actual interpreter from website DOS1.000.060. Evidence **DOS-STATIC**: selected native-code paths read from a hash-pinned unpacked executable and independently peer-reviewed. No original interpreter was executed and no random frequencies were measured. [Input/rebuild](../discovery/inspect-dos-interpreter.md), [range hashes and findings](../../artifacts/rules-audit/dos-randomness-verification.json).

## Kernel and generator

The original kernel-pointer table resolves kernel60 to **0627:0d02**, load-image offset`0x06f72`. The selected handler reads the two supplied bounds, computes `upper − lower + 1`, obtains a raw random word, scales that word, adds the lower bound and caps at the upper bound. This corroborates **inclusive endpoints for ordinary valid nonnegative ranges** used by the audited game paths; it does not establish equal probabilities for those endpoints.

Its generator is at **0bd1:0094**, load-image`0x0bda4`. It reads a16-bit seed at relative DS offset0x0cca. If that seed is zero, it calls DOS interrupt21h/function2ch and takes DX, retrying until nonzero. That is a time-derived seed path, not a user-visible seed selector. This does not prove every seed initialization/reset caller or how the browser emulator supplies DOS time.

For a nonzero stored seed, the selected native path performs unsigned multiplication by **0x7c4d (31821)**. It stores the low16 product bits as the next seed and returns **product bits8…23** as its raw16-bit word. The current output therefore uses more product bits than the stored next seed. Treating the returned word as simply the next seed would change the sequence.

## Bound mapping is scaling

For the inspected ordinary case—two supplied parameters, nonnegative bounds and a representable positive16-bit span—the native result is:

`min(upper, lower + floor(raw16 × (upper − lower + 1) / 65536))`

This is multiplication/scaling, **not modulo by the span**. The trace follows the unsigned product wrapper/helper and the logical shift helper, rather than guessing from a compiler-library call. The shift count is16; the helper clears the high count byte before shifting. The upper clamp is part of the actual handler, even though the ordinary formula already stays within valid bounds.

Negative/reversed bounds, overflowing spans and other argument counts are outside this finding. The game's economic code offsets certain random intervals by100 before subtracting100 later; do not remove such offsets based on an assumed modern random API.

## Probability and replay consequences

Existing rule tables explicitly calculate probabilities under **inclusive uniform reference draws**. Those remain useful analytical idealizations and verify the game's thresholds. They are not measured probabilities of this DOS generator. The native seed recurrence preserves parity, the time-derived seed population is constrained, and a deterministic sequence's reachable states depend on its seed. This audit does not infer independent uniform draws from the word size or the bound mapping.

For example, [lottery thresholds](bytecode-needs-events.md#ev-b02-lottery-thresholds-and-ticket-consumption) still require quantity>draw and use the documented prize tiers. Their501-outcome enumeration checks the conditional formula. It must not be relabelled an exact original-RNG expectation merely because the native bounds are now known.

A faithful deterministic replay would require this generator, initialization, saved state and **all call ordering**, including failed actions and visual effects. The [winner scene](bytecode-flow-and-persistence.md#finish-001-placement-is-assigned-during-presentation) consumes Random calls; other animation/clerk draws also need a complete call-order audit. Native generator identification alone is not a working replay implementation.

For2.0, a new seeded generator and separate visual randomness remain reasonable proposals already listed in planning. They are explicit technical departures, not discovered original behaviour. No application code or translated original RNG implementation is committed here.

## Reproduction boundary

Unpack the exact interpreter using the linked recipe. The metadata records whole-executable and selected native-range hashes plus segment/load-image offsets. `check_economy_frame.py --check` verifies the same interpreter's identity, relocation-derived data/code bases and kernel60 pointer; it does not execute these arithmetic helpers. The arithmetic interpretation was checked separately by two agents against the actual instructions. Original disassembly stays ignored locally.
