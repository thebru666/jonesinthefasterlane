# Validation backlog and reproduction cases

Updated 2026-10-16. Most prescribed runtime cases remain pending. The [multiplayer observations](runtime-observations.md) and [solo control](runtime-solo-control.md) now establish bounded visible results for some variants; they do not fully pass every component of the cases below. A published-script finding is not automatically an OBSERVED finding.

Subsequent original-experience research documents the [setup/layout/content/progress baseline](../original-game/README.md). That resolves many catalogue and normal-path questions below, while their formula/edge-case/runtime work remains open.

## Direct bytecode progress

All 69 website scripts have been independently decoded; [coverage and limits](bytecode-verification.md). Actual bytes confirm the garnishment overwrite, double initial-loan happiness penalty, $50/$45 repayment duplicate economic comparison, and the ordinary refrigerator purchase bonus being skipped. These branch-existence questions no longer require ordinary gameplay. Visible presentation and remaining semantics still have their own evidence requirements. The [original DOS frame trace](economy-frame-semantics.md) subsequently resolves the main omitted argument to the preceding initialization's target draw; the guarded zero is a different stack word.

## Core loop package traces

[Employment](employment.md), [education](education.md), [weekly/opponent](bytecode-weekly-opponent.md) and [location/clock/save](bytecode-flow-and-persistence.md) now directly trace the normal core loop. All37 job records, all11 course records and all13 entry charges are package-checked. Ordinary hiring/raise/study flow no longer depends solely on published-source interpretation. [Connected flow](../original-game/game-flow-and-rule-contract.md) and [readiness](../planning/rules-readiness.md) record what can guide the build and what remains open.

[All-destination AI dispatch](bytecode-ai-actions.md) and [selected needs/event predicates](bytecode-needs-events.md) have since been package-checked. The weekend redraw debit is confirmed in bytes, while ordinary redraw reachability remains open.

Follow-up checks now cover [conditional travel timing](travel-timing.md), [bounded score writer/caller inventory](score-refresh.md), [finance lifecycles](finance-lifecycle.md) and the [native DOS random generator/scaling](dos-randomness.md). The [native update ordering](dos-travel-ordering.md), [ordinary bank continuation](bank-refresh-continuation.md), [native save regions/RNG exclusion](dos-save-state.md) and [stereo fallback](dos-stereo-fallback.md) now have selected static traces. Further work: interrupted travel, visible bank/message/Statistics corroboration, complete RNG initialization/call order/post-restore interaction, remaining event/high-word arithmetic, remaining AI policy/dynamic consumers and saved intermediate states. This does not mark their runtime cases passed.

## Inventory and trading extension

[Grouping/packing](inventory-grouping.md), [pawn used stock](pawn-used-stock.md) and [investment transactions](investment-transactions.md) now verify selected ordinary transaction rules against actual package resources. The nine [money boundary fixtures](money-word-boundaries.md) identify concrete cash/pair/formatter differences, with native signed/unsigned arithmetic support. Remaining work is full high-word valuation and observed edge behavior, not merely locating those constants or the used-stock ownership branches.

## Fresh state and ordinary shopping

The [initial player snapshot](initial-player-state.md), [clothing cadence/rewards](clothing-lifecycle.md), [food/drink category bonuses](fast-food-bonuses.md) and [Z-Mart stock lifecycle](discount-assortment.md) now have bounded package traces. They close normal initialization, repeated-purchase and revisit/reset questions; exact visible messages and arbitrary restored states remain separate. The decoder's symbolic indexed-store fix is covered by targeted regression cases; raw disassembly is unchanged.

## Runtime progress

| Area | Actual progress | Still pending |
| --- | --- | --- |
| Setup / W01 | Two-human targets inherited, appearance dimmed, player2 starts with independent cash200 and clear clock; week1 retained through first handover | Solo Jones difficulties, full rotation/finish/removal edge paths and any refused reselection |
| FIN-001 | Deposits148→48→0 with savings148; separate control200→100→0 with savings200 | Withdrawals and large balances |
| Food / T01 / RT02–03 | Groceries/no-fridge run clear week2 clock; no-food control roughly one-third red; zero carried cash and savings unchanged in both | Exact internal hours, timed notice/happiness capture, illness gate/odds and full prescribed variants |
| Employment / work | Entry-level offer, success feedback, wage3/full pay24, last pay4 and exhausted-time refusal captured in the multiplayer continuation | All hiring boundaries, independently measured residual hours/rounding and garnishment |

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

## Pass 3 analytical checks

- [EVENT-001–008](random-events.md) traced against [11 pinned source inputs](../../artifacts/rules-audit/2026-10-15-events-source-inputs.json), with peer review of probability/ordering claims.
- [Lottery arithmetic checker](../../tools/research/check_lottery_probabilities.py): 1,503 exhaustive integer draw cases across quantities 10, 20 and 100, checked against [tracked distributions and expectations](../../artifacts/rules-audit/lottery-probability-check.json). This checks formula transcription; no runtime execution or measured random frequency is implied.
- [Practical runtime plan](runtime-test-plan.md): prioritised ordinary-play setup, hunger/spoilage, handover, work, loan and durable-purchase cases; precise debugger/prepared-save cases remain separate. All prescribed variants remain pending until actual setup and results are recorded.

## Domain-specific reproduction cases

| Domain | Pending cases | Coverage |
| --- | --- | --- |
| Opponent | [AI-R01–12](computer-opponent.md#reproduction-backlog-and-limits) | Goal allocation, priority, time/cash estimates, confirmations, privileged market inputs, jobs/study and demo/edition differences |
| Food and housing | [14 scenarios](food-and-housing.md#pending-runtime-scenarios-and-gaps) | Mixed food/storage/spoilage, illness cash gates, extensions, arrears, moving and rest |
| Goods and finance | [Nine scenario groups](goods-and-finance.md#validation-cases-and-remaining-boundaries) | Purchase happiness, grouped ownership, repairs/pawn, loan schedules/fees, trades and large balances |
| Personal events | [Focused reproduction backlog](random-events.md#focused-reproduction-backlog) | Weekend priority/redraw, lottery boundaries, mugging entry/exit, joke effects, computer income and recovery; SCRIPT only |
| Presentation | [Capture list](../original-game/screen-reconstruction.md#validation-and-next-evidence) | Text, palette, focus, borders, animation and screen-return equivalence |

These extend the original cases below. Separate observation logs identify which visible components have actually been observed; the full scenario groups remain open.

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
| E06 | Inspect bytecode for duplicated adjustment condition and omitted parent argument | Duplicate condition confirmed; selected original DOS frame trace resolves omitted argument to preceding target draw. Preserve/change decision still open |
| E07 | Validate formulas, then simulate many seeds for both editions and player counts | Measure recovery, slump duration, price distribution, and event exposure |

## Subsequent audit domains

The ordinary baseline now has detailed source findings and linked package traces. The [handoff review](../planning/original-research-handoff.md) records planning readiness; the following list retains fidelity work without implying these domains are still undocumented:

- [All37 jobs](employment.md) and [all11 courses](education.md) are catalogued with selected package predicates/order. Remaining work is visible boundary feedback, untraced callers and extreme/restored state, rather than an absent progression graph.
- [Goods/inventory](inventory-grouping.md), [used stock](pawn-used-stock.md), [clothing cadence](clothing-lifecycle.md), [food bonuses](fast-food-bonuses.md), [assortment](discount-assortment.md) and [Happiness](happiness-catalogue.md) now cover ordinary purchases, repeatability and lifecycle. Retain focused runtime/object-identity checks where a fidelity decision needs them.
- Housing, rent/loan lifecycle, bank continuation and investment trading now have selected package traces. Remaining questions concern unusual balances, callbacks, restored flow and visible notices; the money-boundary notes do not claim a complete overflow model.
- Personal events, economic shocks, illness/theft/repairs and weekend/lottery effects have domain records and selected package checks. Full random-call replay, measured native frequencies, exhaustive flavour/animation and edition equivalence remain separate.
- Jones's source-based priorities and actual destination dispatch are documented; full arithmetic, fallback, demo/CD and win-rate comparisons are not established.
- Ordinary victory/removal/continue/save boundaries are documented. Native save regions and RNG exclusion are traced; every intermediate restore state and browser persistence are not proved.

No application implementation is required by this research backlog. The next planning task selects inherited rules and explicit departures; it should request additional evidence where a decision depends on one of these limits.
