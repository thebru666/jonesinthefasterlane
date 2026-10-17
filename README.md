# Jones in the Faster Lane

A modern, nearly faithful successor to *Jones in the Fast Lane*: a small-town life strategy game with economic swings, humour, and simple choices that compete for limited time.

**Status:** bounded prototype implementation. The React browser interface, separate TypeScript simulation, local saves and reproducible action traces are working. The repository name is a working title. See the [prototype implementation record](docs/implementation/prototype-v1.md) for current coverage and limits.

The first audit pass now documents [time/actions](docs/rules-audit/time-and-actions.md), [weekly processing](docs/rules-audit/weekly-processing.md), and [economy/edition differences](docs/rules-audit/economy.md). A second pass adds [computer policy](docs/rules-audit/computer-opponent.md), [food/housing](docs/rules-audit/food-and-housing.md) and [goods/finance](docs/rules-audit/goods-and-finance.md). Earlier findings came from inspected published scripts. We now independently decode all 69 actual package scripts and [verify selected logic directly](docs/rules-audit/bytecode-verification.md); semantic coverage remains partial.

Start with the [connected game flow and rules](docs/original-game/game-flow-and-rule-contract.md), then the [original-game baseline](docs/original-game/README.md) for how the original was organised: setup, thirteen destinations, screen flow/layout, jobs, courses, progress, saves, and finishing. [Iteration suggestions](docs/planning/follow-up-original-first-iteration.md) are a separate follow-up brief.

The [screen reconstruction studies](docs/original-game/screen-reconstruction.md) rebuild a local gallery of 18 partial composites from decoded artwork and source coordinates. Original assets remain local; these are analytical references, not captured gameplay.

The direct trace now covers employment, education, ordered turn preparation, computer work/exit dispatch, location entry/return, clock, score refresh and save boundaries. [Build-planning readiness](docs/planning/rules-readiness.md) lists the remaining research and compatibility decisions.

## Run the prototype

Requires Node.js 24.12.0 or later and npm.

```sh
npm ci
npm run check
npm run trace
npm run dev
```

`check` typechecks and tests the simulation; `trace` runs actual opening and campaign actions in the console. Use `npm run trace -- --write` to regenerate [trace artifacts](artifacts/prototype/headless-v1/summary.json). Open the Local URL printed by Vite (normally http://127.0.0.1:5173/). `npm run build` creates the static production bundle; no backend is needed. Seed 42 live fixtures finish through work-first and Trade School → Butcher routes in 9 and 16 game weeks respectively; these are policy-specific reachability examples, not balance or session-length claims.

## Start here

- [Prototype status, API and reproduction](docs/implementation/prototype-v1.md)
- [First-playable baseline](docs/planning/first-playable-scope.md)
- [Documentation index](docs/README.md)
- [Original-game reference](docs/original-game/README.md)
- [Agreed project brief](docs/planning/project-brief.md)
- [Decisions and open questions](docs/planning/decisions.md)
- [Discovery findings and sources](docs/discovery/findings.md)
- [Rules audit](docs/rules-audit/README.md)
- [Discovery artifacts](artifacts/README.md)
- [Rebuild the local original-asset catalogue](docs/discovery/rebuild-original-assets.md)

The implementation is a browser game using React and TypeScript, with a separate TypeScript simulation and no application backend. Shared-device multiplayer and a computer opponent must inform the design from the start.

## Working approach

1. Investigate the original and document its rules with evidence.
2. Agree what to keep, reskin, or change.
3. Plan the content, visual direction, screens, and architecture.
4. Build a small playable slice of the agreed design, then iterate with family play-testing.

Commit and push each completed, coherent step to this repository. The reviewed baseline now authorises the bounded prototype; exact tuning remains adjustable through testing.

Original game archives, executables, extracted assets, and decompiled source are not included. Research evidence in this repository consists of notes, metadata, and inventories. No application licence has been selected yet. The separate research exporters carry GPL-3.0-or-later notices and documented upstream attribution.
