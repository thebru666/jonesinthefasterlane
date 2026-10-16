# Initial discovery findings

Research date: 2026-10-15.

Update: the first [rules-audit pass](../rules-audit/README.md#pass-1-findings-2026-10-15) now uses published decompiled scripts. The initial tool-feasibility notes below describe the earlier discovery stage; see the [source register](source-register.md) for current provenance and limits.

Further update: the original reference card was found separately, and a fuller [original-game baseline](../original-game/README.md) now covers setup, layout, locations, progression, saves, and finish. This replaces the earlier speculative screen outline as our starting point.

## Verified from the website and downloaded package

Source: <https://jonesinthefastlane.com/>.

- The page loads `js-dos/js-dos.js` and its stylesheet.
- The page configures the emulator path and runs `bundle.jsdos`.
- The public bundle is a ZIP archive, 1,078,159 bytes as retrieved.
- Its `version` file contains `1.000.060` followed by DOS line endings.
- It contains `sciv256.exe`, `resource.map`, `resource.001`, and `resource.002`.
- The js-dos configuration identifies `sierra.bat` as the startup script.

See the [bundle inventory](../../artifacts/discovery/2026-10-15-bundle-inventory.json) for filenames, sizes, SHA-256, and retrieval metadata. The inventory describes the package without including game contents.

The game was opened in a browser and reached its opening notice. No complete match or controlled gameplay experiment was performed during this initial discovery. Subsequent [runtime sessions](../rules-audit/runtime-observations.md) now establish specific visible setup/transaction/handover/work outcomes; they do not replace the script audits or prove all behaviours.

## Script inspection feasibility

[SCI Companion's decompiler documentation](https://scicompanion.com/Documentation/decompiler.html) describes reconstructing higher-level structures from Sierra script resources. It states that class, instance, property, and method information can survive, while parameter and temporary-variable names are not available. Some methods fall back to disassembly, and results can contain errors.

This supports investigating SCI resources rather than starting with the DOSBox executable. We have not installed or run a decompiler, or decompiled the website archive. The asset exporter subsequently extracted and decompressed script resources, without semantically decompiling them. The subsequent audit instead located and inspected sluicebox's published decompilation for the matching version label and a CD comparison. Script-derived formulas and probabilities are documented with limits; independent bytecode correspondence and controlled runtime verification remain pending.

## Source register

| Source | Use | Evidence limits |
| --- | --- | --- |
| [Playable website](https://jonesinthefastlane.com/) | Reference package and later observed behaviour | Package version is known; gameplay audit pending |
| [SCI Companion decompiler documentation](https://scicompanion.com/Documentation/decompiler.html) | Tool feasibility and limitations | General documentation, not a successful decompile of this game |
| [Original manual scan](https://virtualconsoles.com/wp-content/uploads/2024/03/Jones-in-the-Fast-Lane_Manual_DOS_EN-compressed.pdf) | Interaction conventions and original documentation | Relevant pages visually inspected in pass 1; referenced gameplay card absent; edition matching pending |
| [React: build from scratch](https://react.dev/learn/build-a-react-app-from-scratch) | React/TypeScript build-tool feasibility | Architecture recommendation is our design judgment |

Links were accessed during initial research on 2026-10-15. Sources and remote packages can change; preserve retrieval metadata when adding evidence.

## Research progress and next step

1. Located a published script set for the matching floppy version and pinned its revision; exact bundle/script correspondence remains open.
2. Inspected the manual's interaction pages; its separate reference card is absent from that scan but has now been located and inspected through Sierra Gamers (source S05).
3. Traced time, weekly processing, and economy into their supporting callers and recorded the first rule groups.
4. Pass 2 now documents [AI](../rules-audit/computer-opponent.md), [food/housing](../rules-audit/food-and-housing.md) and [goods/finance](../rules-audit/goods-and-finance.md); source correspondence and runtime validation remain open.
5. [Local analytical screen studies](../original-game/screen-reconstruction.md) combine decoded components with script coordinates; they are not runtime screenshots.
6. The [event audit](../rules-audit/random-events.md) now covers weekend/ticket/lottery/mugging/joke/recovery paths. [Actual captures](../rules-audit/runtime-observations.md) and an [independent solo control](../rules-audit/runtime-solo-control.md) provide bounded observations.
7. Next priority is actual package bytecode correspondence to the published decompilation, with targeted runtime experiments for unresolved questions. The owner redirected effort toward reverse engineering on 2026-10-16; broad exploratory play is deferred.

Do not infer complete mechanics from archive filenames or unverified recollection.
