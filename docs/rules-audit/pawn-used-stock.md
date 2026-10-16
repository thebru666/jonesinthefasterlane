# Package verification: pawn capacity and used stock

Verified 2026-10-16. Evidence: **BYTECODE**, selected control flow in the website DOS1.000.060 package; no gameplay execution or UI reproduction. This extends [GOODS-006](goods-and-finance.md#goods-006-pawn-redemption-expiry-and-used-purchases) and the [pawn/redemption lifecycle](finance-lifecycle.md#fl-004-pawn-redemption-expires-after-three-end-turn-aging-steps). Original/adaptation choices remain undecided.

[Metadata](../../artifacts/rules-audit/pawn-used-stock-verification.json) records hashes and offsets for script212 (`pawnShop`) and script106 (goods-list methods), checked against the original decompressed payloads. Bundle version1.000.060, SHA-256 `c08f3310f4f9cf47316bc32745507ae065bba7741430f7c3620602f534c46180`; see the [retrieval record](../../artifacts/discovery/2026-10-15-bundle-inventory.json). Offsets below are hexadecimal, zero-based decompressed script payload positions including block headers. Original resource bytes, disassembly and published comparison source remain ignored locally.

## PAWN-B01: six slots count grouped records across every player

Script212's capacity helper (`0x042e–0x04b9`) iterates the players list from script1 export2, then each player's durables. It increments its count once per record with `attributes & 0x38 != 0`, regardless of that record's quantity. Both active pawn countdown bits`0x18` and forfeiture bit`0x20` count. Six flagged groups across all players fill the shop; this is not six per player or six physical copies of goods.

The actual pawn action calls this helper and refuses a result `>=6` before selecting/accepting an item (`0x11fd–0x1237`). Redeeming or buying clears the selected source's pawn/forfeiture bits and thereby releases that group's slot, even when the source retains other owned copies.

## PAWN-B02: menu eligibility and actual acceptance differ

The pawn-menu builder (`0x02c8–0x037a`) lists a durable if either its `0x38` bits are clear **or** its quantity is greater than1. The selected-item resolver (`0x037b–0x042d`) uses the same filter to map the cursor back to an object, but returns refusal sentinel−1 if that selected record has any`0x38` bits. Thus a flagged group with extra owned copies can be visible while still being refused; it cannot create another pawn slot for the same record.

Neither clear-flag branch requires positive quantity. Under the selected arithmetic, a retained unflagged quantity0 record could be selected and the accepted pawn's decrement would produce−1. The [inventory retention audit](bytecode-needs-events.md#ne-b05-packing-does-not-discard-empty-inventory-records) establishes that zero records are not generically discarded, but a complete player-facing reproduction of this negative-quantity case has not been run. Treat it as a specific static edge, not an observed exploit.

## PAWN-B03: merely opening Buy marks stock as discount quality

Buy is enabled by a scan for any forfeiture bit`0x20` across all players (`0x0216–0x0285`). Its entry sets mode`local0=3` (`0x1044–0x10b9`); redemption mode is2. The used-list builder (`0x088e–0x0ac1`) scans all players' durable records for bit`0x20`, including the current buyer's own forfeited groups. It creates one control per matching record, with fixed price equal to that source's stored `redemptionPrice`, not a fresh economy-scaled shop price. Quantity does not gate this list.

After initializing/drawing each control, the builder immediately writes `source.attributes |= 0x100` at`0x0a8c`. **This happens while constructing the list, before a purchase or cash check.** The source record may also represent copies its original owner still holds. Those copies therefore acquire the same discount-quality flag when someone browses used stock. The selected list-cleanup method (`0x0ac2` onward) removes/disposes controls and contains no reversal of that durable flag. Leaving Buy without buying does not undo this write in those handlers.

## PAWN-B04: purchase clears source flags before resolving ownership

`aRedeemableItem.doit` (`0x1687–0x1885`) checks carried cash against the fixed control price. Success debits that price, invokes asset/display callbacks, then clears bits`0x38` on the source record with mask`0xffc7` at`0x1727`. The discount bit`0x100` and unrelated fields survive. Failure skips this clearing/transfer, although the earlier browsing-time discount write has already happened.

For mode3, the method scans players until it finds the list containing that exact source record (`0x17bb–0x17e6`). If source quantity is zero, it deletes the record from that owner's list (`0x17ed–0x180d`). It then calls the buyer's `hasType(source.indexNum, 1)` at`0x1826`.

Despite its name, `hasType` **mutates** a matching group: script106 `0x0121–0x0171` finds the first record with that index, adds its second argument to quantity, and returns it. It does not filter pawn flags or replace price/quality fields. A nonzero return ends the transfer path. Consequently an existing buyer group gains one copy and retains its own `pricePaid`, discount/pawn attributes and redemption data. The used source's discount flag is not copied into an already existing buyer group. An existing buyer group carrying pawn/forfeiture bits is still a match; those buyer flags remain if it is a different record from the purchased source.

If no buyer group matches, the method either sets an empty source to quantity1 and adds that same object to the buyer (`0x183b–0x1854`), or clones a nonzero source, sets the clone quantity1 and adds it (`0x1857–0x1876`). The clone/moved record retains the source's historical fields; the purchase handler has no `pricePaid` setter to replace historical purchase cost with today's used price. A source with remaining owned quantity is not decremented by this transfer: its already-pawned copy had been removed when pawning, and those residual copies remain the donor's property.

## PAWN-B05: grouped-copy consequences

These are analytical consequences of the traced branches, assuming ordinary unique ownership of each record and positive retained quantities:

| Starting source and buyer | Result after successful used purchase |
| --- | --- |
| Another player's source quantity0; buyer has no same type | Source removed from donor, becomes quantity1 in buyer's list |
| Another player's source quantity0; buyer already has type | Source removed from donor; buyer's existing quantity increases1 and keeps its own historical fields |
| Another player's source quantity2; buyer has no type | Donor keeps quantity2; buyer receives quantity1 clone with source historical fields |
| Another player's source quantity2; buyer already has type | Donor keeps quantity2; buyer's existing group increases1 without copying source historical fields |
| Buyer's own source quantity2 | Same record matches `hasType`, becoming quantity3; no clone |

In every listed case the source's`0x38` bits were cleared before ownership resolution, and its discount bit remains set. Thus a donor retaining two copies keeps both, but their shared record loses forfeiture/pawn flags and has discount quality. This is a grouped-object side effect, not individual per-copy condition tracking. No payment to the donor appears in the selected used-purchase handler; the buyer's money goes through the ordinary cash debit.

## Evidence limits and planning implications

The selected bytecode agrees with the corresponding local published-source control flow, but this is not full-game equivalence. Hash and byte-span checks establish correspondence to the package; they are not independent interpreter execution. Script callbacks run before the final ownership mutation, so exact UI/score refresh, callback re-entry, aliasing, corrupted/restored lists and negative/overflowing quantities remain separate boundaries. No gameplay exploit, frequency or visible message sequence is claimed.

A faithful rules contract must distinguish browsing-time quality writes, group-level capacity, cursor eligibility versus acceptance, and the mutating `hasType` lookup. Replacing these with per-item stock, a side-effect-free lookup or automatic used-price cost-basis updates would be explicit departures requiring a later decision. This audit approves none of them and adds no application code.
