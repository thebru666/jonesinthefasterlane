# Education: original rules and action flow

Audit date: 2026-10-16. Reference: website DOS **1.000.060** package. Evidence is **BYTECODE** for the paths and object data identified below, compared with the pinned published decompilation; no new runtime experiment is claimed. This records the original, with no approved 2.0 changes. Machine-readable references are in [the education verification artifact](../../artifacts/rules-audit/bytecode-education-verification.json).

## EDU-001: university entry and available courses

Entering Hi-Tech U charges **2 time units**, separately from travel. The initial dialog includes Exit, Enroll and a set of eligible course books; Work and its clock appear if this is the player's employer. A completed qualification is omitted; an unfinished qualification appears only if its prerequisite is complete, or if it has none. Eligibility depends on completed qualifications, not progress toward them. The full [11-course graph](../original-game/content-progression.md#education-the-two-original-starting-branches) is confirmed directly against all eleven instance property tables. IDs 10–20, prerequisites and six-unit lesson costs agree with the existing catalogue. The largest eligible set is four books; this follows from the prerequisite graph and is not a four-enrollment cap.

Package anchors: script 207 `university.init` at `0x089e`, entry charge `0x08fa–0x0901`; course-list builder `0x0257–0x030c`; `UniversityDIcon.addCourse` at `0x030d–0x0356`. Qualifying properties live at instance offsets listed in the artifact.

## EDU-002: enrollment buys permission to start one course

Enroll displays a Yes/No confirmation to a human. Jones follows the same fee object's purchase method without that question. The fee has **base price $50**, adjusted by the shared pricing helper with the current economic index. It is paid from cash, not bank savings. Successful payment increments the player's cumulative `enrollments` by one. There is **no lesson fee**, and the enrollment purchase itself has zero visit time. Neither this button nor its fee object imposes a spent-time refusal, so the examined path allows enrollment after the clock reaches 60, if affordable.

Let `E` be paid enrollments, `D` completed degrees, and `A` active courses. An active course has quantity strictly between zero and its ten-unit graduation threshold. Attendance is permitted when either:

- `E > A + D`, meaning an unused enrollment exists; or
- `E == A + D` and the selected course is already active.

Otherwise it reports that enrollment is required and adds no study progress or time. Buying enrollment does not immediately bind it to a named course: the first attendance starts that course. Multiple active courses are possible if sufficient enrollments have been bought. Graduating replaces one active course with one completed degree, preserving the consumed enrollment. The fee handler has no explicit maximum or surplus-enrollment refund.

Package anchors: script 207 `enrollButton.doit` `0x117a`, fee init `0x0c7a–0x0c86`, fee purchase `0x0c87–0x0caf`; fee base/type/time property words `0x0d08`, `0x0d02`, `0x0d0e`. Admission checks `0x036f–0x03b6`, active counter `0x0205–0x0256`; script 1 `Player.courseActive` `0x1197`. Fee cash debit delegates to script 104 `CostDItem.doit`; type 4 bypasses goods creation. Shared price adjustment is script 109 export 0, not a fixed $50 charge in every economy.

## EDU-003: one click awards one attendance increment

Once admitted, the course checks **spent time is not equal to 60**. It does not require six remaining units. With any valid positive remainder, it receives one education-list unit, tests completion, then charges the course's six-unit visit time. Time clamps at 60 in the shared clock handler. Thus one hour remaining buys a full attendance increment; zero hours buys none. No cash debit occurs in this path. The superclass call is a UI value-return operation, not a second purchase or progress increment.

Progress persists between visits and weeks. The first attendance creates the education record with quantity 1; later attendance adds 1 to the same course record. Without equipment credits it takes ten successful attendances, costing 60 study time plus travel and entry costs. A normal lesson has no direct happiness bonus. Graduation has separate rewards.

Package anchors: script 207 exhausted-clock gate `0x03b9–0x03bf` (failure target `0x062d`), one-unit receipt `0x03c2–0x03d4`, clock call `0x041c–0x0424`. Script 106 `ListOfGoods.recieve` at `0x00dd`, `hasType` at `0x0121`; `Educational.unitsToGraduate` is 10 at raw property offset `0x00c0`. Script 1 `timeKeep.doit` at `0x24f8`, explicit charge `0x250e–0x2517`, cap `0x2538–0x2543`. Script 207 superclass is class 12 (`DIcon`), inheriting class 10's value-return method at script 255 `0x0329–0x032b`.

## EDU-004: study equipment reduces the threshold, not the lesson duration

At start of the player's turn, `extraCredits` resets to zero and is rebuilt from current durable holdings:

| Holding | Credit |
| --- | ---: |
| Encyclopedia (31), dictionary (32) **and** atlas (33), all present | +1 |
| Computer (29), present | +1 |

A single book or two of the three gives no credit. Multiple copies do not multiply credits. The total is therefore 0, 1 or 2 on ordinary paths. After an attendance increment, if quantity is at least `10 − extraCredits`, the university **sets quantity to 10**, permanently completing the qualification. Typical attendance counts are 10, 9 or 8. Finished degrees still count as finished if the equipment later disappears: degree detection uses the snapped quantity, not current equipment.

Credits are a **start-of-turn snapshot**. Purchasing equipment mid-turn does not update this field in the purchase handler. Conversely, selling it mid-turn does not recompute credits there. If the snapshot reduces the requirement below progress already accumulated, opening the university does not itself graduate the player: an attendance action is still required to run the completion path. The opening display clamps an already-met remaining count to at least one until that action. The lesson still costs six nominal time units.

Package anchors: script 111 `startTrn.changeState` reset and holdings reads `0x0333–0x0387`, all-three-book conjunction and increment `0x0389–0x03ad`, computer increment `0x03af–0x03c9`; script 207 threshold/snap `0x03dc–0x040f`. The remaining-count formatter is procedure `0x0736`, including the local initialization guard used for its minimum-one display. Item identity is independently matched to script 211 objects `encyclopedia`, `dictionary`, `atlas` and script 208 `computer`.

## EDU-005: graduation changes several systems at once

After progress and the time charge, the university asks whether the course is now a completed degree. If so, in order it:

1. Clears `notEnoughEd` and applies **+5 happiness** through the shared happiness helper (subject to that helper's bounds).
2. Adds **5 eduCredit**, **5 dependibility** (the game's spelling), and **5 expCredit**.
3. Temporarily disables normal control, opens the diploma presentation for that qualification, then rebuilds available books so newly unlocked courses appear.
4. Sets education goal progress to **`1 + 9 × completedDegrees`**.

One completed degree yields education progress 10; eleven yield 100. An unfinished course gives no partial education-goal progress. The raw Player class default for `eduStat` is zero; do not apply the `1 + 9D` formula before the graduation setter has run. With all eleven complete, the university removes the books and enrollment control and can show its no-further-courses message. Work remains a separate employer action when relevant.

`numDegrees` counts records whose quantity is at least their graduation threshold. `hasDegree(courseId)` requires the matching ID and that same completion test; `hasDegree(0)` is explicitly true, allowing jobs/course definitions to mean no requirement. Jobs can require **two completed qualifications**. Work-development effects of `eduCredit`/`expCredit` are part of the employment/work trace; these are separate from visible education goal progress.

Package anchors: script 207 qualification check `0x0426–0x0431`, state rewards `0x043d–0x0490`, diploma dispatch `0x04c4–0x04d3`, final goal setter `0x0612–0x0628`. Script 1 `Player.numDegrees` `0x10eb–0x112c`, `hasDegree` `0x112d–0x1196`. The course/job join uses IDs, not graphical label text.

## Build reference and remaining boundaries

For a faithful rules model, represent paid enrollments, per-course progress, completed qualifications, the turn's equipment-credit snapshot, visible education progress and work-development credits separately. Treat degree completion as an ordered state transition followed by presentation; do not award fractional progress based on remaining time or immediately graduate from an inventory change. These are translations of the audited original, not new feature proposals.

Verification covered raw class properties across nine dependent scripts, all eleven prerequisite edges, named method tables, the admission/attendance/completion branches and the clock's arithmetic. Eight instruction landmarks and two signed branch destinations were also independently checked directly in raw bytes, beyond the shared disassembler output. This does not claim full equivalence of every instruction to the published source or execution in the DOS interpreter.

Narrow runtime checks still useful: spending the final hour on a lesson; refusal at 60; a second active course with/without a spare enrollment; completing at 8/9/10 attendance; newly obtained/lost equipment across the next turn; diploma/goal refresh ordering. Dynamic UI event routing, the complete diploma animation, shared economic pricing edge cases and computer strategy selection are outside this education-path verification. The original snapshot and short-final-lesson behaviours must be preserved or explicitly changed in 2.0; no choice has been approved here.

Source provenance: [website bundle](https://jonesinthefastlane.com/bundle.jsdos), decoded locally; [published university script](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/university.sc), [player/clock script](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc), [turn-start script](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc). Local decompilation and original payloads remain ignored; the artifact records reproducible hashes and analytical references only.
