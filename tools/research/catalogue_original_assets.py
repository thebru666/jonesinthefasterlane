#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Rebuild the ignored local original-asset reference from a pinned game bundle."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import platform
import shutil
import sys
import urllib.request
import zipfile

from sci_resources import extract, decode_assets
from sci_pictures import export_pictures
from sci_sound import export_sounds

ROOT = Path(__file__).resolve().parents[2]
SOURCE_URL = 'https://jonesinthefastlane.com/bundle.jsdos'
EXPECTED_SHA256 = 'c08f3310f4f9cf47316bc32745507ae065bba7741430f7c3620602f534c46180'
EXPECTED_BYTES = 1078159
MAP_SHA256 = 'f070a57f0e2c86bbf79339b1d41777a15e835d228cb52ff9cd3728a098fa053e'
TOOL_VERSION = '1'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def acquire(source, destination):
    destination.parent.mkdir(parents=True,exist_ok=True)
    if source:
        incoming=source.read_bytes()
    elif destination.exists():
        incoming=destination.read_bytes()
    else:
        request=urllib.request.Request(SOURCE_URL,headers={'User-Agent':'JonesAssetResearch/1'})
        with urllib.request.urlopen(request,timeout=60) as response:
            incoming=response.read(EXPECTED_BYTES+1)
    if len(incoming)!=EXPECTED_BYTES or hashlib.sha256(incoming).hexdigest()!=EXPECTED_SHA256:
        raise ValueError('Reference bundle checksum/size mismatch; refusing to decode or update the source lock.')
    if not destination.exists() or destination.read_bytes()!=incoming:
        temporary=destination.with_suffix('.download')
        temporary.write_bytes(incoming); temporary.replace(destination)
    return destination


def gallery(records, output):
    """Static local-only index: no hosted assets or analytics, just exported files."""
    escape=lambda value: html.escape(str(value),quote=True)
    cards=[]
    for r in records:
        title=f'{r["type"]} {r["number"]:03}'
        roles='; '.join(r.get('roles',[]))
        fields={key:r[key] for key in ['status','width','height','loop_count','cel_count','glyph_count','string_count','device_track_count','midi_export_count','error'] if key in r}
        links=' '.join(f'<a href="{escape(path)}">{escape(Path(path).name)}</a>' for path in r.get('exports',[]))
        preview=r.get('contact_sheet') or next((p for p in r.get('exports',[]) if p.endswith('.png')),None)
        image=f'<a href="{escape(preview)}"><img loading="lazy" src="{escape(preview)}" alt="{escape(title)} decoded reference"></a>' if preview else ''
        raw=f'<a href="{escape(r["raw_file"])}">decompressed payload</a>'
        cards.append(f'<article data-search="{escape((title+" "+roles).lower())}"><h2>{escape(title)}</h2><p>{escape(roles)}</p><pre>{escape(json.dumps(fields,indent=2))}</pre>{image}<details><summary>Exports and source</summary><p>{raw}</p><p class="files">{links}</p><p>SHA-256: <code>{escape(r["sha256"])}</code></p></details></article>')
    document='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Jones original asset reference</title>
<style>body{margin:0;background:#f3f0e8;color:#25353b;font:16px system-ui,sans-serif}header{padding:28px;position:sticky;top:0;background:#f3f0e8ed;border-bottom:1px solid #bbb;z-index:1}h1{margin:0 0 8px;font-size:27px}header p{max-width:1000px;margin:8px 0}input{padding:12px;min-width:300px;max-width:90%;font:inherit}main{padding:24px;display:grid;gap:20px;grid-template-columns:repeat(auto-fit,minmax(min(100%,440px),1fr))}article{padding:20px;background:white;border:1px solid #ccd0ce;border-radius:8px;overflow:hidden}article img{max-width:100%;height:auto;image-rendering:pixelated;background:repeating-conic-gradient(#ddd 0% 25%,#fff 0% 50%) 0 0/16px 16px}pre{font-size:13px}details{margin-top:14px}.files a{display:block;font-size:13px;overflow-wrap:anywhere}code{overflow-wrap:anywhere;font-size:12px}[hidden]{display:none}a{color:#1c5f77}</style>
<header><h1>Jones in the Fast Lane — original asset reference</h1><p>Local decoded resources from DOS 1.000.060. Frames and picture planes are not complete gameplay screenshots. MIDI files are finite event references, not recordings or original-hardware synthesis.</p><p><a href="catalogue.json">Full catalogue</a> · <a href="coverage.json">Coverage and limits</a> · <a href="decoded/sounds/sound-manifest.json">Sound details</a></p><label>Filter by type, resource ID, or script role <input id="filter" type="search" placeholder="e.g. university, view 707, picture"></label></header><main>'''+''.join(cards)+'''</main><script>document.getElementById('filter').addEventListener('input',e=>{const terms=e.target.value.toLowerCase().trim().split(/\\s+/);document.querySelectorAll('article').forEach(a=>a.hidden=!terms.every(t=>a.dataset.search.includes(t)));});</script></html>'''
    (output/'index.html').write_text(document,encoding='utf-8')


def build(args):
    from PIL import __version__ as pillow_version
    output=args.output.resolve()
    allowed=[(ROOT/'work').resolve(),(ROOT/'artifacts/private').resolve()]
    if not any(output.is_relative_to(p) for p in allowed):
        raise ValueError('Output must remain inside ignored work/ or artifacts/private/.')
    output.mkdir(parents=True,exist_ok=True)
    archive=acquire(args.bundle,output/'source/bundle.jsdos')
    game=output/'game'; game.mkdir(exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        version=z.read('version').decode('ascii').strip()
        if version!='1.000.060': raise ValueError('Unexpected game version')
        for name in ['resource.map','resource.001','resource.002']:
            (game/name).write_bytes(z.read(name))
    if digest(game/'resource.map')!=MAP_SHA256: raise ValueError('Resource map checksum mismatch')
    decoded=output/'decoded'
    if decoded.exists(): shutil.rmtree(decoded)
    decoded.mkdir()
    entries=extract(game,decoded)
    decode_assets(decoded,entries)
    pictures=export_pictures(decoded/'resources',decoded)
    sounds=export_sounds(decoded/'resources',decoded/'sounds')
    picmap={r['number']:r for r in pictures}; soundmap={r['resource_id']:r for r in sounds}
    hints=json.loads((ROOT/'artifacts/original-game/asset-role-hints.json').read_text())
    roles={}
    for r in hints['resources']:
        key=(r['resource_type'],r['resource_id'])
        labels=[r.get('role_hint','')]+[f'{q["script"]}: {q["instance"]}' for q in r['references']]
        roles[key]=list(dict.fromkeys(label for label in labels if label and not label.startswith('See script instances')))
    records=[]; seen=set()
    for e in entries:
        key=(e['type'],e['number'])
        if key in seen: continue
        seen.add(key); r=dict(e)
        r.setdefault('status','decompressed')
        if e['type']=='picture': r.update(picmap[e['number']])
        elif e['type']=='sound':
            sound=soundmap[e['number']]
            r['status']=sound['status'];r['exports']=['sounds/'+sound['events_file']] if sound.get('events_file') else []
            if sound.get('error'): r['error']=sound['error']
            r['exports']+=['sounds/'+t['midi_file'] for t in sound.get('tracks',[]) if 'midi_file' in t]
            r['device_track_count']=len(sound.get('tracks',[]));r['midi_export_count']=sum('midi_file' in t for t in sound.get('tracks',[]))
            r['limitations']=sound.get('limitations',[])
        elif e['type'] in ['view','font','cursor','palette'] and r.get('exports'): r['status']='rendered'
        r['roles']=roles.get(key,[])
        if key==('picture',11): r['roles'].insert(0,'Town board background')
        for field in ['raw_file','contact_sheet']:
            if field in r: r[field]='decoded/'+r[field]
        r['exports']=['decoded/'+p for p in r.get('exports',[])]
        for cel in r.get('cels',[]): cel['file']='decoded/'+cel['file']
        records.append(r)
    records.sort(key=lambda r:(r['type'],r['number']))
    if len(entries)!=299 or len(records)!=266: raise ValueError('Resource coverage mismatch')
    failures=[r for r in records if r['status'] in ['failed','unsupported_or_invalid','partial_or_metadata_only']]
    tool_paths=sorted(Path(__file__).parent.glob('*.py'))
    tools={p.name:digest(p) for p in tool_paths}
    source={'url':SOURCE_URL,'archive_sha256':EXPECTED_SHA256,'archive_bytes':EXPECTED_BYTES,'version':version,'map_sha256':MAP_SHA256}
    coverage={'source':source,'tool_version':TOOL_VERSION,'tool_sha256':tools,'runtime':{'python':platform.python_version(),'Pillow':pillow_version},'map_entries':len(entries),'unique_resources':len(records),'identical_duplicate_entries':len(entries)-len(records),'by_type':dict(Counter(r['type'] for r in records)),'by_status':dict(Counter(r['status'] for r in records)),'view_cels':sum(r.get('cel_count',0) for r in records),'font_glyph_slots':sum(r.get('glyph_count',0) for r in records),'text_strings':sum(r.get('string_count',0) for r in records),'midi_files':sum(r.get('midi_export_count',0) for r in records),'failures':failures,'limitations':['Rendered resources are component references, not reconstructed gameplay screenshots.','Sound event/MIDI exports do not synthesize original hardware instruments or execute SCI runtime loops.','Scripts, vocabulary and patch resources are decompressed bytes, not semantically decompiled or rendered.','Palette state, compositing, scaling and timing can differ in the running game.']}
    dump(output/'catalogue.json',{'coverage':coverage,'resources':records})
    dump(output/'coverage.json',coverage)
    dump(output/'run-info.json',{'created_utc':datetime.now(timezone.utc).isoformat(),'input_mode':'offline-bundle' if args.bundle else 'download-or-validated-cache'})
    gallery(records,output)
    hashes={p.relative_to(output).as_posix():digest(p) for p in sorted(output.rglob('*')) if p.is_file() and p.name not in ['run-info.json','output-hashes.json']}
    dump(output/'output-hashes.json',hashes)
    if args.write_summary and not failures:
        summary_path=ROOT/'artifacts/original-game/decoded-asset-summary.json'
        compact=[]
        for r in records:
            compact.append({k:r[k] for k in ['type','number','sha256','unpacked_bytes','status','roles','loop_count','cel_count','glyph_count','string_count','device_track_count','midi_export_count','width','height'] if k in r})
        dump(summary_path,{'coverage':coverage,'resources':compact,'local_reference':'work/original-assets/index.html','note':'Analytical metadata only. Original artwork/audio/text payloads and contact sheets are not committed.'})
    print(json.dumps({k:coverage[k] for k in ['map_entries','unique_resources','by_status','view_cels','font_glyph_slots','text_strings','midi_files']},indent=2))
    print(f'Local catalogue: {output / "index.html"}')
    if failures: raise ValueError(f'{len(failures)} resource decodes failed or are partial; inspect coverage.json')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle',type=Path,help='Offline input; still requires the pinned size/hash.')
    parser.add_argument('--output',type=Path,default=ROOT/'work/original-assets',help='Ignored output directory; decoded/ is regenerated.')
    parser.add_argument('--write-summary',action='store_true',help='Update committed analytical metadata after a verified run.')
    try:
        build(parser.parse_args())
    except (ValueError,OSError,zipfile.BadZipFile) as error:
        print(f'Error: {error}',file=sys.stderr);raise SystemExit(1)
