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

## S10: pass 3 personal-event scripts and arithmetic

- [EVENT-001–008](../rules-audit/random-events.md) inspect the same S02 pinned floppy decompilation for weekend selection/spending, lottery, street mugging, joke products, computer income and emergency recovery. [Eleven source hashes](../../artifacts/rules-audit/2026-10-15-events-source-inputs.json) identify the inspected inputs; no original source payloads are committed.
- [Lottery enumeration metadata](../../artifacts/rules-audit/lottery-probability-check.json) records 1,503 integer draw cases for ticket quantities 10, 20 and 100, with exact probability/expectation fractions. Regenerate or verify it with the [independent arithmetic checker](../../tools/research/check_lottery_probabilities.py); its `--check` mode validates tracked metadata without changing it.
- Evidence: SCRIPT for interpreted behaviour and analytical arithmetic for the enumeration. Neither establishes original RNG frequencies, package-bytecode correspondence or runtime reproduction; edition, overflow and redraw reachability limits remain explicit in the event audit.

## S11: actual website gameplay captures (2026-10-15–16)

- [Multiplayer observations](../rules-audit/runtime-observations.md) and [independent solo control](../rules-audit/runtime-solo-control.md) record ordinary mouse/keyboard sequences, visible values and missed intermediate states. No debugger, edited saves or hidden-state inspection was used.
- A fresh independent bundle download matched the existing S01 SHA-256; neither browser response was intercepted to establish a separate byte-for-byte match. Emulator build/RNG state and save persistence remain unverified.
- [Capture manifest](../../artifacts/rules-audit/runtime-capture-manifest.json) records 48 ignored local JPEG paths, hashes and dimensions. [Gallery tool](../../tools/research/index_runtime_captures.py) verifies available files without substituting missing evidence.
- Evidence: OBSERVED only for listed visible setup, balance, handover, graphical-clock and work outcomes. Exact timed food notices/happiness and internal time counters remain unmeasured. Source/script hypotheses retain their original evidence class.

## S12: direct website-package bytecode analysis (2026-10-16)

- The [local decoder](../../tools/research/sci_scripts.py) consumes S08 decompressed script payloads and vocabulary, without using S02 published decompiled source as input. [Input hashes and coverage](../../artifacts/original-game/bytecode-coverage.json), [portable rebuild](decompile-original-scripts.md).
- [Pinned interpreter input hashes](../../artifacts/original-game/bytecode-source-inputs.json) supplement the S04 format references. Algorithms and GPL notices are recorded in [tool provenance](../../tools/research/THIRD_PARTY.md).
- Evidence: BYTECODE for explicitly verified instructions/properties/control flow in [the findings](../rules-audit/bytecode-verification.md). Decode coverage is not a full semantic audit or runtime proof. Previous S02-based records retain their original provenance unless explicitly strengthened by a linked bytecode finding.
- All original scripts, disassembly, recovered expressions and upstream reference payloads remain ignored locally. Only analytical metadata and original research tooling/notes are committed.

## S13: connected core-loop package trace (2026-10-16)

- Uses the same S01/S08 resource hashes and S12 decoder; no new edition or archive substituted. [Employment](../rules-audit/employment.md), [education](../rules-audit/education.md), [weekly/opponent](../rules-audit/bytecode-weekly-opponent.md) and [flow/persistence](../rules-audit/bytecode-flow-and-persistence.md) identify the selected package paths. Their analytical manifests record all inputs, offsets and verification limits.
- The [connected flow reference](../original-game/game-flow-and-rule-contract.md) synthesizes those results with earlier domain records, preserving their evidence tiers. Published-source candidate paths were compared after inspecting actual method/property tables and instructions; no whole-source equivalence claim.
- A pseudocode snapshot error found during the trace was corrected: variable/property loads now capture instruction-time values rather than referring to variables that can later mutate. Fourteen fixtures include read/mutation/index checks; disassembly and resource hashes are unaffected.
- No new runtime execution, original save roundtrip or original RNG reproduction was performed. Original code, source payloads and scratch verification helpers remain ignored.

## S14: destination action and needs/event package extension (2026-10-16)

- Same website edition/resources; [AI action trace](../rules-audit/bytecode-ai-actions.md) resolves all thirteen destination controllers plus broker and shared dialog dispatch. [Verification metadata](../../artifacts/rules-audit/bytecode-ai-actions-verification.json) identifies2,811 checked instruction spans, controller entries and selected event writes/confirmation branches.
- [Needs/event trace](../rules-audit/bytecode-needs-events.md) and [metadata](../../artifacts/rules-audit/bytecode-needs-events-verification.json) identify1,654 selected instruction spans and ten independently read raw constants/comparison senses. The existing1,503-case lottery checker corresponds to the confirmed ordinary-range thresholds.
- Evidence is BYTECODE for explicitly traced predicates/ordering and analytical probability for inclusive uniform draws, not observed behaviour or reproduction of the DOS RNG. Weekend redraw reachability, object lifetime, every event/default branch and exhaustive human/AI parity remain unproved. Original payloads/listings stay ignored.

## S15: original DOS interpreter and native frame/random paths (2026-10-16)

- The same S01 bundle's `sciv256.exe` is identified by packed and unpacked SHA-256 in the [unpack record](../../artifacts/original-game/dos-interpreter-unpack.json). The [portable inspection recipe](inspect-dos-interpreter.md) pins `mywave82/unlzexe` revision `066aac7be3b27813c221d3b03621ad6dfaecd285`, source/README hashes, separate output and native address conventions. Repeat unpacking produced identical output. No original DOS executable was launched.
- [Economy frames](../rules-audit/economy-frame-semantics.md) combine actual script107 paths with original native opcode/message/kernel handlers and pinned ScummVM frame semantics. A separate agent independently checked pointer conventions, carry, relocations and kernel preservation. The analytical checker validates identities/addresses and script stack invariants; native semantic interpretation is manual.
- [DOS randomness](../rules-audit/dos-randomness.md) traces the selected native generator, bound mapping and arithmetic-library helpers, independently peer-reviewed. [Range hashes](../../artifacts/rules-audit/dos-randomness-verification.json) identify inspected bytes without committing them. This is DOS-STATIC evidence, not measured randomness, original execution or full interpreter equivalence.

## S16: timing, score and finance ordering follow-up (2026-10-16)

- [Travel](../rules-audit/travel-timing.md) combines S12 actual bytecode with pinned ScummVM Animate source/header; hashes and permanent source URLs are in [its metadata](../../artifacts/rules-audit/travel-timing-verification.json). The 25,500-case recurrence check is conditional analytical evidence, not original DOS timing.
- [Score refresh](../rules-audit/score-refresh.md) and [finance lifecycle](../rules-audit/finance-lifecycle.md) inventory all69 decoded resource hashes and selected original instruction spans. Their bounded literal-selector/direct-property searches strengthen normal-path ordering claims without proving absence of reflective/restored/interpreter mutations.
- No new runtime observation or application implementation accompanies this step. Original executables, upstream source, disassembly and extracted assets remain ignored.

## S17: native ordering, save regions and modal continuation (2026-10-16)

- Same S15 unpacked executable. [Native Animate](../rules-audit/dos-travel-ordering.md) links kernel11, cast traversal, vocabulary994 signal ordinal, frozen-clock exclusion and synchronous method invocation to the actual SCI travel loop. [Native save analysis](../rules-audit/dos-save-state.md) traces two serialized intervals and matching decoder destinations, excluding the native PRNG seed. [Stereo fallback](../rules-audit/dos-stereo-fallback.md) follows control type4 and dimension/draw wrappers into the shared cell lookup.
- Their separate artifacts record native range hashes and address conventions. Root cross-checks covered the native instruction paths, kernel pointers, region bounds, vocabulary and resource identities. These are selected DOS-STATIC findings, not executable launch, observed timing, save roundtrip or whole-renderer equivalence.
- [Bank continuation](../rules-audit/bank-refresh-continuation.md) checks3,018 selected instruction spans across five package scripts, extending the prior score inventory through modal housekeeping, Print/BubbleWindow callbacks and Statistics/Goals return. Its normal stale-cache path is BYTECODE analysis; visible score lag remains unobserved.
- Subagents supplied static traces; the parent checked the files and key paths after agent usage-limit errors interrupted final reporting. No original code/assets were committed and no new-game implementation was started.

## S18: inventory grouping, used stock, investments and money boundaries (2026-10-16)

- Same hash-pinned website package and S12 decoder. [Inventory grouping](../rules-audit/inventory-grouping.md) verifies712 selected instruction spans across six resources and selected original native Clone behavior. [Used stock](../rules-audit/pawn-used-stock.md) traces ten selected ranges in scripts212/106, with group capacity, list-time flags and ownership/duplicate resolution.
- [Investment transactions](../rules-audit/investment-transactions.md) identifies all six persistent owned records and separate broker icons, five price setters, selected action/fee/entry branches and fresh bank-local guard defaults. This is package analysis, not a complete loader/refcount or restored-state proof.
- [Money boundaries](../rules-audit/money-word-boundaries.md) identifies the actual32767/32768/32766 constants and signed/unsigned paths in scripts0/115, with selected native arithmetic handlers. Nine finite analytical fixtures were independently checked against the bytecode. The artifact records inputs/results and552 instruction spans; translated helper code stays ignored locally. No universal monetary radix, complete overflow model or observed display outcome is inferred.
- Each note links its input/range metadata and limitations. No application code or original payloads accompany this extension.

## S19: fresh state, ordinary shopping and symbolic indexed stores (2026-10-16)

- Same website package. [Initial-player state](../rules-audit/initial-player-state.md) verifies eight resources, the four resource/progression/score templates, common allocation and selected human/Jones setters. [Clothing](../rules-audit/clothing-lifecycle.md) verifies seven resources, five offers and selected decay/warning/recovery paths. [Fast food](../rules-audit/fast-food-bonuses.md) verifies six records, shared purchase types and two category-latch groups, with bounded direct reset/writer inventory.
- [Z-Mart assortment](../rules-audit/discount-assortment.md) links the actual eighteen-control catalogue, shrinking-list deletion positions, history replay and turn reset. Its metadata identifies selected spans and native indexed-store handler support. These are package/static findings and analytical deletion/reward examples, not measured random distributions or new runtime shopping.
- The indexed-store trace exposed a conservative pseudocode bug: indexed accumulator-destination stores pop the value into the accumulator after computing their target from its old value. Both those forms and indexed stack-destination forms now have tests across four variable spaces. Sixteen fixture groups pass; a complete regeneration leaves53,740 raw instructions and resource hashes unchanged. Generated original code remains ignored. Earlier raw-instruction-based findings do not inherit the old symbolic rendering error.

## Sources not used as proof

Community pages help locate topics, names, and presentation references, but their formulas and edition summaries are not the basis of the script-derived records. In particular, an approximate price formula can conceal integer rounding, the goods subindex, and lower bounds. Where the scripts are surprising, the audit preserves the uncertainty rather than replacing it with a community explanation.

## Reproduction policy

Permanent source links are pinned to revisions. Local source bytes are SHA-256 identified in the metadata. Rule records link the relevant methods/lines. The analytical fixtures validate our arithmetic transcription, not the original executable. Runtime cases are listed separately and remain pending unless explicitly marked observed.
