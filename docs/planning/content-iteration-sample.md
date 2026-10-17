# Content iteration sample

Drafted 2026-10-17. **PROPOSAL — unapproved names, writing and presentation only.** This is a small review sample for the [project brief](project-brief.md), not a complete content bible or permission to build. It preserves original destination roles, job/course identifiers, prerequisite edges and functional item slots. None of the labels below changes a price, wage, reward, action cost or availability rule. Compatibility fixes require their own decisions.

The reference is the inspected website's DOS **1.000.060** package, with evidence levels recorded in the linked research. These proposed fictional game courses and pay values describe a game economy; they are not claims about real qualifications or salaries. All names need a later public-release naming review.

## Town: familiar functions, new signs

Keep the compact small-town ring and the original thirteen destinations. Candidate signs should make the function easy to guess before the player reads a tooltip. A slightly overconfident local business culture supplies the kitsch; Australian flavour comes through occasional wording rather than replacing every sign with slang.

| Place ID | Original destination | Candidate sign | Role retained |
| --- | --- | --- | --- |
| 0 | Low-Cost Housing | **Starter Court** · Budget Apartments | Inexpensive home, rest, original home actions and presentation role |
| 1 | Rent Office | **Keys & Fees** · Rental Office | Pay rent/arrears, choose housing, original rental-office employer |
| 2 | Le Security | **Peace of Mind** · Secure Apartments | More expensive secure home, rest, possession display and original protections |
| 3 | Black's Market | **Corner Basket** · Groceries | Weekly food, lottery, newspaper and grocery employer |
| 4 | P.I.G.G.Y. Bank | **Nest Egg** · Community Bank | Savings, loans, nested broker and bank employer |
| 5 | Factory | **TownWorks** · Manufacturing | Original industrial employer and its job ladder |
| 6 | ACNE Employment | **Next Shift** · Job Agency | Navigate employer job lists; no new agency career ladder |
| 7 | Hi-Tech U | **Next Chapter** · Community University | Enrollment, eligible courses, qualifications and university employer |
| 8 | Socket City | **Circuit Breakers** · Home & Tech | Appliances/electronics and original retail/repair/management roles |
| 9 | QT Clothing | **Good Threads** · Clothing | Three clothing grades and original clothing-store employer |
| 10 | Monolith Burger | **Stack Attack** · Burgers | Original food/drink categories and fast-food employer |
| 11 | Z-Mart | **Bargain Barn** · Variety Store | Six-of-eighteen changing assortment and original discount-store employer |
| 12 | Pawn Shop | **Second Chance** · Pawn & Used Goods | Pawn, redeem, forfeited stock and shared shop capacity |

Source: [destination IDs and placement metadata](../../artifacts/original-game/town-destinations.csv), [original topology and screen roles](../original-game/town-and-screen-layout.md), [content catalogue](../original-game/content-progression.md). Names do not imply relocating buildings, changing travel distance, adding businesses, or turning the broker into a fourteenth destination. Employment remains at the original nine employers; home and pawn-shop signage creates no new jobs.

**Presentation proposal:** show the functional subtitle beneath each playful sign, such as “Next Shift / Job Agency.” Try a milkshake, a small “No worries” notice, or a clerk's dry aside for restrained Aussie flavour. Avoid requiring children or international players to decode slang to understand an action.

## Worked reskin: home-tech retail to repair and management

This sample modernises Socket City's existing three entries. It does **not** introduce a mandatory promotion chain: the original checks each application's qualifications, experience, dependability and opening rules. A player can apply for any qualifying entry without first holding the previous one. Failed applications, clothing checks, employment ceilings and economic wage changes remain separate original rules.

### Qualifications

| Original course ID and name | Candidate course label | Completed prerequisite retained | Existing job relevance |
| --- | --- | --- | --- |
| 10 · Trade School | **Practical Skills** | None | Opens course 11; retains all other original course-10 job uses |
| 11 · Electronics | **Device Repair** | Course 10 | Repair job 12; one requirement of manager job 13 |
| 14 · Junior College | **Community Studies** | None | Other requirement of manager job 13; retains its original successor courses and job uses |

“Community Studies” deliberately remains broad: renaming it narrowly as a repair or management certificate would misdescribe its existing academic and business successors. Course 10 still opens Pre-Engineering (12) as well as Electronics (11). Course 14 still opens Business Administration (15) and Academic (16). This sample supplies no replacement labels for those successors yet.

The verified graph, IDs and six-unit lessons are in the [education metadata](../../artifacts/rules-audit/bytecode-education-verification.json); [education rules](../rules-audit/education.md) cover enrollment permissions, ten ordinary attendances, equipment credits and graduation rewards. The renamed course uses the same record throughout the game, not a new qualification alongside it.

### Jobs at Circuit Breakers

| Original jobNum / item index | Original title | Candidate title | Original base wage | Minimum experience | Declared dependability | Completed course IDs | Required clothing |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| 11 / 47 | Salesperson | **Tech Adviser** | 5/hour | 20 | 30 | None | Dress, 35 |
| 12 / 64 | Electronic's Repair | **Device Technician** | 11/hour | 40 | 40 | 11 | Casual, 36 |
| 13 / 46 | Manager | **Store Manager** | 14/hour | 40 | 40 | 14 **and** 11 | Business suit, 34 |

Source: employer script 219's three records in [employment verification metadata](../../artifacts/rules-audit/bytecode-employment-verification.json), joined to the [original course/job catalogue](../original-game/content-progression.md). `jobNum` identifies the employer-specific job; the item index identifies its occupation type and is not a unique job ID. Values are original game base units before economy adjustment, not proposed modern dollar wages.

**Illustrative player journey, not a guaranteed number of weeks:** earn and build work history in an accessible starter job; obtain dress clothes when qualified to apply for Tech Adviser; complete Practical Skills then Device Repair; build the remaining experience/dependability and apply for Device Technician; complete Community Studies and acquire a business suit before applying for Store Manager. The starting fast-food Cook entry is original job 4 (item 44), with experience 0, declared dependability 10, no course requirement and casual clothing. The original treats declared dependability 10 specially in qualification; its opening check also differs. See [employment rules](../rules-audit/employment.md).

The repair job's return to casual clothing is intentional original data. Do not silently turn it into a “higher job means fancier clothes” ladder. Buying every course is not required for this example. Device Technician is a fictional store role; there is no repair minigame, customer queue, crafting system or new device-maintenance meter attached to the title.

**Proposed feedback wording:** “Device Technician needs Device Repair and more work history.” If the experience threshold is also met but an opening roll fails, show a different explanation. Exact numeric requirement visibility is a presentation decision; never present an opening failure as a missing qualification.

## Possessions: new illustrations in existing slots

These are candidate visual/label replacements for a small portion of the existing catalogue. Retain their existing IDs, prices, stores, grouping, repair, pawn and event rules unless a separate compatibility proposal explicitly changes them. Any associated weekend anecdote and apartment prop must use the same replacement consistently.

| Existing item ID and original | Candidate label / illustration | Functional slot retained; no additional promise |
| --- | --- | --- |
| 21 · Refrigerator | **Fridge**, with magnets and a crooked shopping list | Original grocery-storage role; identical capacity/spoilage rules |
| 25 · VCR | **Movie Box**, a chunky local media player | Existing entertainment durable and associated anecdotes/prop; no recurring streaming bill or study credit |
| 26 · Stereo | **Party Speaker**, with oversized knobs | Existing stereo durable; no music subscription or social system |
| 29 · Computer | **Home Computer**, a colourful compact desktop | Existing equipment study credit and occasional income event; no always-on gig-work action |
| 30 · Black-and-white TV | **Tiny Second-hand TV**, visibly a lesser set | Distinct low-price TV slot; no upgrade into item 24 or extra computer credit |
| 31 · Encyclopedia | **Big Book of Everything** | One member of the existing three-book study set |
| 32 · Dictionary | **Word Wrangler** | Second member of that same set |
| 33 · Atlas | **World Atlas** | Third member; all three still required for the set credit |

Source: [goods and recurring effects](../rules-audit/goods-and-finance.md), [inventory grouping](../rules-audit/inventory-grouping.md) and [Happiness actions](../rules-audit/happiness-actions.md). The original durable-purchase bonus branches skip their nominal rewards on the traced normal path; this sample neither restores those rewards nor advertises them. The computer's income is an occasional event, not a controllable job or guaranteed return. The three books remain deliberately physical, keeping some kitsch and making their combined study role legible.

Movie Box and Party Speaker are illustrative candidates, not approved art assets. New graphics and writing would be original work; decoded original images remain local reference material.

## Three fresh humour samples

These lines are newly written proposals, not transcriptions from the original. They add no mechanical event by themselves.

- **Job agency notice:** “Experience wanted. Experience available elsewhere.”
- **Budget apartment notice:** “Open-plan living. Mostly because the door sticks.”
- **Tech shop clerk:** “No worries. We put the instruction manual somewhere very safe.”

Aim for jokes about institutions, optimism and everyday nonsense. The actionable explanation should remain readable on its own, with the joke as a short extra line.

## Family review prompts

Use the same paper screen or static mockup with each child and an adult. Ask for an explanation before providing a hint; record the phrase or image that caused confusion. This is a proposed review exercise, not a completed playtest.

1. “Where would you go to find a job? Where would you go to actually work?” Check the agency/employer distinction.
2. “You want Device Repair. Which course comes first?” Check that the two-course dependency is understood without real-world qualification knowledge.
3. “You finished Device Repair. What else might stop you getting the technician job?” Check work history versus an opening failure, without implying a guaranteed hire.
4. “The technician wears casual clothes, but the manager needs a suit. Can you tell which clothes you need before travelling?” Check the retained clothing distinction.
5. “Which three books help you study? Does one book do it?” Check the combined-set benefit; then ask what the computer adds.
6. “Is Movie Box something you buy once or pay for every week? What made you think that?” Reject imagery or wording that accidentally promises a subscription mechanic.
7. “Which names or jokes made you smile? Which signs needed explaining?” Compare comprehension and humour across ages without treating children as the sole audience.

The next content step is to select a naming tone, then extend the same one-to-one approach across the remaining jobs, eleven-course graph and possession/event text. Any new career branch, phone, subscription, gig platform, vehicle or social meter would be a separate **mechanical proposal**, not an invisible reskin.
