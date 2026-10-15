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

## Sources not used as proof

Community pages helped locate topics, but their formulas and edition summaries are not the basis of the records in this pass. In particular, an approximate price formula can conceal integer rounding, the goods subindex, and lower bounds. Where the scripts are surprising, the audit preserves the uncertainty rather than replacing it with a community explanation.

## Reproduction policy

Permanent source links are pinned to revisions. Local source bytes are SHA-256 identified in the metadata. Rule records link the relevant methods/lines. The analytical fixtures validate our arithmetic transcription, not the original executable. Runtime cases are listed separately and remain pending unless explicitly marked observed.
