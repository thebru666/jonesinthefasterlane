#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Extract early SCI1 Jones resources; decode VGA views, fonts, cursors and text.

Format/algorithm reference: ScummVM (GPL-3.0-or-later), revision
2b5f9b5d95f267c87889746906148db6088130f8, engines/sci/resource/
decompressor.cpp and engines/sci/graphics/{view,cursor,scifont,palette16}.cpp.
This is a narrow reference exporter, not a general SCI implementation.
"""
import argparse, hashlib, json, struct
from pathlib import Path

TYPES = ['view','picture','script','text','sound','memory','vocabulary','font','cursor','patch','bitmap','palette','cdaudio','audio','sync','message','map','heap']
def u16(b,p): return struct.unpack_from('<H', b,p)[0]
class Bits:
    def __init__(self,b): self.b=b; self.p=0
    def get(self,n):
        v=0
        for _ in range(n):
            v=(v<<1)|((self.b[self.p//8]>>(7-self.p%8))&1); self.p+=1
        return v

def decompress(b,method,size):
    if method==0: out=b
    elif method==1:
        n=b[0]; end=b[1]|256; nodes=b[2:2+n*2]; bits=Bits(b[2+n*2:]); out=bytearray()
        while len(out)<size:
            p=0
            while nodes[p+1]:
                if bits.get(1):
                    step=nodes[p+1]&15
                    if not step: c=bits.get(8)|256; break
                else: step=nodes[p+1]>>4
                p+=step*2
            else: c=nodes[p]
            if c==end: break
            out.append(c&255)
    elif method==2:
        bits=Bits(b); out=bytearray(); offsets=[0]*4096; lengths=[0]*4096; width=9; count=258; limit=511
        while len(out)<size:
            c=bits.get(width)
            if c==257: break
            if c==256: width=9; count=258; limit=511; continue
            if c>=count: raise ValueError(f'bad LZW code {c}/{count}')
            start=len(out)
            if c<256: out.append(c)
            else:
                for i in range(lengths[c]):
                    if len(out)>=size: break
                    out.append(out[offsets[c]+i])
            if count>=4096: continue
            if count==limit and width<12: width+=1; limit=(1<<width)-1
            offsets[count]=start; lengths[count]=len(out)-start+1; count+=1
    else: raise ValueError(f'unsupported compression {method}')
    if len(out)!=size: raise ValueError(f'decompressed length {len(out)} != {size}')
    return bytes(out)

def extract(game,out):
    raw=out/'resources'; raw.mkdir(parents=True,exist_ok=True)
    seen={}; terminated=False
    m=(game/'resource.map').read_bytes(); vols={}; entries=[]
    for p in range(0,len(m)-5,6):
        rid,loc=struct.unpack_from('<HI',m,p)
        if loc==0xffffffff: terminated=True; break
        typ=rid>>11; num=rid&2047; vol=loc>>26; off=loc&0x3ffffff
        if vol not in vols: vols[vol]=(game/f'resource.{vol:03}').read_bytes()
        b=vols[vol]; header,packed,size,method=struct.unpack_from('<HHHH',b,off)
        if header!=rid: raise ValueError('map/header mismatch')
        payload=decompress(b[off+8:off+8+packed-4],method,size)
        name=TYPES[typ] if typ<len(TYPES) else f'type{typ}'
        dest=raw/f'{name}.{num:03}.bin'
        if dest in seen and seen[dest]!=payload: raise ValueError(f'conflicting duplicate {dest.name}')
        seen[dest]=payload; dest.write_bytes(payload)
        entries.append(dict(type=name,number=num,volume=vol,offset=off,packed_bytes=packed-4,unpacked_bytes=size,compression=method,sha256=hashlib.sha256(payload).hexdigest(),raw_file=str(dest.relative_to(out))))
    if not terminated: raise ValueError('resource map has no terminator')
    return entries

def parse_palette(data, offset=0):
    b=data[offset:]; palette=[(0,0,0)]*256
    if b[:2]==b'\x00\x01' or (b[:2]==b'\x00\x00' and u16(b,29)==0):
        start,count,pos,variable=0,256,260,True
    else: start,count,pos,variable=b[25],u16(b,29),37,b[32]!=1
    for i in range(start,start+count):
        if variable: pos+=1
        palette[i]=tuple(b[pos:pos+3]); pos+=3
        if len(palette[i])!=3: raise ValueError('truncated palette')
    return palette

def unpack_vga(data, offset, width, height, transparent):
    pixels=bytearray([transparent])*(width*height); p=offset; dest=0
    while dest<len(pixels):
        op=data[p];p+=1; n=op&63
        if op<128:
            n=op; values=data[p:p+n];p+=n
        elif op<192:
            values=bytes([data[p]])*n;p+=1
        else: values=bytes([transparent])*n
        if not n: raise ValueError('zero-length RLE operation')
        if len(values)!=n: raise ValueError('truncated RLE data')
        count=min(n,len(pixels)-dest)
        pixels[dest:dest+count]=values[:count];dest+=n
    return bytes(pixels),p

def indexed_image(pixels,width,height,palette,transparent=None):
    from PIL import Image
    im=Image.frombytes('P',(width,height),bytes(pixels));im.putpalette([v for rgb in palette for v in rgb])
    if transparent is not None: im.info['transparency']=transparent
    return im

def decode_assets(out,entries):
    from PIL import Image, ImageDraw
    raw=out/'resources'; images=out/'images'; images.mkdir(exist_ok=True)
    palette=parse_palette((raw/'palette.999.bin').read_bytes())
    unique={}
    for entry in entries:
        key=entry['raw_file']
        if key in unique:
            entry['duplicate_of']=key
            entry['status']='identical-duplicate'
            if unique[key]['sha256']!=entry['sha256']: raise ValueError('conflicting duplicate resource')
            continue
        unique[key]=entry
        b=(out/key).read_bytes(); typ=entry['type']; num=entry['number']; exports=[]
        entry['status']='decompressed'
        if typ=='view':
            nloops=b[0]; mirrored=u16(b,2); paloff=u16(b,6)
            pal=parse_palette(b,paloff) if paloff and paloff!=256 else palette
            cels=[]; thumbnails=[]
            for loop in range(nloops):
                lo=u16(b,8+loop*2)
                for cel in range(u16(b,lo)):
                    co=u16(b,lo+4+cel*2); w,h=u16(b,co),u16(b,co+2); clear=b[co+6]
                    if not w or not h: continue
                    pixels=b[co+8:co+8+w*h] if b[1]&64 else unpack_vga(b,co+8,w,h,clear)[0]
                    im=indexed_image(pixels,w,h,pal,clear).convert('RGBA')
                    if mirrored&(1<<loop): im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                    path=f'images/view-{num:03}-loop-{loop:02}-cel-{cel:02}.png';im.save(out/path);exports.append(path)
                    cels.append(dict(loop=loop,cel=cel,width=w,height=h,transparent_index=clear,mirrored=bool(mirrored&(1<<loop)),displacement_x=struct.unpack_from('b',b,co+4)[0]*(-1 if mirrored&(1<<loop) else 1),displacement_y=b[co+5],file=path))
                    thumbnails.append((im,f'{loop}:{cel}'))
            entry.update(loop_count=nloops,cel_count=len(cels),cels=cels,palette='embedded' if paloff and paloff!=256 else 'palette.999')
            # Native-pixel contact sheet: keep each frame at original size.
            tw=max([im.width for im,_ in thumbnails]+[1])+12;th=max([im.height for im,_ in thumbnails]+[1])+24;cols=min(8,len(thumbnails))
            sheet=Image.new('RGB',(max(cols,1)*tw,((len(thumbnails)+max(cols,1)-1)//max(cols,1))*th),(48,48,48));draw=ImageDraw.Draw(sheet)
            for i,(im,label) in enumerate(thumbnails):
                x=(i%cols)*tw;y=(i//cols)*th;sheet.paste(im,(x+6,y+20),im);draw.text((x+6,y+3),label,fill='white')
            path=f'images/view-{num:03}-sheet.png';sheet.save(out/path);exports.append(path);entry['contact_sheet']=path
        elif typ=='font':
            n=u16(b,2); line=u16(b,4);glyphs=[]
            for c in range(n):
                off=u16(b,6+c*2);w,h=b[off],b[off+1];stride=(w+7)//8;pixels=[]
                for y in range(h):
                    for x in range(w): pixels.append(255 if b[off+2+y*stride+x//8]&(128>>(x%8)) else 0)
                glyphs.append((c,w,h,pixels))
            cw=max(x[1] for x in glyphs)+8;ch=max(x[2] for x in glyphs)+20;sheet=Image.new('RGB',(16*cw,((n+15)//16)*ch),(32,32,32));d=ImageDraw.Draw(sheet)
            for c,w,h,pixels in glyphs:
                x=(c%16)*cw;y=(c//16)*ch;d.text((x,y),f'{c:02X}',fill=(150,150,150))
                if w and h: sheet.paste(Image.frombytes('L',(w,h),bytes(pixels)),(x,y+15))
            path=f'images/font-{num:03}-sheet.png';sheet.save(out/path);exports.append(path);entry.update(glyph_count=n,line_height=line,contact_sheet=path)
        elif typ=='cursor':
            im=Image.new('RGBA',(16,16));colors=[(0,0,0,255),(255,255,255,255),(0,0,0,0),(170,170,170,255)]
            for y in range(16):
                aa,bb=u16(b,4+y*2),u16(b,36+y*2)
                for x in range(16): im.putpixel((x,y),colors[(((aa>>(15-x))&1)<<1)|((bb>>(15-x))&1)])
            path=f'images/cursor-{num:03}.png';im.save(out/path);exports.append(path);entry.update(hotspot=[u16(b,0),u16(b,2)])
        elif typ=='palette':
            pal=parse_palette(b);im=Image.new('RGB',(256,256));d=ImageDraw.Draw(im)
            for i,color in enumerate(pal): d.rectangle(((i%16)*16,(i//16)*16,(i%16)*16+15,(i//16)*16+15),fill=color)
            path=f'images/palette-{num:03}.png';im.save(out/path);exports.append(path)
        elif typ=='text':
            folder=out/'text';folder.mkdir(exist_ok=True);strings=b.split(b'\0')
            if strings and strings[-1]==b'':strings.pop()
            path=f'text/text-{num:03}.json';(out/path).write_text(json.dumps([dict(index=i,text=s.decode('cp437')) for i,s in enumerate(strings)],ensure_ascii=False,indent=2)+'\n');exports.append(path);entry['string_count']=len(strings)
        if exports: entry['exports']=exports; entry['status']='decoded'
    return entries

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('game_dir',type=Path);p.add_argument('output_dir',type=Path);p.add_argument('--raw-only',action='store_true');a=p.parse_args()
    entries=extract(a.game_dir,a.output_dir)
    if not a.raw_only: decode_assets(a.output_dir,entries)
    (a.output_dir/'manifest.json').write_text(json.dumps({'resources':entries},indent=2)+'\n')
    print(f'Extracted {len(entries)} resource entries')
