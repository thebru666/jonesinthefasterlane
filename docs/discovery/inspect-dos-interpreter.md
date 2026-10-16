# Rebuild the local DOS interpreter inspection

Recorded 2026-10-16. The website bundle contains the actual `sciv256.exe` interpreter, independently of the69 SCI game scripts. It is a60,373-byte MZ executable compressed with LZEXE0.91. A local unpack produces a115,284-byte MZ image. [Source/tool/output metadata](../../artifacts/original-game/dos-interpreter-unpack.json) pins both hashes and the unpacker source revision.

This is **static native-code inspection**: no DOS executable was launched, no gameplay was used, and no complete native-engine decompilation is claimed. Original executables, disassembly and downloaded unpacker source stay under ignored `work/`.

## Acquire and unpack

First [rebuild the original asset catalogue](rebuild-original-assets.md), retaining the exact `work/original-assets/source/bundle.jsdos`. Use Python3, a C compiler, GitHub CLI and GNU binutils. These instructions reproduce the Linux inspection; they do not require installing DOSBox or ScummVM.

Download the pinned open-source UNLZEXE source into ignored research storage:

```sh
mkdir -p work/interpreter-audit/unlzexe
gh api 'repos/mywave82/unlzexe/contents/unlzexe.c?ref=066aac7be3b27813c221d3b03621ad6dfaecd285' --jq .content \
  | base64 --decode > work/interpreter-audit/unlzexe/unlzexe.c
```

On the original host, `gh` is at `/home/agent/Documents/Codex/tools/gh` if absent from PATH. On another computer use its configured CLI; no authentication material belongs in a recipe or artifact. The [upstream README](https://github.com/mywave82/unlzexe/blob/066aac7be3b27813c221d3b03621ad6dfaecd285/README.md) identifies the authors and history; the source is not vendored here.

Verify source and archive member, then extract a separate local input copy:

```sh
python3 - <<'PY'
from pathlib import Path
import hashlib, zipfile
folder = Path('work/interpreter-audit/unlzexe')
assert hashlib.sha256((folder / 'unlzexe.c').read_bytes()).hexdigest() == 'b6d9814a1e0463371c9e92f0f9d80f80f30493ce4b3fe5f1484401b9afa6783d'
with zipfile.ZipFile('work/original-assets/source/bundle.jsdos') as archive:
    payload = archive.read('sciv256.exe')
assert hashlib.sha256(payload).hexdigest() == '16e0295610d38a3c747e81e2fbb0ba3421fec3286f22501300ccaaa4d734833f'
(folder / 'packed.exe').write_bytes(payload)
PY
```

Inspect the downloaded C source before compiling. From `work/interpreter-audit/unlzexe`, run:

```sh
gcc -O2 -o unlzexe unlzexe.c
./unlzexe packed.exe raw.exe
```

Use the explicit second filename and short basenames in that working directory. This old utility has DOS-style path handling and an in-place mode; the recipe keeps its input separate. The audited build emitted ignored-`fread`-return warnings, returned success, recognized0.91 and produced the output hash below. Two separate unpack runs matched exactly; the packed input hash was unchanged.

## Validate and prepare disassembly

From the repository root:

```sh
python3 - <<'PY'
from pathlib import Path
import hashlib, struct
raw = Path('work/interpreter-audit/unlzexe/raw.exe').read_bytes()
assert hashlib.sha256(raw).hexdigest() == 'e4e5493756739f33af2a570a67bd35340369c823293065200806fd078e92b797'
header = struct.unpack_from('<14H', raw)
assert header[0] == 0x5a4d
assert header[4] * 16 == 8704
Path('work/interpreter-audit/image.bin').write_bytes(raw[header[4] * 16:])
PY
objdump -D -b binary -m i8086 -M intel work/interpreter-audit/image.bin \
  > work/interpreter-audit/image.asm
```

The MZ header has2,050 relocation entries. Stripping its8,704 bytes yields the106,580-byte load image. Addresses in our native-code notes are offsets in that image, **not** file offsets including the header and not relocated DOS process addresses. A segment:offset maps to `16 × segment + offset` before adding the executable's runtime load base. Check relocation entries before interpreting stored segment values.

The interpreter's startup supplies relative data segment1856; the VM handler code is in relative segment0048. The opcode dispatch table is at data-segment offset013c; it contains256 near offsets indexed by the complete encoded SCI opcode byte. Kernel far pointers are at data-segment offset07d0. These identities are established from the actual dispatch instructions, selected handlers and relocation entries, rather than from names in an external decompilation.

Linear objdump output includes data regions and can begin at invalid instruction boundaries. Follow known entries/branches/calls and the native calling conventions; a plausible-looking line by itself is not a verified function. Do not commit generated assembly or original binary excerpts.

## Reproduce the bounded frame check

After also rebuilding the [SCI script listings](decompile-original-scripts.md):

```sh
python3 tools/research/check_economy_frame.py --check
```

This checks source hashes, package stack heights, original DOS relocations and reviewed handler addresses. [The frame finding](../rules-audit/economy-frame-semantics.md) describes the manually traced semantics and peer review. It proves a selected static call relationship, not original execution, every VM instruction or an entire economic simulation.
