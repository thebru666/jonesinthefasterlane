# Architecture and validation proposal

2026-10-17. **PROPOSAL — planning only.** Supports the [draft game specification](2.0-draft-specification.md); no application code or final save schema is introduced. React/TypeScript, shared action rules, reproducibility and local persistence follow the [brief](project-brief.md), while the contracts below still require review.

## Recommended shape

Use React + TypeScript + Vite for presentation and a plain TypeScript simulation that runs without React, DOM, network or wall-clock time. A browser game of lists, portraits, route markers and short animations does not yet justify a separate game framework. SVG/CSS can draw a responsive town; selected animation or audio libraries can be evaluated when an approved art sample demonstrates a need.

| Boundary | Responsibility | Must not decide |
| --- | --- | --- |
| Content | Stable role/item/job/course IDs, names, requirements, balance tables, dialogue references | Turn ordering or mutable player state |
| Simulation | Validate an intent, execute ordered costs/effects/draws, emit outcomes and next flow state | Pixel position, animation speed or browser storage |
| Opponent policy | Choose from the same intents using its explicitly permitted information | Direct balance edits, free purchases or bypassing human action costs |
| Presentation | Render state, collect input, explain outcomes, animate accepted effects | Eligibility, wages, rewards, score refresh or random rule outcomes |
| Persistence | Serialize/validate supported stable states and restore the same rules/content version | Silently reroll outcomes or reset a loaded visit/turn |

Original controller/AI behaviour is the [research reference](../rules-audit/bytecode-ai-actions.md), not a claim that every original privilege satisfies the proposed shared-rules policy. Decide those differences in the [compatibility review](compatibility-proposals.md).

An intent means something such as travel to destination, apply for job, work, buy item, attend course, transfer money or exit location. Availability and results come from simulation rules. UI disabling is an aid; the simulation must also reject invalid intents so human and computer players cannot reach different rules through different controls.

## Ordered transitions and information

Represent the flow explicitly: setup, preparation, board, travel, visit, nested selection, pending feedback, handover and finish. Keep active participant, shared week and visit-local/per-turn flags distinct. Use the [original state inventory](../original-game/game-flow-and-rule-contract.md#state-a-faithful-model-must-preserve) as the checklist, not a ready-made class layout.

An accepted action applies a defined sequence once: checks, rule draws, costs, effects, score/cache updates and notices in the order adopted for that action. A refusal can still cost time or consume randomness when the reference says so. Do not turn the entire game into “charge only on success” or “require the full cost remaining.”

**Proposed departure:** reading Goals/Statistics, rendering, resizing and moving keyboard focus are read-only. Any intentional cache/score refresh belongs to a named simulation transition, never a React render. This requires an explicit successor score-refresh decision; it does not reproduce the original Statistics cache side effect. The [score audit](../rules-audit/score-refresh.md) and compatibility proposal describe the choice.

Acknowledgement advances a recorded continuation. Repeated clicks must not rerun salary, rent, lotteries or turn preparation. An action already resolved before a notice stays resolved when that notice is dismissed. Animation skip/reduced motion changes presentation duration, not action cost or random draws.

## Randomness and saves

Recommend one documented, versioned simulation PRNG stream with its state stored in saves; presentation effects use a separate source. Identical supported state + rules/content versions + seed + intents should yield the same rule outcomes. This is a modern reproducibility contract, not DOS random-call equivalence: the [original generator](../rules-audit/dos-randomness.md) and [seed serialization gap](../rules-audit/dos-save-state.md) are documented separately.

Recommend **one automatic current-game checkpoint plus manual export/import** initially. A browser storage adapter can use IndexedDB; a manual JSON export provides portability. Neither storage choice requires a backend. Validate an import before replacing a current game; show a clear unsupported-version or malformed-save error and preserve the existing checkpoint on failure.

Checkpoint only at supported stable boundaries: town ready, location or nested selection ready with no unresolved mutation, incoming preparation completed, and finish ready. Save the active player/week, location/view, spent time and travel residue if retained, all economic/inventory flags, rule PRNG state, placements, and rules/content/schema identifiers. A selected-but-unconfirmed purchase must not become a committed transaction after reload.

During travel or a pending notice sequence, retain the previous stable checkpoint and report that status. Do not claim every visible frame is saved. At a stable nested view, preserve selection context without recharging entry or rereading assortment randomness. Closing during unsaved presentation can replay from the earlier checkpoint; replaying the same intents reproduces the same lottery result. Different actions can change draw order and outcomes; this is not an anti-reload enforcement system. User-triggered export while busy should be queued until the next stable boundary, with visible feedback.

These stable-boundary saves deliberately avoid serializing a suspended DOS interpreter or arbitrary JavaScript closures. If later requirements include mid-notice saves, extend the schema with serializable pending outcomes and continuation cursors; that is additional scope. Cross-version migration needs explicit transforms and checks; do not promise arbitrary future compatibility.

## Validation plan

Tests below are proposed future implementation checks. The research fixtures validate their stated analytical bounds, not a successor implementation that does not yet exist.

| Layer | Meaningful evidence to require |
| --- | --- |
| Core transitions | Fixed cases for original allocation, hiring/rejection memory, partial work versus lesson progress, course prerequisites, rent/loan/pawn timing, food/clothes and adopted quirk choices |
| Lifecycle | One-/two-/four-human rotation, finished-player removal, week increment, economy per incoming participant, week1 skip and start-turn finish gates |
| Transactions | No unintended duplicate mutation; unaffordable and timed-out attempts follow their specific cost/draw contract; used goods and grouped quantities match adopted rules |
| Replay | Same seed and intent log yields identical state/outcomes in headless simulation; adding presentation frames or opening read-only panels does not alter results |
| Save/restore | Resume from town and nested visit preserves next outcome, per-turn assortment, time, bank balances and placement; import failure leaves current save intact |
| Opponent | Same intent fixtures for human and AI; invalid proposals are rejected; information privileges match the chosen difficulty policy |
| UI | Keyboard and touch navigation, readable scaling, focus returns to caller, acknowledge-once feedback, truthful costs and save status |
| Family | Repeat the [review script](2.0-draft-specification.md#family-review-script), capture assistance and misunderstanding, then change explanations before adding systems |
| Balance | After full rules coverage, run seeded campaigns and human sessions; report session lengths, job/goal routes, setbacks and rival results before tuning |

For each rule scenario record original evidence, adopted successor decision, input state/intents and expected effects. Compare to the original only within its evidenced scope. Correctness against the selected successor contract and resemblance to the original are related but different checks.

## Planning milestones

1. Record owner choices for reference edition, compatibility rows, modes/devices and screen flow; revise this pack into an agreed specification.
2. Approve a small content and illustrated-art comparison without committing to a full asset set.
3. On explicit direction to build, implement the bounded solo slice in the draft specification with headless rules and stable saves.
4. Expand to full destination/rule coverage, then shared-device and computer modes; assess full-game balance and family comprehension.

No backend, account system, online multiplayer, leaderboard service, public deployment or application implementation is part of this documentation step.
