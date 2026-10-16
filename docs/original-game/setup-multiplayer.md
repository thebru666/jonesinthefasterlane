# Original game: setup, multiplayer, and persistence

Research date: 2026-10-15. Reference: DOS floppy **1.000.060**. Evidence is **SCRIPT: published decompilation inspected**, not runtime observation or a decompilation performed by this project. See the [source register](../discovery/source-register.md). This describes the original, without approving adaptation changes.

## Startup and setup journey

A small central startup dialog offers **Play Game**, **Restore Game**, and **Demonstration**. Play proceeds to **How Many Players?**, with **1–4** human players. Demonstration uses a computer-controlled player and is a separate startup route. [Startup](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/select1.sc), [count](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/select1b.sc).

Players then choose from **four preset character bodies**. A chosen body is dimmed and unavailable to subsequent players. Each character selection immediately opens that player's goals dialog before the next participant chooses. The inspected path uses Player 1–4 identifiers and contains no name-entry step. Do not infer different abilities from appearance. [Character selection](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/select2.sc), [caller](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L1207).

Each participant sets **Wealth, Happiness, Education, and Career** with four vertical star sliders: **10–100 in steps of 10**. The first player defaults to **50 each**, total 200; later participants initially inherit the preceding participant's targets and can adjust them independently. Goal Points displays the sum. A question-mark button opens explanations. Thus multiplayer need not use identical targets. [Sliders and defaults](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/select3.sc#L87).

## Original supported combinations

| Setup | Original behaviour |
| --- | --- |
| One human without Jones | Solo goal completion |
| One human with Jones | Optional two-participant computer challenge |
| Two to four humans | Shared-computer play; no Jones prompt on this path |
| Several computer rivals or multiple humans plus Jones | No such setup path found |

Only after configuring **one human** does the game ask whether to challenge Jones. Yes reveals **Take It Easy**, **Play Fair**, and **Go For Broke**, with Play Fair initially focused. Jones's resulting goals are then displayed read-only. [Branching](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L1219), [Jones choices](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/select4.sc).

The inspected difficulty mechanism changes **Jones's targets**: it aims for the human's total plus **40** on Take It Easy, the same total on Play Fair, or **40 fewer** on Go For Broke, bounded to 40–400. Category distribution is randomised within legal limits; wealth initially follows the human's wealth target plus 10, 0, or −10. Play Fair therefore need not give Jones the same four targets. This establishes setup difficulty, not a complete audit of AI strategy or advantages. [Assignment algorithm](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/select4.sc#L20).

## Shared-device turn handover

The player list advances in order, skipping finished/deleted participants. After a rotation wraps, the shared week advances. Handover updates the board's character/number markers, walker and clothing, cash display, and time indicator; the incoming player's turn starts at their housing. [Rotation](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L938), [board update](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L1069).

No dedicated concealed pass-device screen was found in this path. Everyone shares the visible interface, and Goals explicitly allows inspecting each participant's targets and progress. Statistics concerns the current participant. The [first runtime session](../rules-audit/runtime-observations.md) now captures the player1→player2 handover: week remains1, body/marble/number markers change, clock resets and player2 has independent cash200. No blocking ready/privacy step was encountered; exact pacing and other handover paths remain open. [Goals inspection](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/viewGoals.sc#L212), [Statistics](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/Menu.sc#L41).

The options menu also permits **Delete Current Player**, with confirmation when multiple unfinished participants remain. [Deletion](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/Menu.sc#L306).

## Saving, restoring, and quitting

- **Save Game / F5** warns that it overwrites the previous save, then writes a fixed save slot in the configured directory.
- **Restore Game / F7** asks for confirmation; restore is also available at startup. No named multi-slot save browser appears in this path.
- **Set Save Directory / Ctrl-Y** changes location. The single-slot interface does not imply that separate directories cannot hold separate copies.
- Save and restore report missing/incompatible saves or write failure.
- **Quit / Ctrl-Q** asks for confirmation; **Restart / F9** is separate.

Sources: [commands and confirmations](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/Menu.sc#L120), [fixed slot](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/Save.sc#L20). The [manual scan](https://virtualconsoles.com/wp-content/uploads/2024/03/Jones-in-the-Fast-Lane_Manual_DOS_EN-compressed.pdf), printed page 6, independently describes one save at a time (DOCUMENTED; exact edition correspondence unconfirmed).

Website/emulator persistence is separate from these DOS save rules and remains unverified here.

## Remaining verification

Capture startup, every setup screen, Jones difficulty, a two-human handover, and save/restore. Check artwork, cancellation paths, and timing. No runtime tests were performed during the initial script-analysis pass. The later [runtime observations](../rules-audit/runtime-observations.md) confirm two-human setup inheritance/dimming and one handover; Jones difficulty, cancellation and save paths remain open. The parent browser inspection reached an opening notice and then a blank display; it supplied no gameplay observations. See [visual evidence limits](town-and-screen-layout.md#evidence-still-needed-for-visual-fidelity).
