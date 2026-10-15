# Design implications from the rules audits

2026-10-15. These are recommendations and open decisions, not changes approved by the owner.

## Preserve the source of the economic humps

The [economy audit](../rules-audit/economy.md) points to a useful combination: persistent market trends, separately moving investment/goods readings, occasional shocks, and stored wage/rent contracts. A good job secured before a downturn can remain valuable while shopping becomes cheaper. Moving or retraining at the right time matters.

Preserve that strategic relationship before adding new economic concepts. A blanket inflation percentage applied to wages, rent, and goods every week would remove it.

## Choose an edition baseline explicitly

The website uses the floppy version marker. The inspected CD script changes minimum readings, recovery pressure, event timing, and crash frequency. We should pick and document one of:

1. Floppy behaviour, including deliberate compatibility decisions for its quirks.
2. CD economic recovery/timing with near-original gameplay elsewhere.
3. An explicitly tuned adaptation retaining the same contract/trend/shock structure.

Recommendation: validate both and consider the CD recovery changes for the default experience. Do not make that choice until we have measured the effect and discussed it with the owner. A permanent-feeling slump is a different design question from an entertaining recession.

## Keep the action economy recognisable

Travel, entry costs, short final actions, and free transactions at a completed clock are part of the strategy. The [time audit](../rules-audit/time-and-actions.md) shows why the last hour can be unusually valuable. A modern interface can explain costs and refusals without replacing those rules.

Decide separately whether apparent bugs such as partial-shift garnishment deserve compatibility. They are not automatically part of the essential simplicity or humour.

## Model ordered turns before rendering

The [weekly processing audit](../rules-audit/weekly-processing.md) distinguishes a round from a player's turn and separates economy calculation from later consequences. Future state design should represent these phases explicitly, including notices and multiplayer handover. Both human and computer actions should reach the same legality and accounting paths, with any discovered original exceptions documented.

## Humour and presentation can be modernised independently

The manual's interaction pages and the scripts show opportunities for adjustable message pacing and concise feedback. We can preserve character-led humour while making costs, job refusals, and weekly consequences easier to read. Writing original jokes, choosing portraits, and producing mockups remain later planning tasks; this audit does not approve a final art style or copy original dialogue.

## Gates before building

Finish the rule/content areas listed in the [validation backlog](../rules-audit/validation-backlog.md), resolve the key compatibility decisions, and agree the town/content and screen plans. The first playable slice can then validate a concrete specification rather than becoming the place we invent the missing rules.

## Pass 2: choices to review after runtime confirmation

These follow-up suggestions remain **PROPOSAL**, separate from the original findings:

- Preserve the compact town/central-window composition shown in the [screen studies](../original-game/screen-reconstruction.md), then modernise content and original illustrations within it. Complete dynamic text and feedback before approving final wireframes.
- Keep Jones's ordered priorities as the reference policy. Decide explicitly whether the adaptation should expose market trends equally or preserve his information advantage, and whether difficulty should continue changing targets. See [AI-001/008/009](../rules-audit/computer-opponent.md).
- Preserve the food/storage/rent tradeoffs without adding new survival meters. Decide separately on confirmed object-lifetime/spoilage/garnishment quirks after reproducing them. See [needs and housing](../rules-audit/food-and-housing.md).
- Keep bank, broker and pawn transactions small and direct. Explain the actual payment/trade fees in the interface once verified; do not infer modern financial products from original jokes. See [finance](../rules-audit/goods-and-finance.md).
- Maintain a compatibility ledger for apparent unreachable purchase bonuses, repeated loan-rejection penalties and large-balance arithmetic. No fix or faithful preservation of a suspected bug is approved yet.
