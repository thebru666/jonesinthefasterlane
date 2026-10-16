# Rules readiness for 2.0 planning

Updated 2026-10-16. The owner's objective is to extract and document original game flow/rules ready to guide the 2.0 build. The [connected flow reference](../original-game/game-flow-and-rule-contract.md) is the primary reading path; domain notes provide formulas, tables, package offsets and limits. Application implementation has not begun.

## Established planning foundation

- Original setup, thirteen destinations, location/child-screen returns, personal goals, shared-device rotation and supported Jones combination are documented. The [fresh-state contract](../rules-audit/initial-player-state.md) now separates player defaults, common allocation and first-turn preparation.
- All69 compiled scripts are decoded locally with reproducible hashes; selected actual paths now confirm employment, all37 job records, education/all11 courses, turn order, goal gates, AI all-destination action dispatch, entry costs, clock and save calls.
- Employment and education join through qualifications, experience, dependability and graduation credits; these cannot be designed as isolated screens.
- Baseline needs, goods, finance, personal events and economy have detailed published-script audits. Food/illness and selected theft/repair/weekend/lottery/mugging/computer-income predicates now have direct package checks. Selected anomalies are independently package-confirmed; that does not upgrade every numerical statement to BYTECODE.
- Existing local art catalogue and partial screen composites support layout/art planning. They do not provide complete runtime composition, font/focus/animation equivalence.

## Remaining research, ordered by effect on the build

| Topic | Established | Remaining question | Planning consequence |
| --- | --- | --- | --- |
| Travel | [Native-supported ordinary formula](../rules-audit/dos-travel-ordering.md), 25,500 analytical cases, residual/speed boundaries and all13 entry costs | Interrupted/restored paths, abnormal actor state and visible/wall-clock corroboration | A fixed distance/time rule must be specified or explicitly adopted as a departure |
| Score freshness | [All69-script bounded writer/caller inventory](../rules-audit/score-refresh.md); cash and asset refresh are separate, with bank tail mutations | [Normal modal continuation now traced](../rules-audit/bank-refresh-continuation.md); visible lag and reflective/restored paths remain | Specify authoritative refresh points before goal/completion tests |
| Economy | Layered indices and duplicate condition; [original DOS frame trace](../rules-audit/economy-frame-semantics.md) resolves the main omitted argument to the preceding target draw | Long-run behaviour, other callers/editions and some high-word effects | Replacing that draw with zero or repairing the condition changes compatibility |
| Randomness | [Native DOS seed recurrence, output bits and bound scaling](../rules-audit/dos-randomness.md); failed-action and winner-animation draws | Complete initialization/reset callers, full call order and post-restore sequence; actual frequencies | Reproducible modern seeds require an explicit new contract; separate visual draws is a proposal |
| Computer execution | Policy, goal-based difficulty, all-destination dispatch inventory, selected confirmation bypasses, hidden market inputs and two policy anomalies | Remaining policy arithmetic, dynamic action consumers and rare fallback | Do not claim exhaustive human/AI parity yet |
| Needs/events/finance | Selected needs/events plus [rent/extension/move, pawn expiry and due-week loan lifecycle](../rules-audit/finance-lifecycle.md) package checks | Remaining random predicates, unusual/restored inventories and full extreme-value arithmetic | Keep bounded evidence; verify a disputed formula from bytes before implementing it as exact |
| Inventory/used goods | [Grouped receipt/packing](../rules-audit/inventory-grouping.md), [used-stock transfers/capacity](../rules-audit/pawn-used-stock.md), [six investment records/trades and broker lifetime](../rules-audit/investment-transactions.md), and [money boundary fixtures](../rules-audit/money-word-boundaries.md) | Observed edge cases, arbitrary aliasing and full high-word valuation | Individual-item models or one modern integer radix would be explicit departures |
| Ordinary shopping | [Clothing stock/rewards/decay](../rules-audit/clothing-lifecycle.md), [food/drink bonus latches](../rules-audit/fast-food-bonuses.md), [Z-Mart selection/revisit/reset](../rules-audit/discount-assortment.md) | Visible corroboration and a consolidated all-game Happiness modifier catalogue | Repeated rewards, category latches and maximum-stock warnings need explicit compatibility choices |
| Completion/removal | Two pre-turn gates, placement allocation, inactive/removal distinction | Every resumed/deleted/restored intermediate state | Decide supported save points and continuation behaviour |
| Saving | Fixed slot1/version calls; [native serialized regions exclude PRNG seed](../rules-audit/dos-save-state.md) | Full field/fixup format, actual roundtrip and browser persistence | Future local saves should follow the agreed modern state model |
| Presentation | Screen inventory, decoded art/partial composites; [native stereo lookup fallback](../rules-audit/dos-stereo-fallback.md) | Full text/focus/animation/sound and exact clerk returns | Needed for visual fidelity, separate from core simulation correctness |

Remaining bytecode questions should use focused traces or interpreter analysis. Broad manual gameplay is not the default research method. A targeted runtime experiment is appropriate only where it answers a specific interpreter or visible-presentation question.

## Compatibility decisions still owned by the project

These are unresolved choices, not requests to answer immediately and not approved fixes:

1. Confirm website floppy1.000.060 as the behavioural baseline, or deliberately use selected CD economy behaviour.
2. Preserve or repair confirmed quirks: full-shift garnishment, duplicated economic adjustment, double initial-loan penalty, skipped refrigerator bonus, AI home-route units mismatch and shadowed clothes branch. Newly traced inventory/cash boundaries add browsing-time used-stock quality changes, group-wide historical fields and inconsistent carry/display constants to that review.
3. Retain or simplify movement-tick timing and stored-score refresh semantics.
4. Retain goal-based Jones difficulty and privileged economic information, or define a different transparent challenge.
5. Decide the modern randomness/save rules and whether visual randomness shares simulation state.
6. Approve updated content, screen/art treatment, audience/accessibility choices, supported devices and first-slice scope against the original baseline.

The $50 repayment reducing principal by$45 is established original behaviour; deciding a modern loan schedule is separate from discovering that arithmetic. Likewise the short-final-lesson increment and equipment-credit snapshot are real rules, not presumed bugs to remove automatically.

## Next deliverable before application implementation

Create a reviewed rules specification that assigns each original rule **keep / reskin / change**, links its evidence, and states any substitute for an unresolved interpreter quirk. Attach the state/action contract, content identifiers/tables, ordered turn effects, save boundaries and test scenarios. Only then settle detailed React/TypeScript architecture and the first playable slice.

This record does not call the full audit complete. It identifies what is ready to review and the concrete gaps that remain, so implementation cannot silently fill them with assumptions.
