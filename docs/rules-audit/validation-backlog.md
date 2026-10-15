# Validation backlog and reproduction cases

2026-10-15. All runtime cases below are **pending**, not completed tests. A published-script finding is not automatically an OBSERVED finding.

Subsequent original-experience research documents the [setup/layout/content/progress baseline](../original-game/README.md). That resolves many catalogue and normal-path questions below, while their formula/edge-case/runtime work remains open.

## Completed analytical checks

- Pinned and SHA-256 identified the downloaded script references and manual.
- Followed time, work, study, pricing, economy, and event handlers into supporting callers.
- Compared floppy/CD economy scripts directly.
- Checked inclusive random bounds and signed division semantics against ScummVM's SCI implementation.
- Recomputed the [arithmetic fixtures](../../artifacts/rules-audit/2026-10-15-arithmetic-fixtures.json) using an independent local calculator. These check our transcription and examples, not runtime equivalence.

## Pass 2 analytical and visual checks

- Peer-reviewed AI difficulty and shared-rule/information claims, food/housing source coordinates and finance anomalies against pinned sources.
- [AI goal allocation checker](../../tools/research/check_ai_goal_allocation.py): 30,000 configurations, 712,183 permitted draw pairs; no invalid interval or redistribution-capacity failures. This is arithmetic, not original execution or measured random frequencies.
- [Screen-study recipes](../../artifacts/original-game/screen-study-recipes.json): explicit coordinates/defaults reviewed against sources, all 21 recorded script hashes matched, all selected cels resolved; repeated local exports compared exactly.

## Domain-specific reproduction cases

| Domain | Pending cases | Coverage |
| --- | --- | --- |
| Opponent | [AI-R01–12](computer-opponent.md#reproduction-backlog-and-limits) | Goal allocation, priority, time/cash estimates, confirmations, privileged market inputs, jobs/study and demo/edition differences |
| Food and housing | [14 scenarios](food-and-housing.md#pending-runtime-scenarios-and-gaps) | Mixed food/storage/spoilage, illness cash gates, extensions, arrears, moving and rest |
| Goods and finance | [Nine scenario groups](goods-and-finance.md#validation-cases-and-remaining-boundaries) | Purchase happiness, grouped ownership, repairs/pawn, loan schedules/fees, trades and large balances |
| Presentation | [Capture list](../original-game/screen-reconstruction.md#validation-and-next-evidence) | Text, palette, focus, borders, animation and screen-return equivalence |

These extend the original cases below; none is marked OBSERVED.

## Runtime protocol

Use the [identified website bundle](../../artifacts/discovery/2026-10-15-bundle-inventory.json). Record player setup, game/week, starting state, exact actions, clock and money before/after, and the observed result. Retain local saves with hashes where possible. Record screenshots only where useful, following the repository's original-asset policy. If setup requires a debugger or modified save, say so explicitly and keep that separate from ordinary-play observations.

Economy experiments should compare outcomes from controlled states; naturally different random sequences are not proof of a formula error. Do not claim statistically measured odds from a handful of turns.

## Cases

| ID | Setup and action | Script-derived expectation / question |
| --- | --- | --- |
| T01 | Start a normal turn, then a turn after missed food | 60-hour allowance; hunger notice spends 20 hours |
| T02 | At an employed shop workplace with stock available and enough cash, reach spent time 59, work a shift, then try an ordinary purchase and exit | Clock caps at 60; eligible free purchase can still resolve; exit hands over |
| T03 | At an employed workplace with no arrears, compare shifts with 6, 3, 1, and 0 hours remaining | Full/proportional/refused work per TIME-005 |
| T04 | Study an enrolled unfinished course with one hour left | One normal progress increment, then clock at 60 |
| T05 | Fail a job application with one hour left | Attempt consumes the remaining time and still resolves |
| T06 | Repeat T03 with $10/hour wage, one hour left, and rent debts $10, $40, $100 | Reproduce or refute the full-shift garnishment overwrite and equality boundary |
| T07 | Enter bank; open/close broker repeatedly; re-enter bank; repeat at zero time | Establish local-flag lifetime and repeated broker charge behaviour |
| T08 | Travel a measured route; interrupt/re-target; repeat at different game speeds | Determine cost matrix, fractional carry, and speed independence |
| W01 | Two humans, then human plus Jones; advance a full round | Confirm turn order, week wrap, separate economy updates |
| W02 | Approach a fourth-week boundary with unpaid rent and a loan | Confirm notice/payment timing, extensions, late bookkeeping |
| W03 | Hold qualifying goals at turn end, then experience pre-turn events | Establish all win-check timing and any stale-score interactions |
| W04 | Compare a funded bank account with $0 carried cash to carried cash and no savings | Confirm weekend and doctor cash gates without treating savings as cash |
| W05 | Finish/remove a player during a multiplayer game | Verify economic player-count refresh and wrap handling |
| E01 | Track one ordinary item and the $50-base enrollment fee across turns | Match shared factor and split rounding against known goods reading |
| E02 | Keep job and apartment while offers change; then ask for raise or move | Existing wage/rent stay stored; new contracts use current offers |
| E03 | Controlled main readings around 80/120 and weeks 3/4/7/8 in each edition | Validate event eligibility and crash-before-boom short-circuit |
| E04 | Force/locate each crash code in multiplayer | Verify reading changes, cross-player dismissal/pay cuts, and happiness recipients |
| E05 | Severe crash with bank balances below and above 32,767 | Check high-word behaviour before describing loss as all savings |
| E06 | Inspect bytecode for duplicated adjustment condition and omitted parent argument | Confirm decompilation interpretation before any bug-compatibility decision |
| E07 | Validate formulas, then simulate many seeds for both editions and player counts | Measure recovery, slump duration, price distribution, and event exposure |

## Subsequent audit domains

Two script passes and the screen studies provide normal-path coverage; finish the remaining evidence before finalising adaptation:

- All job tables, qualifications, vacancies, rejection memory, promotions, reliability, and career goal calculation.
- Education prerequisites, enrollment capacity, course progress, possession bonuses, and degree effects.
- Runtime/object-lifetime validation for [goods/repairs/pawn](goods-and-finance.md); complete ticket/weekend, clothing and joke-product effects.
- Runtime validation of [housing payment, extension, moving, arrears and garnishment](food-and-housing.md); remaining notice/edge interactions.
- Reproduce [bank/loan/investment findings](goods-and-finance.md), resolve high-value arithmetic and inspect remaining default/event paths.
- All random events, frequencies, ordering, and recovery mechanisms.
- Reproduce [Jones's policy and information differences](computer-opponent.md); finish demo/CD and exhaustive privilege comparison.
- All victory, removal, continued-play, save, and restore paths.

No application implementation is required to resolve these research tasks.
