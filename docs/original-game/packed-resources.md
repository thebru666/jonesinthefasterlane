# Original artwork and other packed resources

Research date: 2026-10-15. Evidence: **PACKAGE** from the previously downloaded website bundle. This is a directory-level inspection, not an artwork export.

## Are the original artifacts in the download?

Yes. The js-dos ZIP contains `resource.map`, `resource.001`, and `resource.002`. The map identifies the original graphics, text, sound, font, and other game resources inside those volumes. They are packed Sierra resources rather than a folder of PNGs or finished screen captures.

| Resource class | Map entries | Distinct resource IDs | Reference use |
| --- | ---: | ---: | --- |
| Views | 92 | 90 | Sprite/interface graphics and possible animation loops/cels |
| Pictures | 7 | 7 | Picture/background resources |
| Sound | 35 | 34 | Encoded sound/music resources; count is not a count of recordings |
| Text | 50 | 39 | Text-resource collections |
| Fonts | 9 | 8 | Font resources |
| Cursors | 3 | 2 | Cursor resources |
| Palette | 1 | 1 | Palette resource |
| Scripts | 85 | 69 | Compiled game/interpreter-support logic resources |
| Vocabulary | 14 | 13 | Vocabulary/lookup resources |
| Patches | 3 | 3 | Encoded patch resources, not a claim about bug-fix files |
| **Total** | **299** | **266** | **Resource IDs, not individual images, frames, or screens** |

Thirty-three IDs recur in the directory sections for the two resource volumes. They are not additional unique assets. Their payload equality has not been checked; the inventory retains every entry and its volume/offset rather than silently discarding one.

A view may contain multiple animation frames. A complete screen can combine a picture, several views, text, controls, and palette data. Counting seven pictures therefore does not mean the game has only seven screens.

## Verification performed

Parsed all six-byte map entries using the SCI0/early-SCI resource directory layout, then checked that each referenced volume offset is inside its file and that the resource header's ID matches the map entry. **All 299 passed.** The map's final terminator also matches that format.

The format and type mapping were checked against pinned ScummVM [resource-map reading](https://github.com/scummvm/scummvm/blob/2b5f9b5d95f267c87889746906148db6088130f8/engines/sci/resource/resource.cpp#L1853) and [resource type mapping](https://github.com/scummvm/scummvm/blob/2b5f9b5d95f267c87889746906148db6088130f8/engines/sci/resource/resource.cpp#L154). See the [full inventory](../../artifacts/original-game/packed-resource-inventory.json) for archive/map hashes, every resource ID/offset, and format-source hashes.

No payload was decompressed, rendered, or listened to in this initial header inspection. A subsequent [local decoding pass](asset-catalogue-notes.md#completed-local-decoding-pass) now exports graphics, text and sound events; it does not establish runtime equivalence. The counts establish availability and address/header consistency; they do not prove every payload decodes correctly or identify every pictured character/item. They do not prove that published decompiled scripts match these bytes.

## Next visual discovery step

The [reproducible exporter](../discovery/rebuild-original-assets.md) now creates a searchable local index and contact sheets for all supported graphics. Continue visual role transcription for player appearances, clothing variants, furnishings and animation sequences; script-role hints are not a complete visual catalogue.

Keep decoded original art and audio in ignored research storage under the current repository policy. Commit original analytical descriptions, resource IDs, mappings, and any new project-owned diagrams. Exporting art for inspection and deciding what assets to use in a public release are separate decisions; no reuse decision has been made here.
