# Documentation consistency and design readiness review

Reviewed: 2026-10-15, after audit pass 1.

## Assessment

The documents consistently establish intent, evidence limits, the distinction between player turns and weeks, and the initial time/economy findings. They are sufficient to draft the main gameplay flow and explore screen layouts. They are **not sufficient for a complete interaction/layout specification or application implementation**.

The audit explains how selected systems behave. It does not yet specify everything a player sees, clicks, or needs to understand. Remaining rules and content affect layout: the number and position of buildings affect travel, course prerequisites affect the university screen, and opponent behaviour affects the shared-device experience.

This was a review of the repository documents and their internal relationships. It did not independently revalidate the published decompilation against the game binary or complete runtime cases.

## Consistency findings and corrections

| ID | Finding | Resolution / status |
| --- | --- | --- |
| C01 | “Computer ownership income” in WEEK-002 could imply special income for the computer-controlled opponent | Clarified to income from owning a computer item; no rule change |
| C02 | TIME's validation summary linked T01–T07 although T08 covers its travel uncertainty | Corrected to T01–T08 |
| C03 | T02 referred to an unspecified six-hour action inside a shop | Specified an employed shop workplace, shift, available stock, and sufficient cash |
| C04 | Original behaviour and adaptation proposals could be mistaken for the same specification when read across files | Existing evidence/mapping labels are consistent; new flow/layout outline explicitly labels every section's status |
| C05 | Original turn-boundary win checks are recorded, while adaptation goal definitions and finish flow remain open | Consistent, but incomplete; do not present the recorded check as the complete victory specification |
| C06 | Four goals and React are discussed both as original findings and future direction | No contradiction: four goals are observed in published scripts; adopting their exact definitions remains proposed. React is supported direction; architecture remains pending |

## Readiness by area

| Area | What is established | What is missing | Readiness |
| --- | --- | --- | --- |
| Core player loop | Travel, entry, action costs, partial final actions, turn handover | Full action catalogue and boundary reproduction | Enough for a draft flow |
| Pre-turn processing | Ordered economy, notices, upkeep, penalties, and boundary win check | Rare branches, full goal semantics, runtime confirmation | Enough for a draft flow with exceptions |
| New game setup | Shared-device play and a computer opponent are required | Player limits/combinations, character setup, goals, defaults, start resources, setup order | Incomplete |
| Town board | Compact town and distinct storefronts fit the brief | Original visual inventory, complete building list, positions, travel relationships, interaction states | Incomplete |
| Location screens | Character-led visits; shared time/money rules | Per-location actions, information hierarchy, offer/prerequisite presentation, failure states | Incomplete |
| Shared-device experience | Separate turns and shared global economic effects | Ready/handover interaction, privacy, opponent pacing, cross-player announcements | Incomplete |
| Progress and possessions | Four original goal checks, item/education effects under investigation | Exact metrics, inventory presentation, home scene, comparison screen | Incomplete |
| Save/resume and finish | Local saves are intended; original has finish handling | Save boundaries, schema, restore feedback, continue-after-win behaviour | Incomplete |
| Visual style and accessibility | Original feel, illustrated retro candidate, child/adult audience | Wireframes, art samples, typography, touch/keyboard states, small-screen strategy | Incomplete |

## What to specify next

1. Draft the whole player journey, screen inventory, and interaction contract using the [flow and layout outline](flow-and-layout-outline.md).
2. Audit the original's visual organisation and location navigation; document composition in original analytical notes without committing extracted assets.
3. Complete job/course/item/location catalogues sufficiently to size menus and lay out the board. Preserve travel relationships until any change is explicitly chosen.
4. Produce low-detail wireframes for the town, a shop/workplace, employment, university, home/progress, and multiplayer handover.
5. Walk through an ordinary opening, a failed application, a final-hour action, a bad economic event affecting several players, and a win/continue path. Record every unresolved interaction.

This work can proceed while numeric edge cases are being verified. Detailed balance uncertainty does not prevent drafting a layout; unknown rules that change navigation or visible choices must remain visible in that draft.

## Acceptance standard before implementation

A reader should be able to follow a complete game journey, identify what is visible and actionable on each screen, and explain the resulting time/money/progress changes without inventing missing transitions. Each proposed departure must be explicit. The current documents do not yet meet that standard.
