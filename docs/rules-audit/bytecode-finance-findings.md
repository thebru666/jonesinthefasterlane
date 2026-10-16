# Website bytecode: wages, garnishment and loans

Verified 2026-10-16. Evidence: **BYTECODE**, recovered directly from the website bundle's decompressed SCI resources. This pass verifies selected branches against the actual shipped bytes; it is not a claim that the complete published decompilation matches the package. No gameplay experiment was needed for these arithmetic/control-flow findings.

The package is the locked [website bundle](../../artifacts/discovery/2026-10-15-bundle-inventory.json), version 1.000.060, ZIP SHA-256 `c08f3310f4f9cf47316bc32745507ae065bba7741430f7c3620602f534c46180`. Original bytes and instruction listings remain under ignored local research folders. Committed [verification metadata](../../artifacts/rules-audit/bytecode-finance-verification.json) records hashes and offsets without reproducing game source.

All hexadecimal offsets below are **zero-based offsets in the decompressed resource payload**, including its SCI block headers. They are not packed-volume positions or source line numbers. Method names are resolved from the package's object name strings and selector vocabulary 997. Global slot 302 is the player receiver used throughout these methods; the label “active player” agrees with the previously examined source, while the slot number and selector messages are independently visible in the package.

## Verified resource and method identity

| Resource | SHA-256 | Relevant identity |
| --- | --- | --- |
| Script 108 | `7527d079401415ea319551176c486ebc439d4e73ec1d595bcffe8d0e7d2aedf9` | Export 0 points to `0x000c`; local work helper begins `0x014c` |
| Script 204 | `237ee1a4e51975b590bf3a02b40a8188dffec26128177b5c3f1341e63eb83408` | `loanPayment` object at `0x0956`, `doit` at `0x0833`; `applyForLoan` object at `0x0c3c`, `doit` at `0x09ba` |
| Script 104 | `ad9311f368bbb483876f0a9b1cc179d3ffc4238dcdd31b6e622d66b2ffde4c61` | Class 55, `CostDItem`, superclass 54; `doit` at `0x03ad` |
| Script 0 | `4a6d8406028aec4efe90d0331904fc4653c0330c1f9e527a7f94bfdaf32af8b0` | Export 10 at `0x0466` changes cash; export 13 at `0x05ea` changes happiness |
| Vocabulary 997 | `1adc0a33a4c7e79022b0c936b0613dcc89deb2a9ffe84f3e4539afec86601850` | Package selector names, including `wage`, `rentOwed`, `loanBal`, `paySched`, `madePayment`, `cash` and `hapStat` |

`loanPayment` inherits class 55. Its property layout resolves byte offset `0x40` to selector 342 (`price`); the object stores initial price 50 and fixed-price flag 1. Thus a property load at `0x40` in the payment method is a price read, rather than an unexplained constant field. Selector 60 is `doit`; selector 102 is `init`.

The independently read instruction boundaries and operand bytes were then compared with the reproducible local decoder: all 1,147 actual instructions across the six inspected ranges agreed (one trailing code-block padding byte was excluded). This cross-check supports decoding consistency; it is not execution of the game.

The instruction interpretation follows pinned ScummVM [SCI VM](https://github.com/scummvm/scummvm/blob/2b5f9b5d95f267c87889746906148db6088130f8/engines/sci/engine/vm.cpp), [object/script format](https://github.com/scummvm/scummvm/blob/2b5f9b5d95f267c87889746906148db6088130f8/engines/sci/engine/script.cpp), and [selector loading](https://github.com/scummvm/scummvm/blob/2b5f9b5d95f267c87889746906148db6088130f8/engines/sci/engine/kernel.cpp). For these SCI16 instructions, the opcode low bit determines variable operand width; conditional branch displacements are signed and relative to the instruction end. Arithmetic consumes stack-left and accumulator-right operands. The examples below use small ordinary values, avoiding separate signed-overflow questions.

## BC-FIN-001: garnishment really overwrites partial-shift pay

**Confirmed in the website package**, strengthening [TIME-006](time-and-actions.md#time-006-rent-garnishment-appears-to-overwrite-partial-shift-pay) and HOME-003 beyond their previous published-source evidence.

| Bytecode range, script 108 | Recovered calculation/control flow |
| --- | --- |
| `0x020f–0x021e` | Read `wage` (selector 424), multiply by 8, store the same result into temporary 0 and temporary 1 |
| `0x0220–0x023c` | If elapsed-hours global 323 plus 6 exceeds 60, replace temporary 1 with `trunc(temporary1 × (60−elapsedHours) / 6)` |
| `0x023e–0x0247` | Read `rentOwed` (429); zero debt jumps to `0x0329` |
| `0x024a–0x025a` | Compare `trunc(temporary0 / 2) > rentOwed`; false jumps to `0x0278` |
| `0x025d–0x0273` | True branch overwrites temporary 1 with `temporary0−rentOwed`, then writes rent owed to zero |
| `0x0278–0x029b` | False branch overwrites temporary 1 with `trunc(temporary0/2)−2`, then writes `rentOwed−trunc(temporary0/2)` |
| `0x031e–0x0327` | Set `rentExt` (431) to −1 |
| `0x0329–0x032c` | Pass temporary 1 to script 0, export 10, the actual cash-change helper |

Temporary 0 retains full-shift gross pay throughout. The debt branches **do not** read the prorated temporary 1 to calculate the amount awarded. The strict comparison and its jump establish that equality takes the second branch, including the extra two-dollar reduction.

For wage 10 and one hour remaining, ordinary partial pay is 13. With rent debt 10, the actual calculation instead awards 70 and clears debt. Debt 40 awards 38 and clears debt; debt 100 awards 38 and leaves debt 60. These are direct arithmetic examples, not observed gameplay captures. The helper subsequently requests six hours from the timekeeper; presentation and timekeeper clamping are separate from the demonstrated pay overwrite.

## BC-FIN-002: initial rejection has two happiness reductions

**Confirmed in the website package**, strengthening FIN-002. In script 204, failed qualification branches from `0x0a47` to `0x0b92`. There is one unconditional happiness-helper call at `0x0b9f`, with one argument −1. Then the method reads `loanBal` (selector 433) and the branch at `0x0bab` jumps to `0x0bd4` when debt is zero.

The nonzero-debt path displays the extension refusal and jumps at `0x0bd1` to the common exit `0x0c2d`, bypassing the second call. The zero-debt path passes −1 again at `0x0bd4–0x0bd7`, then displays the initial-loan refusal. This is two distinct reachable calls, not a decompiler formatting duplication.

Script 0 export 13 is separately verified: `0x05ec–0x05fc` chooses global 302 when fewer than two arguments are supplied; `0x05fe–0x0608` reads `hapStat` (378) and adds the first argument; `0x060a–0x061f` clamps to 0…100; `0x0621–0x0629` writes the result. Consequently an unsuccessful initial application reduces happiness by two **subject to the floor after each call**, while an unsuccessful extension reduces it by one. At happiness 1, the first call reaches zero and the second remains zero. At happiness 0, neither produces a negative value.

The qualification formula itself also matches the package: `0x09f8–0x0a11` calculates `wage + trunc(lqAss/1000)` into temporary 2; `0x0a14–0x0a44` calculates `5 + latePayments + trunc(loanBal/100) + (loanBal != 0 ? 1 : 0)` into temporary 1. The strict greater-than at `0x0a46` governs approval. `0x0a4a–0x0a53` computes the offered additional amount as 100 times the difference. Only the low `lqAss` selector (377) appears in this calculation; no high-word load or recalculation call occurs between the time charge and comparison.

## BC-FIN-003: a full $50 payment removes $45 principal

**Confirmed in the website package**, strengthening the payment arithmetic in FIN-003.

The payment method calls superclass 55's `doit` at `0x0838`, then requires nonzero `loanBal` at `0x083d–0x0846` and success global 416 at `0x0849–0x084c`. At `0x084f–0x0869` it increments `paySched` (435) and writes `madePayment` (436) to 1.

The subtraction at `0x0874–0x0896` reads `loanBal`, compares the price property with 50, uses price when strictly below 50, and otherwise loads 45 at `0x088f`. The selected amount is subtracted and written to `loanBal`. The remaining-balance check at `0x0898–0x08bd` updates the displayed price when debt falls below 50. The zero-balance branch at `0x08bf–0x08e7` resets `paySched` and the payment price to zero.

The actual cash charge comes from script 104's shared superclass method: `0x03cf–0x03d7` compares available cash from script 0 export 11 against price and stores success in global 416; `0x049e–0x04a5` passes `theSign × price` to script 0 export 10. The loan-payment object's sign is −1. Script 0 export 10 reads cash, adds its argument and writes cash (with its separate high-word carry/borrow handling), so this is an actual cash debit rather than just a display cost.

For an ordinary $100 debt with enough cash throughout, successive principal balances are 55, 10 and 0; charged prices are 50, 50 and 10. Total repayment is therefore 110. This derives from the shipped transaction method, not an assumed interest rate.

## Comparison and remaining boundaries

After identifying these package instructions and object/selector mappings, their formulas and branch order agree with the corresponding published-source findings: [n108](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/n108.sc#L127), [bank application](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/bank.sc#L445), and [payment](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/bank.sc#L364). This is selected-path semantic agreement, not a byte-for-byte source comparison or a full-game audit.

The three quirks no longer need ordinary manual play merely to determine whether their branches exist. Runtime remains useful only if exact visible feedback, unusual callback/re-entry effects or interpreter differences become material. Monthly loan scheduling, every high-value arithmetic edge and every default/event consequence remain outside this bytecode pass. Preservation versus correction of these behaviours remains an explicit adaptation decision.
