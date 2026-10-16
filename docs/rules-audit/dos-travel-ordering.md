# Native DOS travel update ordering

Audited2026-10-16. **DOS-STATIC + BYTECODE + ANALYTICAL_CHECK**, using the website bundle's DOS1.000.060 executable. No DOS executable was launched. This selected native trace closes the specific `Animate` dependency left conditional in the [travel timing audit](travel-timing.md); it does not constitute a full interpreter decompilation or runtime compatibility test.

**Result:** the bundled native interpreter calls eligible cast objects' `doit` methods synchronously before returning from `Animate`. It excludes the clock view using frozen signal bit`0x0100`. Combined with the already traced actual game scripts, normal arrival clears the mover before the board's explicit clock test. The ordinary travel formula therefore has **bounded native static support**, beyond agreement with pinned ScummVM.

## Provenance and address convention

The source archive is [bundle.jsdos](https://jonesinthefastlane.com/bundle.jsdos), retrieved2026-10-15, SHA-256 `c08f3310f4f9cf47316bc32745507ae065bba7741430f7c3620602f534c46180`. The packed `sciv256.exe`, unpacking tool provenance, repeat-unpack comparison and MZ header are recorded in [unpack metadata](../../artifacts/original-game/dos-interpreter-unpack.json). The unpacked executable SHA-256 is `e4e5493756739f33af2a570a67bd35340369c823293065200806fd078e92b797`; its106,580-byte load image hashes to `84acd43ecdaa44d8f633d2592850ee534f95730d4f4b469ca77cc0bedb41d318`.

All flat offsets below refer to that **unrelocated load image**, excluding its8,704-byte MZ header. A far address is converted using `segment×16+offset`; DS-relative data uses segment`1856`/image base`0x18560`. These are analytical image addresses, not claimed runtime physical addresses. Original bytes, disassembly and excerpts remain in ignored `work/interpreter-audit/`.

The [verification artifact](../../artifacts/rules-audit/dos-travel-ordering-verification.json) records selected native spans with hashes, the kernel pointer, vocabulary resource hash, bytecode join points and scope limits. The local image hash, pointer, selected instruction landmarks, vocabulary ordinal and return-opcode table entry were checked directly against local binary bytes. Semantic interpretation is a manual bounded trace; the artifact is not an automated native execution transcript.

## DOS-TRAVEL-001: identify the native animation path

The native kernel table at DS:`07d0`/image`0x18d30` gives kernel11 the far target`0627:020b`, image`0x0647b`. This agrees with actual script994's kernel11 call at`0x0481`, passing the cast list and cycle1. The wrapper at`0x0647b–0x0649b` forwards the two arguments when argc is2; its fallback supplies zeroes. Its far call at`0x06492` reaches`0a73:0008`, image`0x0a738`.

In that routine, the nonzero-list branch reaches the cycle test at`0x0a778`. A zero cycle branches directly past the actor-update traversal to`0x0a7b5`. This independently confirms that Main's redraw helper, which supplies cycle0, does not add normal mover updates through this traversal.

## DOS-TRAVEL-002: cast traversal and frozen clock exclusion

For nonzero cycle, the routine traverses the cast-linked structure at`0x0a784–0x0a7b3`. It reads the object pointer from node offset`+6`, obtains its signal property using the dynamically loaded ordinal, and tests bit`0x0100` at`0x0a791`. If set, the branch at`0x0a795` skips the invocation and continues with the next node.

The signal-property interpretation does not rely solely on matching a familiar bit pattern. Initialization at`0x04c81–0x04cca` loads vocabulary resource994 and copies55 words into DS:`235a` onward. The animation routine reads DS:`235e`, the third word of that table. Actual `vocabulary.994` word2 is14; actual script1's marble and clock objects both identify property ordinal14 as selector`signal`. The native test doubles that ordinal before reading the object property. Actual marble signal is0; actual `timeKeep` signal is257/`0x0101`. `View.init` preserves the frozen bit when registering the clock in the cast. Thus the clock is skipped by this automatic native update path, while an ordinary active marble is eligible.

This establishes why the clock does not receive an extra automatic no-argument `doit` on each cast update. It does not mean the clock is absent from the cast or that explicit script calls to it are suppressed.

## DOS-TRAVEL-003: method invocation completes before traversal resumes

For an eligible object, `0x0a797–0x0a7a4` supplies object, selector60/`doit`, and argument count0 to native helper`0b46:0289`, image`0x0b6e9`. Only after that far call returns does `0x0a7a7–0x0a7b3` load the current node's successor and continue the loop.

The helper at`0x0b6e9–0x0b739` constructs the selector/argument frame and directly calls the selector parser at`0x0b532`. For a script method, the parser's method branch directly calls the bytecode dispatch entry`0048:010b`/image`0x0058b` at`0x0b67b`, then resumes parser cleanup and eventually returns to the animation traversal. The actual opcode table maps SCI `ret` (`0x48`) to`0048:07db`/image`0x00c5b`; that handler is a native far return. This is synchronous method execution, with no separate queued actor-`doit` dispatch between this call and traversal continuation on the inspected normal path.

The native animation routine later has a disposal pass, whose selected invocation at`0x0ac6a` uses selector84/`delete`, rather than another `doit`. Its epilogue returns at`0x0ac92`. This note does not audit every graphics helper or arbitrary side effects in every possible cast object's methods. The ordinary marble/clock case and the specific update traversal are the bounded subject.

## Join to the actual game scripts

The actual-package script sequence is already recorded with payload hashes in [travel timing verification](../../artifacts/rules-audit/travel-timing-verification.json):

1. Script994 `Game.doit` calls `Animate(cast,1)` at`0x0481`.
2. The native traversal calls ordinary marble `Act.doit`; actual script998 invokes its mover at`0x04cc`. Script101 initializes its movement phase to`s−1` and consumes `firstMove` without stepping during initialization. Its first mover update advances immediately; subsequent steps are spaced`s` updates apart.
3. On arrival, script101 calls inherited `moveDone` at`0x00a2`; script992 marks completion and sets global58.
4. After native `Animate` returns, script994 sees global58 and invokes the cast's `motionCue` at`0x0495`. `Act.motionCue` calls the completed mover; script992 clears the client's mover at`0x04dd`, then invokes the caller. `marbleMoved.cue` queues room-local arrival at`1:0x0169`.
5. Script994 then calls the board at`0x04a9`. Script1 processes the queued destination cue at`0x227d` before testing for a mover and sending the explicit clock call at`0x2290`. Ordinary arrival therefore lacks that extra travel clock call. The location entry adds its separate two-hour cost.

The native loop and frozen-bit test agree with the pinned ScummVM implementation previously used as a reference. Here they are established from the bundled executable itself rather than inferred from reference-engine agreement.

## Bounded numerical consequence

For distinct endpoints with shortest ring distance`d`, constant movement speed`s` in1…6, initial residual`r` in0…14s, and ordinary uninterrupted travel without earlier exhaustion:

| Quantity | Native-supported static consequence |
| --- | --- |
| Arrival mover update | `1+(d−1)s` |
| No-argument travel clock calls | `N=(d−1)s` |
| Travel hours charged | `floor((r+N)/(14s+1))` |
| Final residue | `(r+N) mod (14s+1)` |

The denominator follows the actual strict clock threshold and reset-to-zero semantics. The existing analytical checker independently advances movement phase and verifies25,500 bounded distance/speed/residue cases. Those checks remain mathematical checks; the stronger engine evidence here is native static analysis, not execution of those cases in DOS.

Residue need not start at0: `marble.cue` resets counters and immediately calls the no-argument clock, ordinarily producing residue1. Reroutes, speed changes, oversized residues after lowering the threshold, same-place explicit movers and turn exhaustion retain the qualifications in the travel audit. A complete original-runtime matrix is not claimed.

## Remaining limits

This closes the ordinary **native update ordering and frozen clock** uncertainty for this bundled executable. It does not prove runtime wall-clock duration, every graphics side effect, abnormal cast mutation, interrupted restores, error paths, or other releases' interpreter behaviour. The executable was not launched and no new observed gameplay result is reported. A fully distance-based or speed-normalized2.0 rule would still be an explicit adaptation decision.
