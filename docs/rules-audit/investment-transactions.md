# Investment prices, unit trades and broker-entry lifetime

Audited 2026-10-16 against website DOS **1.000.060**. Evidence **BYTECODE**, selected actual package records and paths; no runtime trading or complete SCI interpreter equivalence is claimed. [Verification metadata](../../artifacts/rules-audit/investment-transactions-verification.json) records whole-resource and range hashes, all six records, price setters, transaction witnesses and symbolic checks. Original payloads remain ignored. This verifies and narrows [FIN-004](goods-and-finance.md#fin-004-six-investments-one-unit-per-transaction).

## Six records and the price used by a trade

Each participant owns an ordered six-element investment list. `Player.init` constructs six `I` records with base values and indices at the sends below; `I.init` appends each to that list. The class default is shares0. The broker's selected icon key0…5 indexes the same list. The broker icons are separate objects from the participant's owned investment records.

| Key | Investment | Owned base / index; script1 initialization send | Broker record / literal field | Price initialization and setter, script213 |
| --- | --- | --- | --- | --- |
| 0 | Treasury bills | 100 / 65; `0x0b34` | object `0x05ca`; price100 at `0x0602`, fixedPrice1; UI basePrice0 | Fixed record value; no instrument-specific init setter |
| 1 | Gold | 413 / 66; `0x0b50` | object `0x06ce`; base413 at `0x0708` | `0x06b4–0x06c0`: reading global310 → price helper at `0x06ba` → price write `0x06be` |
| 2 | Silver | 14 / 67; `0x0b6b` | object `0x07d6`; base14 at `0x0810` | `0x07bc–0x07c8`: global311 → helper `0x07c2` → write `0x07c6` |
| 3 | Pork bellies | 20 / 68; `0x0b86` | object `0x08de`; base20 at `0x0918` | `0x08c4–0x08d0`: global312 → helper `0x08ca` → write `0x08ce` |
| 4 | Blue-chip stocks | 49 / 69; `0x0ba1` | object `0x09e6`; base49 at `0x0a20` | `0x09cc–0x09d8`: global313 → helper `0x09d2` → write `0x09d6` |
| 5 | Penny stocks | 7 / 70; `0x0bbc` | object `0x0af0`; base7 at `0x0b2a` | `0x0ad6–0x0ae2`: global314 → helper `0x0adc` → write `0x0ae0` |

Broker initialization sends `eachElementDo(init)` before opening/drawing the dialog (`213:0x0112`). The five variable-price instruments call script109 export0 with their own market reading and base. This confirms individual-market pricing; the goods reading is not substituted. Buy and Sell read the selected icon's stored `price`, rather than rerunning the economic formula for each trade. The fixed Treasury-bill price comes from its icon record; its owned record separately has base100 for valuation.

For ordinary non-overflow positive values, let r be the market reading and b the base. The helper (`109:0x000c–0x0085`) computes:

`E = max(50, r − trunc(2 × (100 − r) / 3))` for r<100; otherwise `E = max(50, r + trunc(2 × (r − 100) / 3))`.

`price = max(1, trunc(b × trunc(E / 10) / 10) + trunc(b × (E mod 10) / 100))`.

The two truncated terms are separate. The raw helper also replaces a negative intermediate product with32767; that overflow-sensitive branch is not equivalent to arbitrary-precision multiplication followed by one rounding step. The table below is an analytical low-word check, not observed prices:

| Market reading | Treasury bills | Gold | Silver | Pork | Blue chip | Penny |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 70 | 100 | 206 | 7 | 10 | 24 | 3 |
| 100 | 100 | 413 | 14 | 20 | 49 | 7 |
| 130 | 100 | 619 | 21 | 30 | 73 | 10 |

The Holdings controls multiply each owned record's shares by its selected icon's unit price (`115` export1) and format a money value. The local display-update helper (`213:0x0e7c–0x0ee1`) selects that holding control by key and sends erase/init/draw. It is not a second share mutation or an additional trade fee.

## Ordinary purchase and sale

`buyButton.doit` (`213:0x0c40–0x0ce1`) resolves the selected owned record by key and compares the carried-cash helper against the displayed price (`0x0c68–0x0c76`). Equality succeeds. It then:

1. Writes shares+1 at `0x0c8c`.
2. Calls Main cash helper10 with minus the price at `0x0c9b`.
3. Adds the price to the low `invAss` subtotal at `0x0cba`.
4. Refreshes the selected holding display at `0x0cc6`.
5. Calls the cash panel at `0x0cdd`, which recalculates assets.

Insufficient cash instead displays text213/5 and still reaches the final asset refresh; it changes no shares or cash on that branch. Savings are not automatically withdrawn. No quantity input or multi-share increment is present in the ordinary Buy handler.

`sellButton.doit` (`213:0x0d5e–0x0e19`) tests **nonzero** shares (`0x0d89–0x0d8b`). With ordinary nonnegative holdings that means at least one; the native condition is not a signed `shares>0` guard. It writes shares−1 at `0x0da1`, credits the displayed price through Main helper10 at `0x0dae`, subtracts that price from low `invAss` at `0x0dcd`, updates the holding display and finally recalculates assets at `0x0e15`. With zero holdings it displays text213/7 and still reaches that final refresh. Negative/wrapped or corrupted holdings remain outside the ordinary interpretation.

These cash calls sample cached liquid assets for stored Wealth before the later recalculation; updating assets does not itself update Wealth. See the [score-refresh contract](score-refresh.md). The manually changed investment subtotal is a low-word interim value, not the authoritative complete paired valuation.

## Treasury-bill fee versus its notice

After a successful sale, the selected icon is compared with the actual tBills object (`213:0x0ddd–0x0de4`). Only that branch calls cash helper10 with−3 at `0x0dea`. **The fee executes on every successful Treasury-bill sale**, before testing the notice flag. With unit price100, ordinary sale cash proceeds are97.

Global537 gates only the explanatory notice: if set it is cleared at `0x0df5`, then text213/6 is shown through the shared notice helper at `0x0dfe`. Start-turn changeState0 sets537 to1 at `111:0x0034`. This is a per-start-turn notice latch, not a per-broker-visit fee waiver. The helper invoked here does not test the nonessential-message flag. No corresponding fee call appears on successful sales of the other five instruments in this examined handler; this is a scoped statement about these buttons, not every possible investment event.

## See Broker cost, guard lifetime and exhausted time

`seeBroker.doit` (`204:0x0c88–0x0d32`) first tests spent time **!=60** at `0x0cb4–0x0cba`. If already60 it displays the no-time notice and returns without opening the broker. This test precedes the visit guard; even a previously paid-for broker visit cannot be reopened at60.

If time is not60 and script204 local0 is zero, it calls `timeKeep.doit(2)` at `0x0cca` and writes local0=1 at `0x0cce`. It then opens script213 at `0x0cee/0x0cf1`, with **no second time test after the charge**. Thus an ordinary spent time58 or59 reaches the clock cap60 and still opens the broker. The actor is stationary within the modal bank path; this does not insert immediate movement-driven handover. Buy/Sell contain no spent-time test and no timekeeper call. Trading can therefore continue in the opened dialog at60 under this static path. Once the broker is closed, the bank's See Broker guard refuses another opening at60.

While spent time remains below60, repeated broker openings during the same loaded bank dialog cost no further visit time: broker exit disposes script213 at `213:0x021a`, then returns to `bank.draw` (`204:0x0cfb`). It does not dispose script204 or clear its local0. The complete script204 instruction inventory finds only one ordinary local0 writer: `0x0cce`, setting it to1. Bank initialization does not explicitly reset that local.

Script204's locals resource initializes all three locals to zero. Full bank exit disposes its dialog and calls `DisposeScript(204)` at `0x03d4`. On an ordinary subsequent **fresh load of script204**, local0 consequently begins at its resource default zero, and the next accepted See Broker action charges again. This is the disposal/reload boundary that explains the original lifetime; it is not a weekly flag or the broker's separate local0. Merely re-invoking bank.init without a fresh load would not itself reset it.

The bytecode explicitly proves zero-initialized local data, the absence of a second reset writer, and the separate213/204 disposal calls. This pass does not claim a full native loader/refcount/restore audit. Retained or restored scripts, exceptional re-entry/global518 and deleted/restarted continuations remain distinct interpreter/state questions. The normal fresh-load rule no longer needs broad gameplay to identify its reset source.

## Planning consequence and limits

FIN-004's six bases, one-unit trades, market-specific pricing and repeated $3 fee agree with the actual package. Its earlier generic exhausted-time uncertainty can be narrowed to the concrete pre-charge/no-recheck path above. Its lifecycle wording should distinguish the bank script's local guard from the broker's own disposal and from abnormal retained/re-entered state. No application code, new mechanic or decision to fix these original behaviors is approved by this evidence.

Sources: [website archive](https://jonesinthefastlane.com/bundle.jsdos), [pinned comparison broker source](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/broker.sc), [comparison bank source](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/bank.sc), and [package/source register](../discovery/source-register.md). Raw package instructions, not conservative pseudocode across unknown blocks, settled the fields, arguments and branch order.
