# Initial discovery findings

Research date: 2026-10-15.

Update: the first [rules-audit pass](../rules-audit/README.md#pass-1-findings-2026-10-15) now uses published decompiled scripts. The initial tool-feasibility notes below describe the earlier discovery stage; see the [source register](source-register.md) for current provenance and limits.

## Verified from the website and downloaded package

Source: <https://jonesinthefastlane.com/>.

- The page loads `js-dos/js-dos.js` and its stylesheet.
- The page configures the emulator path and runs `bundle.jsdos`.
- The public bundle is a ZIP archive, 1,078,159 bytes as retrieved.
- Its `version` file contains `1.000.060` followed by DOS line endings.
- It contains `sciv256.exe`, `resource.map`, `resource.001`, and `resource.002`.
- The js-dos configuration identifies `sierra.bat` as the startup script.

See the [bundle inventory](../../artifacts/discovery/2026-10-15-bundle-inventory.json) for filenames, sizes, SHA-256, and retrieval metadata. The inventory describes the package without including game contents.

The game was opened in a browser and reached its opening notice. No complete match or controlled gameplay experiment was performed during this initial discovery.

## Script inspection feasibility

[SCI Companion's decompiler documentation](https://scicompanion.com/Documentation/decompiler.html) describes reconstructing higher-level structures from Sierra script resources. It states that class, instance, property, and method information can survive, while parameter and temporary-variable names are not available. Some methods fall back to disassembly, and results can contain errors.

This supports investigating SCI resources rather than starting with the DOSBox executable. We have not installed or run a decompiler, or extracted script resources from the website archive. The subsequent audit instead located and inspected sluicebox's published decompilation for the matching version label and a CD comparison. Script-derived formulas and probabilities are documented with limits; independent bytecode correspondence and controlled runtime verification remain pending.

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
2. Inspected the manual's interaction pages; it refers to a separate card absent from this scan.
3. Traced time, weekly processing, and economy into their supporting callers and recorded the first rule groups.
4. Next: reproduce the flagged cases and continue employment/education/content and computer-opponent audits using the [validation backlog](../rules-audit/validation-backlog.md).

Do not infer complete mechanics from archive filenames or unverified recollection.
