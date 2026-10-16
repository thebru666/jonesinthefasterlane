# Time, movement, and action boundaries

Pass 1, 2026-10-15. Evidence: SCRIPT via [S02](../discovery/source-register.md), with TIME-006 now independently verified in website package bytecode. Runtime coverage remains limited to the separately recorded observations. Status: partial. Adaptation mapping for every rule below: **undecided**, with preservation recommendations identified separately.

Source links below use the published floppy-version decompilation at pinned revision `870a8015b689474484bf3d8b41416956d4315432`.

## TIME-001: turn allowance and clock

The clock counts **time spent**, from 0 to 60. Explicit action costs add to that counter and are capped at 60. Travel also accumulates a fractional counter, periodically advancing the displayed clock.

The counters reset during turn handover. Start-of-turn penalties then consume some of the allowance. These are abstract game hours, not a literal model of all 168 hours in a week.

Evidence: [room1.sc, marble.cue](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L1072); [timeKeep.doit](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L1460).

## TIME-002: reaching 60 is not always an immediate handover

Time can run out while a player is inside a location. The examined handlers reject further work, study, and job applications when the spent counter is already 60. The player can still complete time-free operations permitted by that location, such as an affordable ordinary purchase or deposit. Leaving the location then advances to the next player.

If time runs out while the marble is moving, the clock triggers the handover path. It is possible to spend the last time travelling without receiving a normal visit at the intended destination.

Evidence: [room1.sc, proc1_9 and Place.endCue](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L50); [timeKeep.doit](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L1509); [WButton.sc, CostDItem.doit](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/WButton.sc#L197); [bank.sc, deposit handler](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/bank.sc#L214).

Do not generalise this to every control: some actions impose their own clock checks.

## TIME-003: short remaining time permits an action to finish

Most examined timed actions require **some** time remaining, not their full nominal cost. Adding the cost clamps the clock at 60. The effects differ by action:

| Action | Nominal time | Effect with fewer hours remaining |
| --- | --- | --- |
| Work | 6 | Pay is prorated, except for the garnishment anomaly in TIME-006 |
| Study | 6 | One study increment is still awarded; no proportional reduction |
| Apply for job / raise | 4 | Application still resolves, including failure |
| Apply for loan | 2 | Application resolves; handler charges time before eligibility outcome |

Evidence: [n108.sc, localproc_0](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/n108.sc#L100); [university.sc, UniversityDIcon.doit](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/university.sc#L202); [employment.sc, JobDItem.doit](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/employment.sc#L206); [bank.sc, applyForLoan.doit](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/bank.sc#L445).

This makes the order of the last actions in a week strategically significant. Requiring full remaining time in the new game would be a mechanical change.

## TIME-004: travel and entry are separate costs

The marble follows a 170-point ring and selects the shorter route around it. The clock advances during motion using a fractional counter and a threshold related to marble speed. Explicit costs do not clear the fractional travel counter.

The examined bank, fast-food restaurant, university, and rent office entry handlers each charge 2 hours. This is additional to travel. Re-entering a location calls its entry handler again. A complete location-by-location inventory and an exact travel cost matrix remain pending; do not hardcode a community estimate of board-crossing time.

Evidence: [marblePath.sc, MarblePath](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/marblePath.sc#L16); [room1.sc, clock and speed threshold](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L1315); location `init` methods in [bank.sc](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/bank.sc#L77), [fastFood.sc](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/fastFood.sc#L137), [university.sc](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/university.sc#L370), [rentOffice.sc](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/rentOffice.sc#L84).

## TIME-005: work has two different time scales

A successful standard work action consumes 6 game hours and pays **8 times the displayed hourly wage**. With `h` hours remaining below 6 and no rent arrears, pay is `trunc(8 × wage × h / 6)`. At wage $10: 6 remaining pays $80, 3 pays $40, 1 pays $13. At zero remaining, work is refused.

Work also increases experience and dependability up to limits. Clothing and work-history checks can refuse work or dismiss the player before the successful shift path. A short successful shift still takes the normal experience/dependability increment rather than a fraction of it.

Evidence: [n108.sc, proc108_0 and localproc_0](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/n108.sc#L17).

<a id="time-006-rent-garnishment-appears-to-overwrite-partial-shift-pay"></a>

## TIME-006: rent garnishment overwrites partial-shift pay

The work helper first computes partial pay, but its arrears branch then replaces that amount using **full-shift pay**:

- Let `F = 8 × wage` and `D = rentOwed`.
- If `trunc(F/2) > D`, cash awarded becomes `F − D` and the debt clears.
- Otherwise, cash awarded becomes `trunc(F/2) − 2`, and debt reduces by `trunc(F/2)`.

The website package bytecode confirms that a $10/hour worker with one hour remaining and $10 rent debt receives $70 and clears the debt, instead of receiving a garnished share of the $13 partial shift. Equality takes the second branch, including its $2 reduction.

Evidence: [n108.sc, localproc_0, lines 127–172](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/n108.sc#L127).

**Confirmed package implementation quirk; visible runtime feedback remains untested for the precision cases.** [BC-FIN-001](bytecode-finance-findings.md#bc-fin-001-garnishment-really-overwrites-partial-shift-pay) records the payload hash, untouched full-pay temporary, branch offsets and final cash-helper call. This is no longer merely a possible published-decompilation error. Do not silently copy or fix it; preservation versus correction remains an adaptation decision.

## TIME-007: repeated broker visits have a special rule

The bank's broker button charges 2 hours only when its local visit flag is unset, then sets that flag. Subsequent openings during the same bank visit do not take that branch. At a fully exhausted clock, the button refuses access. Verify flag reset and re-entry behaviour at runtime before treating every broker opening as a fresh two-hour action.

Evidence: [bank.sc, seeBroker.doit](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/bank.sc#L591).

## Validation and adaptation implications

Preservation candidates: 60-hour turns, travel plus entry costs, short final actions, and time-free final transactions. These are recommendations, not approved adaptation decisions.

Runtime cases T01–T08 are in the [validation backlog](validation-backlog.md). This pass checks script paths and analytical examples; it does not claim observed results for those scenarios.
