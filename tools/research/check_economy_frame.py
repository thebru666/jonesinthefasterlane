#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Check a bounded SCI stack-frame inference, without executing game logic.

Original analytical checker, using the committed decoder's ignored JSON output.
Models stack heights and a synthetic batched-message frame under pinned ScummVM
send/return semantics. No original script bytes or decompiled code are embedded.
Original DOS handler-address checks support a separately peer-reviewed static trace.
This does not execute either interpreter or simulate its economy.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / 'artifacts/rules-audit/economy-frame-verification.json'
SCRIPT_SHA = '4ff0ae66d65f656c91a6fcff2bb6573c8b106509f11b316315a74f1cdfc83525'
VM_REV = '2b5f9b5d95f267c87889746906148db6088130f8'


def stack_effect(instruction: dict) -> int:
    op, args = instruction['opcode'], instruction['args']
    if op in (1, 2, 3, 13, 15, 17):
        return -1
    if op in (27, 28, 51, 59, 60, 61, 70):
        return 1
    if op == 31:
        return args[0]
    if op == 33:
        return -(args[-1] // 2 + 1)
    if op in (24, 25, 26, 36, 49, 50, 53, 54, 64, 67, 82):
        return 0
    raise ValueError(f'Unreviewed stack effect: {instruction["op"]}')


def inspect(script: dict) -> dict:
    if script['number'] != 107 or script['sha256'] != SCRIPT_SHA:
        raise ValueError('Input is not the locked website script107')
    ins = {i['offset']: i for i in script['instructions']}
    init = next(f for f in script['functions'] if f['name'] == 'EconomicIndex.init')
    update = next(f for f in script['functions'] if f['name'] == 'EconomicIndex.doit')
    members = set(init['instruction_offsets'])
    assert ins[init['offset']]['op'] == 'link' and ins[init['offset']]['args'] == [1]
    # Follow every recovered branch, even the semantically impossible alternative.
    heights: dict[int, set[int]] = {}
    predecessors: dict[int, set[int]] = {off: set() for off in members}
    pending = [(init['offset'], 0)]
    returns = set()
    while pending:
        off, height = pending.pop()
        if height in heights.setdefault(off, set()):
            continue
        heights[off].add(height)
        instruction = ins[off]
        after = height + stack_effect(instruction)
        assert after >= 1, ('frame underflow', off, height, after)
        if instruction['op'] == 'ret':
            returns.add(after)
            continue
        targets = list(instruction['targets']) if instruction['op'] in ('bnt', 'jmp') else []
        if instruction['op'] != 'jmp':
            targets.append(instruction['end'])
        for target in targets:
            assert target in members
            predecessors[target].add(off)
            pending.append((target, after))
    assert returns == {1}
    reached = set(heights)
    assert reached == members
    assert all(len(values) == 1 for values in heights.values())
    dom = {off: ({off} if off == init['offset'] else set(reached)) for off in reached}
    changed = True
    while changed:
        changed = False
        for off in sorted(reached - {init['offset']}):
            value = {off} | set.intersection(*(dom[p] for p in predecessors[off]))
            if value != dom[off]:
                dom[off] = value
                changed = True
    writes = [off for off in sorted(reached) if ins[off]['op'] == 'sat' and ins[off]['args'] == [0]]
    assert writes == [0x00f1, 0x00f7]
    assert all(0x00f7 in dom[off] for off in reached if ins[off]['op'] == 'ret')
    assert ins[0x041a]['op'] == 'send' and ins[0x041a]['args'] == [12]
    assert ins[0x01c3]['op'] == 'sat' and ins[0x01c3]['args'] == [0]
    assert ins[0x01c9]['op'] == 'lsp' and ins[0x01c9]['args'] == [1]
    assert ins[update['offset']]['op'] == 'link' and ins[update['offset']]['args'] == [1]

    # Six message words: [selector, argc2, arg, arg, selector, argc0].
    # The second method's missing param1 addresses packet end. The preceding
    # method leaves one allocated local there, and carries SP one word higher.
    packet_words = ins[0x041a]['args'][0] // 2
    init_fp = packet_words
    init_temp0 = init_fp
    init_return_sp = init_fp + next(iter(returns))
    next_argp = packet_words - 1
    next_param1 = next_argp + 1
    next_fp = init_return_sp
    next_temp0 = next_fp
    assert next_param1 == init_temp0
    assert next_param1 != next_temp0
    return {
        'schema': 1,
        'verified_date': '2026-10-16',
        'evidence': 'BYTECODE plus pinned reference-interpreter frame inference; not DOS execution',
        'script': {'number': 107, 'sha256': SCRIPT_SHA},
        'scummvm_revision': VM_REV,
        'input_instruction_records': len(reached),
        'all_static_init_return_stack_deltas': sorted(returns),
        'init_local0_writes': [f'0x{off:04x}' for off in writes],
        'last_write_dominates_all_static_returns': True,
        'caller_send': '0x041a',
        'caller_frame_words': packet_words,
        'synthetic_word_addresses': {
            'init_frame_and_temp0': init_temp0,
            'next_argc_word': next_argp,
            'next_missing_param1': next_param1,
            'next_frame_and_guarded_temp0': next_temp0,
        },
        'conclusion': 'In the pinned reference VM, the omitted parameter aliases the preceding init local0, not the guarded update local0.',
        'limits': [
            'The six-word caller packet and method identities are manually traced from package instructions.',
            'SP carry and out-of-argument-frame stack reads follow the pinned ScummVM implementation.',
            'No interpreter, full VM, RNG or economic distribution is executed; selected DOS machine-code paths are manually traced.',
            'Other call shapes, dynamic rest arguments and interpreter workarounds are outside scope.',
        ],
    }


def inspect_dos(path: Path) -> dict:
    """Validate the exact unpacked MZ and derive reviewed handler addresses."""
    import struct
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == 'e4e5493756739f33af2a570a67bd35340369c823293065200806fd078e92b797'
    header = struct.unpack_from('<14H', raw)
    assert header[0] == 0x5a4d
    header_bytes = header[4] * 16
    image = raw[header_bytes:]
    entry = header[11] * 16 + header[10]
    assert image[entry] == 0xba  # Startup's relocated MOV DX, segment immediate.
    data_segment = struct.unpack_from('<H', image, entry + 1)[0]
    code_segment = struct.unpack_from('<H', image, 0xb67e)[0]
    relocations = {
        seg * 16 + off
        for off, seg in struct.iter_unpack('<HH', raw[header[12]:header[12] + header[3] * 4])
    }
    assert entry + 1 in relocations and 0xb67e in relocations
    table = data_segment * 16 + 0x013c
    handlers = {}
    for opcode in (0x3f, 0x43, 0x48, 0x4a, 0x8f):
        offset = struct.unpack_from('<H', image, table + 2 * opcode)[0]
        handlers[f'0x{opcode:02x}'] = {
            'segment_offset': f'{code_segment:04x}:{offset:04x}',
            'load_image_offset': f'0x{code_segment * 16 + offset:05x}',
        }
    kernels = {}
    for kernel in (60, 61):
        pointer = data_segment * 16 + 0x07d0 + 4 * kernel
        offset, segment = struct.unpack_from('<HH', image, pointer)
        assert pointer + 2 in relocations
        kernels[str(kernel)] = {
            'segment_offset': f'{segment:04x}:{offset:04x}',
            'load_image_offset': f'0x{segment * 16 + offset:05x}',
        }
    return {
        'unpacked_executable_sha256': digest,
        'unpacked_bytes': len(raw),
        'mz_header_bytes': header_bytes,
        'load_image_sha256': hashlib.sha256(image).hexdigest(),
        'startup_entry_image_offset': f'0x{entry:05x}',
        'data_segment_relative': f'0x{data_segment:04x}',
        'vm_code_segment_relative': f'0x{code_segment:04x}',
        'reviewed_opcode_handlers': handlers,
        'reviewed_kernel_handlers': kernels,
        'manual_trace_ranges_load_image': {
            'link_temp_base_and_allocation': '0x00adf–0x00af7',
            'parameter_stack_load': '0x00eed–0x00f0c',
            'return': '0x00c5b',
            'message_loop_and_parameter_base': '0x0b57b–0x0b6c4',
            'kernel_frame_cleanup': '0x00b40–0x00b98',
            'random_preserves_host_saved_vm_bp': '0x06f72–0x06ff6',
            'abs_preserves_host_saved_vm_bp': '0x071be–0x071d3',
        },
        'pointer_convention': 'DOS BP is last occupied VM word; reference VM SP is next free word. Both produce missing parameter1 at initialization temporary0.',
        'semantic_review': 'Manually traced and independently peer-reviewed; this checker validates exact input, relocations and handler addresses, not x86 execution.',
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=ROOT / 'work/bytecode/decoded/script-107.json')
    parser.add_argument('--resource', type=Path, default=ROOT / 'work/original-assets/decoded/resources/script.107.bin')
    parser.add_argument('--dos-exe', type=Path, default=ROOT / 'work/interpreter-audit/unlzexe/raw.exe')
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    script = json.loads(args.input.read_text())
    raw = args.resource.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SCRIPT_SHA:
        raise SystemExit('Raw script differs from locked website edition')
    for instruction in script['instructions']:
        if raw[instruction['offset']:instruction['end']].hex() != instruction['bytes']:
            raise SystemExit('Decoded instruction span differs from raw resource')
    result = inspect(script)
    result['original_dos_static_trace'] = inspect_dos(args.dos_exe)
    result['evidence'] = 'BYTECODE + original DOS interpreter static trace + reference-interpreter frame inference; no runtime execution'
    result['conclusion'] = 'The actual DOS message/frame paths and pinned reference VM both alias omitted parameter1 to initialization temporary0, not the update guard temporary.'
    result['tool_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    if args.check:
        if result != json.loads(args.output.read_text()):
            raise SystemExit('Frame evidence differs; inspect before regenerating')
    else:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print('Verified package stack ledger and original DOS handler addresses; static DOS/reference-frame alias agrees. No runtime execution.')


if __name__ == '__main__':
    main()
