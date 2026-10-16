# Economy's omitted argument: original and reference frame traces

Investigated 2026-10-16. Inputs: actual website script107, edition1.000.060, its original DOS interpreter unpacked locally, and the pinned ScummVM reference. Evidence is **BYTECODE + DOS-STATIC + reference-interpreter inference**, not runtime execution. This resolves the selected static call relationship in [ECON-B02](bytecode-economy-presentation.md#econ-b02-the-omitted-parent-argument-needs-an-interpreter-investigation); it does not assume a missing argument defaults to zero.

## The caller's frame matters

Actual script107 sends two methods to `mainI` in **one packet** at `0x041a`: initialize with the current main trend/reading, then update with zero explicit arguments. The send consumes12 bytes, or six16-bit words. The two methods are `EconomicIndex.init`, entry`0x0042`, and `EconomicIndex.doit`, entry`0x01b5`.

The update's guard does choose0 when argument count is0 and stores that in its own temporary0 (`0x01c3`). Its later arithmetic nevertheless reads parameter1 directly (`0x01c9`). Looking at those instructions alone cannot establish what value is read, because the parameter and temporary areas are positions on the interpreter's shared stack.

## What the pinned reference interpreter does

The source references below are all at ScummVM revision `2b5f9b5d95f267c87889746906148db6088130f8`; their hashes are already in [the source lock](../../artifacts/original-game/bytecode-source-inputs.json).

1. [`send_selector`](https://github.com/scummvm/scummvm/blob/2b5f9b5d95f267c87889746906148db6088130f8/engines/sci/engine/vm.cpp#L239) builds method frames for the packet in order, marking later method stack pointers with `CALL_SP_CARRY`.
2. [`ExecStack`](https://github.com/scummvm/scummvm/blob/2b5f9b5d95f267c87889746906148db6088130f8/engines/sci/engine/vm.h#L108) initially makes frame pointer equal stack pointer. [`link`](https://github.com/scummvm/scummvm/blob/2b5f9b5d95f267c87889746906148db6088130f8/engines/sci/engine/vm.cpp#L816) allocates temporary words above it.
3. [`ret`](https://github.com/scummvm/scummvm/blob/2b5f9b5d95f267c87889746906148db6088130f8/engines/sci/engine/vm.cpp#L921) passes the preceding method's ending stack pointer into that later frame. It does not rewind that carried pointer to the preceding method's frame base.
4. [Parameter/temp addressing](https://github.com/scummvm/scummvm/blob/2b5f9b5d95f267c87889746906148db6088130f8/engines/sci/engine/vm.cpp#L600) uses the packet's argument-count position for parameters and the carried frame pointer for temporaries. [Validation/read](https://github.com/scummvm/scummvm/blob/2b5f9b5d95f267c87889746906148db6088130f8/engines/sci/engine/vm.cpp#L91) permits an out-of-argument-range parameter access inside the stack; an already initialized stack word is returned as stored.

The resulting relative word addresses are:

| Value / location | Relative address |
| --- | ---: |
| End of six-word packet / initialization frame base | 6 |
| Initialization temporary0 | 6 |
| Update argument-count word | 5 |
| Update parameter1, despite argc0 | **6** |
| Carried update frame base / its guarded temporary0 | **7** |

Initialization allocates one temporary. A control-flow stack-height pass through all196 recovered initialization instructions finds ending stack delta **+1 at every static return**. The final write to its temporary0 at`0x00f7` dominates every return, and no later instruction writes that slot. The update therefore reads the **initialization's temporary0**, while its own guarded temporary0 is a different word. Treating the guard as a safe argument default misses this alias.

## Independent trace in the actual DOS interpreter

The [original executable rebuild](../discovery/inspect-dos-interpreter.md) identifies the packed/unpacked inputs. Native load-image offsets below exclude the MZ header. The DOS VM uses **BP as the last occupied VM word**, whereas the reference VM uses a next-free stack pointer; confusing the two conventions would produce an off-by-one error.

| Original native path | Static finding |
| --- | --- |
| Opcode dispatch table, relative DS1856 offset013c | Encoded opcode3f resolves to link at0048:065f; 43 to kernel call at0048:06c0; 48 to return at0048:07db; 4a to send at0048:07dc; 8f to parameter-stack load at0048:0a6d |
| Link, load image`0x00adf–0x00af7` | Temporary base becomes BP+2; BP advances by twice the declared temporary count |
| Parameter load,`0x00eed–0x00f0c` | Reads the argument-base word plus twice its index; this handler has no argument-count rejection/default branch |
| Message packet parser,`0x0b57b–0x0b6c4` | Records each method's argc position as parameter base, invokes its bytecode, then advances to the next message **without resetting VM BP**; pre-packet BP is restored only when the whole packet is exhausted |
| Return,`0x00c5b` | Returns from the bytecode invocation; it does not independently rewind the VM evaluation stack |
| Kernel call cleanup,`0x00b40–0x00b98` | Removes argument bytes and argc word from VM BP; Random60 and Abs61 preserve the caller's BP while using their own host stack frames |

For the six-word packet, DOS BP starts on word5. Initialization's one temporary occupies word6, and its return leaves BP on word6. Update's argument-count word remains word5, so parameter1 reads word6. Its own link allocates temporary0 at word7. The alias is the same as the reference ledger above: **the missing parameter reads the preceding initialization temporary**, while the guard writes a different word.

The native Random60 handler is0627:0d02 (`0x06f72`); Abs61 is0627:0f4e (`0x071be`). Their prologues/epilogues and the kernel-call cleanup preserve the initialization temporary. MZ relocation entries corroborate the data segment, bytecode invocation and kernel far pointers. A separate agent independently checked these addresses, pointer conventions, parser continuation and kernel preservation. The checker records hashes/addresses; the semantic native trace is manual and peer-reviewed, not an automatically executed x86 proof.

## Value supplied by that initialized word

The initialization's temporary contains its trend-target draw, after subtracting100. The actual writes are`0x00f1` and`0x00f7`; the final value is the one used by the initialization's trend comparison. It is not uninitialized stack garbage in this selected DOS/reference call shape.

For ordinary readings, define the existing recovery allowance `high` and downward allowance `low` from [ECON-002](economy.md#econ-002-trend-and-reading-update). The target draw is:

`D = Random(97 − low, 103 + high) − 100`

The matching original-DOS static trace and reference-frame inference give the main reading update an additional **`trunc(D/3)`**, before its event multiplier and clamp. Across the ordinary target range−5…5, that term is−1,0 or+1. For an ordinary reading100, D ranges−3…3, so the term is−1 for−3, +1 for3, and0 otherwise. Subindices that actually receive a parent argument retain that explicit argument; this finding does not replace all their parent effects with D.

This follows from actual package instructions and the selected original-DOS native paths, corroborated by the reference engine. It is not a measured economic distribution, full interpreter equivalence, arbitrary-caller guarantee or proof about other game editions.

## Reproduce the bounded check

After rebuilding the [local script listings](../discovery/decompile-original-scripts.md) and [unpacked original interpreter](../discovery/inspect-dos-interpreter.md), run:

```sh
python3 tools/research/check_economy_frame.py --check
```

The checker verifies the raw script hash, decoded instruction spans, stack heights across the initialization CFG, the dominating final temporary write, selected caller/update anchors, a synthetic packet-address ledger, and the original DOS input/relocations/handler addresses. [Committed metadata](../../artifacts/rules-audit/economy-frame-verification.json) contains analytical addresses/counts/limits, not original code. It does not execute the economy, random generator or DOS interpreter. To regenerate metadata after a reviewed checker change, omit`--check`.

## Planning consequence

The selected zero-versus-stale question is now resolved statically: **both the original DOS paths and pinned reference VM read a specific earlier initialized draw**. A runtime measurement remains useful as corroboration, rather than a prerequisite to identifying this native path. A2.0 implementation should explicitly preserve that term or choose different intended parent/default semantics; it must not treat the defensive-looking guard as proof of a zero result. Long-run economic distributions, other callers and other editions remain separate research.
