# Direct package logic verification

Completed 2026-10-16 against the website bundle, version 1.000.060. We now independently decode the actual compiled scripts, rather than relying exclusively on the published decompilation or watching ordinary play.

## What was recovered

The [local decoder](../../tools/research/sci_scripts.py) recovers object/class tables, selectors, method/export entries, instructions, control-flow blocks and conservative expression listings from all **69 scripts**: **53,740 instructions**, 598 objects/classes and 738 methods. The [coverage record](../../artifacts/original-game/bytecode-coverage.json) identifies every input by hash. All 107,970 code payload bytes are accounted for, including 183 alignment bytes; branch, direct call, method and resource-address checks report no invalid targets.

This is complete instruction decoding for this package, **not complete understanding of every rule**. Generated pseudocode retains explicit unknown stack values across block boundaries (1,217 references) and 56 dynamic argument operations. Another 2,678 instructions are outside reachability from recovered entries; that does not prove they are dead code. Original variable names and fully structured, recompilable source have not been recovered. SCI arithmetic still requires the original 16-bit semantics.

Original listings remain in ignored `work/bytecode/decoded/`. [Rebuild instructions](../discovery/decompile-original-scripts.md) make the work portable; no original script payloads or generated code are committed.

## Rules established from actual bytes

| Finding | Package result | Remaining boundary |
| --- | --- | --- |
| Partial-shift garnishment | Rent-debt branches overwrite prorated pay with calculations based on full-shift gross pay | Visible feedback, timekeeper and unusual re-entry interactions |
| Loan rejection | Initial application rejection calls happiness −1 twice; extension rejection once | Helper clamps each call at zero; not an unrestricted −2 |
| Loan repayment | A full $50 payment removes $45 principal; final payments below $50 remove their full amount | Remaining scheduling/default paths and large-value arithmetic |
| Economic adjustment | Both alternatives compare the same lower bound; first successful branch skips the second, making its positive-risk alternative unreachable | Long-run effects and whether to preserve the quirk |
| Economy parent argument | A guarded default is stored, but the calculation reads the parameter directly | Original DOS interpreter handling of an omitted parameter |
| Refrigerator purchase | Receipt adds quantity before the item checks for zero, so an ordinary successful purchase skips its nominal +1 happiness | Verified for this item; other overrides and unusual states remain separate |
| Apartment stereo | Stored loop 1 is outside the actual view's single loop | ScummVM clamps it; original DOS rendering fallback remains unproved |

See [finance evidence](bytecode-finance-findings.md), [economy/presentation evidence](bytecode-economy-presentation.md), and [purchase evidence](bytecode-purchase-findings.md) for exact offsets, selector identities, examples and limitations. These are selected-path confirmations; they do not establish equivalence of every published source file.

## Validation and next research

Fourteen decoder fixture groups cover operand widths, signed branches, relative calls, method layout, read-value snapshots and indexed reads. A second full export reproduced the generated files and coverage metadata exactly. Independent finance decoding agreed on 1,147 instruction boundaries and operands across six inspected ranges. These establish decoding consistency, not execution of every path.

The next pass now traces [employment](employment.md), [education](education.md), [weekly/opponent control](bytecode-weekly-opponent.md) and [location/time/save flow](bytecode-flow-and-persistence.md). Remaining work includes detailed event arithmetic, exhaustive AI action consumers, precise travel timing and interpreter edge cases. Resolve omitted-argument and invalid-loop cases through interpreter/frame analysis or narrowly instrumented execution. Ordinary gameplay is useful when presentation is the question; it is no longer needed merely to establish that the confirmed branches exist.

No discovered quirk is an approved change to the successor. Preservation versus correction remains a planning decision.
