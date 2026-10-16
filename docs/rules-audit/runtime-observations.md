# Controlled runtime observations: first website session

Session started 2026-10-15; resumed 2026-10-16. Evidence class: **OBSERVED** for the specific screens/actions below, separate from published SCRIPT findings. Reference URL: <https://jonesinthefastlane.com/>. A fresh independent download during this session matched the recorded bundle: 1,078,159 bytes, SHA-256 `c08f3310f4f9cf47316bc32745507ae065bba7741430f7c3620602f534c46180`, version marker 1.000.060. The browser's exact response bytes were not intercepted. No edited save, debugger, memory inspection or injected game state was used.

The site ran in the Codex in-app browser, using its supplied js-dos runtime. The console reported unavailable WebGL and fallback to 2D rendering. Precise emulator build, original-hardware audio equivalence, deterministic RNG state and persistent save export were not verified. The canvas reported 320 × 200, initially displayed at 1152 × 720 within a 1280 × 720 viewport. The later browser panel narrowed; continued captures are 621 pixels wide. Captures retain the viewport and emulator overlays; per-file dimensions are recorded in the manifest. Original captures stay under ignored `work/runtime-validation/2026-10-15/` and `work/runtime-validation/2026-10-16-continuation/`.

## Actual sequence and bounded conclusions

This session uses **two humans**, not the fresh-solo variants in RT02/03. Player 1 chooses the first appearance; player 2 chooses the second. Default targets are initially 50 each. Player 1's wealth slider was dragged until total goal points read 230; player 2 inherited that same visible arrangement/total. The exact drag distance is not a new UI specification.

| Observation | Action and visible result | Evidence files / scope |
| --- | --- | --- |
| OBS-001 | Startup shows Play Game, Restore Game and Watch Demo. Play leads to four numbered human-count choices. | `01-startup.jpg`, `02-player-count.jpg` |
| OBS-002 | Default player-1 goal total200; after dragging wealth, total230. Player2 setup shows total230 with the same star arrangement. First chosen appearance is visibly dimmed in player2 selection; final button changes Next→Play. | `03`–`07` captures; supports inheritance and dimming for this setup; refusing reselection was not separately tested |
| OBS-003 | Two-human configuration enters week1/player1 directly, with no Jones offer encountered. The ordinary town has a large central player body and four numbered corner markers while no location is open. | `08-p1-initial-town.jpg`; this is ordinary board composition, not evidence of a privacy/ready interstitial |
| OBS-004 | First statistics: unemployed, cash200, savings0, rent owed0, loan0, total goods0. A market keyboard attempt did not change those balances; it is not counted as a purchase. | `10-p1-statistics-cash200.jpg`; keyboard behaviour is not established by that attempt |
| OBS-005 | Direct mouse selection of Food For 1 Week reduces cash200→148. Statistics confirms cash148, savings0 and total durable goods0. | `09`, `11`, `12` captures. Actual cost52; do not assume the economy began at a reading of100 |
| OBS-006 | Bank Deposit twice changes cash148→48→0. Statistics confirms savings148/cash0. The second click transfers the remaining48 even though the menu's nominal Deposit label is100. | `13`–`16` captures; confirms partial final deposit in this ordinary balance range |
| OBS-007 | After repeated resident Relax actions filled player1’s clock, Done handed over to player2. Week stayed1; central body/corner markers/marble changed and the clock reset. Player2 Statistics showed cash200, savings0, rent/loan/goods0. | `17`–`20` captures; no blocking ready/privacy step was encountered |
| OBS-009 | Employment → Monolith job list offered Cook at $3/hour; selecting it returned a success speech bubble in the parent agency. | `27`–`29` continued captures; normal application/return observed |
| OBS-010 | First workplace Work selection raised cash0→24. F4 confirmed Works at Monolith, As a Cook, Hourly wage3, Cash24, Savings148 and Rent Owed0. | `30`–`32` continued captures; $24 equals eight displayed wage units; exact elapsed-time counter was not read numerically |
| OBS-011 | Repeated Work reached cash120,144,168 with the clock approaching full. The last Work raised cash168→172 and filled the clock; the next Work displayed a no-time refusal and left cash172. | `33`–`37` continued captures. The $4 final payment is consistent with the published one-hour calculation at wage3, but remaining hours were not independently read as a number |

Image numbering identifies the chronological capture prefix; full filenames/hashes are recorded in the associated metadata. A screenshot during a transition is not used as a final balance reading. The displayed market price is resolved by the clear statistics difference, rather than guessing tiny calculator glyphs.

## OBS-008: interrupted food comparison and continuation

Player2 bought no food, entered the resident apartment, used Relax until the clock filled, and exited. The round wrapped to player1, week2. Capture21 shows player2 at exhaustion; capture22 shows player1’s weekend panel, cash0 and week2. After dismissing it, the following timed notice sequence was not captured before an interruption.

On resuming the same tab on 2026-10-16, capture23 shows player1/week2 with a clear clock, before any new travel/action. Capture24 confirms cash0/savings148. Paging Statistics down shows Casual Clothes under Goods, no food stock line and no durable appliance entries (capture25). The absence of the 20-hour red clock sector is consistent with NEED-003’s spoilage sentinel path. **The spoilage notice, its happiness delta and intermediate state were not captured, so this is partial corroboration, not a fully passed RT02.** No debugger or state edit filled the evidence gap.

The independent solo control resumed successfully and is [recorded separately](runtime-solo-control.md). It showed a roughly one-third red week2 clock with no food and cash0/savings200. The contrast with the clear-clock groceries run is observed; identifying the exact internal hunger/spoilage branches and their happiness deltas remains SCRIPT-based. The other interrupted work-control attempt produced no runtime finding.

## Pending comparisons in this session

The setup, transaction and first handover observations above are established for this run. The [independent solo control](runtime-solo-control.md) now corroborates the contrasting graphical time outcome and unchanged savings. Capturing both complete notice sequences and happiness deltas remains pending. Neither a plan nor a matching asset composite is a passed runtime case. Loan charges, first-durable happiness, exact partial-work residual/rounding and garnishment, forced random thresholds, CD differences, every save path and overall AI fairness remain outside this first capture sequence unless separately added with evidence.

## Evidence gallery and manifest

The [capture manifest](../../artifacts/rules-audit/runtime-capture-manifest.json) records local filenames, hashes, dimensions and observation IDs, without original pixels. `python tools/research/index_runtime_captures.py` builds the ignored `work/runtime-validation/index.html` from available local captures; it reports missing inputs rather than downloading substitute screenshots. On another machine, replay the documented actions to create new evidence; hashes will identify new captures rather than match an expected rendering automatically.

## End of this gameplay pass

The session was left at Monolith, player1/week2, with cash172 and an exhausted clock after the refusal. No purchase at exhausted time was attempted; T02 remains SCRIPT-derived. On 2026-10-16 the owner redirected effort toward reverse engineering. Further gameplay is deferred to narrow experiments that discriminate an unresolved bytecode/runtime question. The next research priority is correspondence between the actual package scripts and the published decompilation, especially the suspicious branches, rather than broader exploratory play.
