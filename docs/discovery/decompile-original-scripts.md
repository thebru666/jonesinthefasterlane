# Decode and inspect the original script logic

Recorded: 2026-10-16 UTC. Reference: the website bundle identifying version `1.000.060`.

This pass reads the **actual decompressed script bytes from the website bundle**. It does not use the published decompiled scripts as input. The result is complete instruction decoding for the inspected code blocks, recovered object/class/method structure and control flow, plus conservative expression pseudocode. It is not a complete recreation of the original structured source.

## Rebuild on another computer

First follow the [original-asset rebuild guide](rebuild-original-assets.md). This acquires and checks the exact archive, then creates `work/original-assets/decoded/resources/`. Retain the committed `artifacts/original-game/decoded-asset-summary.json`; it supplies the expected hashes for all 69 scripts.

From the repository root, use Python 3.10 or newer:

```sh
python3 tools/research/sci_scripts.py --self-test
python3 tools/research/sci_scripts.py \
  --resources work/original-assets/decoded/resources \
  --output work/bytecode/decoded
```

This script uses only the Python standard library. Pillow is needed by the preceding asset exporter, not by script analysis. The asset virtual environment's Python also works. On Windows, use `python` or the appropriate virtual-environment executable with the same arguments.

The script verifies every script resource against the committed resource hashes and checks the selector vocabulary's SHA-256. A missing, additional or changed script is rejected. It does not silently change the reference edition. No network access, ScummVM installation or original game execution is needed after the resources are rebuilt.

To update the tracked analytical coverage after reviewing a tooling change:

```sh
python3 tools/research/sci_scripts.py \
  --coverage artifacts/original-game/bytecode-coverage.json
```

Review that metadata diff before committing. Disassembly, pseudocode, original strings and decoded object definitions must stay ignored locally. Output directories are restricted to the repository's ignored `work/` or `artifacts/private/` trees.

## Local outputs

| File | Contents |
| --- | --- |
| `script-NNN.asm` | Instruction offsets, exact encoded bytes, mnemonics, operands, branch/call targets, method labels and object metadata |
| `script-NNN.json` | Parsed blocks, objects/classes, property values and inherited selector names, methods, exports, locals, instructions, function reachability and basic blocks |
| `script-NNN.pseudo.txt` | Block-local symbolic expressions and explicit labelled branches; unknown incoming state remains visible |
| `selectors.json` | Selector IDs/names decoded from the package's vocabulary resource 997 |
| `coverage.json` | Source/tool hashes, coverage totals, validation results and limitations |

Offsets in `.asm` and pseudocode labels are hexadecimal offsets in the decompressed script resource. JSON offsets are decimal integers. Property offsets identify positions inside an object's property array; they are not script-resource addresses. Resource-address loads in this bundle use signed displacements relative to the next instruction. The tool checks these against actual object addresses or string blocks; applying an absolute-address interpretation gives incorrect targets for this edition.

The tool recovers method and property names from the game's own object tables and selector vocabulary. It retains numerical global/local/kernel references where names are not established by those bytes. Names assigned in the separately published source are useful interpretation aids, but are not proof of an original symbol name.

## Verified coverage

The [committed coverage](../../artifacts/original-game/bytecode-coverage.json) records the exact hashes and results:

| Measure | Result |
| --- | ---: |
| Script resources decoded | 69 |
| Instructions decoded | 53,740 |
| Objects/classes | 598 |
| Methods | 738 |
| Recovered function entry points | 819 |
| Basic blocks | 6,399 |
| Package selector names | 485 |
| Code-block payload bytes | 107,970 |
| Instruction bytes | 107,787 |
| Alignment padding bytes | 183 |
| Reported decode or target-validation failures | 0 |

Instruction bytes plus the identified alignment bytes reconstruct each code-block payload exactly. Branches, local calls, method entries and 1,468 resource-address loads were checked against parsed targets. Ten fixture groups check operand widths, signed displacements, the call offset base after the frame operand, invalid-opcode rejection and a synthetic class/method table. A fresh second export produced identical hashes for all 209 output files.

These checks establish consistent binary decoding. They do not establish that every branch is executed in normal play, that every recovered expression has been manually reviewed, or that the program has been rebuilt and run from generated source.

## Reading the recovered logic

Use object/method names in the JSON or assembly to locate a rule, then follow its instruction offsets and basic-block successors. Pseudocode makes arithmetic and selector messages easier to inspect, while assembly remains the precise reference for operation order and branch conditions. Record any finding with the script number, method/export, instruction range and script SHA-256.

The symbolic pass restarts at each basic block. `incoming_acc`, `incoming_previous_acc` and `incoming_stack_N` explicitly identify state that must be traced from predecessor blocks. A `result_NNNN` label denotes one call/send result; it does not repeat the call when used later in an expression. Branches remain explicit `goto` statements rather than being presented as recovered original `if`/`while` syntax.

The current pseudocode contains **1,217 references to unresolved incoming stack values** and **56 dynamic rest-argument operations**. These are counts of marked references/operations, not counts of distinct uncertain game rules. There are **2,678 instructions not reached from the recovered entry points**. This identifies incomplete static reachability; it does not prove that those instructions are dead code. Dynamic calls, inherited dispatch, cross-script calls and saved/runtime state still require interpretation.

Expressions describe SCI VM operations. Preserve original integer width, signed/unsigned comparisons, division and message semantics when translating a rule; ordinary JavaScript or Python arithmetic is not automatically equivalent. Indexed variable access, unresolved call targets and dynamic argument forwarding need manual attention. No claim is made that generated pseudocode can be compiled back into an equivalent game.

## Provenance and evidence status

Format and VM references are pinned to ScummVM revision `2b5f9b5d95f267c87889746906148db6088130f8`; see [tool provenance and GPL notices](../../tools/research/THIRD_PARTY.md). The generator is committed research tooling, while generated original code remains ignored. Its GPL licence does not select the future game's licence or grant rights to the original game.

Findings from this pass should be labelled **bytecode-verified** when their cited conditions, arithmetic and ordering have actually been traced. A successful decode alone does not verify every existing prose rule. Published-source claims, binary findings, independent arithmetic checks and runtime observations remain separate evidence categories.
