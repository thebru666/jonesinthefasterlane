# Proposed follow-up task: iterate the documented original

Recorded: 2026-10-15. **PROPOSAL — no design changes approved.**

## Task brief

Review the [original-game documentation](../original-game/README.md) with the owner, then produce a side-by-side adaptation specification. Start with the documented original as the default. For each proposed departure, record its purpose, player-visible effect, rule impact, visual/content impact, and validation question. Preserve the economic swings, humour, simplicity, and close mechanical resemblance requested in the [project brief](project-brief.md).

This is a planning task within this repository. It does not create a separate chat, schedule work, approve implementation, or require a new game system.

## Suggested order

The [local resource catalogue](../original-game/asset-catalogue-notes.md), complete course-book label transcription and partial screen studies are now available; follow the [research handoff](original-research-handoff.md) for their actual coverage. Full runtime composition and animation remain bounded rather than prerequisites already claimed complete.

1. Confirm the reference edition and resolve the material floppy/CD differences already recorded in the rules audit.
2. Walk through setup, one complete player's week, handover, progress inspection, and finish using the original-game documents.
3. Produce low-detail wireframes reflecting that original journey. Label any unverified screens and proposed adaptations explicitly.
4. Review a small modern content sample: one career path, its courses, one shop, a few possessions, and representative clerk/event writing.
5. Record the owner's keep/reskin/change decisions. Prepare an agreed scope and remaining research list before application implementation.

## Restrained iteration suggestions

These are alternatives to consider after reviewing the original, not a replacement specification.

| Original reference | Candidate iteration | Why consider it / what to preserve |
| --- | --- | --- |
| [Setup and multiplayer](../original-game/setup-multiplayer.md) | Keep independent goal selection and familiar player/AI choices; add short plain-language explanations beside existing controls. Consider a few labelled goal presets only after confirming the original values. | Helps children aged 8 and 11 and new adult players understand the same choices. Preserve customisation and the shared-device rhythm. Do not assume hidden player information or an online lobby. |
| [Town and screen layout](../original-game/town-and-screen-layout.md) | Retain the compact ring, recognisable destinations, central location view, portraits, and clear time display. Explore original illustrated retro storefronts and characters. | Maintains the board's identity and route-planning readability. Compare one faithful wireframe and one art sample before moving buildings or inventing navigation patterns. |
| [Locations and actions](../original-game/locations-and-actions.md) | Preserve each building's role and existing action structure first. Modernise the business names and clerk personas; add concise feedback on costs and unmet requirements where useful. | Makes the setting contemporary while preserving the work/shop/study/rent loop. Restrained Australian flavour can live in a few names or jokes rather than a new cultural subsystem. |
| [Content progression](../original-game/content-progression.md) | Map existing careers and qualifications to modern equivalents with comparable prerequisites, wages, and steps. Explore trades, technical support, healthcare administration, and contemporary retail as candidate replacements. | New labels can be relatable without changing the progression graph. Compare role-for-role substitutions before adding extra career branches or institutions. |
| [Progression and finish](../original-game/progression-and-finish.md) | Retain the familiar four-goal structure. Consider clearer explanations of goal calculation, achievements, debts, and setbacks, plus an accessible recap. | Improves legibility without flattening the race or changing victory logic. Preserve the owner's preferred economic humps. Confirm any gentler setup separately. |
| [Time and actions](../rules-audit/time-and-actions.md), [economy](../rules-audit/economy.md) | Keep the ordinary time costs and economic relationships as the first balancing baseline. Decide explicitly which verified quirks to preserve using their package/native evidence and any focused runtime corroboration required for the decision. | Preserves the strategic tradeoffs. Bug fixes or smoothing are rule changes, even when they look small. |
| [Weekly processing](../rules-audit/weekly-processing.md) | Rewrite event humour with fresh characters, purchases, and contemporary situations while preserving timing and mechanical consequences initially. | Retains the original's everyday absurdity. Test comprehension and comic tone with the children and adults; no extra stress, popularity, or social-media meter is implied. |

## Suggested review artifacts

- A keep/reskin/change matrix linked to the original evidence and decisions.
- Wireframes for setup, board/location, statistics/goals, handover, save/resume, and finish; mark uncertain original states rather than filling them silently.
- A role-preserving content mapping with one worked career/course path and a small shop inventory.
- A visual comparison sheet using original written analysis and newly created art samples, with a proposed storefront, clerk portrait, interface panel, and apartment possession.
- A short family play-test script: find a job, explain a rejection, plan a rent week, spot a good economic opportunity, understand the next player's turn, and explain how to win.

## Completion criteria

The owner can identify what is inherited from the original, what is proposed to change, and why. Important unknowns have explicit follow-up evidence tasks. No feature is approved simply because it appears in a mockup. Application work begins only after the owner's direction, in accordance with [AGENTS.md](../../AGENTS.md).
