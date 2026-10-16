# Z-Mart's six-product assortment and return visits

Audited 2026-10-16 against website DOS **1.000.060**. Evidence **BYTECODE**, plus a selected **DOS-STATIC** indexed-store check. No runtime shopping, draw-frequency measurement or full interpreter equivalence is claimed. [Metadata](../../artifacts/rules-audit/discount-assortment-verification.json) pins catalogue fields, instruction/range hashes, the bounded history-access inventory and abstract replay examples. Original code, images and native disassembly remain ignored.

## Selection removes twelve products; buying does not

On a normal fresh location initialization, script211 constructs a list of22 controls: background, clerk, item-display icon and Exit, followed by18 product controls (`211:0x049f–0x04fb`). While size>10 (`0x0501–0x0506`), it deletes one control at a position in4…size−1. The four leading controls are protected, so twelve deletions leave exactly six products. An employee's Work control is inserted **after** this selection (`0x054a–0x0577`), and the time-clock control is added later. Employment therefore does not alter the selection bounds or product count on this path.

Successful purchases **do not delete or replace an offered product**. The only product-list deletion sends in the complete script211 literal-selector inventory are the two branches of this initialization loop (`0x051f`, `0x053c`). The other delete send belongs to the Work handler and removes Work itself after its employment result (`0x1427`). The shared cash/inventory transaction, DiscountDItem override, the eighteen product controls' override/inherited paths, purchase-feedback callback and display-icon callback contain no shelf-removal call. A successful purchase can consequently be repeated from the same offered control, subject to cash and its item rules. An unsuccessful purchase also leaves the assortment unchanged.

This is an assortment-selection mechanism, not a six-unit stock ledger or replenishment after each sale. The merchant's greeting about new weekly specials does not override the actual turn-scoped history described below.

## What the eighteen candidates identify

These are literal script211 control fields; bases precede the ordinary goods-price helper. `key` is a keyboard/event identifier, `indexNum` is an inventory identifier, and `celNum` is a display-image identifier. They are different namespaces. In particular the event keys are not a contiguous1…18 list.

| Initial list position | Control identifier / product | key | Inventory index | Goods type | Units | Base | celNum |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 4 | refrigerator | 1 | 21 | 0 | 1 | 650 | 0 |
| 5 | stove | 2 | 23 | 0 | 1 | 490 | 1 |
| 6 | stereo | 3 | 26 | 0 | 1 | 450 | 2 |
| 7 | colorTV | 4 | 24 | 0 | 1 | 349 | 3 |
| 8 | bwTV | 5 | 30 | 0 | 1 | 110 | 4 |
| 9 | microwave | 6 | 27 | 0 | 1 | 220 | 5 |
| 10 | vcr | 7 | 25 | 0 | 1 | 250 | 6 |
| 11 | casualClothes | 8 | 36 | 1 | 9 | 35 | 7 |
| 12 | leisureSuit / dress clothes | 20 | 35 | 1 | 9 | 90 | 8 |
| 13 | baseballTickets | 10 | 37 | 1 | 4 | 45 | 9 |
| 14 | theatreTickets | 11 | 38 | 1 | 4 | 30 | 10 |
| 15 | concertTickets | 12 | 39 | 1 | 4 | 40 | 11 |
| 16 | encyclopedia | 23 | 31 | 0 | 1 | 475 | 12 |
| 17 | dictionary | 14 | 32 | 0 | 1 | 70 | 13 |
| 18 | atlas | 24 | 33 | 0 | 1 | 55 | 14 |
| 19 | dogFood | 16 | 0 | 3 | 1 | 18 | 15 |
| 20 | eightTrack | 17 | 0 | 3 | 1 | 75 | 16 |
| 21 | trumanCapote | 18 | 0 | 3 | 1 | 100 | 17 |

Type0 receives durable inventory, type1 consumables, and type3 has no inventory-receive branch in the shared CostDItem transaction. The three joke products' zero inventory indices therefore do not denote three durable products of the same type. All18 controls have fixedPrice0 and visitTime0. Initialization sends `init(1)` to the selected controls (`0x0614`), so the inherited cost-control initializer selects goods reading global309 and the script109 price helper. None of this proves that every item-specific happiness branch succeeds; the known superclass-first quantity trap remains separate.

On successful receipt, `DiscountDItem.doit` calls the shared transaction first (`0x02f7`), then, only if both returned inventory object global418 and success global416 are nonzero, sets its discount attribute bit0x100 (`0x031e`). Failed payment skips that flag write. Type3 successes do not produce an inventory object through that receive switch. The shared path calls the item's display/feedback callbacks; these affect inventory metadata, presentation or item-specific scores, not the six-product selection.

## Saved deletion positions reproduce the same assortment

For deletion number i, initialization first reads global[385+i] (`211:0x050b`). If nonzero it deletes the control currently at that saved position (`0x0519–0x051f`) without calling Random. If zero it draws `Random(4,size−1)` at `0x0533`, deletes that position and stores the position in global[385+i] at `0x0542`.

The stored values are **positions in the successively shrinking list**, not inventory IDs, cel numbers or original positions. Rebuilding the same ordered22-control list and replaying those twelve positions reproduces the same six survivors in their original relative order. Repeated equal stored numbers are valid: position4 can refer to a different product after each deletion. Every generated position is at least4, so zero works as an unused-history sentinel.

The twelve first-visit draw intervals, in order, are4…21,4…20,…,4…10. There is no rejection loop for duplicate products: deletion itself removes a candidate from later draws. These bounds do not establish equal probabilities or the native generator's reachability of every abstract sequence. The [native randomness audit](dos-randomness.md) establishes scaling and seed behavior separately.

Normal shop exit calls `DisposeScript(211)` at `0x076b`. That disposes the local control/display state, while the global deletion history persists. A normal same-player return constructs the full list again and replays the nonzero history, so it uses **zero selection-Random calls** for those twelve slots. Other greeting, clerk-animation or feedback draws can still occur. Exceptional re-entry with global518 nonzero skips normal construction/selection and resumes the existing dialog; this is not a reroll path.

The separate six-word local0…5 array is filled from the surviving controls' celNum fields (`0x0579–0x05d9`). The FS display cycle reads this array to rotate product images; `items.doit` temporarily shows the selected cel and delays cycling. Neither edits the assortment list or global deletion history. The local array is display state, not an additional randomized stock list.

## Active-turn reset and Jones

Shared start-turn processing clears global385…399, fifteen words, with a loop over i=0…14 (`111:0x031c–0x0330`). Only twelve entries are needed by the ordinary selection loop. This reset is inside the active/non-finished turn path after the completion gates; it is not conditional on the weekly economy index changing. Both humans and Jones reach this shared reset for an ordinary active turn. Thus another participant's next turn starts with fresh selection history, and a participant's later turn does not retain their previous assortment. There is no per-player saved history array in this inspected mechanism.

The all69-script bounded inventory finds the direct indexed global385 history accesses only in startTrn and discount.init. This covers immediate global bases385…399 and their indexed forms; it does not exclude computed addresses, restored memory, native save effects or other editions.

Jones's controller is installed when playing==29 (`211:0x047c–0x049d`) **before** the same list construction and selection used by humans. It does not install a separate catalogue or choose a different six here. Its book/clothes branches test whether the desired control is still in the selected list before sending its key. The optional ticket branch draws0…1 at `0x1827`, then, after its conditions succeed, increments local6 and chooses a key10…12 at `0x1851`. It does not test ticket membership before that key draw; an unavailable ticket key does not replenish or modify stock. Local6 counts these attempts and is reset at normal shop initialization (`0x0428`), rather than being the global assortment history. This is selected controller behavior, not an exhaustive AI-policy parity claim.

## Indexed-store interpretation matters

An earlier conservative-pseudocode export misidentified the values stored at211:0x0542 and111:0x032b as their loop indices; the decoder has since been corrected. Raw instructions push the intended value, load the index into the accumulator, then execute `sagi385`. The selected original DOS handler for encoded opcode0xb0 resolves through the dispatch table to0048:0ed3, load-image offset0x1353. It forms the target from the immediate base plus the accumulator index, **then pops the stored value from the VM stack** (`0x1353–0x136b`). The first call therefore stores the drawn deletion position; the second stores the pushed zero. The pinned reference VM's `op_sagi` agrees. See [native input/address convention](../discovery/inspect-dos-interpreter.md).

This native check resolves the particular indexed-store ambiguity. It does not upgrade conservative pseudocode to authoritative source or prove every indexed opcode implementation.

## Draw order and remaining limits

A fresh zero-history assortment consumes its twelve selection draws before control initialization/opening and the optional greeting draw0…10 (`211:0x069b`). Successful purchase feedback, when the shared message flag permits it, draws11…26 at `0x018d` and rejects an immediate repeat of local7; local7's resource default is−1. That feedback is separate from selecting or consuming shelf stock. Failed purchases do not run the successful feedback callback, although the failure notice and other presentation may still consume events or unrelated animation draws.

The metadata verifies two boundary-position streams and a mixed stream, then replays each history against a freshly constructed abstract list and checks identical six survivors with no further draws. These are analytical rank-deletion fixtures, not samples of actual DOS randomness. Visible layout, restored/corrupt history, interrupted initialization, full random call order and full native resource lifetime remain bounded questions. Neither stock depletion nor a uniform assortment distribution should be invented to fill those gaps. No 2.0 mechanic change is approved here.

Sources: [website package](https://jonesinthefastlane.com/bundle.jsdos), [pinned published comparison](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/discount.sc), [reference VM indexed stores](https://github.com/scummvm/scummvm/blob/2b5f9b5d95f267c87889746906148db6088130f8/engines/sci/engine/vm.cpp#L1277), and [source register](../discovery/source-register.md). Package instructions and the selected native store trace settle the analysis; original payloads are not committed.
