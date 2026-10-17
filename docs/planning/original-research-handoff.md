# Original-game research handoff for 2.0 planning

Reviewed 2026-10-17 against the current repository and website DOS **1.000.060** inputs. The assigned discovery goal is to extract and document detailed original flow/rules with actual-package and clearly bounded evidence, ready to inform2.0 planning. The result is an original-game reference for review and iteration. It is not an approved successor design, application implementation or proof of complete original-engine emulation.

## Start here

1. Read the [connected flow and rule contract](../original-game/game-flow-and-rule-contract.md) for the journey, screen families, ordered preparation, ordinary action loops and state distinctions.
2. Use [fresh player state](../rules-audit/initial-player-state.md), [the destination/action catalogue](../original-game/locations-and-actions.md) and [content progression](../original-game/content-progression.md) to instantiate and walk the original rules. The actual package catalogues contain13 destinations,37 job records and11 courses; counts identify scope, not proof of every predicate.
3. Use [Happiness](../rules-audit/happiness-catalogue.md), [score refresh](../rules-audit/score-refresh.md), [travel](../rules-audit/dos-travel-ordering.md), [economy](../rules-audit/economy.md) and domain notes for calculations/order. Follow each evidence label rather than treating every older published-source statement as independently package-proved.
4. Use [screen/layout studies](../original-game/screen-reconstruction.md) and the [asset catalogue](../original-game/asset-catalogue-notes.md) for the original composition and kitsch reference. Original pixels/audio/code remain local; reproduce them using the linked checksum-locked guides.
5. Review the separate [iteration brief](follow-up-original-first-iteration.md), then record keep/reskin/change choices. No change is adopted because it appears among those suggestions.

## Requirement-by-requirement review

The requirements below derive from the owner's discovery requests, the project brief and repository instructions. Evidence was inspected at the scope named; decode counts and successful hash checks alone are not treated as semantic completeness.

| Required outcome | Authoritative reference and inspected evidence | Result for planning |
| --- | --- | --- |
| Describe the original before redesigning | [Original baseline](../original-game/README.md), connected journey and separate proposal brief | Original mechanics/content are separated from unapproved modernization ideas |
| Explain setup, defaults and human/Jones modes | [Setup](../original-game/setup-multiplayer.md), [actual initial state](../rules-audit/initial-player-state.md), setup dispatch and allocation traces | One-to-four humans; optional Jones in the one-human path; selected targets versus zero scores and common resource allocation explicit |
| Explain navigation, functional layout and actions | [Town/layout](../original-game/town-and-screen-layout.md), destination catalogue, thirteen entry methods, screen-study recipes | Town ring, central location dialogs, contextual controls, nested returns, progress/system/finish families documented; final pixel fidelity remains bounded |
| Extract compiled logic rather than rely on broad gameplay | [Decoder/coverage](../rules-audit/bytecode-verification.md), native interpreter notes and original resource hashes | All69 scripts decoded; selected substantive rules traced from their actual instructions, with unknown/dynamic cases retained |
| Explain time, rotation, preparation and completion | [Lifecycle](../rules-audit/bytecode-weekly-opponent.md), [entry/clock/score/save flow](../rules-audit/bytecode-flow-and-persistence.md), [native travel order](../rules-audit/dos-travel-ordering.md) | Ordered effects, week1 exception, partial final actions, residual clock, two stored-score gates and placement/continuation boundaries explicit |
| Explain employment and education progression | [Employment](../rules-audit/employment.md), [education](../rules-audit/education.md), actual37-job/11-course records | Applications, qualifications, failures, raise memory, clothing, work growth, enrollment, credits and graduation documented |
| Explain ordinary shopping, needs and possessions | [Needs](../rules-audit/food-and-housing.md), [clothing](../rules-audit/clothing-lifecycle.md), [inventory](../rules-audit/inventory-grouping.md), [assortment](../rules-audit/discount-assortment.md), [used stock](../rules-audit/pawn-used-stock.md) | Food/storage/illness, grade decay, grouped metadata, retained empty records, stock persistence, pawn expiry/ownership and recurring consequences documented |
| Explain finance and economic swings | [Finance](../rules-audit/goods-and-finance.md), [lifecycle](../rules-audit/finance-lifecycle.md), [investments](../rules-audit/investment-transactions.md), economy and [native frame finding](../rules-audit/economy-frame-semantics.md) | Contracts versus offers, bank/loan/rent flags, unit trades/fees, layered readings/shocks and material floppy/CD differences documented; long-run balance not measured |
| Explain all identified ordinary Happiness modifiers | [Catalogue](../rules-audit/happiness-catalogue.md), action/event manifests and whole-package inventory | All76 identified literal helper sites map exactly to47 action and29 event sites, with gates, recipients, skipped nominal branches and bounded writer search |
| Account for computer-player planning and execution | [Opponent policy](../rules-audit/computer-opponent.md), [all-destination routing](../rules-audit/bytecode-ai-actions.md), selected native/package quirks | Source-based priorities and market privileges plus package dispatch/selected arithmetic are distinguished; exhaustive dynamic parity is not claimed |
| Preserve provenance and rebuild local discovery | [Source register](../discovery/source-register.md), asset/script/native rebuild guides and input hashes | Website edition, bundle checksum, pinned comparison sources, research tools and local-only originals identified |
| Preserve evidence limits and design ownership | Domain evidence labels, [readiness/choices](rules-readiness.md), decisions and proposal brief | Original quirks are findings; successor fixes, content, devices, privacy, RNG/save model and scope remain explicit choices |
| Save completed work in the requested repository | Coherent commits on main, remote-tip check after publication, ignored-original audit | Analytical notes/metadata/tooling are publishable research; original bundles, assets, scripts and native disassembly are excluded |

This review finds the ordinary game domains and structural screen families represented. The fresh-state, clothing, food-category, assortment and consolidated Happiness gaps identified in the final review are now supplied. It does not infer that every rare execution state has been enumerated.

## Walkthroughs the reference now supports

These are static contract walkthroughs, not new playtest results:

- **Opening:** choose independent goals, allocate common starting resources, run first preparation, travel to the agency, apply, buy any required clothing and work. Fresh setup and later handover clock routes are distinguished; initial market quotes are not assumed to remain100.
- **Progression:** enroll, attend eligible courses, retain progress/equipment-credit snapshots, graduate and qualify for better work. Final partial lessons and refused actions use their recorded rules rather than a universal full-cost gate.
- **Upkeep:** advance a participant's turn through weekend, food/storage, clothing, obligations and notices. Pay rent, extend or move using separate duration/debt flags; loan due-week payment flags are not replaced by calendar wording.
- **Shopping and finance:** revisit an unchanged six-product assortment, receive grouped stock, take per-category or repeatable bonuses, transfer savings, trade one unit, redeem or buy forfeited stock. Cache refresh, ownership changes and price history have distinct ordered effects.
- **Economic setback:** update indices and prices for the incoming participant, apply eligible mood/asset/news effects at their recorded stages, then apply crash job consequences to the explicitly selected unfinished players. Another participant's resources can change outside their own active turn.
- **Finish:** compare stored scores at the documented start-turn gates, run presentation/second gate, record placement and continue remaining participants. A final action filling a visible indicator is not an invented immediate finish trigger.

## Known limits carried into planning

The following are recorded fidelity/validation questions, not missing default rules to fill silently:

- No complete original DOS/emulator execution equivalence, arbitrary restored/aliased/corrupt state proof or exhaustive signed-word overflow model. Selected money-boundary discrepancies are documented rather than normalized.
- No full RNG call-order/replay reproduction or measured native frequencies. The native generator/scaling is identified; native saves exclude its seed. Browser filesystem durability and a native save roundtrip remain untested.
- AI arithmetic is not wholly package-verified, despite detailed published-source policy and all-destination action routing. Full win-rate, demo/CD and rare fallback behavior remain separate.
- Screen studies are partial analytical compositions. Exact focus, typography, palette transitions, animation, audio playback and every flavour line are not reproduced. Recorded gameplay observations cover only their stated visible subsets.
- Long-run economic distributions, family comprehension and eventual play balance remain validation/design work. These do not justify changing the original rules during documentation.

[Rules readiness](rules-readiness.md) and the [validation backlog](../rules-audit/validation-backlog.md) retain focused follow-ups. Require additional evidence where a future keep/change decision depends on one of those limits. A requirement for bit-identical emulation would need a further specification and proof beyond this planning reference.

## Next planning task

Review the evidence-backed original with the owner and produce the [keep/reskin/change specification](follow-up-original-first-iteration.md). Give each proposed departure a purpose and player-visible effect; preserve humour, simplicity, economic swings and nearly original mechanics as the baseline. Agree the updated town/content/art examples and rules-version policy, then settle React/TypeScript architecture and the first playable slice. This handoff does not start that application work or approve those choices.
