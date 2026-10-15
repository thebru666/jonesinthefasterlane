# Decisions and open questions

Last updated: 2026-10-15.

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

## Proposed technical and design choices

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

## Questions to resolve during discovery

Pass 1 has produced [specific implications and recommendations](audit-implications.md). No new adaptation decision has been approved by that research alone.

- Which original release is the behavioural reference? The inspected website bundle identifies version 1.000.060; other editions may differ.
- How does the original economy change, and how are wages, prices, jobs, and events connected to it?
- Which awkward behaviours are intentional, which are bugs, and which should the adaptation preserve?
- The [opponent audit](../rules-audit/computer-opponent.md) now traces priorities, goal-based difficulty and privileged market inputs. Runtime confirmation and the adaptation's information/difficulty policy remain open.
- How much information should other players see during shared-device play?
- Should the new game use floppy or CD economy recovery/timing, given the documented script differences?
- After reproduction, should the duplicated economic adjustment condition and partial-shift garnishment behaviour be fixed or preserved?

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
