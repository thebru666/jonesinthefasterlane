# Decisions and open questions

Last updated: 2026-10-17.

## Confirmed direction

| ID | Decision | Basis |
| --- | --- | --- |
| D001 | Plan substantially before building the application | Explicit owner instruction |
| D002 | Stay nearly identical in core gameplay | Owner preference |
| D003 | Preserve economic swings, humour, and simplicity | Owner's essential surviving factors |
| D004 | Use a small US-style town with restrained Australian flavour | Owner preference |
| D005 | Plan for shared-device multiplayer and a computer opponent | Owner preference |
| D006 | Include ages 8 and 11 in play-testing while allowing a broader audience and possible public release | Owner context |
| D007 | Preserve the original visual feel; explore illustrated retro | Owner preference; specific style pending |
| D008 | Use this repository for planning, discovery evidence, audit, and later code; commit and push completed steps | Explicit owner instruction |
| D009 | Document the existing game's flow, layout, and content first; iterate from that reference, with suggestions kept in a separate follow-up | Explicit owner instruction after the consistency review |
| D010 | Keep original assets local and ignored; commit source provenance, reproducible export tools and analytical metadata so the reference can be rebuilt elsewhere | Explicit owner instruction during asset discovery |
| D011 | Expand transport as a planning direction: slower walking, buying a bike, bus travel and driving, with time/cost tradeoffs | Explicit owner pointers2026-10-17; formulas/prices not approved |
| D012 | Explore newer locations, different job boards and modern devices, plus further suggestions | Explicit owner pointers2026-10-17; exact destinations/jobs/effects not approved |
| D013 | Pursue a planning goal through modern content direction and visual iteration before settling the first playable scope and starting implementation | Explicit owner goal request2026-10-17; final instruction targets step3 |

## Proposed technical and design choices

Current entry point: [modern-direction review pack](modern-direction-review.md), with [transport](transport-proposal.md), [town/content](modern-town-and-content.md) and [visual concepts](visual-direction-v1.md). It explicitly revises the earlier fixed-speed travel and agency-only planning baseline. New directions D011–D013 do not approve its specific recommendations.

The [2.0 draft specification](2.0-draft-specification.md), [compatibility proposals](compatibility-proposals.md), [content sample](content-iteration-sample.md) and [architecture proposal](architecture-and-validation-proposal.md) now make these choices concrete for review. They add no confirmed decision. In particular, floppy-only reference, original mode combinations, desktop/tablet priority and C01–C17 are recommendations, not owner approvals.

| Proposal | Status / reason |
| --- | --- |
| React + TypeScript + Vite, with simulation outside UI components | Supported direction; detailed architecture pending |
| Static frontend with local saves | Matches initial scope; persistence design pending |
| Human and computer players share legal actions and costs | Recommended for consistent rules and testability |
| Seeded random generator and versioned saves | Recommended for reproducibility and future compatibility |
| Four familiar life goals | Proposed; confirm exact definitions after audit |
| Short-game option targeting 30–45 minutes | Proposed; no agreed session target |
| Clear explanations with an optional gentler starting setup | Proposed; difficulty design pending |
| Modern content before new meters or subsystems | Recommended to preserve simplicity |

## Discovery questions and current status

Pass 1 has produced [specific implications and recommendations](audit-implications.md). No new adaptation decision has been approved by that research alone.

- Which original release is the behavioural reference? The inspected website bundle identifies version 1.000.060; other editions may differ.
- How does the original economy change, and how are wages, prices, jobs, and events connected to it?
- Which awkward behaviours are intentional, which are bugs, and which should the adaptation preserve?
- The [opponent audit](../rules-audit/computer-opponent.md) now traces priorities, goal-based difficulty and privileged market inputs. Runtime confirmation and the adaptation's information/difficulty policy remain open.
- How much information should other players see during shared-device play?
- Should the new game use floppy or CD economy recovery/timing, given the documented script differences?
- After reproduction, should the duplicated economic adjustment condition and partial-shift garnishment behaviour be fixed or preserved?

The [completed research handoff](original-research-handoff.md) now supplies the connected flow, economic relationships and evidence limits requested above. The remaining edition, compatibility and opponent questions are adaptation choices; the [compatibility table](compatibility-proposals.md) recommends specific answers without adopting them. Earlier pass-readiness sections below remain a historical progress record rather than the current summary of research coverage.

## Questions to resolve before implementation

- Desktop/tablet priority versus equally supported phones; board layout at small sizes.
- Player counts, human/computer combinations, opponent difficulty, and handover flow.
- Victory conditions, configurable goals, expected session length, and recovery from setbacks.
- Complete town map and content scope; education prerequisites and career progression.
- Art samples, animation scope, audio direction, and reading/accessibility requirements.
- Naming, project licence, and intended public release scope.
- Architecture, save format, and rules-version policy.

These are a planning backlog, not a request for the owner to answer everything immediately. Research should resolve what it can before asking for choices.

## Flow and layout readiness

The earlier [consistency review](consistency-review.md) identified missing player-facing documentation. The subsequent [original-game baseline](../original-game/README.md) now describes those structures from original material and published scripts. Use it before the historical [speculative outline](flow-and-layout-outline.md). The [follow-up brief](follow-up-original-first-iteration.md) contains suggestions only; it does not approve new setup combinations, handover/privacy screens, placement changes, or game actions.

The original's supported setup is now documented: one to four humans, with optional Jones only in the one-human path. Whether the adaptation should offer broader combinations remains an adaptation choice. Course/job catalogues, screen families, saved-game interface, and finish handling now have original references; runtime and graphical transcription gaps remain explicit.

## Pass 2 readiness

[Screen studies](../original-game/screen-reconstruction.md) now give a source-linked visual composition reference. [Food/housing](../rules-audit/food-and-housing.md), [goods/finance](../rules-audit/goods-and-finance.md) and [opponent](../rules-audit/computer-opponent.md) have detailed script-based rules and pending reproduction scenarios. These strengthen the original baseline without approving application implementation or new mechanics. Complete runtime presentation, remaining event/content branches and compatibility choices remain gates before a final specification.

## Research priority after the first runtime pass

On 2026-10-16 the owner questioned further manual gameplay and asked how much could be reverse engineered. Prioritise verification of the extracted package bytecode against published decompiled scripts, starting with suspicious conditions and source/resource discrepancies. Use runtime only for narrow unresolved experiments. This does not approve application implementation or choose new mechanics.

## Core-loop research progress (2026-10-16)

The owner explicitly assigned the objective of extracting/documenting game flow and rules ready for2.0 planning. [Connected flow](../original-game/game-flow-and-rule-contract.md) now joins package-verified employment, education, weekly dispatch, selected AI execution, entry/clock, score-refresh and save/finish boundaries. [Rules readiness](rules-readiness.md) records unresolved research and compatibility choices. This advances discovery, not approval to build or silently repair quirks.


## Interpreter and lifecycle follow-up (2026-10-16)

Original DOS static inspection now resolves the main economy's omitted argument and identifies its random generator/bound scaling. Conditional travel timing, the bounded score-refresh inventory, and rent/pawn/loan lifecycles are documented in [rules readiness](rules-readiness.md). These findings strengthen the original reference; preserving/fixing quirks and choosing a modern timing/randomness contract remain owner decisions. No implementation is approved by this audit.
