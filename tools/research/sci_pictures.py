#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Narrow SCI1 VGA picture exporter for the checksum-pinned Jones reference.

Adapted from ScummVM's picture.cpp/screen.cpp algorithms, revision
2b5f9b5d95f267c87889746906148db6088130f8. See THIRD_PARTY.md and COPYING.
Exports picture planes, not composite running-game screenshots.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
from sci_resources import u16, parse_palette, unpack_vga, indexed_image


def render_picture(data):
    w, h = 320, 200
    planes = [bytearray([255]) * (w*h), bytearray(w*h), bytearray(w*h)]
    colors = [255, 255, 255]
    palette = [(i, i, i) for i in range(256)]
    p = 0
    commands = Counter()
    embedded = []

    def absolute():
        nonlocal p
        v, x, y = data[p:p+3]; p += 3
        return x + ((v & 240) << 4), y + ((v & 15) << 8)

    def relative(x, y, medium=False):
        nonlocal p
        v = data[p]; p += 1
        if medium:
            y += -(v & 127) if v & 128 else v
            v = data[p]; p += 1
            x += -(128-(v & 127)) if v & 128 else v
        else:
            x += -((v >> 4) & 7) if v & 128 else v >> 4
            y += -(v & 7) if v & 8 else v & 7
        return x, y

    def put(x, y, use=None):
        if 0 <= x < w and 0 <= y < h:
            for i in (range(3) if use is None else use):
                if colors[i] != 255:
                    planes[i][y*w+x] = colors[i]

    def line(a, b):
        x, y = max(0,min(w-1,a[0])), max(0,min(h-1,a[1]))
        endx, endy = max(0,min(w-1,b[0])), max(0,min(h-1,b[1]))
        dy, dx = endy-y, endx-x
        sy, sx = (-1 if dy<0 else 1), (-1 if dx<0 else 1)
        dy, dx = abs(dy)*2, abs(dx)*2
        put(x,y); put(endx,endy)
        if dx > dy:
            f = dy-(dx//2)
            while x != endx:
                if f >= 0: y += sy; f -= dx
                x += sx; f += dy; put(x,y)
        else:
            f = dx-(dy//2)
            while y != endy:
                if f >= 0: x += sx; f -= dy
                y += sy; f += dx; put(x,y)

    def fill(x, y):
        if not (0 <= x < w and 0 <= y < h): return
        active = [i for i in range(3) if colors[i] != 255]
        if not active: return
        match = active[0]; search = planes[match][y*w+x]
        empty = 255 if match == 0 else 0
        if search != empty or colors[match] == empty: return
        active = [i for i in active if planes[i][y*w+x] != colors[i]]
        stack = [(x,y)]
        while stack:
            x,y = stack.pop()
            if planes[match][y*w+x] != search: continue
            left = right = x
            while left>0 and planes[match][y*w+left-1] == search: left -= 1
            while right<w-1 and planes[match][y*w+right+1] == search: right += 1
            for xx in range(left,right+1): put(xx,y,active)
            for yy in [y-1,y+1]:
                if not 0 <= yy < h: continue
                run = False
                for xx in range(left,right+1):
                    found = planes[match][yy*w+xx] == search
                    if found and not run: stack.append((xx,yy))
                    run = found

    terminated = False
    while p < len(data):
        op = data[p]; p += 1; commands[f'{op:02x}'] += 1
        if op in (0xf0,0xf2,0xfb):
            i = {0xf0:0,0xf2:1,0xfb:2}[op]
            colors[i] = data[p] if i == 0 else data[p]&15; p += 1
        elif op in (0xf1,0xf3,0xfc): colors[{0xf1:0,0xf3:1,0xfc:2}[op]] = 255
        elif op in (0xf5,0xf6,0xf7):
            point = absolute()
            while p < len(data) and data[p] < 0xf0:
                nxt = absolute() if op == 0xf6 else relative(*point,medium=op==0xf5)
                line(point,nxt); point=nxt
        elif op == 0xf8:
            while p < len(data) and data[p] < 0xf0: fill(*absolute())
        elif op == 0xfe:
            sub = data[p]; p += 1; commands[f'fe-{sub:02x}'] += 1
            if sub == 2:
                palette = parse_palette(data,p); p += 1284
            elif sub == 1:
                x,y = absolute(); size = u16(data,p); p += 2
                width,height = u16(data,p),u16(data,p+2); clear = data[p+6]
                if p+size > len(data): raise ValueError('embedded cel exceeds picture')
                pixels,end = unpack_vga(data,p+8,width,height,clear)
                if end > p+size: raise ValueError('embedded RLE exceeds declared block')
                for yy in range(height):
                    for xx in range(width):
                        if 0 <= x+xx < w and 0 <= y+yy < h:
                            color = pixels[yy*width+xx]
                            if color != 255:
                                planes[0][(y+yy)*w+x+xx] = color
                                planes[1][(y+yy)*w+x+xx] = 0
                embedded.append(dict(x=x,y=y,width=width,height=height,clear_index=clear))
                p += size
            elif sub == 3: p += 4
            elif sub == 4: p += 14
            elif sub == 0:
                while p<len(data) and data[p]<0xf0: p += 1
            else: raise ValueError(f'unsupported VGA extended opcode {sub:02x}')
        elif op == 0xff: terminated=True; break
        else: raise ValueError(f'unsupported picture opcode {op:02x} at {p-1}')
    if not terminated: raise ValueError('picture missing terminator')
    return planes,palette,dict(commands),embedded


def export_pictures(raw_dir, output_dir):
    output_dir = Path(output_dir); dest = output_dir/'pictures'; dest.mkdir(parents=True,exist_ok=True)
    records = []
    for source in sorted(Path(raw_dir).glob('picture.*.bin')):
        number = int(source.name.split('.')[1])
        record = dict(type='picture',number=number,exports=[])
        try:
            planes,palette,commands,embedded = render_picture(source.read_bytes())
            for name, pixels in zip(['visual','priority','control'],planes):
                pal = palette if name=='visual' else [(i*17,i*17,i*17) if i<16 else (0,0,0) for i in range(256)]
                file = dest/f'picture-{number:03}-{name}.png'
                indexed_image(pixels,320,200,pal).save(file)
                record['exports'].append(file.relative_to(output_dir).as_posix())
            record.update(status='rendered',width=320,height=200,commands=commands,embedded_cels=embedded,palette_source='embedded picture palette',limitations=['Picture planes only; no runtime view/text/menu composition or palette animation.'])
        except Exception as error:
            record.update(status='failed',error=str(error))
        records.append(record)
    return records


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('raw_dir',type=Path); parser.add_argument('output_dir',type=Path)
    args=parser.parse_args(); records=export_pictures(args.raw_dir,args.output_dir)
    (args.output_dir/'picture-manifest.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps([{k:r.get(k) for k in ['number','status','error']} for r in records]))
    raise SystemExit(any(r['status']=='failed' for r in records))
