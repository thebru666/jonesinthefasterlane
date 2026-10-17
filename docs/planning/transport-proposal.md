# Transport: time, money and a town worth crossing

2026-10-17. **PROPOSAL — tuning and detailed behaviour are unapproved.** The owner has explicitly requested slower walking and a larger role for transport, including buying a bike, catching a bus and driving at a cost. Those directions are confirmed; the particular rules and figures below are recommendations for review, not findings about the original.

Read alongside the [project brief](project-brief.md), [draft specification](2.0-draft-specification.md) and [compatibility choices](compatibility-proposals.md). This proposal would **replace C03's fixed original-speed travel recommendation**, rather than sit on top of it. The [original native travel audit](../rules-audit/dos-travel-ordering.md) remains unchanged as the historical reference.

## Recommended small system

Keep the 60-unit turn and the compact town. Make walking a real opportunity cost, provide affordable public transport from the start, and let ownership buy convenience. A player should think “Is this journey worth the bus fare?” without managing fuel gauges, bus timetables or tyre condition.

Use a logical route graph independent of artwork, screen size and animation. For the worked examples, the town has 13 destinations on a ring, with one distance unit per neighbouring pair; shortest-route distance `d` is therefore 1–6. Equal edge lengths are an illustrative simplification, **not** an original fact or a commitment to the final town geometry. An alternative arrangement must publish its logical distances before tuning these costs.

| Mode | Access and acquisition | Illustrative travel time | Illustrative cash cost | Strategic role |
| --- | --- | --- | --- | --- |
| Walk | Always available; everyone starts able to walk | `3 × d` | Free | Reliable fallback; nearby errands remain practical |
| Bike | Own one; base purchase $120 | `ceil(1.5 × d)` | No per-trip charge | Useful early investment, especially for repeated nearby trips; no wear meter |
| Town bus | Available from every destination; no purchase | `2 + d` | $3 per trip | Good longer-distance travel before owning a vehicle; the two time units represent waiting/boarding |
| Car | Own one; base purchase $1,200 | `1 + ceil(d / 2)` | $4 per trip, plus $20 on the first car trip of each personal turn | Fastest longer journeys; substantial upfront and operating costs, so ownership is optional |

**All figures are provisional illustrative dollars/time units.** A time unit is a game resource, not an asserted real-world hour. Existing work, study and entry costs remain the comparison points. Entry still costs a separate two units; the travel formulas do not conceal it.

Treat the car's $20 first-use amount as one simple operating package, covering that turn's registration/insurance/maintenance abstraction. It is **not an automatic weekly bill**: a player who does not drive pays nothing, and an unaffordable package does not create another debt system. The $4 trip charge covers fuel/parking. No fuel purchase action, parking search, licence course, accident roll, repair meter or randomly cancelled bus is recommended for this first version.

Initial vehicle purchase quotes can use the existing goods-price economic layer; do not add a ninth transport index. The $120/$1,200 amounts are base prices, with the actual current quote visible before purchase. Keep fares and operating costs fixed during the first comparison playtests so that the added decision is understandable; changing those with the economy is a later explicit balance choice.

## Acquisition and interface

Offer bikes in an existing shop/workshop role and cars through a nested vehicle listing at an existing destination. Do not require another board building just to support a purchase. The final modern town proposal should select the host locations. One bike and one car per player is enough; they are separate transport ownership records, not additional copies of a household appliance group.

Keep the opening allocation unchanged apart from the availability of public transport: no owned vehicle and $200 cash. A base-price bike is immediately attainable but competes with food, clothes and a cash buffer. A bus ticket is bought as part of a trip, not as an item to stockpile. Vehicles give no automatic Happiness, Career or Education reward; their time benefit is their initial purpose. A transport resale/used-vehicle market is deferred from this small system rather than assumed to inherit the original pawn rules.

Selecting a destination opens one small choice panel with available modes, exact time, total cash charge, and time remaining after arrival/entry. Keep the last successfully used mode selected where legal; changing the selection is free. A destination preview might read:

> **Town bus — 7 time + 2 entry, $3. Arrive with 23 time left.**

The car row must show its complete charge: “$24 including this turn's operating package” before the first drive, then “$4” thereafter. An unavailable option says “Own a bike”, “Need $24” or “Need 9 time”; it must not silently switch mode or spend money. Show approximate route distance on the board and a clear bus/bike/car symbol, with text labels as well as colour.

## Trips that expose the tradeoffs

Illustrations assume the ring above, sufficient cash/time, and an open destination. Each total includes two-unit entry once. Car cash is shown as later-trip / first-trip charge in that personal turn.

| Trip | Walk | Bike | Bus | Car |
| --- | --- | --- | --- | --- |
| Next door, `d=1` | 5 time, $0 | 4 time, $0 | 5 time, $3 | 4 time, $4 / $24 |
| Three edges, `d=3` | 11 time, $0 | 7 time, $0 | 7 time, $3 | 5 time, $4 / $24 |
| Across town, `d=6` | 20 time, $0 | 11 time, $0 | 10 time, $3 | 6 time, $4 / $24 |

For three journeys of distances 1, 3 and 6 in one turn, including three entries:

- Walking spends 36 time and no money.
- A purchased bike spends 22 time and no trip money; the purchase itself is additional and its visit/entry must be budgeted separately.
- The bus spends 22 time and $9.
- A purchased car spends 15 time and $32 operating costs; the purchase visit is also additional.

The seven time units saved by the car over bus/bike can be valuable relative to a six-unit shift, but that does not prove it earns back its costs: the extra time must actually be spendable at a workplace, and wage, route and opening position matter. These are arithmetic examples, not a claim of tested balance.

## Proposed action boundaries and edge cases

This section deliberately chooses a simple successor contract. It is a **departure from interrupted original travel and C02's original travel/entry exhaustion cases**, while preserving partial work/study rules inside a location. The compatibility table and main specification must reflect that choice if adopted.

1. **Quote before committing.** A trip needs enough spendable cash for the full selected charge and enough remaining time for travel **and** entry. Savings are not silently withdrawn. On confirmation, validate the live state again, then commit cash, time, destination and entry together. Failure changes nothing; a double tap cannot buy two trips.
2. **No stranded travellers.** A confirmed trip always reaches the selected location. Travel animation may be skipped; it consumes no additional game time or randomness. No mid-road purchase, transfer or forced second fare is needed. The proposed initial save policy still excludes an animation in progress; its next checkpoint is the completed arrival.
3. **Exact exhaustion.** If travel plus entry exactly consumes the remaining time, arrival is valid. Existing legal zero-time transactions may still be completed there, followed by handover on Exit; timed actions cannot start. If the trip cannot fit, keep the player where they are. Provide an explicit **End Turn** control so a player with too little time to travel can finish voluntarily; this is a new interaction, not an original finding.
4. **Same destination.** Selecting the location already occupied does not create a trip, fare, operating charge or extra entry. Returning from a nested view is also free. Leaving a visit and reopening at the same board location needs a separately agreed entry rule; recommend keeping the existing location context until an actual trip or end-turn, to avoid charging an unexplained second entry.
5. **Operating package.** First successful car trip sets `carOperatingPaidThisTurn`; further car trips charge only $4. Reset the flag once at the next incoming turn for that owner. Buying a car does not waive the charge. A rejected trip, preview, save/reload or another player's turn cannot set/reset it incorrectly. If the first-use total is unaffordable, walk/bike/bus remain options.
6. **Handover and saves.** Save ownership, current destination, remaining time and the operating-paid flag in versioned logical state. Mode selection is a convenience preference, not a paid reservation. Handover never transfers a vehicle or free driving credit to another participant. Resuming must preserve the same quote eligibility and subsequent effects.
7. **Computer rival.** Use the same route distances, public prices, purchases, time checks and operating charges. Compare visible costs against reachable useful actions; do not give the rival free travel or an invisible vehicle. Different preferences can change its choices without changing the legal action rules.
8. **Ownership changes.** Vehicle resale, vehicle theft and forced repossession are not included in this initial proposal. Existing events affecting household durables do not automatically include vehicles. If any is later added, define its treatment of an already-paid operating package and recovery options explicitly.

## Protect the useful alternatives

A car should be attractive without becoming compulsory. Keep bus access universal, and require no transport type for a job or course. Walking must always reach every destination when sufficient turn time remains. A bicycle must remain useful even after bus access: it pays no repeat fares and beats the bus on short journeys. A car should save enough time across town to feel different, but should not grant extra goal points, exclusive jobs or immunity to setbacks.

Tune from a few shared opening/recovery situations: unemployed with $200; employed with little cash; studying while working; long cross-town commute; rent due and unable to drive. Compare actions that actually become possible, cash left for necessities and turns to recover. If car ownership becomes the only sensible strategy, change its price/time advantage or operating costs before adding congestion, repairs or fuel management.

## Three owner questions for the visual/content review

1. Is the proposed step up right: walking is viable but expensive in time, a bike is an early achievable upgrade, and a car is a later convenience rather than an essential life goal?
2. Should the bus be a dependable town-wide service as recommended, or should a few visible stops/routes become part of the strategic map? Stops would add access/transfer rules and need a separate simplicity review.
3. Are travel plus entry previews and all-or-complete trips preferable to reproducing the original possibility of running out of time mid-journey?

These questions are for iteration on a concrete proposal. They do not block drafting the modern town, device catalogue or art brief, and no application implementation is authorized by this document.
