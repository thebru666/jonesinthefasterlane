# Computer opponent: Jones policy and execution

Research date: 2026-10-15. Reference: DOS floppy **1.000.060**. Status: **partial script audit**. The original detailed tables below are **SCRIPT**, from sluicebox's published decompilation at commit `870a8015b689474484bf3d8b41416956d4315432`. The 2026-10-16 [actual-package trace](bytecode-weekly-opponent.md#ai-b01-policy-location-controller-and-shared-action-are-separate-layers) independently verifies bounded policy/execution anchors, difficulty entry/bounds, privileged trend inputs and two suspect branches as **BYTECODE**; it does not promote all table entries or establish whole-source equivalence. No controlled opponent scenarios were run. Adaptation mapping for every rule remains **undecided**. This describes the original rather than approving a new AI design.

Jones is an ordered, stateful heuristic: first address work and survival, then career development, then discretionary goals and investment. He selects a destination and action flags, travels on the board, and has location-specific scripts issue keyboard events to the same buttons a person uses. The policy includes random choices and direct access to internal economic trends. Calling it simply “a human player with automated clicks” would conceal those information and planning differences.

## AI-001: activation, difficulty and goal allocation

Computer control uses `playing == 29`; the challenge setup separately marks `playingAsJones`. Supported challenge setup is one human plus Jones; demonstration is a separate computer-controlled route. See [original setup](../original-game/setup-multiplayer.md).

The three settings call the same target allocator with offset `d`:

| Setting | d | Intended Jones total relative to human total |
| --- | --- | --- |
| Take It Easy | +10 | +40, capped at 400 |
| Play Fair | 0 | Same total |
| Go For Broke | −10 | −40, floored at 40 |

Let human targets be `W,H,E,C` and `T = clamp(W+H+E+C+4d,40,400)`. First set Jones wealth `Jw = clamp(W+d,10,100)`. Let `R=T−Jw`, `lo=max(1,trunc(R/30)−2)`, `hi=min(10,trunc(R/30)+2)`. Draw happiness and education independently as `10×Random(lo,hi)`. Career receives the remaining total, clamped to 10…100. Any excess/shortfall is redistributed in tens among wealth/happiness/education: the random selector gives wealth one outcome, happiness two, and education two, retrying when a selected category is already at its limit. Thus Play Fair does not imply identical four-category targets. Targets affect later stop/buy/study decisions even though the destination controller has no separate difficulty parameter.

An independent [allocation arithmetic check](../../artifacts/rules-audit/ai-goal-allocation-check.json) enumerated all 30,000 human-target/setting combinations and every permitted happiness/education draw pair: random intervals were valid and sufficient redistribution capacity existed in each case. This checks the formula and bounds, not original SCI execution or random-loop timing. Regenerate with `python3 tools/research/check_ai_goal_allocation.py` from the repository root; the [independent checker](../../tools/research/check_ai_goal_allocation.py) uses only Python standard-library modules.

No setting-dependent wage multiplier, free cash, extra time, superior hiring chance or alternate strategy switch was found in the examined challenge allocator, destination policy and location controllers. This is a scoped negative finding, not proof that every script is free of special treatment.

Evidence: [select4 target allocator](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/select4.sc#L20), [difficulty buttons](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/select4.sc#L333), [room1 computer turn](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L1374).

## AI-002: destination selection and action queue

`WhereShouldIGo` (script 300) returns the **first applicable** destination. `global403` stores a diagnostic branch number; it is not a difficulty level. `global407`, `global409`, and `global410` carry action codes; the shared membership helper accepts a match in any of the three. `global408` normally carries a count or money target, initially 1. Some fields are reused: university scheduling stores an encoded travel/time budget in `global410`, so these are not a clean general-purpose action queue.

| Code | Meaning in examined consumers |
| --- | --- |
| 1 | Work shifts |
| 2 | Food |
| 3 / 4 / 5 | Find job / ask for raise / seek better job |
| 6 | Relax at home |
| 7 / 8 | Rent payment or housing move / request extension |
| 9 / 10 | Pawn / redeem |
| 11 / 12 / 13 | Work clothing / reference books / lottery tickets |
| 15 / 16 | Appliances / education |
| 17 / 18 | Obtain needed cash / deposit surplus |
| 19 / 20 | Buy / sell investments |
| 21 / 22 | Loan payment / repeated withdrawals |

Code 21 has a bank consumer but no assignment in the inspected destination controller. Code 14 is absent from this controller. Do not invent missing policy branches from numerical gaps.

Board movement invokes the selector when the destination is invalidated. The shared dialog controller resets the destination and reevaluates before leaving a location; if Jones chooses the same location and time remains, it loops there. Work-button events invoke the shared work routine, not a duplicate pay calculation. Delay values such as `cycles=60` are presentation scheduling, not 60 hours of game time.

Evidence: [selector initialization](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/WhereShouldIGo.sc#L117), [action membership helper](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/Main.sc#L977), [shared dialog controller](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/DialogScript.sc#L12), [normal bank work button](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/bank.sc#L657).

## AI-003: cached information, travel and affordability estimates

Before choosing, Jones derives these values from his own current state:

- `happyDone`: happiness meets its target. `onlyMoneyLeft`: wealth is below target while happiness, education and career all meet theirs.
- Cash helper: high cash word means **32767** for comparisons; negative low cash means zero. Bank cache: high bank word means **2000**, otherwise the low balance. These are planning proxies, not the true full balances.
- Food destination: market (place 3) with refrigerator (item 21), otherwise fast food (place 10). Nominal food budget is respectively 55 or 65, repriced by the goods helper. Any positive food quantity in items 2–5 counts as available; otherwise item 1 quantity is used.
- Clothing budget: business/leisure/casual nominal 295/125/73, repriced using the goods helper.
- Pawn liquidity estimate: sum, for positively owned durables, of `trunc(4×priceHelper(goodsReading,pricePaid)/10)`. Redemption sums use items with attribute mask `0x0018`; the minimum individual redemption is also cached. The pawn estimate does not establish that every estimated item can actually be pawned in a particular visit.

The route estimator sums shortest ring distances between place indices on a **170-step** perimeter, choosing `170−distance` when the direct difference exceeds 85. It adds two hours' worth of ticks per leg. Multi-stop helpers compare visit order or permutations; nearest-choice ties retain the first listed destination. Let `Q=global475`, `h=elapsed hours`, `r=residual movement ticks`, and `D=estimated future ticks`: a plan passes only if `h+trunc((r+D)/Q)<60`. Thus estimated arrival at exactly 60 fails. `Q` is set from marble movement speed ×14. This is a heuristic feasibility estimate, not proof every queued activity will finish.

For several survival plans, required shifts are `max(1,ceil((requiredCash−cash)/(8×wage)))`; route cost adds six hours per shift. The estimate uses full gross wages, while actual pay still goes through partial-shift and garnishment rules. See [TIME-001–007](time-and-actions.md).

The “can obtain funds” helper accepts a high liquid-asset word, liquid assets at least the target, **or liquid assets plus rent owed plus loan balance at least the target**. This is how the policy judges funding availability; do not replace it with a generic available-cash test when describing this original.

Evidence: [route and funds helpers](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/WhereShouldIGo.sc#L15), [cached values](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/WhereShouldIGo.sc#L138), [cash proxy](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/Main.sc#L1069), [movement tick scale](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L1315).

## AI-004: ordered destination priorities

This table preserves the selector's order. Numbers are the original diagnostic branch values for tracing, **not** new rule IDs. A row can contain several ordered alternatives; earlier rows and earlier successful alternatives preempt later ones. Place numbers follow the [town map](../original-game/town-and-screen-layout.md).

| Order / branch numbers | Trigger and selected plan |
| --- | --- |
| 1 | No wage and employment not visited this turn: employment (6), find a job. |
| 2–11 | Rent-office visit not yet made and week divisible by four or rent account `leaveOpen`: arrange rent with food and/or expiring clothes when affordable; buy clothes alone if needed and affordable; choose food if cash is below rent but covers food; otherwise pay rent if affordable. Failing that, work enough shifts for rent if route/time allows; obtain bank cash if assets and time allow; request extension if not tried and cash plus three gross shifts covers rent; finally pawn if estimated proceeds cover shortage. Multi-destination plans initially choose the nearest listed stop. |
| 12–14,16–20,220–222 | Clothing expires within one week or outfit unsuitable: with zero weeks, first obtain bank cash, pawn, or buy clothes. Otherwise combine food/clothes where possible, using work, bank or pawn to finance the combined budget if needed; then try clothes alone and bank/pawn fallbacks. The repeated diagnostic 222 purchase condition follows a previous identical cash test; [AI-B03](bytecode-weekly-opponent.md#ai-b03-two-suspicious-policy-branches-are-real-package-logic) confirms it is shadowed in ordinary package execution. |
| 21–27,224–225 | No food: if short, work, withdraw/finance, or pawn with route-time tests. With cash >1500 and refrigerator, may combine three first-work shifts and a deposit; otherwise combine three first-work shifts and food. Then try deposit plus food or food alone. |
| 28 | Ask for raise: fewer than two raises, dependability ≥ minimum+10+5×raises, current goods-adjusted base wage exceeds current wage, employment not visited this turn. |
| 29 | Seek better job: no unresolved education rejection, experience ≥ job maximum, dependability ≥ minimum+10, employment unvisited, maximum experience <80 and current wage below goods-adjusted nominal 25. |
| 30 | If education is not flagged as insufficient, work toward the next experience/dependability threshold and employment visit when time permits. Shift target starts at 1, otherwise the experience gap, and may be reduced to the smaller dependability gap; reserve eight extra hours in the route estimate. |
| 31–36,334 | First successful work not yet done this turn, employed and appropriately dressed: combine three shifts with redemption when eligible and time permits; relax if relaxation is exactly 10, otherwise combine work and home if below 17; then a 1/2 random branch combines work and study if possible (or just work); then combine work with appliances if cash >1500, items missing, happiness unfinished and route permits; otherwise three shifts. |
| 37 | Relaxation <17 and a feasibility check passes: home. **Package-confirmed mismatch:** passes current place and home as separate arguments to a helper that reads only its first parameter as estimated ticks; this is not the expected route-distance calculation. See [AI-B03](bytecode-weekly-opponent.md#ai-b03-two-suspicious-policy-branches-are-real-package-logic). |
| 38 | Not only money left, redeemable goods exist, cash covers cheapest redemption and route allows: pawn shop (12), redeem. |
| 39 | Not only money left, cash >800, discount unvisited, 1/3 random gate and at least one reference book missing: discount (11), books. |
| 40 | Cash >800, 1/2 random gate, appliance missing, appliance shopping not blocked and happiness unfinished: appliance shop (8). |
| 41 | Cash >1500 with refrigerator: bank (4), deposit. |
| 42 | Cash >750 or cached bank >750, main trend >0, investment reading <80+15×main trend, no purchase this turn: bank/broker, invest. If cash <750, plan up to ten withdrawals first. |
| 43 | Investment assets beyond the fixed-price investment are nonzero, main trend <−1, no trend-sale this turn: bank/broker, sell negative-trend holdings. |
| 44 | Fewer than 11 degrees and route allows: study if an enrollment is unfinished, or cash >400 and either a 3/4 random gate while more than money remains, or an education-rejection flag. |
| 46 | Employed and dressed, route allows: work three shifts. |
| 47 | Already at university, elapsed+6 ≥60, fewer than 11 degrees, enrollment unfinished or cash >400, and more than money remains: study without the usual route feasibility gate. |
| 48 | Already at workplace, elapsed+6 ≥60: work a final shift. Actual shared routine handles closing-time/partial-shift boundaries. |
| 49 | Final fallback: return home and relax. |

Evidence: [survival priorities](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/WhereShouldIGo.sc#L231), [career/first-work priorities](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/WhereShouldIGo.sc#L759), [discretionary/final priorities](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/WhereShouldIGo.sc#L932).

The priority order is significant: having only wealth left suppresses some redemption/books/study, but not every discretionary branch. Having happiness complete suppresses appliance objectives, but does not universally prohibit spending.

The later [all-destination action trace](bytecode-ai-actions.md) inventories the actual controllers and shared dialog route for all thirteen destinations plus broker, including selected computer confirmation shortcuts. Candidate-ranking and other unexamined strategy arithmetic below retain SCRIPT status.

## AI-005: employment and work execution

At employment, Jones examines candidate jobs in descending **catalogue index**, not a global best-pay sort. Starting limit is all 37 entries; unsuccessful attempts continue lower in the catalogue. Candidate screening requires the listed experience and dependability, an improvement over wage (or a different job within one unit of its wage comparison), required degrees if a previous education rejection is flagged, and a clothing/food affordability buffer. That buffer is repriced nominal food 65 plus clothing 0/125/295 for casual/leisure/business uniforms; it is not the vacancy roll. The wage comparison uses the catalogue wage values, so its ranking should not be described as sorting all live offers. Actual applications still invoke the normal hiring logic, including qualification checks, vacancy randomness and the per-visit rejection list. An unsuccessful degree check sets `notEnoughEd` and influences future study. A raise selects the current workplace/job key.

The shared dialog handler issues the planned number of `w` events while time remains. Near dialog exit, if the current place is a workplace, Jones is dressed and has not yet worked successfully this turn, it inserts **three shifts, or four when only money remains**. A successful shared work action clears the first-work flag. This opportunistic insertion can differ from the originally selected objective.

Evidence: [candidate scan](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/employment.sc#L623), [normal qualification/vacancy checks](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/employment.sc#L129), [shared work scheduling](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/DialogScript.sc#L30), [actual work](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/n108.sc#L100).

## AI-006: food, clothing, housing and relaxation execution

- Market food objective buys one/two/four weeks for cash <200 / <400 / otherwise. Subsequent states may buy another four weeks if cash >800, and a freezer permits an additional four-week purchase under that cash condition. All are actual shop-button events, with normal storage/payment checks.
- A market visit also has a 1/4 newspaper opportunity before closing, then a 1/3 lottery opportunity when cash ≥100. Lottery count is `min(5,Random(1,trunc(cash/100)))`; it repeats the ticket action that many times.
- Fast-food choices depend on completed happiness, cash >750, hamburger affordability and random selection; once happiness is done it chooses key 4. Optional treats have a 1/5 gate with cash >750 and happiness unfinished. Exact key-to-item effects are part of the food audit, not established from controller names alone.
- Clothing matches the required uniform. It can also buy expiring clothing opportunistically during a visit if affordable and not already purchased there.
- Rent objective can replace payment with a move: from cheap housing, choose security if both refrigerator and stove are owned with cash >600, or security's new price is below stored rent. From security, choose cheap housing if cheap's new price <stored rent−200 **and** security's new price <stored rent−100. Otherwise pay rent. It also pays garnishment opportunistically when cash exceeds the payment by >300.
- At home, the controller repeats relax while time remains and its counter is nonzero; the selector's default count is one. Repeated reevaluation can lead to further visits/actions.

Evidence: [market actions](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/market.sc#L552), [fast food](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/fastFood.sc#L486), [clothing](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/clothing.sc#L413), [housing actions](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/rentOffice.sc#L836), [home](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/lowcost.sc#L172).

## AI-007: education and shopping execution

University first prefers an already active displayed course, scanning backwards through available course icons; otherwise it picks a random displayed candidate. If enrollments equal degrees and enrollment fee is affordable, it buys enrollment before study. This uses normal course/enrollment buttons; it does not grant degrees directly. For study as a secondary objective, default lesson budget is ten, possibly reduced by an encoded route budget. After incidental university work it schedules two study actions when education is below target or flagged as insufficient for work, otherwise one. Exact lesson count can still be interrupted by closing or course completion.

Appliance objective prioritises missing affordable refrigerator → stove → colour TV → microwave → stereo → freezer → VCR. An opportunistic later state, with cash >800, uses that order but inserts hot tub → computer before VCR. Missing-item selection in the destination policy includes all nine (21–29), while the first purchase state omits hot tub/computer. If no candidate is available it sets a block flag; an eligible item clears it. These flags do not imply guaranteed purchases.

Reference-book objective checks atlas first, then dictionary and encyclopedia, with the latter two additionally requiring cash ≥800. A discount visit can also buy up to two event-ticket items under repeated 1/2 gates while cash >800 and happiness unfinished. This is discretionary behaviour beyond the main destination label.

Evidence: [university controller](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/university.sc#L843), [appliance affordability helper](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/appliance.sc#L73), [appliance order](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/appliance.sc#L676), [discount controller](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/discount.sc#L893).

## AI-008: banking, investment policy and privileged inputs

The normal bank controller deposits repeatedly while cash >500 for a deposit objective, withdraws repeatedly for a counted withdrawal objective, or obtains a requested money amount by first withdrawing deposits, then selling investments, then applying for a loan once per turn. The money target uses the selector's cash proxy and cannot be assumed to equal actual available credit. The bank contains a loan-payment action consumer; no corresponding destination-plan assignment was found in script 300.

Broker purchase considers the five variable-price holdings and chooses an affordable one with the highest internal market **trend**, preferring ties randomly with a 1/3 replacement gate. If that best trend is <1 it selects the fixed-price investment; if best is exactly 1 it switches to fixed-price with probability 1/6. It buys repeatedly with a reserve threshold of 800 when week mod four is 3, otherwise 500. The comparison is made around repeated events, so this is a stopping heuristic rather than a guarantee the final cash balance stays above the reserve.

For a requested cash amount, the broker selects owned investments with the weakest trend, with the fixed-price holding treated as trend zero, and sells toward the target. For the `−1` trend-sale mode, it cycles variable holdings with trend ≤−1 and sells their shares. The purchase and trend-sale suppression flags are set by successful controller action paths and reset at turn start.

**Information difference:** the policy directly reads main trend `global315`, investment reading `global308`, and individual market trends `global318…322`. The displayed economy/prices are not equivalent to exposing all those internal state values. There is no evidence here that Jones reads future random draws, human private inventory or future prices; equally, this audit has not exhaustively searched every game script for such access.

Evidence: [bank controller](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/bank.sc#L716), [broker decisions](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/broker.sc#L574), [destination investment gates](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/WhereShouldIGo.sc#L1000), [trend meanings](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/economicIndex.sc#L221).

## AI-009: actual special handling and shared-rule limits

Confirmed special handling includes automated confirmation: Jones accepts the pawn offer without the human confirmation prompt, and moving apartments clears prepaid old rent without asking whether to forfeit it. These paths still execute the ordinary transaction afterward; they do not demonstrate a discount. The bank also automatically accepts approved loans ([bank.sc#L471](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/bank.sc#L471)), and university enrollment bypasses human confirmation ([university.sc#L730](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/university.sc#L730)). Appearance and cursor behavior also differ for the computer marker.

The inspected work, job, shopping, enrollment and bank controllers generally dispatch the normal UI actions. Common start-turn processing initializes/reset flags for players without a separate Jones wage/time branch in the examined portions. This supports shared-rule execution, while the financing estimates, internal market information and confirmation shortcuts are genuine differences. It does **not** establish exhaustive fairness or absence of every exception.

Evidence: [pawn confirmation shortcut](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/pawnShop.sc#L775), [cheap housing confirmation](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/rentOffice.sc#L519), [security housing confirmation](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/rentOffice.sc#L643), [turn-reset flags](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L65).

## Reproduction backlog and limits

No scenario below has been marked OBSERVED. Record setup/save hash, cash/needs, week, goods/trend readings where available, elapsed time, destination branch and resulting UI actions. Fixed RNG state or repeated trials are required for probabilistic paths.

| Scenario | Expected from this audit / boundary to settle |
| --- | --- |
| AI-R01: identical human goals, each challenge setting | Jones target total equals clipped human total +40/0/−40; per-category redistribution stays 10…100 and sums to that total. Test totals 40 and 400 too. |
| AI-R02: unemployed, hungry, rent week | Employment branch preempts survival; after attempt, rent/food/clothes plans proceed in documented order. Check failure and no available job. |
| AI-R03: rent deficit, arrears, low/high-word balances | Work/bank/extension/pawn order; compare gross-wage estimate with actual garnished pay; bank proxy 2000 and cash proxy 32767. |
| AI-R04: route arrival just below/exactly 60; equal distances | Strict feasibility boundary, first-candidate tie, multi-stop order, and whether destination reset/current-place fields remain coherent. |
| AI-R05: relax <17 away from home | Trace branch 37's suspicious extra argument; determine if it selects home despite an infeasible actual route. |
| AI-R06: partial final work/study | Branches 47/48 invoke shared closing/partial-action rules, including zero-time boundary; test when already at destination. |
| AI-R07: happiness done / only wealth left | Observe suppressed appliance/books/redemption/study paths, four incidental shifts, and remaining lottery/treat behavior. |
| AI-R08: investment trends and reserve boundaries | Confirm best/worst trend choice, fixed-price fallback, 500/800 reserve handling, cash exactly 750, and once-per-turn buy/sell flags. |
| AI-R09: employment and education rejection | Descending catalogue fallback, vacancy rejection, degree requirement flag, raise count and dependability threshold. |
| AI-R10: move and pawn confirmations | Confirm no click is required, prepaid rent forfeits normally, normal prices/costs apply. |
| AI-R11: shopping and active course selection | Distinguish first planned purchase from later opportunistic purchases; confirm omitted hot-tub/computer first-state behaviour and study counts. |
| AI-R12: demonstration versus challenge, other editions | Do not assume equal starting resources or policy details; compare demo setup and CD controller separately. |

Known uncertainty: unexamined published-decompiler control flow and omitted-argument semantics still need checks. AI-R05's extra-argument mismatch and the repeated clothes test are now verified in package bytecode; their visible consequences remain unobserved. No statistical win-rate/difficulty evaluation, full demo audit, CD policy comparison, exhaustive all-script privilege scan or controlled original-game trace has been performed. Stable IDs AI-001–009 describe this pass; AI-R01–12 are future validation scenarios, not passed tests.
