# Original game: locations and action screens

Research date: 2026-10-15. Reference: DOS floppy version **1.000.060**, using the published decompilation at revision `870a8015b689474484bf3d8b41416956d4315432`. This document describes the existing game, not a proposed redesign. Findings below are **script findings**, not independently observed runtime behaviour. Names are taken from textual menus/greetings where available; a few normalized location labels describe scripts whose signs are image resources.

## The original interaction pattern

The town has **13 destinations**. Selecting a building moves the player's marble along the town route; entering it opens a compact location dialog over the town. Most staffed locations combine an illustrated background, an animated clerk, a short priced list, and Exit. Shops show item art; workplaces add Work and a time-clock display **only when this player works there**. Jobs are obtained through the employment agency, then performed by visiting the employer. There is no separate job-management dashboard. [Town entry/return logic][town]; [representative shop][appliance]; [employment menus][employment].

The dialog is not invariably available in its full form. Homes offer Relax only to their resident; the rental office's service menu depends on the rental period. Course lists depend on completed qualifications. This context sensitivity is part of the original layout, rather than an optional later enhancement.

All thirteen destination entries cost two units of the turn's time, in addition to movement; Work and study each consume six. Exact accounting and final-action exceptions remain in the [time-and-actions audit](../rules-audit/time-and-actions.md).

## Destination catalogue

Numbers below are original `placeNum` identifiers, not an invented order or priority.

| ID | Destination | What appears / what the player does | Conditions and characteristic feedback | Employment |
| --- | --- | --- | --- | --- |
| 0 | Low-Cost Apartments | Apartment interior; Exit; resident can Relax. Original decorative objects include an old chair, stool, and wall saying. | A different background is used if this is not the player's home; Relax then disappears. Relax takes six time units, adds relaxation up to a cap, and the first successful relaxation in the turn grants happiness. [Source][lowcost] | None |
| 1 | Rent Office | When open for business: pay one month's rent, request more time, rent either apartment type; pay garnishment balance when owed. Employee can Work. | Full services appear at the month boundary (`week mod 4 = 0`) or under the retained-open flag; an employee can still access Work outside service periods. Rent is quoted for the current contract; moving has confirmation and rental feedback. Insufficient cash is reported. [Source][rent] | Groundskeeper, Apartment Manager |
| 2 | Security Apartments | Better apartment interior; resident can Relax; owned Color TV, Stereo, encyclopedia/books, and VCR appear as room props. | Resident-only Relax; other visitors get a different background. The source explicitly checks these four possessions for visible props; do not assume every appliance decorates the room. [Source][security] | None |
| 3 | Black's Market | Buy Food for 1, 2, or 4 Weeks; 10 Lottery Tickets; Newspaper. Food art and clerk response accompany purchases. Newspaper opens its own screen and returns here. | Cash check; short clerk quips after purchases. Food quantities are counted in weeks, rather than a detailed grocery inventory. Newspaper reading costs an additional unit of time. [Source][market] | Janitor, Checker, Butcher, Assistant Manager, Manager |
| 4 | Bank | Deposit, Withdraw, Loan Payment, Apply for Loan, See the Broker; Work when employed. Piggy-bank animation accompanies transfers. | Transfers occur in up-to-$100 increments, limited by available funds. Loan application gives an offer/confirmation or explains that more money or a better job is needed. Existing borrowers can request an extension. [Source][bank] | Janitor, Teller, Assistant Manager, Manager, Investment Broker |
| 5 | Factory | Factory worker/manager presentation, Work when employed, Exit. | This is a workplace, not a factory-building or production-management screen. Work checks clothing, remaining time, and work history; repeated failures of dependability can trigger warning/dismissal. [Sources][factory], [work] | Nine factory jobs; full table in [content progression](content-progression.md) |
| 6 | ACNE Employment | Choose one of nine employers, then select a job from that employer's menu showing offered hourly wages. | Applying takes four time units. Feedback distinguishes missing education, insufficient experience, poor work history, and no opening. Applying for the same job is also the route to requesting a wage adjustment. [Source][employment] | Agency itself does not employ the player |
| 7 | Hi-Tech University / Hi-Tech U | Enroll; choose an available course shown on a book-style list; see sessions remaining; attend repeatedly; graduation opens a diploma presentation. Work when employed. | Prerequisites filter the list. Enrollment is required; failure messages cover not enrolled, no remaining time, and insufficient cash. Graduating removes the completed course and reveals newly eligible courses. When all courses are complete the university has no further classes to offer. [Source][university] | Janitor, Teacher, Professor |
| 8 | Socket City Appliance | Buy Refrigerator, Freezer, Stove, Color TV, VCR, Stereo, Microwave, Hot Tub, Computer; item display and clerk; Work when employed. | Prices reflect the economy; purchases check cash and update possessions. These are discrete purchase rows, not a grid-based furnishing editor. [Source][appliance] | Salesperson, Electronic's Repair, Manager |
| 9 | QT Clothing | Business Suit, Dress Clothes, Casual Clothes; clerk and item illustration; Work when employed. | Clothing is a consumable with different work suitability; buying a suit is a strategic qualification for work, not purely cosmetic character customization. [Sources][clothing], [work] | Salesperson, Assistant Manager, Manager |
| 10 | Monolith Burgers | Hamburgers, Cheeseburger, Astro Chicken, Fries, Shakes, Colas; clerk and food illustrations; Work when employed. | Individual fast-food purchases, rather than the market's bulk grocery weeks. Some purchases have first-purchase-in-turn happiness rewards. The original menu includes a mixture of consumable food and immediate-effect products. [Source][fastfood] | Cook, Clerk, Assistant Manager, Manager |
| 11 | Z-Mart Discount | **Six available products** drawn from an 18-product pool; item display and clerk; Work when employed. Pool includes appliances, clothes, books, entertainment tickets, and joke purchases. | The script removes products at random until six remain; saved selection indices maintain the assortment across re-entry within this player's turn and reset on next turn. It is not an always-complete catalogue. Purchased goods receive a discount-store attribute. [Source][discount]; reset in [start of turn][startturn]. | Clerk, Assistant Manager, Manager |
| 12 | Pawn Shop | Pawn, Redeem, or Buy; each opens the appropriate item selector and transaction flow; Exit. | Owned goods constrain pawn choices; global pawn stock constrains purchases and redemption. The shop can refuse because it has no room, does not need another matching item, or has no items in that category. Pawn offers require acceptance; redemption/purchase checks cash. [Source][pawn] | None |

## Subscreens and returns

These belong to destinations, rather than extra stops on the town route:

| Entry | Subscreen | Return / result |
| --- | --- | --- |
| ACNE Employment → employer | One of nine employer job lists | Application/raise feedback, then agency menu; going to work still requires town travel |
| Bank → See the Broker | Investments: T-Bills, Gold, Silver, Pork Bellies, Blue Chip Stocks, Penny Stocks; prices/holdings; Buy/Sell | Return to banking screen; broker is **not a fourteenth building** |
| Black's Market → Newspaper | Newspaper presentation | Returns to market |
| Hi-Tech U → completed course | Diploma | Returns to updated eligible-course list |
| Pawn Shop → Pawn / Redeem / Buy | Corresponding inventory list and transaction controls | Returns to pawn-shop flow |

Broker evidence: [broker.sc][broker]. Other transitions are in their destination scripts above.

## Character and feedback structure to preserve in the reference

Shop greetings and transaction remarks are short, varied, and usually interrupt the ordinary purchase/work loop. The writing gives each otherwise small menu a personality: cynical employment advice, exaggerated educational promises, grocery puns, cheap retail boasts, and an unsympathetic landlord/pawnbroker. This is an analytical description of the original dialogue structure, not a new dialogue brief. Source text pools exist in the cited scripts; the large banks of original dialogue have deliberately not been reproduced here.

The interface also provides practical feedback in that same character-led presentation: no cash, no savings, no time, prerequisites missing, declined application, job obtained, or raise outcome. The employment script explicitly constructs rejection reasons; the university refreshes the course list after a diploma; staffed workplaces remove Work when dismissal occurs. [Employment][employment], [university][university], [work][work].

## Verification boundaries

- This is a source-level screen/action inventory. It does not claim screenshots were captured, play sessions were run, or image-resource labels were transcribed.
- Reproduce the rental-office closed/open states, home visit states, Z-Mart's turn-specific assortment, all pawn branches, and successful/unsuccessful job applications before finalizing pixel-level replicas.
- Inspect actual art to confirm exact sign lettering, character placement, product thumbnails, and course text baked into book graphics. Course names in the [progression reference](content-progression.md) are normalized script identifiers where the art supplies the visible lettering.
- Food storage/spoilage, discount reliability, theft, loan repayment, and pawn expiration need dedicated formula/edge-case audit beyond the action inventory. Do not infer complete rules from the fact a button exists.
- See the existing [coverage table](../rules-audit/README.md) and [validation backlog](../rules-audit/validation-backlog.md) for broader outstanding work.

[town]: https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc
[lowcost]: https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/lowcost.sc
[rent]: https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/rentOffice.sc
[security]: https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/security.sc
[market]: https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/market.sc
[bank]: https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/bank.sc
[factory]: https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/factory.sc
[work]: https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/n108.sc
[employment]: https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/employment.sc
[university]: https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/university.sc
[appliance]: https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/appliance.sc
[clothing]: https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/clothing.sc
[fastfood]: https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/fastFood.sc
[discount]: https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/discount.sc
[startturn]: https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc
[pawn]: https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/pawnShop.sc
[broker]: https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/broker.sc
