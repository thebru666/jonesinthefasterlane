# Original DOS stereo loop fallback

Investigated 2026-10-16 in website DOS **1.000.060**. Evidence: **BYTECODE + DOS-STATIC**, selected native paths and actual resource values; no new gameplay observation. This resolves the selected fallback left open in [PRESENT-B01](bytecode-economy-presentation.md#present-b01-the-stereos-invalid-loop-is-genuine). [Verification metadata](../../artifacts/rules-audit/dos-stereo-fallback-verification.json) records input/range hashes, relocation-backed kernel pointers and package anchors. [Rebuild the original interpreter](../discovery/inspect-dos-interpreter.md) to inspect these paths locally.

## Result

The security-apartment stereo really stores **view702, loop1, cel4**. That view contains only loop0, with five cels. The original DOS cell lookup clamps the requested loop to the last available loop, then clamps the cel to the last available cel if needed. For this positive-index request, both dimensions and drawing resolve to **loop0, cel4**. The object itself continues to store loop1; this is a lookup fallback, not a property correction.

This agrees with the pinned reference renderer for this request. It does not establish identical fallback for every invalid index: the native comparisons are unsigned, whereas the reference clamp treats its indices as signed. Negative indices, empty views and every rendering state are outside this result.

## Package path into native drawing

In script202, `security.init` checks residence and durable quantity26, then adds the stereo at `0x0121`. Its initialization packet runs item initialization, `setSize` and dialog opening at `0x015d–0x017c`. The actual stereo fields are at `0x0472/0x0474/0x0476`.

The stereo is a DIcon, class12, inheriting control class10. Script255 `DIcon.setSize` calls native CelWide at `0x05cc` and CelHigh at `0x05dc`, passing its stored view, loop and cel. Its inherited draw method calls DrawControl at `0x03c4`. These paths matter because proving a generic DrawCel fallback alone would not establish how this dialog icon is drawn.

## Native path

All offsets below are in the unpacked **load image**, excluding the MZ header. Kernel pointers are derived from the actual table at relative DS1856:07d0 and checked against MZ relocations.

| Path | Finding |
| --- | --- |
| CelWide15 at `0x06b03`; CelHigh16 at `0x06b2c` | Both call the corresponding dimension wrapper, which calls the shared cell lookup |
| DrawControl23 at `0x06e33` → dispatcher `0x05321` | Reads control type; the type4 jump-table entry resolves to `0x05520` |
| Icon branch `0x05520–0x0558d` | Reads selectors5/6/7 (view/loop/cel), loads the view and calls draw wrapper `0x1711c` |
| Draw wrapper `0x1711c`; width `0x17170`; height `0x17198` | All call shared lookup at `0x16f4c` before using the cell header |
| Shared lookup `0x16f4c–0x16fb6` | Reads low-byte loop count, compares requested loop unsigned and selects count−1 if out of range; after locating that loop, does the corresponding unsigned cel-count comparison |

The selected view's loop0 has no mirrored-loop complication. With loop count1, request1 becomes0; with cel count5, request4 remains4. The native trace establishes resource selection, not a full screenshot: palette state, final position, ownership visibility, window compositing and animation remain separate evidence.

## Consequence for the reference studies

The security-room composition can now use loop0/cel4 as a **statically justified original DOS fallback**, while retaining loop1 in any literal object-property transcription. A study using that cel is still an analytical composite, not an observed screen. This finding approves no new-game art, implementation or bug fix, and original pixels/native code remain ignored locally.
