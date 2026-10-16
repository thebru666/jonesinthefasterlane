# Research exporter provenance and licence

The Python files in this directory are research tooling, licensed **GPL-3.0-or-later**. They include narrow Python adaptations of SCI format/decoding algorithms from ScummVM. This notice does not select a licence for the future game application or grant rights to original game assets.

Upstream: [ScummVM](https://github.com/scummvm/scummvm), pinned revision `2b5f9b5d95f267c87889746906148db6088130f8`.

Copyright (C) 2001–2026 the ScummVM contributors; names and upstream notices are retained in [SCUMMVM_COPYRIGHT](SCUMMVM_COPYRIGHT). The GPL text is retained in [COPYING](COPYING). The upstream files' GPL-3.0-or-later notices apply to the adapted algorithms. Local modifications implement a narrow offline exporter for the hash-pinned Jones floppy bundle rather than a complete interpreter.

| Local file | Upstream algorithm / format references |
| --- | --- |
| `sci_resources.py` | `engines/sci/resource/decompressor.cpp`, `resource.cpp`, `resource.h`; `engines/sci/graphics/view.cpp`, `cursor.cpp`, `scifont.cpp`, `palette16.cpp` |
| `sci_pictures.py` | `engines/sci/graphics/picture.cpp`, `screen.cpp`; shared VGA cel/palette helpers above |
| `sci_sound.py` | `engines/sci/resource/resource_audio.cpp`; `engines/sci/sound/midiparser_sci.cpp` |
| `index_runtime_captures.py` | Original local capture hashing/index reporting; GPL-3.0-or-later, no game payloads embedded |
| `check_lottery_probabilities.py` | Original independent enumeration of the documented lottery arithmetic; no original SCI execution or script payload, GPL-3.0-or-later |
| `check_ai_goal_allocation.py` | Original independent arithmetic check of documented target bounds/capacity, not original SCI execution; GPL-3.0-or-later |
| `reconstruct_screen_studies.py` | Original project image composition and HTML reporting using analytical recipe metadata; GPL-3.0-or-later, no copied game script implementation |
| `catalogue_original_assets.py` | Project orchestration, checksum lock, source-role joins, manifests and local HTML index; GPL-3.0-or-later for consistent tooling distribution |

For every path above, source is available at `https://github.com/scummvm/scummvm/blob/2b5f9b5d95f267c87889746906148db6088130f8/<path>`. The decoded catalogue records hashes of the local Python implementations. The committed source lock records the upstream revision; reproducing the export does not download or build ScummVM.

The only Python package dependency is Pillow, pinned in [requirements.txt](requirements.txt). Pillow has its own licence; see [Pillow's licence](https://github.com/python-pillow/Pillow/blob/main/LICENSE). No Pillow code or package is copied into this repository.

No original game images, sounds, text collections, compiled scripts, decompressed payloads, or reference contact sheets are included in these tooling files.
