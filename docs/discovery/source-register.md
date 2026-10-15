# Audit sources and provenance

Research date: 2026-10-15. This register supersedes the initial source-status notes where they differ.

## S01: website package

- Page: <https://jonesinthefastlane.com/>.
- Archive: <https://jonesinthefastlane.com/bundle.jsdos>.
- Version marker: `1.000.060`.
- Identification: [initial inventory](../../artifacts/discovery/2026-10-15-bundle-inventory.json).
- Evidence: PACKAGE. This is the reference package for future runtime experiments.

## S02: published decompiled scripts

- Author/repository: [sluicebox/sci-scripts](https://github.com/sluicebox/sci-scripts).
- Pinned revision: `870a8015b689474484bf3d8b41416956d4315432`.
- [Methodology and attribution](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/README.md).
- Reference folder: `jones-dos-1.000.060/src`.
- Comparison folder: `jones-cd-dos-1.0/src`.
- Evidence: SCRIPT, specifically **published decompilation inspected by us**. We did not run a decompiler ourselves or independently establish byte-for-byte correspondence with S01's script resources. The folder/version match is strong identification evidence, not a substitute for that check.
- Downloaded source remains in ignored `work/audit/scripts/`. Only our analysis and [source metadata](../../artifacts/discovery/2026-10-15-audit-sources.json) are committed.

The original-experience pass retrieved the remaining forty floppy script references at the same pinned revision. Their identification is recorded in [additional source inputs](../../artifacts/original-game/2026-10-15-source-inputs.json); inclusion in the manifest does not imply every method was fully audited.

The initial pass follows named methods and their callers. It does not claim all downloaded files were fully audited, or that a decompiler output is infallible. Apparent bugs require bytecode or runtime confirmation before we decide whether to reproduce them.

## S03: original manual scan

- [Manual PDF](https://virtualconsoles.com/wp-content/uploads/2024/03/Jones-in-the-Fast-Lane_Manual_DOS_EN-compressed.pdf).
- 12 PDF pages; the scan is image-based. Text extraction returned no usable text, so relevant pages were rendered and inspected visually.
- PDF page 5 / printed page 3 refers to an accompanying reference card. That card is not present in this scan.
- PDF page 7 / printed page 5 covers startup, input, and skipping the opening sequence.
- PDF page 8 / printed page 6 covers menus, saving, restoring, and quitting. It describes a single saved game at a time.
- PDF page 9 / printed page 7 lists shortcuts, including statistics, goals, reading speed, game speed, and skipping nonessential messages.
- Evidence: DOCUMENTED. Useful for interaction conventions; insufficient to establish economic formulas or the complete gameplay rules. Exact correspondence to version 1.000.060 is unconfirmed.

The manual hash and size are in the source metadata. The original PDF and rendered pages remain local only.

## S04: SCI arithmetic and random semantics

- Repository: [ScummVM](https://github.com/scummvm/scummvm).
- Pinned revision: `2b5f9b5d95f267c87889746906148db6088130f8`.
- [SCI Random implementation](https://github.com/scummvm/scummvm/blob/2b5f9b5d95f267c87889746906148db6088130f8/engines/sci/engine/kmath.cpp#L38).
- [SCI numeric division](https://github.com/scummvm/scummvm/blob/2b5f9b5d95f267c87889746906148db6088130f8/engines/sci/engine/vm_types.cpp#L113).
- Two-argument Random uses inclusive endpoints. Numeric division uses signed integer division, truncating toward zero.
- Evidence: SCRIPT from an interpreter reimplementation, used to interpret S02. This does not establish matching random seeds or exact random sequences under the original interpreter running in js-dos.

## S05: original reference card, found separately

- [Preservation page](https://www.sierragamers.com/jones-in-the-fast-lane/); [reference-card PDF](https://www.sierragamers.com/wp-content/uploads/2019/12/Jones_In_The_Fast_Lane_Reference_Card.pdf).
- Retrieved 2026-10-15; two scanned PDF pages, both rendered and inspected. Printed copyright is 1992; precise edition correspondence remains unconfirmed.
- Evidence: DOCUMENTED, original publication. Annotated pictures explain goals, comparison/statistics, cash and clock; accompanying instructions describe the basic life loop. This fills the companion-card gap left by S03, without changing what is present in that manual scan.
- A money/net-worth description disagrees with the inspected floppy scoring path; the discrepancy is retained in [progress and finish](../original-game/progression-and-finish.md).
- Hash/size in [source inputs](../../artifacts/original-game/2026-10-15-source-inputs.json). The scan/rendered pages remain local-only.

## S06: existing summaries and retrospective guides

The [existing-summaries guide](../original-game/existing-summaries.md) identifies accessible player summaries, screenshots to consult, and source limits. Community descriptions are DOCUMENTED evidence, not runtime or primary rule proof. Version-specific tables and formulas in the new baseline derive from S02. Full Sierra Chest and MobyGames screenshot pages returned access failures; they are not treated as inspected visual evidence.

## S07: packed-resource directory inspection

The S01 archive's map was parsed and all 299 volume addresses/resource header IDs validated. [Inventory](../../artifacts/original-game/packed-resource-inventory.json) and [interpretation/limits](../original-game/packed-resources.md). Format/type definitions were checked against `engines/sci/resource/resource.cpp` and `resource.h` at the S04 pinned ScummVM revision; source hashes are recorded with the inventory. This is PACKAGE evidence, without payload decoding or rendered-art inspection.

## S08: local decoded resource catalogue

- Rebuilt 2026-10-15 from the exact S01 bundle, validated against its archive and map hashes; no alternate game edition substituted.
- [Portable recipe and validation](rebuild-original-assets.md), [tracked coverage and metadata](../../artifacts/original-game/decoded-asset-summary.json), [script-role hints](../../artifacts/original-game/asset-role-hints.json).
- Algorithms adapted from S04 pinned ScummVM source, with paths, attribution and GPL notices in [tool provenance](../../tools/research/THIRD_PARTY.md). Python source hashes and Python/Pillow versions are recorded with each run.
- Evidence: PACKAGE for extraction/inventory and DECODED for exported components, text and sound events. All 266 unique resources decompress; 108 graphics resources render, 39 text resources decode and 34 sound resources export events/MIDI. The other 85 resources remain decompressed bytes.
- Fresh acquisition and offline builds matched 1,390 output hashes. No complete runtime screenshot reconstruction, audio listening/hardware comparison or script-bytecode correspondence is claimed. Original resource payloads and rendered exports remain ignored local files.

## S09: pass 2 scripts and analytical screen reconstruction

- [AI policy](../rules-audit/computer-opponent.md), [food/housing](../rules-audit/food-and-housing.md), [goods/finance](../rules-audit/goods-and-finance.md) inspect the same S02 pinned floppy decompilation; [25 cited input hashes](../../artifacts/rules-audit/2026-10-15-pass2-source-inputs.json) identify the local source files. No bytecode match or runtime confirmation is asserted.
- The [AI arithmetic check](../../artifacts/rules-audit/ai-goal-allocation-check.json) is reproducible with its committed independent Python checker; it establishes formula bounds/capacity only.
- The [screen recipes](../../artifacts/original-game/screen-study-recipes.json) record 21 source hashes, selected resource/cel coordinates and explicit state assumptions; [screen studies](../original-game/screen-reconstruction.md) combine those with S08 decoded pixels. Rendered composites remain ignored local files.
- Evidence: SCRIPT for behaviour/placement, DECODED for original components, analytical arithmetic/composition checks for the new artifacts. Full runtime text, ports/borders, palette transitions, timing and the security stereo discrepancy remain open.

## Sources not used as proof

Community pages help locate topics, names, and presentation references, but their formulas and edition summaries are not the basis of the script-derived records. In particular, an approximate price formula can conceal integer rounding, the goods subindex, and lower bounds. Where the scripts are surprising, the audit preserves the uncertainty rather than replacing it with a community explanation.

## Reproduction policy

Permanent source links are pinned to revisions. Local source bytes are SHA-256 identified in the metadata. Rule records link the relevant methods/lines. The analytical fixtures validate our arithmetic transcription, not the original executable. Runtime cases are listed separately and remain pending unless explicitly marked observed.
