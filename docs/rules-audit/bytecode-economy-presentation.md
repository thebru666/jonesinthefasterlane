# Package bytecode: economy and apartment presentation

Verified 2026-10-16 against decompressed resources from the website bundle, version 1.000.060. This is **BYTECODE** evidence, independent of whether the published decompilation is accurate. Original payloads and disassembly stay in ignored `work/`; committed [evidence metadata](../../artifacts/rules-audit/bytecode-economy-presentation.json) records hashes, offsets, selectors and analytical conclusions. Offsets below are hexadecimal byte offsets into decompressed resource payloads, without an added resource header.

## ECON-B01: the duplicated condition exists in the actual game

`script.107`, not script 110, contains the `EconomicIndex` class. Its class block begins at `0x0216`; selector 102 (`init`) points to `0x0042`, and selector 60 (`doit`) points to `0x01b5`. Selector names come from the package's vocabulary 997, and property positions come from the class's own selector table.

Both adjustment alternatives compare property slot 10 (`adjustment`, property byte offset 20) against slot 8 (`lowerRange`, property byte offset 16): the first comparison begins at `0x0179`, the second at `0x0198`. They do **not** compare against different bounds. The first true branch subtracts a random risk amount and then unconditionally jumps from `0x0195` to the return at `0x01b4`. If the first comparison fails, neither compared property changes before the second comparison. Therefore the following alternative that adds a random risk amount is unreachable under ordinary sequential execution, including when the subtraction would have been zero.

This confirms the suspicious condition in [ECON-002](economy.md#econ-002-trend-and-reading-update) is present in the website binary, rather than introduced by the published decompiler. It does not establish the author's intention or quantify long-run economic bias. Fixing or preserving it remains an adaptation decision.

## ECON-B02: the omitted parent argument needs an interpreter investigation

The same actual method tests its argument count at `0x01b7`, selects the first argument or zero and stores that result into temporary slot 0 at `0x01c3`. However, the subsequent reading calculation loads **parameter slot 1 directly** at `0x01c9`, rather than loading that guarded temporary. This distinction also exists in the actual bytes; a faithful transcription cannot replace it with a safe default silently.

The meaning of reading parameter slot 1 with an argument count of zero depends on the interpreter's parameter-frame handling and the caller's frame. This pass does not prove that it supplies zero, a stale value, or a stable value specific to this caller. Keep the main-index default-parent interpretation explicitly provisional. There is no need for a long gameplay session: inspect the precise send frame and interpreter implementation, or run one targeted instrumented invocation.

## PRESENT-B01: the stereo's invalid loop is genuine

`script.202` contains the `theStereo` object in the block beginning at `0x0436`; its stored name points to `0x05f9`. Directly stored values are:

| Property | Package selector | Value | Value offset |
| --- | --- | --- | --- |
| species | 0 | 12 (`DIcon`) | `0x0442` |
| nsTop | 9 | 43 | `0x044e` |
| nsLeft | 10 | 121 | `0x0450` |
| view | 5 | 702 | `0x0472` |
| loop | 6 | 1 | `0x0474` |
| cel | 7 | 4 | `0x0476` |

The class is independently resolved through vocabulary 996: class 12 belongs to script 255. Its class block at `0x05e4` supplies the property selector table. This avoids relying on the published source's property labels. Vocabulary 997 resolves selector IDs to the names above.

The actual `view.702` header has one loop, indexed 0, and that loop has five cels, indexed 0–4. Thus the literal loop 1 does not identify an available loop in this resource. The source/artwork discrepancy identified in the [screen reconstruction](../original-game/screen-reconstruction.md) is an actual package inconsistency.

The pinned ScummVM reference clamps a requested loop and cel to the available range in `GfxView::getCelInfo` and `getCelCount`. For this resource, its `getCelInfo(1, 4)` selects loop 0, cel 4. That is **reference-interpreter evidence**, not proof that the bundled original DOS interpreter uses the same fallback. The reconstruction should retain its uncertainty label until that original rendering path is established; do not claim the object itself contains loop 0.

## Evidence boundaries and next work

These checks validate particular conditions, parameter accesses and object properties, not every method in these scripts. No whole-script equivalence claim is made. The economic duplicate and stereo literal are now resolved at the package level; original interpreter handling of the omitted parameter and out-of-range loop remains open.

The interpreter reference is [ScummVM `view.cpp`, pinned revision](https://github.com/scummvm/scummvm/blob/2b5f9b5d95f267c87889746906148db6088130f8/engines/sci/graphics/view.cpp#L397). Object and method decoding follows [ScummVM `object.cpp`](https://github.com/scummvm/scummvm/blob/2b5f9b5d95f267c87889746906148db6088130f8/engines/sci/engine/object.cpp#L49), opcode definitions in [kernel_tables.h](https://github.com/scummvm/scummvm/blob/2b5f9b5d95f267c87889746906148db6088130f8/engines/sci/engine/kernel_tables.h#L1538) and execution semantics in [vm.cpp](https://github.com/scummvm/scummvm/blob/2b5f9b5d95f267c87889746906148db6088130f8/engines/sci/engine/vm.cpp). These references interpret bytes; the bundle itself supplies the values and branch targets.
