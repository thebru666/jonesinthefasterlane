# Local original-asset research

These tools decode the **exact** original package identified in [the rebuild guide](../../docs/discovery/rebuild-original-assets.md). They do not build the new game.

```sh
python3 -m venv work/asset-venv
work/asset-venv/bin/python -m pip install -r tools/research/requirements.txt
work/asset-venv/bin/python tools/research/catalogue_original_assets.py
```

Use Python 3.10 or newer. On Windows, the virtual-environment executable is `work\asset-venv\Scripts\python.exe`; the exporter itself uses portable paths. An existing Python with the pinned Pillow version works too. See [the rebuild guide](../../docs/discovery/rebuild-original-assets.md) for offline input, coverage, failure behaviour, and deterministic output checks.

The default result is `work/original-assets/index.html`. Open that file directly in a browser. It is a static local reference with search, image sheets, decompressed payload links, text JSON, and sound-event/MIDI references. Everything generated stays under ignored `work/`.

`--write-summary` updates the tracked analytical catalogue only after a complete decode. It contains resource IDs, hashes, counts, role hints, and statuses, not the original resource payloads. Review the diff before committing it.

The tools are GPL-3.0-or-later; [provenance and notices](THIRD_PARTY.md). They deliberately support this reference edition rather than every SCI format. Unknown picture opcodes or invalid streams fail explicitly. Audio exports are finite MIDI/event references, not original-hardware playback or recordings.

After decoding, render the analytical screen studies with:

```sh
work/asset-venv/bin/python tools/research/reconstruct_screen_studies.py
```

Open `work/original-screen-studies/index.html`. These are partial static composites; [state and geometry limits](../../docs/original-game/screen-reconstruction.md) apply. Recipes are committed metadata; generated original artwork stays ignored.

The actual gameplay evidence is separate from analytical composites. `python3 tools/research/index_runtime_captures.py --check` checks retained screenshot hashes and builds `work/runtime-validation/index.html`; it reports missing evidence rather than downloading replacements. New captures on another computer require replaying the [recorded actions](../../docs/rules-audit/runtime-observations.md).
