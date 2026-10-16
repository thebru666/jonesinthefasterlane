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

## What belongs here

Original research notes, metadata, inventories, analysis tables, and later original mockups or diagrams. Link artifacts from the relevant findings or rule records and identify how they were produced.

Keep downloaded original game bundles, executables, extracted art/audio, and decompiled source in ignored local research folders. They are not project deliverables and must not be included in commits. `artifacts/private/` and the repository's `work/` directory are ignored for that purpose. Local-only material is not backed up by Git.

The original archive is now also cached under ignored `work/original-assets/source/`. The [portable rebuild guide](../docs/discovery/rebuild-original-assets.md) records its download URL, checksums, dependency versions and exact commands; another computer can regenerate the local catalogue without this machine’s paths.
