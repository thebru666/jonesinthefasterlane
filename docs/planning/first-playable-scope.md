# First playable: a complete small life loop

2026-10-17. **PROPOSAL — concrete scope for review before building.** The owner has directed continued planning and positively received the Learning recommendation. That supports developing this pack; exact scoring, defaults, prototype scope and application implementation are not approved by “keep going.” Confirmed direction remains [decisions](decisions.md).

The intended deliverable after build authorisation is a local browser prototype in React/TypeScript: one person can start unemployed, find work, manage food/clothes/rent, choose transport, develop through work or Trade School, buy a useful possession, save/resume and finish a short four-goal race. It should answer whether the game feels right, rather than claim full original-game coverage or a public release.

## Recommended review baseline

| Area | Proposed first-slice choice | Why |
| --- | --- | --- |
| Mode | One human; no computer opponent or multi-human setup UI yet | Keeps the first test focused; actor-specific state and shared action rules remain required for later modes |
| Devices | Desktop and landscape tablet, mouse/touch/keyboard | Test legibility and handover-ready layout before a separate phone design |
| Town | Working15-stop map A; seven locations have services in this preview | Tests real routes while keeping full town ambition visible |
| Goals | Wealth10, Happiness20, Career30, Learning10 as the initial short-preview preset | Both work-first and one-course routes can be exercised; measured duration remains unknown |
| Goal customisation | Show the four preset targets and plain definitions; full custom setup can follow | No claim the preset is balanced or a30–45-minute game |
| Starting state | Cash200, unemployed, low-cost home, rent stock3, casual stock6, no food/durables/vehicle/courses, work-time0 | Start from a real opening, unlike the analytical employed checkpoint |
| Learning | Use the [recommended scoring/growth contract](learning-goal-proposal.md) as a proposed prototype baseline | Removes classroom dependency without another visible meter |
| Money and scores | Whole-dollar money; atomic adopted score updates; inspection panels read-only | Applies the endorsed consistency principles; exact compatibility detail remains reviewable |
| Transport | Walking, town-wide bus, purchasable bike and car, full quote before commitment | Makes transport a real part of the slice; no fuel/timetable/resale system |
| Finish | Check all four goals at the adopted incoming-turn gate | Retain delayed victory; do not win on the purchase/work button |
| Persistence | One automatic stable checkpoint and manual export/import; explicit version/seed | A small game still needs reliable continuation |

Preset Wealth10 means1000 in adopted liquid-asset units, not a thousand-dollar possession collection. Learning10 can come from20 full work shifts, one first qualification, or a mixture under the proposed formula. Career30 requires actual employed dependability24 under the retained stepped formula; it is not simply a job title. Happiness needs its own deliberate actions/outcomes.

The preset does not guarantee a rent-week encounter before winning. Acceptance uses both a normal fresh-game journey and a controlled rent-due scenario; do not introduce a hidden minimum-week rule merely to make a test pass.

## Active places and the useful choices

| Location | Included actions/content |
| --- | --- |
| Starter Court | Relax, possessions display, Goals/Statistics/menu access; current home only |
| Civic House | Town job index, apply/raise route, rent payment and retained relevant rent-period behaviour |
| Corner Basket | Local job board; checkout and Butcher work; one-/two-/four-week groceries using the retained storage rules |
| Daily Grind / Copper Spoon | Local job board; Cook, Counter Assistant, Shift Supervisor and Venue Manager; simple hamburger/cheeseburger food choices |
| Next Chapter | Enroll, Trade School, attendance/progress, diploma and prerequisite explanation |
| Reboot | Bike/car purchase; refrigerator purchase; visible ownership information |
| Good Threads | Casual, smart/dress and business clothing, suitability, stock and replacement feedback |

The other eight places are clearly marked preview destinations. Inspecting their future role is free and cannot move the player or spend time; they do not masquerade as usable shops. Their ring positions still count when travelling between active destinations. This is a development limit, not a proposed final town with permanently empty buildings.

Nested employers/services share their physical arrival. Reopening the current destination or switching services within that site adds no trip fare or arrival charge. Work occurs at the employer, not at the civic index. An in-store application uses the same record, requirements, cost and rejection state as the index; switching boards does not give another opening roll. A clerk response should distinguish qualifications, experience, work history and openings, without hiding the true reason in early turns.

## Career content and tuning inputs

Six job records are enough for the first comparison. Use named prototype IDs separate from original numeric job IDs; the original anchors below identify provenance, not code to copy.

| Job / workplace | Proposed wage | Experience / dependability | Qualification | Clothing |
| --- | ---: | --- | --- | --- |
| Cook / Hospitality |4 |0 /10, with original recovery-job qualification/opening exceptions |None |Casual |
| Counter Assistant / Hospitality |5 |10 /20 |None |Casual |
| Shift Supervisor / Hospitality |10 |25 /25 |None |Casual |
| Venue Manager / Hospitality |14 |35 /35 |None |Casual |
| Checkout Assistant / Market |8 |20 /20 |None |Casual |
| Butcher / Market |12 |30 /30 |Trade School |Casual |

Cook, original counter Clerk, checkout and Butcher have [original employment anchors](../rules-audit/employment.md); the10/14 management roles and thresholds are new recommendations. The literal declared-dependability10 exception belongs to the retained Cook rule, not every entry job. All six included roles accept casual clothing; smart/dress and suits are optional demonstration stock, not promotion requirements in this slice. Clothing gates work; a successful application does not supply clothes. Current wages remain contracts; changing price/offer levels does not automatically rewrite them.

Trade School uses provisional base enrollment50, ten ordinary lessons at six nominal time each, unique completion and the proposed Learning reward. Preserve the original last-partial-lesson behaviour as a deliberate default, while successful work Learning/history use actual time. Show prerequisites/work-history needs honestly. Only one course is offered in the slice; this is not a replacement for the sixteen-course full-game proposal.

Transport tuning starts from the current proposal: bike120, car1200; bus3 per leg; car4 per leg plus20 on first use each personal turn. Walking3d, bikeceil(1.5d), bus2+d, car1+ceil(d/2), plus2 per distinct arrival. Map A provides the actual edges. The car can be bought if affordable; its normal campaign affordability is not assumed. A trip must fit its total cash/time quote, including entry. Provide explicit End Turn when the player wants to stop or no useful trip fits.

Food/clothes/refrigerator anchors come from the [needs](../rules-audit/food-and-housing.md), [clothing](../rules-audit/clothing-lifecycle.md) and [goods](../rules-audit/goods-and-finance.md) audits. In the initial neutral-price fixture: groceries55/100/190; hamburger79; cheeseburger89; casual73, dress125, suit295; fridge876. These are nominal original scaling inputs, not promised quotes under every economy reading. The fridge gives storage, not a new purchase-Learning reward. The short preset may finish before a fridge or car is affordable: exercise both purchases in controlled funded fixtures as well as normal play, without promising them in every winning journey. Fast-food coverage, spoilage, first-category Happiness and clothing decay follow the specifically adopted audited rules.

Phone information, laptop/home work, extra training branches and the new clinic/banking careers remain full-game direction, **not requirements to implement this slice**. The prototype should not sell a laptop with an implied home-working benefit when its included jobs are physical roles.

## Economy, upkeep and recovery

Include the audited floppy economy's normal8-layer incoming-turn update for implemented wages, goods and rent offers; keep original C07/C08 behaviour as the proposed baseline. Use seeded randomness separate from animation. Preserve the original ordering for relevant stages rather than applying needs after arbitrary clicks. Week1 exceptions and incoming finish gates remain explicit.

Implement the slice-relevant effects: food/storage/spoilage, hunger/doctor interruptions, clothing stock and suitability, rent/arrears/garnishment, relevant work warnings/dismissal, economic job shock, graduation and retained first-turn exceptions. The actual player-facing feedback for an automatic doctor interruption does not imply the Clinic is an active employer in this slice.

Full weekend/lottery/ticket pools, appliance breakdown/theft breadth, pawn/broker/loans and all thirteen original destination controllers are deferred. Omitting those is an explicit prototype rules version, not original equivalence. Do not run an event that asks for an absent service without defining its current resolution. A data/rules coverage list should distinguish implemented, deliberately inactive and pending branches.

**Recovery is a required check:** Cook remains the original reliable fallback when its actual requirements/clothes permit. Preserve the relevant audited emergency-clothing support if no usable clothes and too little money would otherwise prevent recovery; reproduce its predicates rather than invent an unconditional grant. Add a controlled rent/food/clothes setback case to ensure the available actions offer a documented way forward. Recovery does not mean every bad choice is free or every failed application succeeds.

## Minimum screen flow

Start/New/Resume → short setup/goal explanation → incoming notices → town → trip quote → visit → action/result → visit/town → End Turn or exhausted exit → next preparation. Goals, Statistics and Menu return to their caller without spending time or drawing rule randomness. Course completion has one diploma, unique award and a visible return to the location. Finish shows attained goals/turn and New Game/Exit; no multiplayer placements UI yet.

Show prices, time, unmet requirements, current player and remaining time. A failed timed action follows its specific cost rule; do not invent a universal free-refusal rule. Allow legal zero-time purchases inside a location at exhaustion; timed work/study cannot begin at zero. Acknowledge-once feedback must not rerun a salary, diploma, rent payment or turn.

The four-goal panel uses **Learning**, with an optional explanation of work contribution and completed qualifications. Existing decorative illustrations are references; a readable interface and a small coherent asset subset are enough for the first family test. No production asset catalogue is implied by a composite image.

## Completion checks for the slice

| Journey / check | Reviewable result required |
| --- | --- |
| Fresh opening | Correct allocation; first-turn notices/quotes; a legal route to initial work, food and appropriate clothing |
| Work-first path | Earn through ordinary work and reach a promotion/Learning target with no courses; no invisible college gate |
| Practical path | Complete Trade School, build actual required work history and reach Butcher without another formal course; continuing Cook versus an intermediate job is a real choice |
| Four-goal finish | Each route can reach its preset targets and finish at the correct incoming gate; do not substitute a cash chart for this test |
| Transport | Quote/execute short and long trips; bike acquisition/first-car charge/cash failure/exact exhaustion; no animation-dependent costs |
| Useful purchase | Fridge changes food storage; bike/car changes travel; ownership is visible at home; no duplicate reward on reopening a panel |
| Rent/upkeep | Pay a due week, handle an unaffordable/extended/arrears path as adopted, replace expiring clothes and understand food consequences |
| Setback/recovery | A specified rejected opening or job shock retains correct state and offers a documented legal recovery route |
| Save/replay | Restore town and nested visit boundaries with the same time, stock, qualification set, Learning work total and next rule outcome |
| Guarded interactions | Double click, repeated acknowledgement and view/animation changes cannot duplicate cash, score or preparation |
| Future modes | A controlled two-actor headless fixture checks actor separation/rotation/economy update; not a claim of a playable multiplayer or AI mode |
| Family review | Each child and an adult can identify job versus workplace, interpret rejection, compare transport, explain Learning and recognise the finish rule; record help and actual session duration |

These are future acceptance criteria, not completed tests. If the new Learning growth rule changes the earlier paper paths, update the expectation rather than forcing the engine to reproduce the old cash worksheets.

## Build sequence after authorisation

1. Translate this adopted subset into plain TypeScript state/actions with versioned content and deterministic rule draws. The first milestone is a headless fresh-work/turn trace, not a complete UI.
2. Add Learning, work-first/course progression, relevant economy/needs and controlled finish/recovery scenarios; verify actual-action ledgers.
3. Build the town/visit/quote/goal panels and stable persistence; use the existing original-style direction with a small asset subset.
4. Run family sessions, adjust explanations and tune numbers only with observed evidence. Then add shared-device/AI and full content in later agreed increments.

Use the [architecture proposal](architecture-and-validation-proposal.md) for separation of simulation, presentation, opponent policy and storage. No leaderboard, account service, online multiplayer, public deployment or application code is part of **this planning step**.

## Review summary

The concrete recommended choices are: Learning scoring/growth contract, fifteen-stop map A, one-human prototype with the seven active places above, six jobs/one course, short-preview10/20/30/10 goals, all four transport choices, fridge/food/clothes/rent and relevant economy/recovery, plus stable saves. These can be reviewed as one coherent scope; exact balance is not presented as proven. Existing data, diagrams and mockups remain supporting artifacts, not independent feature approvals.
