# Modern direction: review pack 2

**Numeric follow-up:** [career budgets v1](career-budget-comparison-v1.md) compares butcher, trades and doctor from a shared early-employed checkpoint, with tuition/upkeep/travel, work-history constraints and setbacks. Figures remain proposals; results are not full-game balance or original opening timings. Town-layout comparison is the next dependency.

**Latest career review:** the owner accepts preserving Trade School → Butcher, skilled trades and a longer professional/doctor path in a compact town. [Career/town graph v2](career-and-town-graph-v2.md) supplies a new proposed graph and stop roster. The13-stop/37-job/11-course mapping below is now the earlier reference, not the complete successor content plan.

**Owner review update2026-10-17:** transport progression/town-wide bus and in-store applications are accepted as directions, along with broad consistency/fairness fixes. New employer options, reasons to explore, recruited offers and functional devices are developed in [the latest options](employers-offers-and-useful-possessions.md). Its proposals extend the earlier read-only-phone/no-home-work baseline below; the specific new effects and revised career graph are not yet selected.

2026-10-17. **PROPOSAL — no application implementation approved.** This is the current planning entry point following the owner's transport, newer-location, job-board and device pointers. The [original reference](original-research-handoff.md) remains unchanged. The [first draft](2.0-draft-specification.md) is the starting structure, not a constraint against the explicitly requested new mechanics.

## Goal and current boundary

Work through the compatibility recommendations, visual mockups and modern content direction (steps1–3), making the first-playable scope ready to agree as step4. Supply concrete alternatives for review rather than treating silence or a generated picture as approval. No game, service or deployment is being built in this step.

The owner has confirmed the **direction** of more meaningful transport, including walking, bikes, buses and cars at different costs; newer locations/job boards; and different devices. Names, transport figures, exact board topology, device effects and job graph changes remain proposals. The pack below is ready for owner/family iteration; it does not claim that review has happened.

## Recommended direction

Keep the compact town and the four-goal race. Make **time versus money** more tangible through transport. Modernise the workplace identities and make the relationship between training, jobs and work locations easier to see. Let possessions visibly improve a funny, slightly scruffy apartment.

The town is trying to reinvent itself, sometimes successfully: TownWorks builds and repairs things; Next Chapter teaches practical skills; Reboot sells desirable but chunky devices; the civic jobs desk is optimistic, with a stapler chained to the counter. This keeps the small-town, kitsch character without making the whole game a joke about smartphones.

| Review material | What it supplies | Status |
| --- | --- | --- |
| [Transport proposal](transport-proposal.md) | Complete provisional walk/bike/bus/car rules, acquisition, quotes, trip examples, end-turn and save/AI boundaries | New system requested; detailed recommendation unapproved |
| [Town and content direction](modern-town-and-content.md) |13 destination identities; all37 proposed job titles and11 course labels; job boards; devices; eight ranked ideas | Full naming baseline supplied; no new care/gig career graph implied |
| [Content mapping CSV](../../artifacts/planning/modern-content-mapping.csv) | Stable job/employer IDs, proposed titles and unchanged original requirements/pay/clothing | Reviewable mapping, not an application data file |
| [Visual review](visual-direction-v1.md) | Original generated town/transport and shop/home concept images, exact prompts, inspection notes and known mismatches | Art and layout exploration; not a runnable game or pixel specification |
| [Compatibility proposals](compatibility-proposals.md) |17 evidence-linked recommendations | Apply the amendments below when considering this newer direction |

## How this revises the earlier draft

These are recommended amendments, not owner-approved rules. There is one proposed successor baseline, rather than a plan for several compatibility modes.

| Earlier recommendation | New direction / explicit departure |
| --- | --- |
| C03: fixed original-speed ring travel | Replace with the transport proposal's logical-distance model. Slower walking, ownership and fares are substantial new mechanics. Animation remains separate from cost. |
| C02: original travel exhaustion/entry behaviour | Retain partial work/study and allowed zero-time purchases. Replace interrupted travel with a complete trip+entry quote that must fit. Add explicit End Turn. Exact exhaustion can arrive and allow legal zero-time transactions. |
| Original170-point path and carry | Retain as historical evidence only. Current examples use a13-node equal-edge ring; final edge distances still need agreement. No original residue is carried into this new proposed travel model. |
| Agency-only applications | Recommend shared job data at civic index and employer boards, with local applications permitted at either venue. Same application cost, qualifications, opening/rejection state; no reroll by changing board. This is a new application venue. |
| Household goods only | Retain eight proposed device replacements, plus separate new transport ownership. A phone is optional flavour/reference; no default remote work, banking, groceries or instant applications. |
| Original home prop subset | Show owned devices and transport clues in both housing tiers. This changes visible presentation, not furniture placement or goal rewards. |
| Existing first solo slice | Step4 must include at least one transport comparison and job-board discovery test; the old slice cannot validate the new central idea on its own. Exact scope is still to agree. |

C01's floppy reference remains recommended for unchanged rules, as do C04–C17's separately stated choices. Adding transport does not approve a symmetric economy fix, instant victory, stronger durable-purchase rewards or privileged AI. The earlier [architecture proposal](architecture-and-validation-proposal.md) still supports independent simulation and stable saves; new transport ownership/operating flags would join its adopted state contract.

## Transport recommendation in plain terms

Walking always works but consumes precious time. A bike is an early purchase that makes repeated errands cheaper in time. A dependable town bus is affordable before owning a vehicle. A car saves more time across town but has an upfront price and a clearly quoted operating charge when used.

Illustrative base prices are **bike$120 and car$1,200**; bus fare$3; car$4 per trip plus$20 on the first drive in each personal turn. They are tuning examples, not real-world prices or measured balance. A three-edge journey including entry takes walk11 / bike7 / bus7 / car5 time. First-drive car charge is$24. The [full proposal](transport-proposal.md) supplies the formulas and recovery cases.

Recommend buying vehicles through Reboot's nested Transport menu, avoiding an extra building. No vehicle pawn/resale/loan/repair subsystem initially. Do not grant automatic Happiness or liquid Wealth for ownership; purchase cash is debited normally and therefore reduces liquid assets. Vehicle book valuation in Statistics, eligibility for generic theft/events and any later resale must be explicitly settled before building; the initial proposal excludes vehicles from household depreciation/theft/repair and resale. A vehicle image is not evidence that those systems exist.

## Suggestions worth trying next

1. **Window adverts with personality:** same job information as the civic index, written by the employer. “Machine-shop assistant wanted. Ability to find the10mm socket appreciated.” No extra application odds hidden behind the joke.
2. **A local paper that explains the economic hump:** describe what just changed in the actual economy, without predicting secret future rolls. A bad week becomes understandable, not merely a falling number.
3. **A home that changes with ownership:** bike outside, laptop on the desk, ludicrous speaker beside the couch. Let the children point to what their money bought.
4. **Visible course-to-job connections:** show which existing roles a selected qualification can unlock, alongside remaining work-history requirements. Keep success uncertain where openings are uncertain.
5. **Modern local outings in existing ticket slots:** game night, live show or local sport, with fresh event writing. Keep the mechanical slot until a new activity system has a separate purpose.

Clinic/care work and delivery/freelance work are promising follow-ons, but would need genuinely new employers, prerequisites and balance. They should be considered as deliberate branch replacements or additions after this town is reviewed. A medical title is not a harmless relabel of an electronics qualification. Subscriptions, followers, fuel gauges, detailed timetables and crafting would add more administration than this first direction needs.

## Visual iteration and decisions to carry forward

Start with the [concept images](visual-direction-v1.md), then read the transport table while looking at the town. Ask each child and an adult to find work, food, college and home; choose a mode for a short and long trip; explain what a laptop or bike would change. Record what they infer from the picture separately from what the rules actually promise.

The next review only needs to settle a few large choices:

- **Transport:** dependable town-wide bus as recommended, or a smaller stop network with extra access rules? Is the slower walk/early-bike/later-car progression appealing?
- **Town:** retain13 compact roles with new employers, or replace/add a destination for a genuinely new career branch? The supplied mapping is the compact baseline, not a refusal to explore another town.
- **Job boards:** apply locally as well as at the civic desk, or use employer boards only for discovery initially?
- **Devices/art:** which possessions feel worth wanting, and does the illustrated retro style retain enough of the original's character?

After that feedback, revise the images and content together, record selected decisions, and agree step4: the smallest playable scope that tests the updated loop. These are review prompts, not a request to approve every balance constant or begin application implementation now.
