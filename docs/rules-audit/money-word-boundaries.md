# Money pairs: carry, asset addition and display boundaries

Audited 2026-10-16 against website DOS **1.000.060**. Evidence **BYTECODE**, selected **DOS-STATIC** arithmetic handlers and nine **ANALYTICAL** fixtures. This does not execute SCI code or reproduce a high-balance game session. [Metadata](../../artifacts/rules-audit/money-word-boundaries.json) records resource/range hashes, constants, fixture inputs/results and limits. It strengthens the warning in [FIN-005](goods-and-finance.md#fin-005-valuation-money-score-and-integer-boundaries), rather than selecting a corrected numeric representation for2.0.

## MONEY-B01: these helpers do not share one normalization rule

A pair below is written **(high, low)**. The actual arithmetic words are16-bit; examples use signed low words and ordinary small high words. Three constants occur in different roles:

| Path | Actual package instructions | Selected behavior |
| --- | --- | --- |
| Main cash-change helper, export10 | `0:0x04ab`, `0x04b6`, `0x04d6` contain32767 | Positive change with unsigned summed low word≥32767 increments high once and subtracts32767. Negative change borrows32767 only when high is nonzero and the signed summed low word is negative. |
| Main pair-add helper, export12 | Threshold32767 at `0x05c7`; adjustment−32768 at `0x05b5/0x05d6` | Adds low words, selects its signed-negative-input or unsigned-overflow branch, adjusts high by−1/0/+1 and adds input high words. The low adjustment is32768, despite the32767 threshold. |
| Decimal formatter, script115 export0 | Constant32766 at `0x0058` | For nonzero high and nonnegative low, bounded digit arithmetic forms the decimal value32766×high+low. If high is zero **or low is negative**, the direct `%d` branch formats low alone. |

The pair-add negative-input branch additionally requires a negative summed low word and at least one nonzero input high word before borrowing. It cannot be replaced by unconditional unsigned carry propagation. The cash helper likewise does not loop to normalize an arbitrary mathematical integer; its input is one SCI word.

The original DOS opcode table maps the relevant add/subtract and comparisons to native16-bit handlers. Selected native paths confirm word addition/subtraction, signed less-than and unsigned greater-or-equal; the artifact records those handler offsets and hashes. This avoids deriving wrap or signedness merely from the published source's appearance. Division, every possible arithmetic input and a full x86/SCI execution equivalence proof are outside this selected check.

## MONEY-B02: finite boundary consequences

These fixtures were calculated from the selected package branches using explicit16-bit wrapping. They verify transcription and expose differences; they are not measured original outputs or proof that every supplied pair is reachable through ordinary play.

| Operation | Output pair | Predicted formatter numeric text |
| --- | --- | --- |
| Cash(0,32765), add1 | (0,32766) | 32766 |
| Cash(0,32766), add1 | **(1,0)** | **32766** |
| Cash(0,32766), add100 | (1,99) | 32865 |
| Cash(1,0), subtract1 | (0,32766) | 32766 |
| Cash(0,0), subtract1 | (0,−1) | −1 |
| Pair(0,32766)+(0,1) | **(1,−1)** | **−1 if passed to this formatter** |
| Pair(0,32766)+(0,2) | (1,0) | 32766 if formatted |
| Pair(1,0)+(0,−1) | (0,32767) | 32767 if formatted |
| Pair(0,0)+(0,−1) | (0,−1) | −1 if formatted |

The cash panel actually passes `cashHi` and `cash` to formatter115/0 at `1:0x2419`, so that join is identified for cash. The asset-pair rows describe the arithmetic and formatter separately; they do not assert that every asset display invokes that formatter with those exact pairs. Nor do they establish universal conservation of a single inferred monetary value across the different helpers.

For the bounded positive-high examples, the formatter's digit accumulation agrees with32766×high+low. High words large enough to overflow individual digit products, negative high words and noncanonical restored states are outside that description.

## MONEY-B03: affordability and Wealth are different consumers

Main export11 returns32767 whenever `cashHi` is nonzero; otherwise it returns zero for a negative low cash word or the low cash word itself (`0x0545–0x0581`). This is a spending/comparison proxy, not the formatted number and not an unrestricted combined balance. For cash(1,0), the proxy is32767 while the formatter's numeric result is32766.

Main export10 separately sets stored Wealth from cached liquid assets. Any nonzero cached asset high word selects100, without a sign test; otherwise the helper divides the signed low field by100 and clamps0…100. Asset recalculation and its timing remain governed by [the score contract](score-refresh.md) and [bank continuation](bank-refresh-continuation.md). Identifying the numeric helpers does not make Wealth continuously fresh.

Investment valuation repeatedly uses pair addition through script115 export1; `Player.calcLiquidAssets` then combines investment totals, cash/savings and debt. Thus replacing all pairs with one modern integer can affect more than display rounding. This pass does not settle the full valuation overflow graph, large durable-price multiplication, every debt combination or all broker subtotal mutations.

## Reproduction and planning boundary

Rebuild [local package listings](../discovery/decompile-original-scripts.md) and the [native image](../discovery/inspect-dos-interpreter.md). The artifact lists selected methods in scripts0,1,115, their552 checked instruction spans and four native arithmetic-handler ranges plus their shared comparison true-result tail. Inspect the stated constants/branches; the original helper transcription used for the nine local calculations stays ignored under `work/money-boundaries/`.

The analytical fixture data is committed; original resource bytes, decompiled/transcribed helper code and native assembly are not. These examples do not establish runtime display timing or a general high-balance compatibility implementation. A new integer-money contract, chosen overflow limits and deliberate correction of these discrepancies would be explicit adaptation decisions. No such choice or application work is approved here.
