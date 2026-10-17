#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Rebuild a bounded package-wide Happiness call/writer inventory.

Original analytical inventory tooling; no game rule implementation or payload.
Consumes the ignored decoder output and verifies its instruction spans against
hash-identified raw resources. Candidate sends still require manual target review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from sci_scripts import selectors

ROOT = Path(__file__).resolve().parents[2]
BUNDLE_SHA = 'c08f3310f4f9cf47316bc32745507ae065bba7741430f7c3620602f534c46180'
VOCAB_SHA = '1adc0a33a4c7e79022b0c936b0613dcc89deb2a9ffe84f3e4539afec86601850'


def inventory(decoded: Path, resources: Path) -> dict:
    vocab = (resources / 'vocabulary.997.bin').read_bytes()
    assert hashlib.sha256(vocab).hexdigest() == VOCAB_SHA
    assert selectors(vocab)[378] == 'hapStat'
    scripts = [json.loads(p.read_text()) for p in sorted(decoded.glob('script-*.json'))]
    assert len(scripts) == 69
    resource_records, calls, literal_loads, direct_writes = [], [], [], []
    templates = []
    checked = 0
    for script in scripts:
        number = script['number']
        payload = (resources / f'script.{number:03}.bin').read_bytes()
        assert hashlib.sha256(payload).hexdigest() == script['sha256']
        instructions = script['instructions']
        owner = {}
        for function in script['functions']:
            for offset in function['instruction_offsets']:
                owner.setdefault(offset, []).append(function['name'])
        resource_records.append({'script': number, 'sha256': script['sha256'],
                                 'bytes': len(payload), 'instructions': len(instructions)})
        for index, ins in enumerate(instructions):
            offset, args = ins['offset'], ins['args']
            assert payload[offset:ins['end']].hex() == ins['bytes']
            checked += 1
            common = {'script': number, 'offset': hex(offset), 'owners': owner.get(offset, [])}
            if ((ins['op'] == 'callb' and args[0] == 13) or
                    (ins['op'] == 'calle' and args[:2] == [0, 13])):
                scope = 'actions' if 200 <= number <= 213 else 'events'
                assert scope == 'actions' or number in (1, 111, 232)
                calls.append({**common, 'instruction': ins['op'],
                              'argument_words': args[-1] // 2, 'scope': scope})
            if ins['op'] == 'pushi' and args == [378]:
                following = instructions[index + 1]
                assert following['offset'] == ins['end']
                assert following['op'] in ('push0', 'push1')
                literal_loads.append({**common, 'following_argc_literal':
                                      0 if following['op'] == 'push0' else 1})
            if (number == 1 and any(name.startswith('Player.') for name in owner.get(offset, []))
                    and ins['op'] in ('aTop', 'sTop', 'ipToa', 'dpToa', 'ipTos', 'dpTos')
                    and args == [24]):
                direct_writes.append({**common, 'instruction': ins['op']})
        if number == 1:
            for obj in script['objects']:
                if obj['name'] in ('Player', 'player1', 'player2', 'player3', 'player4'):
                    prop = next(p for p in obj['properties'] if p['name'] == 'hapStat')
                    assert prop['selector'] == 378 and prop['offset'] == 24 and prop['value'] == 0
                    templates.append({'name': obj['name'], 'value': prop['value']})
    assert checked == 53740 and len(calls) == 76
    assert sum(c['scope'] == 'actions' for c in calls) == 47
    assert sum(c['scope'] == 'events' for c in calls) == 29
    assert sum(c['argument_words'] == 2 for c in calls) == 8
    assert len(literal_loads) == 8 and not direct_writes and len(templates) == 5
    assert [(c['script'], c['offset']) for c in literal_loads if c['following_argc_literal']] == [(0, '0x621')]
    domain_records = []
    for scope, name in [('actions', 'happiness-actions-verification.json'),
                        ('events', 'happiness-events-verification.json')]:
        path = ROOT / 'artifacts/rules-audit' / name
        domain = json.loads(path.read_text())
        actual = {(site['script'], int(site['call_offset'], 16)) for site in domain['sites']}
        expected = {(site['script'], int(site['offset'], 16)) for site in calls if site['scope'] == scope}
        assert actual == expected and len(actual) == len(domain['sites'])
        domain_records.append({'scope': scope, 'artifact': str(path.relative_to(ROOT)),
                               'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                               'mapped_sites': len(actual)})
    return {
        'schema': 1, 'audit_date': '2026-10-17', 'version': 'website DOS1.000.060',
        'evidence': 'BYTECODE bounded static inventory, not runtime or general absence proof',
        'bundle_sha256': BUNDLE_SHA,
        'provenance': 'artifacts/original-game/bytecode-coverage.json',
        'tool_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'selector_vocabulary_sha256': VOCAB_SHA,
        'resources': resource_records,
        'checked_instruction_spans': checked,
        'literal_Main_export13_calls': calls,
        'literal_hapStat_load_candidates': literal_loads,
        'direct_Player_property24_mutations': direct_writes,
        'template_values': templates,
        'domain_coverage': domain_records,
        'summary': {'call_sites': 76, 'action_sites': 47, 'event_sites': 29,
                    'explicit_player_argument_sites': 8,
                    'identified_literal_setter': 'Main export13 send at0:0x0629'},
        'semantic_review': {'helper': '0:0x05ea-0x062b, active player unless second argument; add delta then clamp0..100',
                            'actions': 'docs/rules-audit/happiness-actions.md',
                            'events': 'docs/rules-audit/happiness-events.md'},
        'limits': ['Literal helper calls and literal selector candidates only; dynamic/computed calls may be missed.',
                   'Known Player methods only for direct property-slot search; not every possible alias/inherited/native effect.',
                   'An argc candidate is not a proof of receiver identity; selected actual sends were manually reviewed.',
                   'Default property values are initialization evidence, not executable setters.',
                   'Amounts, gates and reachability are in manually reviewed domain notes; this tool does not execute them.']}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--decoded', type=Path, default=ROOT / 'work/bytecode/decoded')
    parser.add_argument('--resources', type=Path, default=ROOT / 'work/original-assets/decoded/resources')
    parser.add_argument('--output', type=Path, default=ROOT / 'artifacts/rules-audit/happiness-inventory.json')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = inventory(args.decoded, args.resources)
    if args.check:
        assert json.loads(args.output.read_text()) == result, 'Tracked inventory differs; regenerate after review'
    else:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print('Verified 69 resources / 53,740 instruction spans; 76 helper sites = 47 actions + 29 events.')


if __name__ == '__main__':
    main()
