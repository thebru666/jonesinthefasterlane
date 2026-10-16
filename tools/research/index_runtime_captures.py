#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Index locally retained gameplay captures; never download substitute evidence."""
import argparse
import hashlib
import html
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'artifacts/rules-audit/runtime-capture-manifest.json'


def build(check=False):
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    output = ROOT / 'work/runtime-validation/index.html'
    output.parent.mkdir(parents=True, exist_ok=True)
    cards = []
    missing = []
    changed = []
    esc = lambda value: html.escape(str(value), quote=True)
    for capture in manifest['captures']:
        path = (ROOT / capture['local_path']).resolve()
        if not path.is_relative_to((ROOT / 'work/runtime-validation').resolve()):
            raise ValueError('Capture path must remain in ignored work/runtime-validation/.')
        exists = path.is_file()
        valid = exists and hashlib.sha256(path.read_bytes()).hexdigest() == capture['sha256']
        if not exists:
            missing.append(capture['local_path'])
        elif not valid:
            changed.append(capture['local_path'])
        relative = os.path.relpath(path, output.parent).replace(os.sep, '/')
        preview = f'<a href="{esc(relative)}"><img loading="lazy" src="{esc(relative)}" alt="{esc(capture["caption"])}"></a>' if valid else '<p>Original local capture unavailable or hash changed. Replay the documented case to create new evidence.</p>'
        cards.append(f'<article><h2>{esc(capture["id"])}</h2><p>{esc(capture["caption"])}</p>{preview}<p>Observations: {esc(", ".join(capture["observations"]) or "context only")}</p><small>{esc(capture["local_path"])}</small></article>')
    document = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Jones runtime evidence</title><style>body{font:16px system-ui;background:#eee9df;color:#20333b;margin:24px}header{max-width:1050px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,480px),1fr));gap:20px}article{background:white;padding:20px;border:1px solid #bcc3c3;border-radius:8px;min-width:0}img{width:100%;height:auto;image-rendering:pixelated}small{overflow-wrap:anywhere}h2{font-size:19px}p{line-height:1.45}</style><header><h1>Jones — actual runtime captures</h1><p>Original website game, ordinary mouse/keyboard play. These are viewport captures, separately identified from analytical screen composites. No edited saves, debugger or injected game state. Read runtime-observations.md for exact claims and limits; a capture does not validate every rule shown on its screen.</p><p>Original images remain ignored local files. The committed manifest retains filenames, dimensions and hashes. Missing images are reported rather than replaced.</p></header><main>''' + ''.join(cards) + '</main>'
    output.write_text(document, encoding='utf-8')
    print(json.dumps({'captures': len(cards), 'missing': missing, 'hash_changed': changed, 'gallery': str(output)}, indent=2))
    return 1 if check and (missing or changed) else 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Exit unsuccessfully for missing/changed original captures.')
    raise SystemExit(build(parser.parse_args().check))
