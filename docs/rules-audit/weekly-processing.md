# Turn handover and weekly processing

Pass 1, 2026-10-15. Status: partial. Evidence: SCRIPT from the published floppy decompilation, [S02](../discovery/source-register.md). Mapping: **undecided**. No controlled runtime validation in this pass.

## WEEK-001: a week and a player turn are distinct

Players rotate through the active list. The week number advances when play wraps to the next round, with special handling for removed/finished players. Each player gets a separate turn allowance. Economy processing runs from `Player.startTurn`, so it is not a single shared update at the start of a round.

The stored player count used in economic event odds is assigned from the list at initialisation. Whether every later removal path refreshes it has not been audited; do not assume odds automatically change after a player exits.

Evidence: [room1.sc, players.init / doit](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L937); [marble.cue](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L1072); [Player.startTurn](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L730).

## WEEK-002: processing order

The script state machine separates calculation, display, and acknowledgement. The following is the meaningful order for a normal ongoing turn after week 1; numbered states are anchors, not game hours.

| Order | Operation | Script location |
| --- | --- | --- |
| 1 | End previous turn: reduce dependability, recalculate career score, age durable protection flags, process debt/rent bookkeeping | `Player.endTurn` |
| 2 | Select next player; reset time counters; advance week on wrap as applicable | `players.doit`, `marble.cue` |
| 3 | Compute global economy and event flags | `Player.startTurn` → script 107 |
| 4 | Apply selected ownership happiness effect; check completion of all four goals and handle finish flow | `startTrn` states 0–1 |
| 5 | Reset per-turn flags, calculate education bonuses and assets, show/process weekend | state 2 |
| 6 | Resolve lottery tickets | state 2, after weekend |
| 7 | Possible computer ownership income; relaxation decay; possible apartment theft | states 4–7 |
| 8 | Find food coverage; spoil/cap groceries; expire fast food; hunger and possible doctor outcome | states 8–15 |
| 9 | Decrement consumables; fourth-week rent notice | state 16 |
| 10 | Clothing state/warning; fourth-week loan warnings | states 18–20 |
| 11 | Possible durable repair charges | state 22 |
| 12 | Show economic event news and apply active-player event happiness | state 24 |
| 13 | Apply eligible crash employment/bank consequences across unfinished players | states 26–32 |
| 14 | Possible emergency donation | state 34 |
| 15 | Restore normal player controls | state 36 |

Sources: [room1.sc, endTurn](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L739); [startTrn.sc](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L57).

Week 1 jumps over much of the recurring processing after the initial setup/lottery path. The economy is called before that jump: do not skip the whole economy merely because it is week 1.

This ordering has consequences: the economic calculation precedes the weekend, but crash dismissal notices are applied later. A faithful implementation needs ordered state transitions rather than an unordered collection of weekly callbacks.

## WEEK-003: victory is checked at a boundary

The inspected start-turn state tests money, happiness, education, and career against their configured goals, provided the player has not already finished. A recurring ownership happiness increment can occur immediately before this check. The finish flow supports deciding what happens to remaining players.

This establishes a start-turn check, not that it is the only check in the complete game. Full win/finish paths and goal formulas remain a separate audit area.

Evidence: [startTrn.sc, states 0–1](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L79).

## WEEK-004: recurring time penalties

The food pass distinguishes available coverage from spoilage and expiry. Lack of food gives a happiness penalty and a notice whose handler spends **20 hours**. A doctor notice spends **10 hours**, plus its preceding cash and happiness effects. These can consume time before the player regains control.

Doctor eligibility includes cash-on-hand and random checks; it is not simply an unconditional consequence of every missed meal. Food coverage, spoiled food, and minimum relaxation affect the path. A complete probability table and item mapping are still pending.

Evidence: [startTrn.sc, states 8–16](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L328); [moveNotice, state 4](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L967).

## WEEK-005: rent and loans follow a four-week cadence

The recurring notice paths use `week mod 4 == 0`. Rent is not automatically a weekly cash debit: the rent office has explicit payment, extension, and moving controls, while arrears can lead to garnishment at work. End-turn processing records unpaid rent using flags to avoid charging it repeatedly.

The loan path checks a repayment schedule on fourth weeks; end-turn bookkeeping decrements that schedule and counts missed payments. Exact extension conditions, interest, default, and eviction behaviour are not complete in this pass.

Evidence: [startTrn.sc, states 16–20](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L437); [room1.sc, endTurn](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L775); [rentOffice.sc](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/rentOffice.sc#L247).

## WEEK-006: weekend outcomes use possessions and carried cash

Weekend selection checks event tickets, then owned durable opportunities, then a general random-event pool. Spending is capped to cash on hand rather than automatically withdrawing savings. A player with no available cash avoids that cash-spending path. Different outcome groups select different expense ranges; this is not a fixed universal weekend fee.

Evidence: [weekend.sc, localproc_2](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/weekend.sc#L108); [weekend.init](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/weekend.sc#L149); [weekendText.draw](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/weekend.sc#L244).

## Implications for planning

Keep a distinction between round, active player, pre-turn processing, location visit, and handover. A single “end week” function called after every player action would not preserve this behaviour. Presenting notices in a friendly summary may be a useful UI change, but their calculation order should be specified first.

See [validation backlog](validation-backlog.md) for boundary cases and unverified exceptions.
