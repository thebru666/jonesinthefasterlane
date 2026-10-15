# Jones in the Faster Lane

A modern, nearly faithful successor to *Jones in the Fast Lane*: a small-town life strategy game with economic swings, humour, and simple choices that compete for limited time.

**Status:** discovery and planning. No application has been built yet. The repository name is a working title.

The first audit pass now documents [time/actions](docs/rules-audit/time-and-actions.md), [weekly processing](docs/rules-audit/weekly-processing.md), and [economy/edition differences](docs/rules-audit/economy.md). A second pass adds [computer policy](docs/rules-audit/computer-opponent.md), [food/housing](docs/rules-audit/food-and-housing.md) and [goods/finance](docs/rules-audit/goods-and-finance.md). Findings come from inspected published scripts; runtime validation and the remaining systems are tracked explicitly.

Start with the [original-game baseline](docs/original-game/README.md) for how the original was organised: setup, thirteen destinations, screen flow/layout, jobs, courses, progress, saves, and finishing. [Iteration suggestions](docs/planning/follow-up-original-first-iteration.md) are a separate follow-up brief.

The [screen reconstruction studies](docs/original-game/screen-reconstruction.md) rebuild a local gallery of 18 partial composites from decoded artwork and source coordinates. Original assets remain local; these are analytical references, not captured gameplay.

## Start here

- [Documentation index](docs/README.md)
- [Original-game reference](docs/original-game/README.md)
- [Agreed project brief](docs/planning/project-brief.md)
- [Decisions and open questions](docs/planning/decisions.md)
- [Discovery findings and sources](docs/discovery/findings.md)
- [Rules audit](docs/rules-audit/README.md)
- [Discovery artifacts](artifacts/README.md)
- [Rebuild the local original-asset catalogue](docs/discovery/rebuild-original-assets.md)

The intended implementation is a browser game using React and TypeScript, with a separate TypeScript simulation and no application backend initially. Shared-device multiplayer and a computer opponent must inform the design from the start.

## Working approach

1. Investigate the original and document its rules with evidence.
2. Agree what to keep, reskin, or change.
3. Plan the content, visual direction, screens, and architecture.
4. Build a small playable slice of the agreed design, then iterate with family play-testing.

Commit and push each completed, coherent step to this repository. Planning comes before implementation.

Original game archives, executables, extracted assets, and decompiled source are not included. Research evidence in this repository consists of notes, metadata, and inventories. No application licence has been selected yet. The separate research exporters carry GPL-3.0-or-later notices and documented upstream attribution.
