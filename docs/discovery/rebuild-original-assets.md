# Rebuild the local original-asset catalogue

Recorded: 2026-10-15. Purpose: make the reference artwork and other resources inspectable on another machine, without committing original game assets or depending on this computer's paths.

The committed source inventory identifies the reference input. The rebuild tooling produces local research output under ignored `work/`. A resource directory listing, decompressed payload, rendered sprite, and screenshot of the running game are different kinds of evidence; their statuses must remain explicit.

## Reference input

| Field | Expected value |
| --- | --- |
| Download | <https://jonesinthefastlane.com/bundle.jsdos> |
| SHA-256 | `c08f3310f4f9cf47316bc32745507ae065bba7741430f7c3620602f534c46180` |
| Archive size | 1,078,159 bytes |
| Version marker | `1.000.060` |
| Resource-map SHA-256 | `f070a57f0e2c86bbf79339b1d41777a15e835d228cb52ff9cd3728a098fa053e` |
| First recorded retrieval | 2026-10-15 UTC |

The [initial bundle inventory](../../artifacts/discovery/2026-10-15-bundle-inventory.json) records archive entries. The [packed-resource inventory](../../artifacts/original-game/packed-resource-inventory.json) records all 299 resource-map entries and validates their volume offsets/header IDs. That earlier inventory explicitly did **not** decompress or render payloads. It is a baseline input check, not proof that all resources have now been decoded.

The map has **299 entries representing 266 unique resources**: 33 entries repeat identical resources. The earlier map-entry counts include these repetitions and must not be used as unique asset counts. A view can contain multiple loops/cels; resource counts are not counts of images, animations, recordings, or complete screens.

## Portable rebuild procedure

Use **Python 3.10 or newer** and the pinned Pillow dependency. Run from the repository root:

```sh
python3 -m venv work/asset-venv
work/asset-venv/bin/python -m pip install -r tools/research/requirements.txt
work/asset-venv/bin/python tools/research/catalogue_original_assets.py
```

On Windows use `work\asset-venv\Scripts\python.exe` for the last two commands. An existing Python environment with the pinned dependency is also supported. No developer-specific absolute runtime path is required. The only package dependency is `Pillow==12.3.0`.

The default run downloads the recorded HTTPS URL or validates its cached archive, checks the exact size/SHA-256 and version/map identifiers, then rebuilds `work/original-assets/decoded/`. Open **`work/original-assets/index.html`** in a browser to search by type, ID, or script role, browse image contact sheets, and follow links to text JSON, audio event/MIDI exports, and decompressed payloads.

For an offline input archive, replace the example path with your local copy:

```sh
work/asset-venv/bin/python tools/research/catalogue_original_assets.py --bundle /path/to/bundle.jsdos
```

This mode skips the bundle download and uses the same checksum validation. Install Python/Pillow beforehand; offline input does not install dependencies. A mismatch exits with an error before decoding or changing the source lock. The tool does not silently accept another edition or update the expected hash. An unavailable network source can be replaced by a locally supplied copy of the exact reference bytes; a changed source requires a separate provenance record and deliberate reference-edition decision.

To use a different ignored output directory:

```sh
work/asset-venv/bin/python tools/research/catalogue_original_assets.py --bundle /path/to/bundle.jsdos --output work/original-assets-check
```

Output is restricted to ignored `work/` or `artifacts/private/` inside the repository. The target's `decoded/` directory is regenerated. The original archive is retained at `<output>/source/bundle.jsdos`.

After a complete successful run, review and update the committed analytical summary with:

```sh
work/asset-venv/bin/python tools/research/catalogue_original_assets.py --bundle /path/to/bundle.jsdos --write-summary
```

Review the diff to `artifacts/original-game/decoded-asset-summary.json` before committing. It contains hashes, counts, resource identifiers, status, and role hints, without original payloads. Script-role joins come from the committed `artifacts/original-game/asset-role-hints.json` and are navigation aids rather than runtime proof.

## Verified output and coverage

The inspected `work/original-assets/coverage.json` records Python 3.12.14, Pillow 12.3.0, tool version `1`, the four tool-source hashes, **266 unique resources**, and no reported decode failures.

| Unique resource type | Count | Output/status |
| --- | ---: | --- |
| View | 90 | Rendered frame/contact-sheet references: 752 cels across these resources |
| Picture | 7 | Rendered picture-component references |
| Font | 8 | Rendered sheets covering 1,024 glyph slots |
| Cursor | 2 | Rendered images |
| Palette | 1 | Rendered palette reference |
| Sound | 34 | Device directory/events decoded; 169 finite MIDI exports |
| Text | 39 | Decoded JSON containing 677 strings |
| Script | 69 | Decompressed raw bytes |
| Vocabulary | 13 | Decompressed raw bytes |
| Patch | 3 | Decompressed raw bytes |

Status totals: **108 `rendered`**, **34 `directory_and_events_decoded`**, **39 `decoded`**, and **85 `decompressed`**. These total 266, not 299. The decompressed status does not imply semantic decompilation.

Local output includes:

- `index.html`: static searchable catalogue, with no hosted assets or analytics.
- `catalogue.json`: full per-resource records, resource hashes, exports, and available loop/cel data.
- `coverage.json`: input/tool/runtime identifiers, counts, failures, and limitations.
- `output-hashes.json`: relative-path SHA-256 manifest for generated output, excluding itself and timestamped `run-info.json`.
- `run-info.json`: generation timestamp and input mode, separated from deterministic content records.
- `decoded/sounds/sound-manifest.json`: sound-device tracks, event metadata, and MIDI export details.

To check reproducibility, run again into a fresh ignored output directory using the same bundle, tool files, and runtime/dependency versions. Compare the relative-path hashes in `output-hashes.json`. Runtime identifiers and tool hashes are part of metadata, so a changed environment or tool revision can change those files even if decoded resource bytes match. Compare individual resource/export hashes when investigating such a difference.

## Reproducibility records

The catalogue and coverage records identify:

- Input URL when applicable, archive SHA-256, byte count, version marker, and resource-map SHA-256.
- Tool version and local Python-file SHA-256 values. Decoder algorithms include narrow Python adaptations of ScummVM code; [THIRD_PARTY.md](../../tools/research/THIRD_PARTY.md) records the upstream revision, source paths, local scope, and licence.
- Python/Pillow versions and repository-relative export paths. The portable invocations are given above.
- Per-resource type/number, volume/offset, compression identifier, packed/unpacked byte lengths, and SHA-256 of decompressed payloads.
- For decoded graphics: loop/cel identifiers, dimensions, offsets/origins, palette source, transparency, output filenames, and decoding errors or limitations.
- For audio: whether the output is raw SCI data, decoded event data, or actually synthesised audio; any device/synthesis dependency.
- Generated output hashes and coverage totals by type and processing stage, with run timestamps in a separate file.

Store generated original assets, executable resources, raw/decompressed game payloads, and third-party research material under ignored `work/` or `artifacts/private/`. Committed files may contain original analytical notes, checksums, coverage counts, resource identifiers, filenames, and reproducible tooling. Do not place contact sheets containing original art among tracked public artifacts.

The research Python tools are **GPL-3.0-or-later**; their provenance is pinned to ScummVM revision `2b5f9b5d95f267c87889746906148db6088130f8`. Relevant attribution and licence text are retained in [SCUMMVM_COPYRIGHT](../../tools/research/SCUMMVM_COPYRIGHT) and [COPYING](../../tools/research/COPYING). Rebuilding does not require downloading or compiling ScummVM. This tooling licence does not select the future application's licence.

## Status vocabulary

The following includes conceptual pipeline terms as well as actual catalogue status labels; the verified run uses the four labels in its status totals above.

| Status | Meaning | Does not establish |
| --- | --- | --- |
| `indexed` | Resource-map entry and location recorded | Payload successfully extracted or understood |
| `decompressed` | Compression removed and expected size checked | Graphics/audio/text decoded correctly |
| `decoded` | Supported structure parsed; currently text strings | Final composite appearance or sound on an original device |
| `directory_and_events_decoded` | Sound device directory/events parsed and finite MIDI references exported | Original hardware synthesis, SCI runtime loops, or a recording |
| `rendered` | Inspectable bitmap/contact sheet generated; current exporter applies this to graphics | Running-game screen composition, animation timing, or exact original audio playback |
| `unsupported_or_invalid` / `partial_or_metadata_only` | Exporter could not fully handle or validate the requested resource | Complete decoding; these count as failures for a successful run |
| `failed` | Attempted supported stage failed; error retained | Success at later stages |
| `observed-in-game` | A separate recorded runtime capture/experiment confirms appearance or behaviour | Automatic confirmation of every resource in the catalogue |

A renderer may produce separate layers or frames. Such output must identify missing compositing, palette, mirroring, positioning, or timing behaviour. A `.snd` or MIDI-like event export must not be described as an original audio recording. Raw script bytes are not decompiled source.

## Validation and remaining limits

The verified run establishes the exact input, resource coverage, supported decoding outputs, output hashes, and zero reported decode failures. This is a decode-coverage claim, not a complete pixel-by-pixel or audio/runtime validation. A fresh HTTPS download and offline input rebuild produced identical hashes for 1,390 files (excluding the timestamp record and hash manifest itself). All 874 PNGs passed image-file verification, and 1,382 catalogue resource links resolved to files. An invalid archive was rejected before game extraction and left the tracked summary unchanged. An injected sound-decoder failure was recorded in coverage without replacing the verified summary. Browser inspection confirmed filtering for `view 707` and its course-label contact sheet. Representative decoded images inspected are listed in the [catalogue notes](../original-game/asset-catalogue-notes.md#completed-local-decoding-pass). Compare actual scene composition with the [town/screen specification](../original-game/town-and-screen-layout.md) and a future runtime capture rather than treating decoded pieces as finished screenshots.

The local catalogue is research material for understanding the original presentation. The adaptation's asset plans and newly created illustrations should remain separately identified.
