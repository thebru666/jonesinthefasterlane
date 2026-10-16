# Inventory receipt, grouping and packing

Audited2026-10-16 against the website bundle's DOS1.000.060 package. **BYTECODE** applies to the selected script paths below, with a selected **DOS-STATIC** confirmation of normal object cloning. No original-game runtime result is claimed. The [verification artifact](../../artifacts/rules-audit/inventory-grouping-verification.json) records six resource hashes, selected range hashes and712 instruction/payload comparisons. Original objects, scripts and listings remain ignored.

This extends [the refrigerator receipt trace](bytecode-purchase-findings.md) and [NE-B05's packing finding](bytecode-needs-events.md#ne-b05-packing-does-not-discard-empty-inventory-records). It audits shared inventory semantics, not the full pawn transfer, broker, or every caller's transaction flow. The published [Goods.sc](https://github.com/sluicebox/sci-scripts/blob/870a8015b689474484bf3d8b41416956d4315432/jones-dos-1.000.060/src/Goods.sc) was a comparison aid; actual payload instructions are authoritative here.

## INV-001: receipt groups by index and mutates before returning

Actual script106 spells the selector **`recieve`**, rather than `receive`. Its method at`0x00dd–0x0120` accepts an item index and optional quantity; omitted quantity defaults to1. It first calls `hasType(index,units)` at`0x00f7`.

Despite its predicate-like name, `hasType` at`0x0121–0x0171` **mutates** the first record whose `indexNum` matches: it reads that record's quantity, adds the supplied units, writes the sum at`0x0160`, and returns the same object. It does not filter by positive quantity, purchase price, attributes, discount quality, pawn state or object class. It stops at the first index match. Therefore receipt into an existing quantity0 record reuses that record and its metadata. A direct caller must not treat `hasType(index,delta)` as a read-only existence check.

If no record matches, `recieve` calls the list's `newGoods` factory, sets the requested `indexNum` and quantity, appends the object and returns it. Actual overrides create Consumable, Durable or Educational clones at`0x02ce`, `0x0306` and`0x033e`. Shared defaults include quantity1, pricePaid0 and index0; the relevant default attributes are Consumable129/`0x0081`, Durable69/`0x0045`, Educational1/`0x0001`. The requested quantity replaces the factory default on this new-record path.

The receipt helper itself does not write `pricePaid`, clear pawn flags or normalize quality. Grouping is an index-match rule, not a per-purchase history. It also does not prove that arbitrary direct list additions or restored/corrupted states can never contain duplicate indices. If duplicates already exist, this method increments only the first match; `pack` does not merge them later.

## INV-002: price and quality belong to the grouped record

The successful shared purchase control in script104 obtains the returned receipt object, writes its index, then tests `attributes&0x0038` at`0x0489–0x0490`. When that mask is zero, it writes the control's current `price` into the record's `pricePaid` at`0x049c`. When any of those bits is set, it leaves the stored price unchanged. This is caller behaviour after receipt, not a special price calculation inside script106.

Consequently an ordinary later purchase of the same index increases the existing quantity and normally **replaces its one stored price**. There is no weighted average, accumulated purchase total, or separate price per unit in this path. If a control receives several units for one transaction price, this write still records the control's `price`; the shared helper does not divide it by units.

Script211's `DiscountDItem.doit` calls the shared purchase first, requires a receipt object and success, then ORs`0x0100` into that object's attributes at`0x031e`. Because the object may already represent several units, the flag applies to the group. A later ordinary receipt into that record does not clear it. Existing pawn/redemption bits likewise survive the shared receipt, and can suppress the normal price replacement even though quantity increases.

These instructions support group-level effects of repeat purchases. They do not independently establish every used-stock transaction's ownership changes; that script212 work is separate from this audit.

## INV-003: packing replaces selected objects, including empty ones

`ListOfGoods.pack`, actual script106 `0x0172–0x023f`, uses bit`0x0001` as its selection condition. Its normal sequence is:

1. Obtain script1's temporary list. In original list order, clone each record with attribute bit1 set, clear that bit on the clone, and append the clone to the temporary list.
2. Walk the original inventory backward; remove and dispose each bit1 original.
3. Append the replacements to the inventory in temporary-list order, then release the temporary list's links.

Actual script999 `Obj.new` calls kernel4/Clone; the bundled native Clone path copies the normal valid object's property words before changing interpreter object metadata. Thus quantity, stored price and item flags are carried into the replacement; script106 then clears **only item attribute bit1**. This item flag is distinct from the interpreter's own object metadata flags. Actual `Collect.add` appends, while `Collect.release` deletes the temporary collection's membership links without disposing its remaining item objects. Releasing that temporary list therefore does not delete the replacements just added to the inventory.

There is **no quantity read or quantity0 rejection anywhere in `pack`**. A bit1 quantity0 record is replaced by a clone whose quantity remains0. A record without bit1 remains untouched even if its quantity is0. Packing is neither garbage collection for empty goods nor coalescing by index. The method can change object identity, and selected replacements move behind unselected records; a system using only a sorted content catalogue would not reproduce that list operation.

The selected location-return path calls `pack` on consumables, durables and education at`1:0x061d–0x0648`. That call does not establish that every possible removal elsewhere in the game is absent.

## INV-004: object lookup differs from usable quantity

Actual script106 `objectAtIndex`, `0x0240–0x0271`, returns the first index-matching object without testing quantity or attributes; it returns0 if absent. `objectAtIndexQuan`, `0x0272–0x0288`, calls that lookup and returns the object's current quantity, or0 when there is no object.

| Inventory state | `objectAtIndex(index)` | `objectAtIndexQuan(index)` |
| --- | --- | --- |
| No matching record |0 |0 |
| Matching record, quantity0 | Object reference |0 |
| Matching record, positive quantity | Object reference | That quantity |

An object-presence test can therefore succeed while a quantity test fails. The quantity wrapper is not a pre-purchase cache, previous-ownership test or removal operation. This is why the superclass-first refrigerator check sees the quantity after receipt, as already proved in BC-GOODS-001.

## Consequences for pawn stock and repairs

The shared list contract permits an empty durable record to retain price, pawn/redemption/forfeiture flags and identity after packing. Thus a pawn or used-stock path may inspect a persistent indexed record while the owner has zero carried units. Neither an empty visible inventory nor `objectAtIndexQuan==0` proves the record or its flags were removed. The [finance lifecycle audit](finance-lifecycle.md#fl-004-pawn-redemption-expires-after-three-end-turn-aging-steps) supplies the separate pawn/expiry trace; this note does not re-audit script212's transfer or sale handling.

Actual script111's selected repair loop iterates durable **records** at`0x0ba8–0x0d07`. It requires cash>500, excludes book indices31/32/33 and requires attribute`0x0040`. It then permits a candidate when `(attributes&0x0038)==0` **or** quantity>1. There is no separate blanket quantity>0 condition. A retained quantity0 record with repair eligibility and no protected bits would therefore pass these selected inventory predicates, if such a state reaches this pass; this conditional consequence is not a demonstration that normal play produces it.

The repair draw uses the group's discount flag to choose inclusive Random(0,35) or Random(0,50), giving nominal probabilities1/36 or1/51 for that tested candidate. Its bill bounds use the same grouped `pricePaid`: trunc(pricePaid/20)…trunc(pricePaid/4). Quantity is not a multiplier for independent per-unit repair trials in this loop. Repeat purchases that replace stored price or set discount quality can consequently affect the group's later repair treatment. Native RNG arithmetic and notice/resume behaviour are separate evidence, not new claims made by this inventory trace.

For2.0 planning, replacing records with individual durable instances, averaging purchase prices, automatically deleting empty records, or separating quality per unit would change this contract. None of those departures is approved by this research.
