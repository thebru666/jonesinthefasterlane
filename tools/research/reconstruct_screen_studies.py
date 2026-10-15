#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Render local analytical screen studies from decoded assets and tracked recipes.

Original project orchestration; does not execute/decompile SCI or reproduce its
window manager. No original game payload is embedded in this file or the recipes.
"""
import argparse
import hashlib
import html
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[2]


def build(assets,output):
    output=output.resolve()
    if not any(output.is_relative_to((ROOT/p).resolve()) for p in ['work','artifacts/private']):
        raise ValueError('Output must be inside ignored work/ or artifacts/private/.')
    output.mkdir(parents=True,exist_ok=True)
    recipes_path=ROOT/'artifacts/original-game/screen-study-recipes.json'
    recipes=json.loads(recipes_path.read_text())
    catalogue=json.loads((assets/'catalogue.json').read_text())
    if catalogue['coverage']['source']['archive_sha256']!=recipes['bundle_sha256']:
        raise ValueError('Decoded asset source does not match recipe bundle.')
    resources={(r['type'],r['number']):r for r in catalogue['resources']}
    used={}
    def read_image(path):
        file=assets/path
        used[path]=hashlib.sha256(file.read_bytes()).hexdigest()
        return Image.open(file).convert('RGBA')
    def cel(view,loop,number):
        record=resources['view',view]
        matches=[c for c in record['cels'] if c['loop']==loop and c['cel']==number]
        if len(matches)!=1:raise ValueError(f'Unknown cel {view}/{loop}/{number}')
        return read_image(matches[0]['file'])
    town=read_image('decoded/pictures/picture-011-visual.png')
    town.save(output/'town.png')
    cards=[];records=[]
    esc=lambda s:html.escape(str(s),quote=True)
    for study in recipes['studies']:
        canvas=town.copy()
        x,y=study['dialog_origin'];w,h=study['dialog_size']
        # Neutral analytical fill where the runtime window's surface is not supplied.
        ImageDraw.Draw(canvas).rectangle((x,y,x+w-1,y+h-1),fill='#d0d0d0')
        boxes=[]
        for layer in study['layers']:
            image=cel(layer['view'],layer['loop'],layer['cel'])
            left=x+layer['x']; top=y+layer['y']
            canvas.alpha_composite(image,(left,top))
            boxes.append(dict(name=layer['name'],rect=[left,top,image.width,image.height],view=layer['view'],loop=layer['loop'],cel=layer['cel'],source=layer['source']))
        file=study['id']+'.png';canvas.save(output/file)
        annotated=canvas.copy();d=ImageDraw.Draw(annotated)
        for i,b in enumerate(boxes,1):
            a,t,bw,bh=b['rect'];d.rectangle((a,t,a+bw-1,t+bh-1),outline='#ff00aa');d.text((a,t),str(i),fill='#ff00aa',stroke_width=1,stroke_fill='#ffffff')
        annotated.save(output/(study['id']+'-annotated.png'))
        rows=''.join(f'<li><a href="{esc(b["source"])}">{esc(b["name"])}</a>: view {b["view"]}, loop {b["loop"]}, cel {b["cel"]}; screen rect {esc(b["rect"])}</li>' for b in boxes)
        cards.append(f'<article id="{esc(study["id"])}"><h2>{esc(study["title"])}</h2><p>{esc(study["state"])}</p><img src="{file}" alt="Analytical composite of {esc(study["title"])}"><p><a href="{study["id"]}-annotated.png">Numbered component bounds</a> · <a href="{esc(study["source"])}">Published script</a></p><details><summary>Layers and source coordinates</summary><ol>{rows}</ol></details><p><strong>Omitted / uncertain:</strong> {esc(study["omitted"])}</p><p>Next: {esc(", ".join(study["next"]))}</p></article>')
        records.append({'id':study['id'],'image':file,'layers':boxes,'image_sha256':hashlib.sha256((output/file).read_bytes()).hexdigest()})
    finish=resources['view',609]['contact_sheet']
    image=read_image(finish);image.save(output/'victory-components.png')
    header='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Jones original screen studies</title><style>body{margin:24px;background:#f2eee5;color:#24353b;font:16px system-ui}h1{margin-bottom:8px}header{max-width:1050px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,570px),1fr));gap:24px}article{background:white;padding:20px;border:1px solid #bcc4c4;border-radius:8px;min-width:0}img{width:100%;image-rendering:pixelated;background:#ddd}article>img{aspect-ratio:8/5}a{color:#155b7a}li{margin:6px 0}nav{line-height:2}p{line-height:1.45}strong{color:#94352a}</style><header><h1>Jones in the Fast Lane — screen studies</h1><p><strong>Analytical composites, not captured gameplay.</strong> Decoded floppy 1.000.060 artwork plus coordinates from a separately published decompilation. Static states are selected explicitly. Grey fill is a research placeholder. Runtime text, window borders/port adjustments, focus, music, animation, palette changes and board indicators are incomplete.</p><p>Images use native 320 × 200 logical geometry, enlarged with square pixels. Original 4:3 display aspect is not applied. Links identify source scripts and numbered component bounds. Read the committed screen-reconstruction.md alongside these local references.</p>'''
    nav='<nav>'+ ' · '.join(f'<a href="#{s["id"]}">{esc(s["title"])}</a>' for s in recipes['studies'])+'</nav></header>'
    tail='<article><h2>Victory components — no composite</h2><img src="victory-components.png" alt="Decoded victory component sheet" style="aspect-ratio:auto"><p>Actor baselines, winner appearance, pedestal, stars and confetti require runtime state. This sheet is a lookup aid; no static victory screen is asserted.</p></article>'
    (output/'index.html').write_text(header+nav+'<main><article><h2>Town background</h2><img src="town.png" alt="Decoded town background"><p>Decoded picture11 only. Runtime menu, cash, clock, week, player/marble and doors are not reconstructed here.</p></article>'+''.join(cards)+tail+'</main>',encoding='utf-8')
    report={'evidence':recipes['evidence'],'recipe_sha256':hashlib.sha256(recipes_path.read_bytes()).hexdigest(),'bundle_sha256':recipes['bundle_sha256'],'renderer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'studies':records,'input_export_sha256':used,'limitations':['Not a running-game capture or a full window-manager reconstruction.','Dynamic text/state, priority masks, palette flags, borders, focus, timing and actor coordinates are not reproduced.','Published scripts have not been matched to package bytecode.','No application implementation or adaptation design is included.']}
    (output/'manifest.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f'{len(records)} analytical composites + town and victory component studies: {output / "index.html"}')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--assets',type=Path,default=ROOT/'work/original-assets')
    p.add_argument('--output',type=Path,default=ROOT/'work/original-screen-studies')
    a=p.parse_args();build(a.assets,a.output)
