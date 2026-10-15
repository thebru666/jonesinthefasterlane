# Asset role hints from original scripts

Recorded: 2026-10-15. Evidence classes: **SCRIPT** for role assignments and **DECODED** for explicitly inspected exported pixels. This note is an original analytical index, not an export of original script source.

The [machine-readable role index](../../artifacts/original-game/asset-role-hints.json) records 53 distinct resources referenced by literal instance properties, 177 instance references, and additional dynamic-callsite hints. Every reference links to a line in the pinned published decompilation at revision `870a8015b689474484bf3d8b41416956d4315432`. The [existing source manifest](../../artifacts/original-game/2026-10-15-source-inputs.json) records source-file hashes. Those published scripts have not been established as byte-identical to the website package.

## Priority lookup

| Screen or component | Resource hints | Evidence and limits |
| --- | --- | --- |
| Town board | Picture 11 | `room1` picture property; the picture alone is not the composed game screen |
| Shared controls | View 250 | Reused exit/work/enrol/progress buttons across dialogs; loop/cel references are indexed |
| Board time display | View 270 | `timeKeep`; loops/cels selected dynamically from remaining time |
| Body-coloured dialog header | View 0, loop 0 | `Main` explicitly draws a cel selected by body index |
| Character selection | Views 500 and 499 | Background and selection dimming/player-number components |
| Setup choices | Views 10 and 11 | Start/setup controls and challenge-Jones dialog background |
| Goal setting/progress | View 501 | Goal controls, thermometers and related components; inspect loops rather than one cel |
| Inventory | View 505, loop 4; font 4 | A text-selector inventory; do not assume every possession has an individually illustrated inventory icon |
| Low-cost/security apartments | Views 700 and 702 | Runtime alternates 699/698 when current player does not live there; several furnishing components share these view resources |
| Rent office | Views 701 and 351 | Background/title components and clerk Talker |
| Market/bank | Views 803/804 and 353/354 | Dialog backgrounds and Talkers |
| Factory/employment | Views 705/706 and 355/356 | Dialog backgrounds and Talkers |
| University | Views 807, 707 and 357 | Background, books/course controls and Talker |
| Appliances/clothing/fast food/discount | Views 808/809/810/811 and 358/359/360/361 | Backgrounds and Talkers; additional display/animation controls use views 708–711 |
| Pawn shop | Views 712 and 362 | Background/transaction components and Talker; one merchandise control references view 708 |
| Broker | View 696 | Background and investment controls |
| Newspaper | View 603 | Newspaper background/control, with text supplied separately |
| Graduation | View 607 | Diploma display/animation components |
| Victory | View 609 | Jones, pedestal, stars and confetti; winner uses current walker graphics; sound 7 is selected for music |

The full index preserves script identifiers to aid lookup. A clerk's `Talker` view can be combined with other dialog artwork; its resource number does not establish a complete portrait or finished screen on its own.

## Precise course-label transcription targets

[University script](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/university.sc#L547) assigns view 707, loop 2 to eleven selectors:

| Cel | Script course identifier | Decoded book label |
| --- | --- | --- |
| 0 | tradeSchool | Trade School |
| 1 | electronics | Electronics |
| 2 | preEngineering | Pre Engineer. |
| 3 | engineering | Engineering |
| 4 | juniorCollege | Jr. College |
| 5 | ba | Bus. Admin. |
| 6 | academic | Academic |
| 7 | graduate | Grad. School |
| 8 | postDoctoral | Post Doctoral |
| 9 | research | Research |
| 10 | publishing | Publishing |

Labels were read from the exported view 707 contact sheet, loop 2, on 2026-10-15; spacing is normalised here. In particular, `ba` is painted “Bus. Admin.” and `academic` is painted “Academic”. This establishes the visible labels in the pinned package, without proving bytecode correspondence to the published scripts.

## Dynamic graphics require care

The [turn-start walker selection](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L1110) starts from body-dependent resource bases 280, 284, 290 and 294, with Jones base 274, then applies clothing-related offsets. The [initial walker assignment](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L1297) uses 282, 286, 292 and 296, or 276 for Jones. Catalogue every decoded resource before giving each clothing variant a visual label.

Resources, loops and cels are different levels: one view may supply multiple objects, frames may be reused, and controls inherit properties. Missing loop/cel properties in the JSON mean no explicit assignment in that instance property list, not necessarily zero. Runtime resource substitutions and palette flags also affect final composition.

No complete screen reconstruction, audio listening pass or runtime visual equivalence is claimed by this script index. Use it with the local decoding report to label what has actually been exported and reviewed.

## Completed local decoding pass

The [rebuild guide](../discovery/rebuild-original-assets.md) and [metadata summary](../../artifacts/original-game/decoded-asset-summary.json) record all 266 unique resources. The local searchable index includes all 90 views (752 cels), seven picture backgrounds with priority/control planes, eight font sheets, two cursors, one palette, 39 text collections and 34 sound event resources. Scripts, vocabulary and instrument patches remain decompressed bytes.

Representative inspection covered town picture 11, course-label view 707, goal view 501, apartment views 700/702, clerk view 358 and font 0. These were recognisable component exports; no full runtime scene or original-device sound comparison has been completed. Cursor inversion is represented as a static reference rather than background-dependent inversion.
