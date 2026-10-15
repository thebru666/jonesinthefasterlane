# Existing summaries and how to use them

Research date: 2026-10-15. Scope: the original game, before adaptation proposals.

The most useful starting point is the original reference card, followed by a location-by-location community guide. This document is a reading guide, not another complete reproduction of those guides. Our own [original-game index](README.md) organises the resulting specification by screen and system; the [rules audit](../rules-audit/README.md) records exact script findings separately.

## Evidence labels

- **DOCUMENTED / original publication:** original instructions hosted by a preservation site; establishes what Sierra told players, without proving every executable detail.
- **DOCUMENTED / community:** retrospective descriptions, walkthroughs, and wiki entries. Useful for discovery, terminology, screenshots, and independent cross-checks. Edition and correctness need checking.
- **SCRIPT:** our analysis of the published decompilation at the pinned revision in the [source register](../discovery/source-register.md). This is stronger evidence for version-specific mechanics but is not runtime observation.
- **OBSERVED:** only use after a recorded runtime experiment. Opening a web guide or viewing its screenshot does not establish behaviour observed in our reference executable.

## Original reference material: read first

### Sierra reference card

- [Preservation page](https://www.sierragamers.com/jones-in-the-fast-lane/)
- [Reference-card PDF](https://www.sierragamers.com/wp-content/uploads/2019/12/Jones_In_The_Fast_Lane_Reference_Card.pdf)
- Evidence: **DOCUMENTED / original publication**; precise release correspondence unconfirmed.
- Use for the original explanation of setup, goals, turns, town services, and player-facing action vocabulary.
- The project records analytical notes and metadata; the scan and rendered pages remain in ignored local research storage.

### Sierra manual

- [Manual PDF](https://virtualconsoles.com/wp-content/uploads/2024/03/Jones-in-the-Fast-Lane_Manual_DOS_EN-compressed.pdf)
- Evidence: **DOCUMENTED / original publication**; precise release correspondence unconfirmed.
- Use for mouse/keyboard conventions, menus, save/restore, statistics/goals views, and pacing settings. It explicitly delegates much of the gameplay explanation to the accompanying reference card and learning through play.
- The earlier audit's [source register](../discovery/source-register.md) identifies useful scan pages. This manual alone is not a complete rulebook.

## Existing player summaries

### Giant Bomb: best single location-by-location overview found

- [Jones in the Fast Lane game wiki](https://wiki-origin.giantbomb.com/wiki/Games/Jones_in_the_Fast_Lane)
- [Page revision referenced by its footer](https://giantbomb.com/wiki/index.php?title=Games/Jones_in_the_Fast_Lane&oldid=985104)
- Evidence: **DOCUMENTED / community**. Edition unspecified; screenshots and prose may not all describe the same release.

Its Introduction covers character choice, four independently adjustable goal sliders, weekly turns, shared-device play, and the optional Jones opponent. Its Locations section tours all thirteen named locations, with interior screenshots, offered services, available jobs, and the university prerequisite tree. Strategy and Hints & Tips give examples of the interlocking work/study/food/rent loop. It is the most convenient existing summary to read alongside our location catalogue.

Do not import its claims uncritically. Statements that weekend descriptions have no effect, that AI is only a solo option, and that particular workplaces are always bad choices need qualification or script checks. Fixed prices are starting examples rather than universal prices. Its categorical wording about bankruptcy, recovery, and when play ends must be checked against our progression/finish notes.

### Jones in the Fast Lane Wiki: targeted system reference

- [Jobs](https://jonesinthefastlane.fandom.com/wiki/Jobs)
- [List of Jobs](https://jonesinthefastlane.fandom.com/wiki/List_of_Jobs)
- [Hi-Tech U](https://jonesinthefastlane.fandom.com/wiki/Hi-Tech_U)
- [Junior College](https://jonesinthefastlane.fandom.com/wiki/Junior_College)
- Evidence: **DOCUMENTED / community**. Some entries explicitly distinguish CD-only content, but that does not make every other statement version-neutral.

The Jobs page separates qualification, working, wages, clothing, and career-goal topics. The List of Jobs provides a compact comparison table and marks two positions as CD-only. Hi-Tech U explains enrolment/study interactions and includes screenshots; individual degree pages make prerequisites and job relationships easier to follow. These are useful navigational cross-checks for [content progression](content-progression.md), not the authority for numeric transcriptions.

The wiki's ordinary work-session summary and partial-session explanation should be compared with [time and actions](../rules-audit/time-and-actions.md), where exact integer arithmetic and edge cases are documented. Check every table against the chosen release before treating it as our baseline.

### Hardcore Gaming 101: experience and presentation retrospective

- [Bobinator, “Jones In The Fast Lane”](https://www.hardcoregaming101.net/jones-in-the-fast-lane/amp/)
- Evidence: **DOCUMENTED / community retrospective**. Edition unspecified.

Useful for its discussion of digitised characters, board presentation, the weekly clock, financial pressure, and the humour of everyday setbacks, with screenshots illustrating the game. Its tone is intentionally critical and comic. Claims about food having no difference, invisible progress, clothing intervals, and economic randomness should not become specification facts without stronger evidence.

### Sierra Chest walkthrough: located, not fully inspected

- [Walkthrough](https://sierrachest.com/index.php?a=games&fld=walkthrough&id=331&title=jones-in-the-fast-lane)
- Evidence: **DISCOVERY LEAD ONLY** for this pass. Search indexing exposes a gameplay synopsis, but direct retrieval returned HTTP 403 during this research. We did not inspect the complete walkthrough and do not cite it as proof of particular mechanics.

## Recommended reading order by question

| Question | Existing starting material | Project specification / verification |
| --- | --- | --- |
| What happens when starting a game? | Reference card; Giant Bomb Introduction | [Setup and multiplayer](setup-multiplayer.md) |
| What does the town look like and how do screens relate? | Reference card; Giant Bomb interior screenshots; HG101 screenshots | [Town and screen layout](town-and-screen-layout.md) |
| What can I do in each building? | Reference card; Giant Bomb Locations | [Locations and actions](locations-and-actions.md) |
| How do courses and jobs connect? | Fandom job/degree entries; Giant Bomb university section | [Content progression](content-progression.md) |
| How do goals, recovery, and winning work? | Reference card; Giant Bomb Introduction | [Progression and finish](progression-and-finish.md) |
| What is the exact weekly/economic behaviour? | Summaries provide orientation only | [Time and actions](../rules-audit/time-and-actions.md), [weekly processing](../rules-audit/weekly-processing.md), [economy](../rules-audit/economy.md) |

## Limits and next evidence

This search found useful summaries; it did not establish that any one summary is complete or correct. Original edition differences and internal contradictions remain visible in the individual specification notes. A systematic reference-game capture is still needed for exact screen geometry, all menu states, timing/animation, sound, and input edge cases. No web retrospective is labelled a runtime test.

Links were retrieved or checked on 2026-10-15 except where the access failure is stated. This document paraphrases selectively and links to the full sources; no original screenshots, manual pages, or community tables are committed here.
