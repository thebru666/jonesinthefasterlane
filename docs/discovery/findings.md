# Initial discovery findings

Research date: 2026-10-15.

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

This supports investigating SCI resources rather than starting with the DOSBox executable. It does **not** establish that this particular package has been successfully decompiled. No decompiler has been installed or run, no scripts have been extracted, and no hidden formulas or event probabilities have been verified yet. Tool/platform suitability must be checked in the next research step.

## Source register

| Source | Use | Evidence limits |
| --- | --- | --- |
| [Playable website](https://jonesinthefastlane.com/) | Reference package and later observed behaviour | Package version is known; gameplay audit pending |
| [SCI Companion decompiler documentation](https://scicompanion.com/Documentation/decompiler.html) | Tool feasibility and limitations | General documentation, not a successful decompile of this game |
| [Original manual scan](https://virtualconsoles.com/wp-content/uploads/2024/03/Jones-in-the-Fast-Lane_Manual_DOS_EN-compressed.pdf) | Candidate source for stated player-facing rules | Located/opened; detailed reading and edition matching pending |
| [React: build from scratch](https://react.dev/learn/build-a-react-app-from-scratch) | React/TypeScript build-tool feasibility | Architecture recommendation is our design judgment |

Links were accessed during initial research on 2026-10-15. Sources and remote packages can change; preserve retrieval metadata when adding evidence.

## Next research step

1. Establish the reference edition and a practical SCI inspection workflow.
2. Read and map the manual's stated rules.
3. Identify scripts/resources that govern time, weekly processing, and economy.
4. Produce the first evidence-backed rule records and document remaining uncertainty.

Do not infer complete mechanics from archive filenames or unverified recollection.
