# Discovery artifacts

Store reproducible evidence that supports documentation and the rules audit here.

## Index

- [2026-10-15 bundle inventory](discovery/2026-10-15-bundle-inventory.json): source URL, retrieval date, archive SHA-256, filenames, uncompressed sizes, and version marker.
- [2026-10-15 audit source metadata](discovery/2026-10-15-audit-sources.json): pinned script revision, per-file hashes, manual identification, and interpreter references. Lists downloaded research inputs; inclusion does not mean every file received a full audit.
- [2026-10-15 arithmetic fixtures](rules-audit/2026-10-15-arithmetic-fixtures.json): derived prices, rounding counterexample, work/garnishment examples, and eligible event probabilities. Analytical checks, not observed gameplay.
- [Original town arrangement](original-game/town-arrangement.svg): analytical schematic, not extracted game art.
- [Original destination inventory](original-game/town-destinations.csv): thirteen destinations, original IDs/path indices/click regions.
- [Original-experience source inputs](original-game/2026-10-15-source-inputs.json): additional pinned script inputs and the original reference-card identification.
- [Packed-resource inventory](original-game/packed-resource-inventory.json): all 299 original map entries, type counts, volume offsets, and matched header IDs; no original payloads included.

- [Decoded-asset metadata](original-game/decoded-asset-summary.json): 266 unique resources, export coverage, hashes and local reference paths; no original payloads.
- [Script-to-asset role hints](original-game/asset-role-hints.json): pinned source references for 53 resources; dynamic selections remain qualified.

- [Screen-study recipes](original-game/screen-study-recipes.json): source-linked layers/coordinates and selected states for 18 analytical composites; no original pixels.
- [Pass 2 source inputs](rules-audit/2026-10-15-pass2-source-inputs.json): 25 pinned source hashes for AI, needs, goods and finance research.
- [AI target-allocation check](rules-audit/ai-goal-allocation-check.json): independent arithmetic coverage and regeneration command linked from AI-001; no runtime claim.

- [Event source inputs](rules-audit/2026-10-15-events-source-inputs.json): 11 pinned source hashes supporting EVENT-001–008; metadata does not establish package-bytecode equivalence.
- [Lottery probability check](rules-audit/lottery-probability-check.json): 1,503 exhaustive integer draw cases, distributions and exact expected-value fractions; [regeneration/check tool](../tools/research/check_lottery_probabilities.py). Analytical arithmetic only, not gameplay or measured odds.

- [Runtime capture manifest](rules-audit/runtime-capture-manifest.json): 48 local viewport captures, hashes and dimensions; observation logs bound the claims and images remain ignored.

- [Bytecode coverage](original-game/bytecode-coverage.json): 69 actual package scripts, input hashes, decoder checks and explicit semantic limits.
- [Bytecode interpreter references](original-game/bytecode-source-inputs.json): pinned engine-source hashes used to interpret the format.
- [Finance verification](rules-audit/bytecode-finance-verification.json) [economy/presentation verification](rules-audit/bytecode-economy-presentation.json), and [purchase verification](rules-audit/bytecode-purchase-verification.json): original analytical conclusions, offsets and resource hashes; no original code.

- [Employment verification](rules-audit/bytecode-employment-verification.json): selected paths and all37 actual job records.
- [Education verification](rules-audit/bytecode-education-verification.json): all11 courses, prerequisites and progression checks.
- [Weekly/opponent verification](rules-audit/bytecode-weekly-opponent-verification.json): methods, resources and bounded branch/call checks.
- [Flow/persistence verification](rules-audit/bytecode-flow-verification.json): all13 entry calls, clock and lifecycle landmarks, scoring/save boundaries.

- [AI action verification](rules-audit/bytecode-ai-actions-verification.json): all14 destination/broker controller entries, shared dispatch and selected confirmation branches.
- [Needs/event verification](rules-audit/bytecode-needs-events-verification.json): selected condition/amount/order checks and raw landmarks.

- [DOS interpreter unpack record](original-game/dos-interpreter-unpack.json): source pins, packed/unpacked hashes, MZ facts and repeat-unpack check; no executable payload.
- [Economy frame verification](rules-audit/economy-frame-verification.json): script CFG/stack ledger and original DOS handler/relocation checks.
- [DOS randomness verification](rules-audit/dos-randomness-verification.json): selected native-range hashes, seed/output/scaling findings and limits.
- [Travel timing verification](rules-audit/travel-timing-verification.json): conditional engine inputs, route-step matrix and 25,500 analytical cases.
- [Score refresh verification](rules-audit/score-refresh-verification.json): bounded whole-package caller/writer inventory and selected paths.
- [Finance lifecycle verification](rules-audit/bytecode-finance-lifecycle-verification.json): package paths and bounded setter inventory for rent, pawns and loans.

- [Native travel ordering](rules-audit/dos-travel-ordering-verification.json): original Animate spans, signal vocabulary and script join points.
- [Bank continuation](rules-audit/bank-refresh-continuation.json): selected modal, notice, menu and bank method range hashes.
- [Native save regions](rules-audit/dos-save-state-verification.json): fixed/heap serialization, matching restore destinations and PRNG seed exclusion.
- [Native stereo fallback](rules-audit/dos-stereo-fallback-verification.json): relocated kernel pointers, control type4 path and shared cell lookup range hashes.

- [Inventory grouping verification](rules-audit/inventory-grouping-verification.json): six payload hashes, selected receipt/pack/purchase/repair spans and normal native Clone confirmation.
- [Pawn used-stock verification](rules-audit/pawn-used-stock-verification.json): capacity, list-time quality writes and ownership/duplicate branches.
- [Investment transaction verification](rules-audit/investment-transactions-verification.json): six owned/icon records, market price setters, fee and broker-entry lifecycle.
- [Money boundary fixtures](rules-audit/money-word-boundaries.json): selected helper/native hashes and nine analytical outputs; original helper transcription is ignored.

- [Initial-player verification](rules-audit/initial-player-state-verification.json): eight resources, four default-instance comparisons and selected allocation/setup paths.
- [Clothing lifecycle verification](rules-audit/clothing-lifecycle-verification.json): five offers, shared records, decay/dressing/warning and support-counter paths.
- [Fast-food verification](rules-audit/fast-food-bonuses-verification.json): six product records, four reward overrides and direct latch reset/setter inventory.
- [Z-Mart assortment verification](rules-audit/discount-assortment-verification.json): eighteen candidates, twelve deletion-position draws, same-turn replay, reset inventory and native indexed-store support.

## What belongs here

Original research notes, metadata, inventories, analysis tables, and later original mockups or diagrams. Link artifacts from the relevant findings or rule records and identify how they were produced.

Keep downloaded original game bundles, executables, extracted art/audio, and decompiled source in ignored local research folders. They are not project deliverables and must not be included in commits. `artifacts/private/` and the repository's `work/` directory are ignored for that purpose. Local-only material is not backed up by Git.

The original archive is now also cached under ignored `work/original-assets/source/`. The [portable rebuild guide](../docs/discovery/rebuild-original-assets.md) records its download URL, checksums, dependency versions and exact commands; another computer can regenerate the local catalogue without this machine’s paths.
