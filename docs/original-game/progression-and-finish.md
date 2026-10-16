# Original game: goals, progress, statistics, and finishing

Research date: 2026-10-15. Reference: DOS floppy **1.000.060**. Mechanical findings are **SCRIPT: published decompilation inspected**, without runtime verification by the author of this pass. See the [source register](../discovery/source-register.md). This is the original baseline, not a redesign.

Later direct-package traces confirm [stored-score refresh and placement allocation](../rules-audit/bytecode-flow-and-persistence.md) plus [two ordered start-turn goal gates](../rules-audit/bytecode-weekly-opponent.md). The formulas below describe ordinary values; full refresh-caller/high-word behaviour and restored intermediate states remain unresolved.

## Goal meanings

The player must reach **all four personal targets**. One filled category cannot compensate for another. The game's help describes accumulating money/investments, enjoying purchases and leisure, graduating, and improving working life, delivered with brief jokes. [Original definitions](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/goalsDefine.sc#L18). See [setup](setup-multiplayer.md) for configurable individual thresholds.

| Goal | Inspected scoring | Implication |
| --- | --- | --- |
| Wealth | Liquid assets divided by $100, bounded to 0–100. Liquid assets include cash, savings, Treasury bills and market-valued investments, less rent owed and loans. | A 50-point target corresponds to $5,000 in this measure, subject to score-refresh timing. |
| Happiness | Accumulated score bounded to 0–100, modified by actions and events. | Purchases, leisure, achievements and setbacks contribute; the complete modifier catalogue remains pending. |
| Education | On graduation, `1 + 9 × completed degrees`; initial stored score is zero. | First completion gives 10, second 19; a 50-point target needs six completions (55). |
| Career | If employed: `10 × floor(dependability / 8)`, capped at 100; otherwise zero. Updated by work, hiring and end-turn paths. | Wage/title alone does not set this meter; weekly dependability loss can reduce it. |

Sources: [wealth score](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/Main.sc#L1038), [liquid assets](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L852), [happiness bounds](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/Main.sc#L1100), [education](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/university.sc#L270), [career after work](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/n108.sc#L114), [career at turn end](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L740).

**Documentary discrepancy:** the [©1992 reference card](https://www.sierragamers.com/wp-content/uploads/2019/12/Jones_In_The_Fast_Lane_Reference_Card.pdf) describes money points in terms of net worth including goods, whereas the inspected floppy score update uses liquid assets. The Statistics screen separately calculates Net Worth including possessions. Keep these accounts separate: the card's exact edition correspondence is unconfirmed, and no runtime test has resolved the discrepancy. Do not implement a goods-based Wealth rule merely by merging the two descriptions. Full asset-refresh call timing also remains to be traced.

## Progress and statistics screens

**Goals / F6** opens an overview with an illustrated thermometer, participant marker, and percentage for each player. Selecting a participant opens their four-goal detail. Jones uses his own marker. The detail reuses the setup star arrangement, locks targets, adds current indicators, and retains the definitions button. [Overview/layout](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/viewGoals.sc#L69), [detail](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/select3.sc#L39).

The displayed percentage sums category scores **capped at their individual targets**, then divides by total target points and truncates. This weights categories by target size, rather than averaging four normalised percentages. Surplus in one category cannot conceal another's deficit. The actual finish rule checks all four separately. [Percentage](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/viewGoals.sc#L22), [finish check](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L85).

**Statistics / F4** is a separate current-player scrolling inventory/status panel containing:

- Participant, workplace, occupation and hourly wage, or unemployment information.
- Cash, savings, rent owed, loan balance, goods value, investment total and net worth.
- Clothing, weeks of food and quantities of durable possessions.
- Completed degrees and investment holdings.

This is generated from inventory and employment state, rather than being another goals dashboard. [Statistics content](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/inventories.sc#L19), [scrolling panel](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/inventories.sc#L158).

The shortcut help also specifies right mouse / Shift-left for Statistics, middle mouse / Ctrl-left for Goals, and Escape for menu/pause. Reading speed, animation speed, nonessential messages, music, effects and graphics detail are adjustable. [Help/options](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/Menu.sc#L120).

## Completion sequence

The finish check runs at **the start of a participant's turn**, after the clock reset and economy update, before most remaining weekly processing: all four scores must meet their targets and the participant must not already have finished. The inspected flow therefore does not award victory immediately within the action that fills the final meter. [Start-turn sequence](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L54).

Completion launches a celebration with the character on a pedestal, animated stars, music, a Jones figure crossing the scene, and confetti. Pedestal labels allocate **WINNER**, **2ND PLACE**, **3RD PLACE**, then **4TH PLACE** as further participants finish. Input advances beyond the animation once it is underway. [Celebration](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/winnerScript.sc#L21), [placement labels](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/winnerScript.sc#L351).

The finishing week is recorded and the participant retires from normal turns. With other participants remaining, the game offers **Continue**, **Restart**, or **Quit**. Continue lets others pursue later places. When none remain active, a thank-you prompt offers Restart or Quit. [Finish handling](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L105), [retirement/final prompt](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L956).

## Remaining verification

Verify marker appearance, scrolling, initial displayed scores, investment/debt score-refresh timing, final-action-to-next-turn victory, Jones winning, and later placements in the reference runtime. The parent browser inspection reached an opening notice and then a blank display, supplying no gameplay observations; see [visual evidence limits](town-and-screen-layout.md#evidence-still-needed-for-visual-fidelity). Other editions were not compared in this pass. No online leaderboard or persistent cross-game high-score system appears in the inspected finish path; absence across every resource has not been established.
