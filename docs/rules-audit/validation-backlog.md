# Validation backlog and reproduction cases

2026-10-15. All runtime cases below are **pending**, not completed tests. A published-script finding is not automatically an OBSERVED finding.

## Completed analytical checks

- Pinned and SHA-256 identified the downloaded script references and manual.
- Followed time, work, study, pricing, economy, and event handlers into supporting callers.
- Compared floppy/CD economy scripts directly.
- Checked inclusive random bounds and signed division semantics against ScummVM's SCI implementation.
- Recomputed the [arithmetic fixtures](../../artifacts/rules-audit/2026-10-15-arithmetic-fixtures.json) using an independent local calculator. These check our transcription and examples, not runtime equivalence.

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

The current pass addresses time/weekly processing/economy. Complete these before finalising the adaptation:

- All job tables, qualifications, vacancies, rejection memory, promotions, reliability, and career goal calculation.
- Education prerequisites, enrollment capacity, course progress, possession bonuses, and degree effects.
- Item catalogue, durations, happiness, relaxation, duplicates, theft, warranty/repair flags, and pawn values.
- Housing payment, extension, moving, arrears, and garnishment interactions.
- Bank interest, borrowing, repayment, default, investments, and high-value arithmetic.
- All random events, frequencies, ordering, and recovery mechanisms.
- Jones's destination/action policy, setup modes, difficulty, and any asymmetric rules.
- All victory, removal, continued-play, save, and restore paths.

No application implementation is required to resolve these research tasks.
