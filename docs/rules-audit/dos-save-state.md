# Original DOS saves and random state

Investigated 2026-10-16 in the actual website DOS1.000.060 interpreter. Evidence: **DOS-STATIC**, selected native-code analysis, with no executable launch, saved-file roundtrip or gameplay observation. The native save payload identified here **excludes the original random seed**. Saving and restoring the game therefore must not be treated as capturing the complete random/replay state.

The input is the bundle's `sciv256.exe`, unpacked locally using the [documented recipe](../discovery/inspect-dos-interpreter.md). Unpacked executable SHA-256: `e4e5493756739f33af2a570a67bd35340369c823293065200806fd078e92b797`; load image SHA-256: `84acd43ecdaa44d8f633d2592850ee534f95730d4f4b469ca77cc0bedb41d318`. [Verification metadata](../../artifacts/rules-audit/dos-save-state-verification.json) records kernel-pointer entries, native range hashes, region bounds and limitations. Original bytes and disassembly remain ignored under `work/interpreter-audit/`.

All native offsets below are **zero-based load-image offsets after removing the 8,704-byte MZ header**, unlike decompressed SCI resource offsets used in the script audits. Far pointers are the executable's original relative segment:offset values before loader relocation. `DS:` denotes an offset within the interpreter's data segment, relative segment`0x1856`.

## DOS-SAVE-001: native save serializes selected regions

The pointer table at `DS:0x07d0`, indexed by four-byte entries, resolves the relevant script kernel IDs independently in the executable:

| Kernel | Native relative target | Load-image offset |
| --- | --- | --- |
| 41 SaveGame | `0e6b:0008` | `0x0e6b8` |
| 42 RestoreGame | `0e6b:010b` | `0x0e7bb` |
| 93 GetSaveFiles | `0e6b:0755` | `0x0ee05` |
| 101 CheckSaveGame | `0e6b:029f` | `0x0e94f` |

The [SCI caller audit](bytecode-flow-and-persistence.md#save-001-fixed-slot-kernel-boundary) already establishes the game's fixed slot1, game-name/version arguments and menu confirmations. The table above connects that call boundary to native handlers; this pass does not re-audit the full save-list UI.

On the selected successful SaveGame path, `0x0e74a–0x0e78e` writes two length words and version text, then invokes the region encoder twice:

| Captured data | Save call | Restore call |
| --- | --- | --- |
| Fixed `DS:[0x1926,0x1996)`, 112 bytes | `0x0e77a` | `0x0e83b`, destination`0x1926` |
| Near heap `DS:[word[0x1ae0],word[0x1ae2])` | `0x0e789` | `0x0e846`, destination`word[0x1ae0]` |

The length fields are respectively `0x1996−0x1926` and `word[0x1ae2]−word[0x1ae0]`. The version writer at `0x0eda3–0x0ee04` writes the version string plus newline. Validation at `0x0e9b2–0x0ea1e` reads those lengths and a version line, checks both current expected region lengths and compares the supplied version. These are compatibility checks for the identified format, not evidence for accepting arbitrary interpreter versions.

The encoder at `0x0ea5f–0x0eba7` traverses the supplied start/end interval, emits literal or repeated-byte records, and terminates each encoded region with marker`0xff`. Its output helpers reach the DOS file-write wrapper at `0x03e2c`, which executes interrupt21h/function40h. The paired decoder at `0x0eba8–0x0ec71` consumes those records and writes sequentially to its supplied destination; its input reaches DOS file-read interrupt21h/function3fh at `0x03d8c`.

This is selective interpreter/heap serialization. It is not a full data-segment dump, CPU-state snapshot or emulator snapshot. The restore handler subsequently performs resource reload/fixup work; the individual meanings of every byte in the fixed112-byte block and every fixup are outside this pass.

## DOS-SAVE-002: the native seed lies outside those regions

The [native randomness audit](dos-randomness.md) identifies the generator's16-bit seed at `DS:0x0cca`. The generator reads it at load-image`0x0bda7` and writes its next value at`0x0bdbc`. Its initial executable-image word is zero; the generator's zero-seed path obtains a time-derived nonzero input from DOS.

The fixed save block starts at`DS:0x1926`, above the seed. The heap boundary is also directly recoverable: initialization at `0x17b39–0x17b64` passes start`0x243e` to the allocator initializer at`0x17ad0`; that initializer stores the start in `DS:0x1ae0` at`0x17af8`, and computes/stores the upper limit in `DS:0x1ae2` at`0x17af2`. The ordinary near heap consequently begins above both the seed and the fixed block.

Thus `DS:0x0cca` belongs to neither of the two captured intervals, and the identified normal restore destinations do not restore it. The selected serialization path has no separate seed field. A supplementary whole-image search for the little-endian immediate offset bytes`ca 0c` finds only the two generator references above. This corroborates the explicit-offset trace; it is not an absence proof against computed pointers or aliasing.

For a valid ordinary save, the static result is that **native save serialization does not capture or reinstate this PRNG seed**. This conclusion follows from interval bounds and matching decoder destinations, not from assuming that saved script objects include every interpreter global.

## DOS-SAVE-003: replay and remaining limits

Rewinding game objects through RestoreGame does not by itself rewind this interpreter-owned random state. A same-process reload therefore cannot be promised to repeat the next outcome; restarting the interpreter also reaches the independently time-derived initialization path if the seed remains zero until a draw. The exact sequence visible after a restore still depends on draw order, including presentation calls already identified in the [finish audit](bytecode-flow-and-persistence.md#finish-001-placement-is-assigned-during-presentation), and any native callbacks around the restore. This pass does not assert how many draws a complete restore interaction consumes or experimentally demonstrate a changed outcome.

A future reproducible TypeScript save should specify its random state and draw policy explicitly. That is a proposed technical contract for2.0, not a discovered capability of the original save format; no application implementation or departure has been approved here.

Remaining boundaries: no actual save bytes or roundtrip were generated; this is not a complete parser/serializer specification; corrupted compressed streams and destination overruns are outside the valid-save finding; native indirect-call behavior has not been exhaustively proved. Browser filesystem persistence, emulator snapshots and other releases are separate systems. An emulator-level memory snapshot may capture more state than native SaveGame and must not be conflated with this kernel path.
