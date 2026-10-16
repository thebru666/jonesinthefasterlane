# Economy, prices, wages, and shocks

Pass 1, 2026-10-15; targeted package verification added 2026-10-16. Status: partial. Evidence: SCRIPT from [S02 and S04](../discovery/source-register.md), original analytical calculations, and **BYTECODE** for the adjustment condition and direct parent-argument access in [ECON-B01–002](bytecode-economy-presentation.md). These checks do not establish whole-script equivalence or runtime price behaviour. All adaptation mappings remain **undecided**.

## ECON-001: layered economy with memory

The game stores eight pairs of **trend index** and **reading**: a main economy, investments, goods, and five individually varying investment markets. A reading starts at 100; index state persists between updates.

Each player's start-turn runs the economy once, in this order:

1. Main economy updates using its previous state.
2. Investment and goods readings each update using their own state, with the new main trend as an input.
3. Gold, silver, pork, blue-chip, and penny markets each update using their own state, with the new investment trend as an input.

General shop/job offers use the **goods reading**, not the main reading used to determine economic shock eligibility. Investment valuation uses the individual market readings. There is no single universal percentage that explains every price at once.

Evidence: [Main.sc, globals 307–322](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/Main.sc#L406); [economicIndex.sc, economicIndex.doit](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/economicIndex.sc#L201); [WButton.sc, CostDItem.init](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/WButton.sc#L177); [room1.sc, calcLiquidAssets](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L849).

## ECON-002: trend and reading update

The following is an analytical description of the published script, not imported game code. Let `I` be the previous trend, `R` the previous reading, and `P` the parent trend. `trunc` means division toward zero; random endpoints are inclusive.

1. A crash biases `I` downward by 3, clamping that change to −3 when starting above −3; if already at or below −3, decrement it instead. A boom mirrors that operation upward around +3.
2. Compute an upward recovery allowance from low readings and a downward allowance from high readings. In the floppy edition: recovery allowance 2 below 40, 1 below 70, otherwise 0; downward allowance 2 above 160, 1 above 130, otherwise 0.
3. Draw an integer between `−3 − downwardAllowance` and `3 + recoveryAllowance`. Move `I` one step toward that draw, with the corresponding bound. Consequently the index is not universally restricted to −3…+3.
4. Draw adjustment `A` between `−3 + 2 × min(I, 0)` and `3 + 2 × max(I, 0)`.
5. If `A` equals its lower endpoint, subtract another random value between 0 and `risk × abs(I)`. The following alternative repeats the **same lower-endpoint condition**, making its apparent intended positive counterpart unreachable. This is now confirmed in the actual website script107 at `0x0179` and `0x0198`; see [ECON-B01](bytecode-economy-presentation.md#econ-b01-the-duplicated-condition-exists-in-the-actual-game).
6. Add `A + trunc(P/3)` to the reading. The main update omits the parent argument. Actual bytecode guards that argument into an unused temporary, then reads parameter slot 1 directly for this calculation. Its value when omitted remains unproved; **do not assume zero**. See [ECON-B02](bytecode-economy-presentation.md#econ-b02-the-omitted-parent-argument-needs-an-interpreter-investigation).
7. Apply an event multiplier, if present, then clamp the reading: floppy 10…190; CD 70…190.

Risk is 4 by default, 2 for gold and silver, 1 for blue-chip, and 10 for penny stock.

Evidence: [economicIndex.sc, EconomicIndex.init / doit and instance defaults](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/economicIndex.sc#L29).

The duplicated condition is a **package-confirmed apparent implementation defect**, not a verified design intention or a decompiler-only suspicion. Do not patch it silently while claiming exact fidelity. This pass has not simulated long runs, so it makes no claim that a permanent slump has been statistically demonstrated.

## ECON-003: exact ordinary price calculation

The shared price helper converts a reading `R` into an integer factor `F`:

- Below 100: `F = R − trunc(2 × (100 − R) / 3)`.
- At or above 100: `F = R + trunc(2 × (R − 100) / 3)`.
- Clamp `F` to a minimum of 50.

For base price `B`, in the normal non-overflow range:

`price = max(1, trunc(B × trunc(F/10) / 10) + trunc(B × (F mod 10) / 100))`

The split integer operations matter: this need not equal one final rounding of `B × F / 100`. The actual helper also guards a signed-overflow case in an intermediate product; very large base prices require separate validation before assuming this normal-range expression is sufficient.

| Reading | Factor | Base $50 | Base $325 |
| --- | --- | --- | --- |
| 10 | 50 | $25 | $162 |
| 70 | 50 | $25 | $162 |
| 100 | 100 | $50 | $325 |
| 130 | 150 | $75 | $487 |
| 190 | 250 | $125 | $812 |

Although the floppy reading can fall to 10, ordinary prices do **not** fall to 10% of base: the helper's factor floor is 50%. The very low reading still matters to trend recovery and future shock eligibility.

Evidence: [n109.sc, proc109_0](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/n109.sc#L10). Examples are independently recorded in [arithmetic fixtures](../../artifacts/rules-audit/2026-10-15-arithmetic-fixtures.json).

## ECON-004: offered prices versus existing contracts

The shared non-fixed-price item initialiser uses the goods reading. Examined callers establish the following:

- Job applications set the player's wage to the current offer when successful. Existing wages are stored rather than recomputed continuously. Applying again for the same position can request a raise; it does not lower the wage automatically when the offer falls.
- Moving to an apartment stores the selected offered price as current rent. Existing rent is then used by payment/bookkeeping paths rather than being continuously repriced. Base rents are $325 and $475.
- University enrollment uses a $50 base price through the same helper. It is a fee to unlock enrollment capacity; study uses separate progress rules.
- `fixedPrice` items bypass the shared repricing initialiser; item-specific exceptions require a full catalogue rather than a universal “all prices fluctuate” rule.

Evidence: [employment.sc, JobDItem.doit](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/employment.sc#L206); [rentOffice.sc, low-cost apartment](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/rentOffice.sc#L483), [security apartment](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/rentOffice.sc#L605); [university.sc, enrollmentFee](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/university.sc#L522); [WButton.sc, CostDItem](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/WButton.sc#L162).

Strategic implication: a falling economy can make a previously secured wage valuable while offering cheaper purchases and a chance to move into a lower rent. A boom can improve job offers while making qualifications and goods costlier. This is a strong preservation candidate for the requested economic humps.

## ECON-005: shock eligibility and probabilities

Let `N` be the stored number of players and `Rmain` the main reading **before** this turn's update.

| Edition | Crash eligibility and roll | Boom eligibility and roll |
| --- | --- | --- |
| Floppy | Week ≥4 and `Rmain ≥80`; zero on Random(0, 20N) | If crash branch did not succeed and `Rmain ≤120`; zero on Random(0, 30N) |
| CD | Week ≥8 and `Rmain ≥80`; zero on Random(0, 30N) | If crash branch did not succeed, week ≥8 and `Rmain ≤120`; zero on Random(0, 30N) |

Inclusive bounds mean eligible floppy crash chance is `1/(20N+1)` per turn, and the boom roll is `1/(30N+1)` when reached. In the overlapping region, the unconditional boom chance is reduced by the chance that the crash branch has already succeeded. These are per-turn opportunities, not per-round guarantees.

A successful crash selects severity code 1, 2, or 3 uniformly. Code 1 is the strongest effect. A boom and crash cannot both be selected in the same invocation.

Evidence: [floppy economicIndex.doit](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/economicIndex.sc#L201); [CD comparison](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-cd-dos-1.0/src/economicIndex.sc#L203); [S04 random semantics](../discovery/source-register.md#s04-sci-arithmetic-and-random-semantics).

## ECON-006: a shock affects more than the active player

The event flags bias every economic layer during its update. After each layer's ordinary adjustment, crash severity codes 1/2/3 multiply its reading by 17/20, 18/20, or 19/20, respectively; a boom multiplies by 11/10. Integer truncation and the reading clamp follow. These are **reading** changes, not a promise that all visible prices change by exactly 15%, 10%, 5%, or 10%.

Later in start-turn processing, severity 1 or 2 calls `Player.doScandal` for unfinished players, including players whose turn is not active:

| Code | Employment effect in the published script | Additional effect |
| --- | --- | --- |
| 1 | Employed player is always dismissed | Sets the low bank-balance field to zero; high-balance representation requires separate checking |
| 2 | Employed player has a 1/2 dismissal chance; otherwise wage becomes `max(1, trunc(wage × 0.8))` | No bank reset in this method |
| 3 | No `doScandal` call from the examined event path | Still changes readings and active-player happiness |

Dismissal or a pay cut has its own happiness effect for the affected player. Separately, the active player takes event happiness changes: severity 1/2/3 gives −3/−2/−1, plus −5/−2/−1 if investment assets exceed $1,000 (or have a high-word balance). A boom gives +5 only to the active player meeting that investment test.

Evidence: [economicIndex.sc, EconomicIndex.doit](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/economicIndex.sc#L125); [startTrn.sc, states 24–32](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/startTrn.sc#L596); [room1.sc, doScandal](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/room1.sc#L812).

## ECON-007: important floppy/CD differences

| Mechanic | Floppy 1.000.060 | CD 1.0 |
| --- | --- | --- |
| Minimum reading | 10 | 70 |
| Recovery allowance 2 / 1 | Reading below 40 / below 70 | Below 80 / below 90 |
| Crash earliest week | 4 | 8 |
| Crash roll denominator | 20N + 1 | 30N + 1 |
| Boom earliest week | No week gate in this branch | 8 |
| Repeated lower-endpoint adjustment condition | Present | Present in inspected comparison |

Evidence: direct comparison of the pinned [floppy](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/economicIndex.sc) and [CD](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-cd-dos-1.0/src/economicIndex.sc) economy scripts. Other CD scripts were downloaded as references but have not received a full edition-difference audit.

The CD changes strengthen recovery pressure earlier and prevent the reading falling as far. That supports treating it as a candidate reference for recovery behaviour, but choosing CD behaviour would depart from the website's floppy edition. No choice has been approved yet.

## Remaining work

Reproduce price/contract behaviour; extend targeted bundle/script correspondence checks beyond ECON-B01–002; resolve the omitted parent parameter through the caller/interpreter frame; trace fixed-price/pawn exceptions; audit all investment transactions and cash high words; measure long-run economy distributions and multiplayer effects after the arithmetic is validated. See [validation backlog](validation-backlog.md).
