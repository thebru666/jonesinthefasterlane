# Website bytecode: receipt precedes purchase-bonus test

Verified 2026-10-16. Evidence: **BYTECODE**, from the locked website bundle, version 1.000.060. This selected-path verification confirms the suspicious ordering in GOODS-002 for the appliance-shop refrigerator. It does not establish whole-source equivalence or claim that every shop item has been independently checked.

The bundle SHA-256 is `c08f3310f4f9cf47316bc32745507ae065bba7741430f7c3620602f534c46180`. Script hashes and exact ranges are also recorded in [analytical verification metadata](../../artifacts/rules-audit/bytecode-purchase-verification.json). Local instruction listings and recovered game code remain ignored. Offsets below are zero-based positions in decompressed payloads, including SCI block headers, matching the [finance verification convention](bytecode-finance-findings.md).

## BC-GOODS-001: ordinary refrigerator purchase misses its nominal +1 bonus

The package's `refrigerator` object is at script 208 offset `0x072e`; its `doit` selector points to `0x06f5`. Inherited class properties identify its item index as 21, goods type as 0 (durable branch), and units as 1. Its superclass is class 55, `CostDItem` in script 104.

The decisive sequence is:

| Package location | Verified action |
| --- | --- |
| Script 208 `0x06f7–0x06fa` | Call superclass 55's `doit`, before the item-specific quantity check |
| Script 104 `0x03cf–0x03da` | Compare available cash against price, set success global 416 and branch on failure |
| Script 104 `0x0404–0x0421` | For durable goods type 0, call the player's `durables` list's `recieve` selector with the object's item index and units; save the returned object |
| Script 106 `0x00dd–0x0120` | `ListOfGoods.recieve` checks for an existing indexed object; if absent, creates and adds an object with the requested index and quantity |
| Script 106 `0x0121–0x0171` | Existing-object helper `hasType` searches by index and adds the requested units to its quantity before returning that object |
| Script 208 `0x06ff–0x0714` | After the superclass returns, require success global 416 and call `durables.objectAtIndexQuan(indexNum)` |
| Script 106 `0x0272–0x0288` | `objectAtIndexQuan` looks up the object, then reads its current `quantity`; this is neither a previous-quantity cache nor a removal operation |
| Script 208 `0x0716–0x071c` | Negate the quantity result; skip the happiness call when quantity is nonzero; otherwise call script 0 export 13 with +1 |

For a normal successful first purchase, the shared transaction creates quantity 1 **before** the item method tests quantity. With an already present nonnegative quantity, the receipt increments it by one, also leaving it nonzero. In either ordinary case the item's nominal +1 happiness branch is skipped. The package therefore contains the same ordering anomaly previously inferred from the published decompilation; it is not merely a decompiler's placement of the call in a misleading source block.

This conclusion concerns that item-specific purchase bonus. A refrigerator can still affect food storage, and other durable or start-turn happiness effects are separate rules. It does not infer a different total happiness outcome for every possible event state.

## Lookup and receipt proof details

`ListOfGoods.objectAtIndex`, script 106 `0x0240–0x0271`, iterates the list and compares `indexNum` with its argument. The quantity wrapper calls it at `0x027a`, branches on the returned object at `0x027e`, and sends selector 353 (`quantity`) at `0x0281–0x0285`. Thus the later item check reads the owned object's current quantity, not whether the UI control has previously been clicked.

For a new object, receipt sets `indexNum` and `quantity` at `0x0102–0x0117`, then adds the object to the list at `0x011c`. For an existing object, `hasType` reads current quantity at `0x0143–0x0152`, adds the receipt argument at `0x0154–0x0157`, then writes the sum at `0x0160` and returns the indexed object at `0x0167–0x0169`.

The player's ordinary durable-list class is `Durables`, class 66, subclass of `ListOfGoods` class 64. Its `newGoods` override at script 106 `0x0306–0x030d` creates a class-62 `Durable`. Selector identities come from package vocabulary 997, rather than from source variable names. The package spells the receipt selector `recieve`.

The superclass performs additional UI/sound/cash callbacks between receipt and return. The appliance's named `items.doit` callback, script 208 `0x0ef6–0x0f1d`, updates animation/cel/drawing; `boughtItem.doit`, `0x02cd–0x0306`, chooses and displays a purchase response. Neither of those methods writes inventory quantity. This pass does not claim a universal invariant under corrupted states, negative quantities, overflow or unusual re-entry through other callbacks. The directly proved order and ordinary positive-quantity result are sufficient to resolve the suspected source-ordering error without manual shopping sessions.

## Evidence and scope

| Resource | SHA-256 |
| --- | --- |
| Script 208 | `9c90ddd511adfc9ecaffd7c35e8f3c985ef44d24d800e7e655d9e9c98c45d1c9` |
| Script 104 | `ad9311f368bbb483876f0a9b1cc179d3ffc4238dcdd31b6e622d66b2ffde4c61` |
| Script 106 | `2f7161260d6f5ac46f0e0ae7c0c47cc7f1f59cd9135c829916ad97d9e89ca24d` |
| Vocabulary 997 | `1adc0a33a4c7e79022b0c936b0613dcc89deb2a9ffe84f3e4539afec86601850` |

An independent instruction-framing pass matched all 142 instructions in the refrigerator, receipt, existing-object increment and lookup ranges against the reproducible decoder. Superclass and happiness-helper boundaries were separately checked in the finance pass. No runtime outcome is claimed. Broad appliance/discount catalogue coverage still uses the [published-source references in GOODS-002](goods-and-finance.md#goods-002-durable-catalogue-and-purchase-happiness-trap); the bytecode proof here is explicitly scoped to the refrigerator path. Whether to retain or repair the missed bonus remains an adaptation decision.
