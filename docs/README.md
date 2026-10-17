# Documentation

[View all seven rendered diagrams](diagrams/README.md): PNG previews and zoomable SVGs for the career graph, game flow, original progression, town and screen relationships. Earlier drafts are labelled separately from current proposals and original references.

## Original game: starting point for iteration

Start with the [research handoff](planning/original-research-handoff.md) for requirement coverage, the evidence reading path, known limits and the next planning task.

- [Connected game flow and rule contract](original-game/game-flow-and-rule-contract.md): lifecycle, screen families, action loops and state distinctions.

- [Original-game baseline](original-game/README.md): existing summaries and documented original setup, town, screens, actions, content, progress, saves, and finish.
- [Screen reconstruction studies](original-game/screen-reconstruction.md): local composites and annotated source layers, with state/geometry limits.
- [Follow-up iteration brief](planning/follow-up-original-first-iteration.md): restrained suggestions to review against that baseline; no changes approved.

## Planning

[Career budgets v1](planning/career-budget-comparison-v1.md): provisional butcher/trades/doctor costs and payoffs, with chart, auditable ledger, eligibility constraints and cash-buffer/setback comparisons. Analytical planning, not a playable model or approved balance.

Current career expansion: [career/town graph v2](planning/career-and-town-graph-v2.md), preserving the early butcher route and proposing skilled trades, doctor and other professional paths, with a compact-town roster for review.

Latest owner review: [employer options, recruited offers and useful possessions](planning/employers-offers-and-useful-possessions.md), with accepted principles recorded in D014–D018 and detailed alternatives still open.

Start with the [modern-direction review pack](planning/modern-direction-review.md) for the latest owner pointers and proposed amendments: [transport](planning/transport-proposal.md), [modern town/jobs/courses/devices](planning/modern-town-and-content.md) and [visual concepts](planning/visual-direction-v1.md). Exact choices remain open for iteration; no application is implemented.

- [2.0 draft specification](planning/2.0-draft-specification.md): proposed keep/reskin/change scope, screen flow, layout sketches, slice and family review.
- [Compatibility proposals](planning/compatibility-proposals.md): seventeen explicit recommendations for preserving or changing audited rules and quirks.
- [Modern content sample](planning/content-iteration-sample.md): thirteen destination signs, one verified career/course mapping, possessions and fresh humour.
- [Architecture and validation proposal](planning/architecture-and-validation-proposal.md): simulation/UI boundaries, stable saves, reproducibility and staged validation.

These four documents are an **unapproved review pack**, not permission to implement the application.

- [Rules readiness for 2.0](planning/rules-readiness.md): established foundation, remaining research and compatibility choices.
- [Project brief](planning/project-brief.md): agreed audience, tone, scope, and process.
- [Decisions](planning/decisions.md): confirmed direction, recommendations, and unresolved choices.
- [Audit implications](planning/audit-implications.md): economic fidelity, edition baseline, and compatibility choices from pass 1.
- [Consistency and readiness review](planning/consistency-review.md): what is established and what still blocks a complete flow/layout specification.
- [Earlier flow and layout outline](planning/flow-and-layout-outline.md): historical speculative outline; use the original-game baseline first.

## Discovery

- [Findings](discovery/findings.md): inspected package, tool feasibility, sources, and limitations.
- [Source register](discovery/source-register.md): pinned script references, manual inspection, and arithmetic semantics.
- [Rebuild original assets locally](discovery/rebuild-original-assets.md): checksum-locked source, exporters, catalogue coverage and limitations.
- [Decompile the original scripts locally](discovery/decompile-original-scripts.md): direct bytecode decoder, reproducible outputs and semantic limits.
- [Inspect the original DOS interpreter](discovery/inspect-dos-interpreter.md): reproducible local unpacking, native addresses and evidence boundaries.
- [Artifact index](../artifacts/README.md): committed research evidence and local-only material policy.

## Rules audit

- [Audit plan and coverage](rules-audit/README.md)
- [Direct bytecode verification](rules-audit/bytecode-verification.md): actual-package logic findings and remaining gaps.
- [Native travel ordering](rules-audit/dos-travel-ordering.md), [bank continuation](rules-audit/bank-refresh-continuation.md), [native saves/random state](rules-audit/dos-save-state.md) and [stereo fallback](rules-audit/dos-stereo-fallback.md): selected original-interpreter and callback gaps resolved statically.
- [Inventory grouping](rules-audit/inventory-grouping.md), [used-stock transfer](rules-audit/pawn-used-stock.md), [investment transactions](rules-audit/investment-transactions.md) and [money boundaries](rules-audit/money-word-boundaries.md): grouped-state and pricing/ownership contracts.
- [Initial player state](rules-audit/initial-player-state.md), [clothing lifecycle](rules-audit/clothing-lifecycle.md), [fast-food bonuses](rules-audit/fast-food-bonuses.md) and [Z-Mart assortment](rules-audit/discount-assortment.md): everyday initialization, rewards and reset rules.
- [Happiness catalogue](rules-audit/happiness-catalogue.md): all76 identified literal modifier sites, amount/recipient/ordering and evidence limits.
- [Rule record template](rules-audit/rule-template.md)
- [Employment](rules-audit/employment.md): package-verified hiring, raises, work, growth and dismissal.
- [Education](rules-audit/education.md): package-verified enrollment, course progression, equipment and rewards.
- [Turn and opponent bytecode trace](rules-audit/bytecode-weekly-opponent.md): rotation, preparation, finish gates and computer execution.
- [All-destination computer action trace](rules-audit/bytecode-ai-actions.md): event routing and confirmation shortcuts.
- [Needs/event bytecode trace](rules-audit/bytecode-needs-events.md): food, illness, selected theft/repairs, weekends, lottery, mugging and computer income.
- [Location, clock, score and persistence trace](rules-audit/bytecode-flow-and-persistence.md).
- [Travel timing](rules-audit/travel-timing.md), [score refresh](rules-audit/score-refresh.md) and [finance lifecycles](rules-audit/finance-lifecycle.md): focused ordering and boundary traces.
- [Economy call frames](rules-audit/economy-frame-semantics.md) and [original DOS randomness](rules-audit/dos-randomness.md): actual native interpreter findings.
- [Time and actions](rules-audit/time-and-actions.md)
- [Turn and weekly processing](rules-audit/weekly-processing.md)
- [Economy and edition differences](rules-audit/economy.md)
- [Computer opponent](rules-audit/computer-opponent.md)
- [Food and housing](rules-audit/food-and-housing.md)
- [Goods and finance](rules-audit/goods-and-finance.md)
- [Weekends, tickets and personal events](rules-audit/random-events.md)
- [Runtime observations](rules-audit/runtime-observations.md) and [independent solo control](rules-audit/runtime-solo-control.md): actual visible outcomes, capture provenance and limits.
- [Controlled runtime test plan](rules-audit/runtime-test-plan.md)
- [Validation backlog](rules-audit/validation-backlog.md)

## Planned deliverables

1. Original-game research reference: supplied at the bounded coverage in the [handoff](planning/original-research-handoff.md); full engine equivalence is not claimed.
2. Adaptation specification: draft review pack supplied above; owner choices and an agreed specification remain.
3. Content and art bible: a small content sample is supplied; full mapping, original art samples and approved style remain.
4. Architecture and validation: proposal supplied; detailed adopted rules, schema, implementation and actual playtests remain.

Use relative Markdown links so documentation works both on GitHub and locally.
