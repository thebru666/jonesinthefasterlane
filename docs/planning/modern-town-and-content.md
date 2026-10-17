# Modern town and content direction

**Successor graph proposal:** [career/town v2](career-and-town-graph-v2.md) develops the accepted broader trades/professional direction. This document's37-job/11-course mapping remains a complete original-graph naming baseline; it is not the new career graph and does not supply doctor/electrician/plumber roles.

**Latest review:** [employer options, offers and useful possessions](employers-offers-and-useful-possessions.md) proposes reasons to visit employers, local notices, recruitment and functional phone/laptop benefits after owner feedback. In-store applications are accepted in principle. The tables below remain the complete original-graph naming baseline; new restaurant/clinic/depot roles would need a revised graph. Earlier restrictions on remote use describe the prior proposal, not a rejection of the owner's newer direction.

Drafted 2026-10-17. **PROPOSAL — concrete review material, not an approved content bible or application implementation.** The owner now wants transport to matter, newer locations, different job boards and devices to buy. Those are confirmed directions; the names, mappings and effects below are recommendations. This extends the [earlier content sample](content-iteration-sample.md), which deliberately offered only reskins. A disagreement between samples is a candidate alternative, not a silent change to the original audit.

## Recommended identity

A compact, slightly overconfident town trying to reinvent itself: an old factory has become a practical manufacturing hub, the college teaches useful skills, second-hand electronics look strangely desirable, and a community noticeboard promises a brighter future in unusually small print. Some people prosper during a boom; others exploit the bargains when things turn down.

Keep the readable ring, thirteen destination roles, short location menus, visible possessions and four familiar goals. Make the modern differences tangible through transport choices, recognisable careers and devices. Avoid adding a separate meter for every contemporary concern. Original art, dialogue and analytical evidence remain references; new production art and writing would be original work.

## Thirteen destinations, with deliberate replacements

These are exact original **place IDs**, not proposed travel distances. The [destination metadata](../../artifacts/original-game/town-destinations.csv) and [original town layout](../original-game/town-and-screen-layout.md) supply the reference. Keep the existing ring order for initial mockups; transport balance will need its own explicit distance/time specification. Functional subtitles should accompany playful names.

| Place ID | Original | Proposed destination / subtitle | Jobs and services | Change classification |
| --- | --- | --- | --- | --- |
| 0 | Low-Cost Housing | **Starter Court / Budget Apartments** | Home, rest, possession display | Preserve home role. Showing more owned props here is a presentation extension, not new furniture gameplay. |
| 1 | Rent Office | **Keys & Fees / Housing Office** | Rent, arrears, housing offers; groundskeeper and property manager | Preserve two jobs and rental function; titles may be refreshed. |
| 2 | Le Security | **Parkside / Secure Apartments** | More expensive home, rest, existing housing protections | Preserve second housing tier; security is clearly explained rather than implied by a luxury label. |
| 3 | Black's Market | **Corner Basket / Groceries** | Food packs, local paper, lottery; cleaner, checkout assistant, food-prep worker, supervisor, manager | Preserve grocery function and five-job baseline. Food-prep title replaces butcher; course 10 remains broad practical training. No cooking/crafting activity added. |
| 4 | P.I.G.G.Y. Bank | **Nest Egg / Community Bank** | Savings, loans, broker; cleaner, teller, assistant manager, manager, investment broker | Preserve banking and five jobs. Investments remain nested here, not a separate exchange building. |
| 5 | Factory | **TownWorks / Manufacturing & Repair** | Existing nine-job industrial ladder with assembly, machine work, engineering and office roles | Modern employer identity: modular products, repaired machinery and conspicuously optimistic signage. No production or resource-management minigame. |
| 6 | ACNE Employment | **Town Hall Annex / Jobs & Community Desk** | Unified job index; noticeboard; transport information | Agency function retained inside a new civic setting. No council career ladder or clinic is included by this proposal. Transport information is new presentation. |
| 7 | Hi-Tech U | **Next Chapter / Community College** | Existing eleven-course graph and three jobs: campus cleaner, tutor, lecturer | Modern educational identity. Long academic ladder remains stylised; labels below are fictional game qualifications, not real accreditation. |
| 8 | Socket City | **Reboot / Devices & Repairs** | Devices/appliances; tech adviser, device technician, store manager; bicycle and nested compact-car purchase menu | Preserve three-job baseline. Transport sales are a proposed **new service** here, not a fourteenth destination; ownership does not imply a repair minigame. |
| 9 | QT Clothing | **Good Threads / Clothes for Life** | Three clothing grades; sales assistant, assistant manager, manager | Preserve clothing gates and three-job baseline. Clearly show casual, smart and suit equivalents. |
| 10 | Monolith Burger | **The Daily Grind / Café & Takeaway** | Existing food/drink categories; cook, counter assistant, shift supervisor, café manager | New café identity; four-job/food-rule baseline retained. Replacing a milkshake picture with coffee must not silently change category effects. |
| 11 | Z-Mart | **Bargain Barn / Everyday & Oddities** | Rotating six-of-eighteen assortment; clerk, assistant manager, manager | Preserve rotating bargains and three jobs. New product illustrations must agree with their actual effects. |
| 12 | Pawn Shop | **Second Chance / Buy, Pawn & Redeem** | Pawn, redemption and forfeited goods | Preserve pawn role and no employer ladder. No used-vehicle sales in the initial proposal; vehicle valuation and stock are not silently inherited from appliances. |

This baseline retains **nine employers and 37 job entries**, not 37 newly designed careers. Every title change should preserve the original job identifier until its requirements are explicitly revised. The complete proposed naming inventory below covers all 37 entries and all eleven course names; the worked branch demonstrates how the unchanged prerequisites fit together.

Bus-stop signs are overlays at agreed existing destinations, not fourteenth and fifteenth businesses. A bus depot, clinic, hospital, delivery platform or separate makerspace would be a further destination/employer decision. “Different locations” can begin with meaningfully different employers and services inside a legible town rather than making the board larger by default.

## Complete proposed career and course naming inventory

The [37-job mapping CSV](../../artifacts/planning/modern-content-mapping.csv) records every verified employer-script/jobNum pair, original occupation item ID, proposed employer/title, original base wage, experience, declared dependability, both course fields and clothing. **All numeric fields remain original baseline data**, not approved modern balance. Zero in a course field means no requirement. Occupation item IDs can repeat across employers; use the employer script and jobNum to identify a job rather than a title alone. Job 17 is the assembly entry and job 18 the factory cleaner even though the original menu lists the cleaner first.

| Proposed employer / place ID | Complete proposed titles, with original jobNums |
| --- | --- |
| Bargain Barn / 11 | 1 Store Assistant; 2 Shift Supervisor; 3 Store Manager |
| The Daily Grind / 10 | 4 Cook; 5 Counter Assistant; 6 Shift Supervisor; 7 Café Manager |
| Good Threads / 9 | 8 Clothing Adviser; 9 Assistant Manager; 10 Store Manager |
| Reboot / 8 | 11 Tech Adviser; 12 Device Technician; 13 Store Manager |
| Next Chapter / 7 | 14 Campus Cleaner; 15 Tutor; 16 Lecturer |
| TownWorks / 5 | 17 Assembly Technician; 18 Workshop Cleaner; 19 Office Coordinator; 20 Machine-Shop Assistant; 21 Executive Coordinator; 22 Machinist; 23 Production Manager; 24 Design Engineer; 25 Site Director |
| Nest Egg / 4 | 26 Branch Cleaner; 27 Customer Service Teller; 28 Assistant Branch Manager; 29 Branch Manager; 30 Investment Broker |
| Corner Basket / 3 | 31 Store Cleaner; 32 Checkout Assistant; 33 Food-Prep Worker; 34 Store Supervisor; 35 Store Manager |
| Keys & Fees / 1 | 36 Groundskeeper; 37 Property Manager |

These are deliberately recognisable local jobs rather than a town full of influencers. Several are modern titles for older work, not genuinely new career mechanics. “Device Technician,” “Design Engineer” and “Tutor” describe fictional game occupations: their simplified checks do not represent professional licensing or real qualification standards. Clinic/care and gig careers remain deferred. There is no unmentioned new employer, application path or salary scale in this table.

| Course ID | Original qualification | Proposed course label | Required completed course ID | Existing direct job requirement |
| --- | --- | --- | --- | --- |
| 10 | Trade School | **Practical Skills** | None | Assembly Technician, Food-Prep Worker |
| 11 | Electronics | **Device Repair** | 10 | Device Technician; Store Manager at Reboot alongside 14 |
| 12 | Pre-Engineering | **Design & Engineering Basics** | 10 | Machine-Shop Assistant |
| 13 | Engineering | **Engineering** | 12 | Machinist; production/engineering leadership with 14 or 15 |
| 14 | Junior College | **Community Foundations** | None | Office, management, banking and housing roles; required alongside 11 or 13 for some roles |
| 15 | Bus. Admin. | **Business & Management** | 14 | Higher retail, office, banking and site leadership; broker alongside 16 |
| 16 | Academic | **Academic Studies** | 14 | Tutor; broker alongside 15 |
| 17 | Graduate | **Advanced Studies** | 16 | No job directly requires 17; opens 18 |
| 18 | Post-Doctoral | **Research Methods** | 17 | No job directly requires 18; opens 19 |
| 19 | Research | **Applied Research** | 18 | Lecturer |
| 20 | Publishing | **Publishing & Communication** | 19 | No job directly requires 20; final academic qualification and education-goal progression |

Source: the [eleven verified course records](../../artifacts/rules-audit/bytecode-education-verification.json) and job/course joins in the [original catalogue](../original-game/content-progression.md). Every prerequisite edge is unchanged: 10→11, 10→12→13, 14→15, and 14→16→17→18→19→20. Enrollment permissions, lesson increments and course rewards remain baseline values pending compatibility decisions. Course names do not introduce a different degree level or a new subject-specific examination.

The long academic ladder and some broad job prerequisites remain visibly inherited from the original. Calling the venue a community college does not make its advanced research ladder realistic. Present Next Chapter as a fictional local learning centre with partner study, or choose a different sign during visual review; do not imply that this naming exercise has solved academic realism. Similarly, retaining course 16 for a broker is an explicit original-graph compromise, not a claim that an academic course is the natural modern broker qualification. A replacement graph would need its own design and balance review.

## Different job boards, one job system

**Recommendation:** the agency shows the whole town; each employer shows its own postings. Both read the same job records, offered wages, qualifications and rejection state. A change in the economy updates those records; it does not create contradictory agency and employer versions of a vacancy.

| Surface | What it helps the player discover | Where applying happens |
| --- | --- | --- |
| Civic jobs index, at place 6 | Compare all employers, offered pay, required courses/clothes and work location; filter “qualified now” | Agency can submit the original-style application through the shared rules. Work still takes place at the employer. |
| Employer window/noticeboard | See that employer's same jobs and a short characterful advert | **Proposal:** apply there through the same application action, costs and turn-level retry restrictions; this adds a second application venue to the original agency baseline. |
| College careers notice | See which existing roles a course helps unlock | Read-only link into job details. No application or course completion from a poster. |
| Apartment newspaper or phone, if adopted | Review previously discovered jobs, owned transport, current obligations and last-seen quotes | Read-only reference by default; no remote application, work, banking or grocery purchase. |

A displayed quote should say whether it is current or last seen. Default recommendation is current employer/agency quotes when visiting those locations; cached remote quotes show the week/turn they were seen. Live remote wage refresh is an additional information advantage and should not arrive accidentally with a phone illustration.

**Important flow:** discover → inspect requirements → travel if needed → apply → receive a specific result → travel to the employer to work. Finding a listing is not a reserved vacancy or guaranteed hire. Applications retain their shared time cost and outcomes whether initiated at agency or employer; visiting two boards does not clear a failed application's retry restriction. For an initial narrow slice, the agency can remain the only application venue, with employer boards read-only, until the second venue is deliberately included.

“Qualified” and “there is an opening” remain different concepts. Use feedback such as “You need Device Repair” versus “You qualify. No opening this turn.” Do not tell a child to buy another course when the real reason was an opening roll.

## Worked career branch: practical tech

**Verified baseline:** [employment metadata](../../artifacts/rules-audit/bytecode-employment-verification.json), [education metadata](../../artifacts/rules-audit/bytecode-education-verification.json), [original catalogue](../original-game/content-progression.md). Values below are original game base units before economy adjustment, not real-world wages or educational advice.

| Qualification ID | Original → proposed name | Completed prerequisite |
| --- | --- | --- |
| 10 | Trade School → **Practical Skills** | None |
| 11 | Electronics → **Device Repair** | 10 |
| 14 | Junior College → **Community Foundations** | None |

Course 10 also opens course 12; course 14 also opens 15 and 16. These names must stay broad enough for those edges. The complete eleven-course naming inventory below retains the other edges as well. This is a reskinned original graph, not a newly designed modern qualification system.

| Original jobNum / occupation item ID | Proposed role at Reboot | Base hourly wage | Minimum experience / declared dependability | Completed courses | Clothing |
| --- | --- | ---: | --- | --- | --- |
| 11 / 47 | Tech Adviser | 5 | 20 / 30 | None | Dress, 35 |
| 12 / 64 | Device Technician | 11 | 40 / 40 | 11 | Casual, 36 |
| 13 / 46 | Store Manager | 14 | 40 / 40 | 14 **and** 11 | Business suit, 34 |

An illustrative route: start in an accessible earning job; build experience and dependability; complete Practical Skills then Device Repair; apply for Device Technician once qualified; later add Community Foundations and a suit to apply for Store Manager. Tech Adviser is an alternative earning step, **not a mandatory predecessor**. The repair role deliberately accepts casual clothes even though the sales role needs dress clothes. Successful qualifications do not guarantee an opening.

At the café, the original Cook entry is job 4 / occupation 44: base wage 4, experience 0, declared dependability 10, no course and casual clothes. The special original treatment of declared dependability 10 and Cook's opening check remains documented in [employment rules](../rules-audit/employment.md); do not infer the same exception for a new delivery or care role.

A “care assistant → nurse → clinic manager” or “delivery rider → logistics manager” ladder is **new content**, requiring its own job IDs, course requirements, balance, clothing and employer definition. None is represented by renaming Device Repair or Business Administration. Do not import actual regulated professional titles while pretending the original prerequisite graph already models them.

## Modern devices: recognisable objects, honest effects

Retain some chunky, second-hand charm. Show possessions in the apartment so buying something feels tangible. The following original item IDs identify functional slots; candidate labels are proposals, not claims that every item already has a positive purchase reward. The audited normal durable-purchase paths skip their nominal Happiness rewards; [compatibility choices](compatibility-proposals.md) must settle whether to change that.

| Original ID / object | Proposed object | Existing role to preserve | New effect? |
| --- | --- | --- | --- |
| 21 / Refrigerator | Magnet-covered fridge | Original food-storage role | No |
| 25 / VCR | **Game Console & Movie Box** | Existing entertainment durable, possession and relevant event references | Label/art only. No study bonus, playable games or subscription. All old VCR event text needs coordinated rewriting. |
| 26 / Stereo | **Big Little Speaker** | Existing stereo ownership/event role | No streaming fees or party/social meter |
| 29 / Computer | **Home Laptop** | Existing study equipment credit and occasional income event | No new gig-work action or guaranteed income |
| 30 / Black-and-white TV | **Tiny Used TV** | Lower-price separate TV slot | No upgrade into the colour-TV or computer slot |
| 31 / Encyclopedia | **Big Book of Everything** | One part of three-book study set | No |
| 32 / Dictionary | **Word Wrangler** | Second part of that set | No |
| 33 / Atlas | **World Atlas** | Third part; all three required for set credit | No |
| New ID / no original equivalent | **Basic Phone** | Candidate apartment/handheld prop and read-only reference | **New effect** if owned phone unlocks remote notes/quotes. Do not reuse an unrelated item ID. |
| New IDs / no original equivalent | **Bicycle, compact car** | Transport choices requested by owner | **New mechanics**: purchase/upkeep/travel rules belong to the transport proposal. Bus travel uses a per-ride fare; no bus-pass purchase in the initial proposal. |

Sources: [goods and finance](../rules-audit/goods-and-finance.md), [inventory grouping](../rules-audit/inventory-grouping.md), [Happiness actions](../rules-audit/happiness-actions.md). No smartphone remote services are assumed by the audited computer or electronics catalogue.

**Phone recommendation:** put a simple information panel in the interface for every player, with a paper/notebook look before phone ownership. A bought phone may change the illustration and flavour without withholding essential instructions from a new player. If it needs a strategic effect, choose one narrowly specified convenience later; do not bundle remote everything into it. A purely cosmetic phone should be labelled as such before purchase and priced accordingly.

**Repairability recommendation:** keep “used and affordable” visually appealing. A new gadget should not automatically replace a cheaper item's benefit. Avoid RAM, battery, data, chargers, screen time, storage and app-install meters. Existing breakdown/repair and pawn rules already create enough consequences to explain first.

## More ideas, ranked by fit with simplicity

Ranking is a design recommendation, not a research result. “Small” means fewer rule changes, not a measured development estimate.

| Rank | Idea | Why it fits | Cost / recommended disposition |
| --- | --- | --- | --- |
| 1 | **Transport as an early investment** | Turns repeated town routes into a clear money-versus-time choice; bike visibly changes the character | Medium mechanical change; include in modern direction. Balance with transport proposal, not invented here. |
| 2 | **Employer window adverts plus agency comparison** | Makes buildings feel like employers; children can connect job and workplace | Small presentation change if boards read-only; second application venue is a separate explicit rule extension. Include. |
| 3 | **Visible possessions in both apartment tiers** | Immediate reward for a console, laptop or comically large speaker | Small presentation extension; no placement editor. Include in visual mockups. |
| 4 | **Local paper explains the economy** | “Factory orders fall; job offers soften” gives context for a bad week | Small if explanatory only. Derive from actual economy changes, never invent predictive certainty. Include sample. |
| 5 | **A distinct clerk at each destination** | Original-style short humour and recognizable faces need no extra meter | Small content/art expansion; include a few in mockups, not a dialogue tree. |
| 6 | **One weekend activity swap** | Replace a dated ticket category with a local game night, show or sports fixture | Small if same cost/category/effect slot. Choose after full event-text mapping; defer mechanical activities. |
| 7 | **Clinic/care career branch** | Modern, understandable work beyond shops and industrial jobs | Large graph/employer decision; defer from first scope. Later choose a deliberate replacement or enlarged town rather than a hidden extra business. |
| 8 | **Delivery or freelance gigs** | A bike or computer could unlock a different earning route | Large balance interaction with travel, employment and work limits; defer. No universal instant-cash button. |

Also defer subscriptions, social followers, crafting inventory, complex timetables, detailed vehicle components and an always-online marketplace. Those could become games of their own; first establish whether travel, learning and a changing economy already provide enough interesting decisions.

## Writing samples for the mockups

Newly written examples; none adds an event or changes a rule.

- **TownWorks sign:** “Building the future. Reusing most of the screws.”
- **Café clerk:** “The coffee's strong. The local economy is taking its time.”
- **Civic jobs board:** “Find your next opportunity. The stapler stays here.”
- **Used-tech ticket:** “Previous owner says it builds character. Includes power cable.”
- **Rejection:** “You need Device Repair before applying. Next Chapter teaches it.” Follow with the optional joke: “The screwdriver is not the qualification.”

Keep actionable information first. Aim jokes at overconfident businesses and everyday absurdity, not unemployment, debt, illness, children or people needing help. Restrained Australian flavour might be one “No worries” from a character; the town should not require slang knowledge.

## What the next mockups should let the family judge

Show the thirteen-stop town with recognisable functions, bus-stop overlays, a bike outside Starter Court, and TownWorks looking different from a generic office. Show Reboot's device shelf and local job board; show the college course path; show the same apartment before and after a visible purchase.

Ask each reviewer to point to a place to find jobs, the place they must work, where to buy food, and where a repair course is taught. Ask whether the proposed laptop, console and bike feel worth wanting. Ask which employer or activity is missing from their idea of a modern town. Record preferences separately from comprehension failures.

The review should select a coherent town tone, the first device replacements and the job-board/application model. It does not need to settle every occupation or approve new care/gig systems before visual iteration can begin.
