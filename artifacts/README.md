# Discovery artifacts

Store reproducible evidence that supports documentation and the rules audit here.

## Index

- [2026-10-15 bundle inventory](discovery/2026-10-15-bundle-inventory.json): source URL, retrieval date, archive SHA-256, filenames, uncompressed sizes, and version marker.
- [2026-10-15 audit source metadata](discovery/2026-10-15-audit-sources.json): pinned script revision, per-file hashes, manual identification, and interpreter references. Lists downloaded research inputs; inclusion does not mean every file received a full audit.
- [2026-10-15 arithmetic fixtures](rules-audit/2026-10-15-arithmetic-fixtures.json): derived prices, rounding counterexample, work/garnishment examples, and eligible event probabilities. Analytical checks, not observed gameplay.

## What belongs here

Original research notes, metadata, inventories, analysis tables, and later original mockups or diagrams. Link artifacts from the relevant findings or rule records and identify how they were produced.

Keep downloaded original game bundles, executables, extracted art/audio, and decompiled source in ignored local research folders. They are not project deliverables and must not be included in commits. `artifacts/private/` and the repository's `work/` directory are ignored for that purpose. Local-only material is not backed up by Git.

The initial bundle was retrieved during the preceding discovery conversation and remains outside the repository in the chat workspace's `work/jones-research/` directory. The committed inventory is sufficient to identify the inspected bytes; it does not include those bytes.
