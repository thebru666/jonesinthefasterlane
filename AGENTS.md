# Project instructions

## Scope and workflow

- The owner has authorised the bounded first-playable prototype (D024). Continue within `docs/planning/first-playable-scope.md`; use `docs/implementation/prototype-v1.md` for current implementation status. Do not treat this as permission for full content expansion, public deployment or release.
- Read `docs/planning/project-brief.md` and `docs/planning/decisions.md` before making design decisions.
- Preserve the intended near-original mechanics, simplicity, humour, and economic swings. Mark proposed departures explicitly.
- Commit and push completed, coherent steps to `thebru666/jonesinthefasterlane`, as requested by the user. Check remote changes before pushing; never force-push without explicit authorization.
- Prefer GitHub CLI for GitHub operations. If absent from PATH, check `/home/agent/Documents/Codex/tools/gh`. Never expose credentials.

## Research standards

- Separate verified package facts, script findings, observed behaviour, documentary claims, hypotheses, and design proposals.
- A downloaded archive is not a completed rules audit. Never imply scripts have been decompiled or behaviours tested without evidence.
- Record source URLs, retrieval dates, game versions, and reproducible evidence where available.
- Keep original game bundles, executables, extracted game art/audio, and decompiled source out of commits. Use ignored local research folders for those materials and commit original analytical notes and metadata.
- Update the audit coverage table and open questions when research advances.

## Implementation direction

- React/TypeScript frontend; plain TypeScript simulation separate from rendering.
- Human and computer players use the same action rules.
- Design for shared-device multiplayer, reproducible randomness, and versioned local saves.
- Preserve the separate simulation/presentation boundaries and versioned rules/content. Keep exact prototype tuning editable; distinguish tested implementation coverage from unbuilt UI, later modes and original-game equivalence.
