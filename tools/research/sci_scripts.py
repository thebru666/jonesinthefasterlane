#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""SCI0/SCI1 script structure + disassembly and conservative expression recovery.

Format/VM references: ScummVM 2b5f9b5d95f267c87889746906148db6088130f8,
engines/sci/engine/{script.cpp,object.cpp,kernel_tables.h,vm.cpp,scriptdebug.cpp}.
Recovered listings contain original game code and MUST remain in ignored work/.
This is not a source-level decompiler: local labels/variable names are recovered
only where present in package vocabulary; control flow remains explicit gotos.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

NAMES = '''bnot add sub mul div mod shr shl xor and or neg not eq? ne? gt? ge? lt? le? ugt? uge? ult? ule? bt bnt jmp ldi push pushi toss dup link call callk callb calle ret send INVALID INVALID class INVALID self super rest lea selfID INVALID pprev pToa aTop pTos sTop ipToa dpToa ipTos dpTos lofsa lofss push0 push1 push2 pushSelf line lag lal lat lap lsg lsl lst lsp lagi lali lati lapi lsgi lsli lsti lspi sag sal sat sap ssg ssl sst ssp sagi sali sati sapi ssgi ssli ssti sspi +ag +al +at +ap +sg +sl +st +sp +agi +ali +ati +api +sgi +sli +sti +spi -ag -al -at -ap -sg -sl -st -sp -agi -ali -ati -api -sgi -sli -sti -spi'''.split()
FORMATS = {23:'r',24:'r',25:'r',26:'s',28:'s',31:'v',32:'rb',33:'vb',34:'vb',35:'vsb',37:'b',40:'v',42:'b',43:'vb',44:'s',45:'sv',49:'v',50:'v',51:'v',52:'v',53:'v',54:'v',55:'v',56:'v',57:'s',58:'s',63:'w'}
for _op in range(64,128): FORMATS[_op]='v'
BLOCKS={1:'object',2:'code',3:'synonyms',4:'said',5:'strings',6:'class',7:'exports',8:'relocations',9:'preload',10:'locals'}
def u16(d,p): return struct.unpack_from('<H',d,p)[0]
def signed(n): return n-65536 if n>=32768 else n
def cstr(d,p):
 if not 0<=p<len(d): return None
 return d[p:d.find(b'\0',p) if b'\0' in d[p:] else len(d)].decode('cp437')
def selectors(d):
 n=u16(d,0)+1
 return {i:d[(o:=u16(d,2+2*i))+2:o+2+u16(d,o)].decode('cp437') for i in range(n)}
def instruction(d,p):
 start=p; ext=d[p];op=ext>>1;p+=1
 if NAMES[op]=='INVALID': raise ValueError(f'invalid opcode {ext:02x} at {start:04x}')
 args=[]; targets=[]
 for f in FORMATS.get(op,''):
  width=1 if f=='b' or (f not in 'bw' and ext&1) else 2
  if p+width>len(d):raise ValueError('truncated operand')
  v=int.from_bytes(d[p:p+width],'little',signed=f in 'rs');p+=width;args.append(v)
  if f=='r':targets.append(p+v) # corrected below for relative call with trailing argument byte
 if op in (23,24,25,32): targets=[p+args[0]]
 return {'offset':start,'end':p,'bytes':d[start:p].hex(),'opcode':op,'op':NAMES[op],'args':args,'targets':targets}
def parse_script(d,num,sels):
 result={'number':num,'sha256':hashlib.sha256(d).hexdigest(),'size':len(d),'blocks':[],'objects':[],'exports':[],'locals':[],'instructions':[],'strings':[],'issues':[]};p=0
 while p+2<=len(d):
  t=u16(d,p)
  if not t:break
  if p+4>len(d):raise ValueError('truncated block header')
  n=u16(d,p+2)
  if n<4 or p+n>len(d):raise ValueError(f'bad block {p}:{n}')
  b={'offset':p,'size':n,'type':t,'kind':BLOCKS.get(t,'unknown')};result['blocks'].append(b)
  if t in (1,6):
   assert u16(d,p+4)==0x1234
   count=u16(d,p+10);base=p+12;values=[u16(d,base+2*i) for i in range(count)];mp=base+u16(d,p+8)-2;nm=u16(d,mp)
   obj={'offset':base,'block_offset':p,'kind':BLOCKS[t],'name':cstr(d,values[3]),'species':values[0],'superclass':values[1],'properties':[{'index':i,'offset':i*2,'value':v,'signed_value':signed(v)} for i,v in enumerate(values)],'methods':[{'selector':(s:=u16(d,mp+2+2*i)),'name':sels.get(s,str(s)),'offset':u16(d,mp+4+2*nm+2*i)} for i in range(nm)]}
   if t==6:
    for i,v in enumerate(obj['properties']):v['selector']=u16(d,base+2*count+2*i);v['name']=sels.get(v['selector'],str(v['selector']))
   result['objects'].append(obj)
  elif t==5:
   q=p+4
   while q<p+n:
    z=d.find(b'\0',q,p+n)
    if z<0:break
    if z>q:result['strings'].append({'offset':q,'value':d[q:z].decode('cp437')})
    q=z+1
  elif t==7:result['exports']=[u16(d,p+6+2*i) for i in range(u16(d,p+4))]
  elif t==10:result['locals']=[u16(d,q) for q in range(p+4,p+n,2)]
  elif t==2:
   q=p+4
   while q<p+n:
    # SCI word-aligned code blocks may end with a single zero pad byte.
    if q==p+n-1 and d[q]==0:b['padding_offset']=q;break
    ins=instruction(d,q)
    if ins['end']>p+n:raise ValueError(f'instruction crosses block at {q:04x}')
    result['instructions'].append(ins);q=ins['end']
  p+=n
 for b in result['blocks']:
  if b['type']==2:
   rebuilt=b''.join(bytes.fromhex(i['bytes']) for i in result['instructions'] if b['offset']+4<=i['offset']<b['offset']+b['size'])
   if 'padding_offset'in b:rebuilt+=b'\0'
   if rebuilt!=d[b['offset']+4:b['offset']+b['size']]:raise ValueError('code payload byte reconstruction mismatch')
 return result

def annotate_all(scripts,sels):
 classes={o['species']:o for s in scripts for o in s['objects'] if o['kind']=='class'}
 for s in scripts:
  byoff={o['offset']:o for o in s['objects']};insts={i['offset']:i for i in s['instructions']};starts=set(insts)
  entries={e:f'export_{i}' for i,e in enumerate(s['exports']) if e in starts}
  for o in s['objects']:
   base=o if o['kind']=='class' else classes.get(o['species'])
   if base:
    for p in o['properties']:
     if p['index']<len(base['properties']):
      for k in ('selector','name'):
       if k in base['properties'][p['index']]:p[k]=base['properties'][p['index']][k]
   for m in o['methods']:
    if m['offset'] not in starts:s['issues'].append(f'method target {m["offset"]:04x} is not an instruction')
    entries[m['offset']]=f'{o["name"]}.{m["name"]}'
  for i in s['instructions']:
   op=i['opcode'];a=i['args']
   if op==28 and a and a[0] in sels:i['selector_hint']=sels[a[0]]
   if op in (57,58):
    i['object_target']=(i['end']+a[0])&0xffff;i['object_name']=byoff.get(i['object_target'],{}).get('name')
    if not i['object_name']:i['string_hint']=cstr_from_blocks(s,i['object_target'])
    if not (i['object_target'] in byoff or any(b['type']==5 and b['offset']+4<=i['object_target']<b['offset']+b['size'] for b in s['blocks'])):s['issues'].append(f'unresolved lofs target {i["object_target"]:04x}')
   if op==32 and i['targets'][0] in starts:entries.setdefault(i['targets'][0],f'procedure_{i["targets"][0]:04x}')
   for target in i['targets']:
    if target not in starts:s['issues'].append(f'non-instruction branch/call target {target:04x} from {i["offset"]:04x}')
  # Reachability identifies function membership without assuming all code terminates at first ret.
  s['functions']=[]
  for entry,name in sorted(entries.items()):
   seen=set();pending=[entry]
   while pending:
    p=pending.pop()
    if p in seen or p not in insts:continue
    seen.add(p);i=insts[p];op=i['opcode']
    if op in (23,24,25):pending.extend(i['targets'])
    if op not in (25,36):pending.append(i['end'])
   s['functions'].append({'offset':entry,'name':name,'instruction_offsets':sorted(seen),'instruction_count':len(seen)})
  for o in s['objects']:
   props={p['offset']:p.get('name',str(p['offset'])) for p in o['properties']}
   methodstarts={m['offset'] for m in o['methods']}
   for f in s['functions']:
    if f['offset'] in methodstarts:
     for off in f['instruction_offsets']:
      i=insts[off]
      if 49<=i['opcode']<=56:i['property_hint']=props.get(i['args'][0])
  leaders=set(entries)
  for i in s['instructions']:
   if i['opcode'] in (23,24,25):leaders.update(i['targets']);leaders.add(i['end'])
   if i['opcode']==36:leaders.add(i['end'])
  blocks=[];current=None
  for i in s['instructions']:
   if current is None or i['offset'] in leaders or current['end']!=i['offset']:
    current={'offset':i['offset'],'instructions':[],'end':i['end']};blocks.append(current)
   current['instructions'].append(i['offset']);current['end']=i['end']
  for b in blocks:
   i=insts[b['instructions'][-1]];op=i['opcode'];b['successors']=list(i['targets']) if op in (23,24,25) else []
   if op not in (25,36) and i['end'] in insts:b['successors'].append(i['end'])
  s['basic_blocks']=blocks
  reachable={i for f in s['functions'] for i in f['instruction_offsets']}
  s['code_coverage']={'code_payload_reconstruction_matches':True,'instruction_bytes':sum(i['end']-i['offset'] for i in s['instructions']),'alignment_padding_bytes':sum('padding_offset' in b for b in s['blocks']),'code_payload_bytes':sum(b['size']-4 for b in s['blocks'] if b['type']==2),'reachable_instructions':len(reachable),'not_reached_from_recovered_entries':sorted(set(insts)-reachable)}

def cstr_from_blocks(s,p):
 for text in s['strings']:
  if text['offset']==p:return text['value']
 return None

BINOPS={1:'+',2:'-',3:'*',4:'/',5:'%',6:'>>',7:'<<',8:'^',9:'&',10:'|',13:'==',14:'!=',15:'>',16:'>=',17:'<',18:'<=',19:'u>',20:'u>=',21:'u<',22:'u<='}
def pseudocode(s,sels):
 """Conservative block-local symbolic evaluation. Unknown incoming values remain explicit."""
 insmap={i['offset']:i for i in s['instructions']};out=['// Conservative bytecode-derived pseudocode; labels and unknown values are intentional.', '// Globals/locals retain numeric indexes; message selectors are package vocabulary names.']
 entries={f['offset']:f['name'] for f in s['functions']}
 for b in s['basic_blocks']:
  out.append(f'\nL{b["offset"]:04x}: // '+entries.get(b['offset'],''));stack=[];acc='incoming_acc';previous='incoming_previous_acc';unknown=0
  def pop():
   nonlocal unknown
   if stack:return stack.pop()
   unknown+=1;return f'incoming_stack_{unknown}'
  for off in b['instructions']:
   i=insmap[off];op=i['opcode'];a=i['args'];stmt='';v=a[0] if a else 0
   if op in BINOPS:

    if 13<=op<=22:previous=acc
    acc=f'({pop()} {BINOPS[op]} {acc})'
   elif op in (0,11,12):acc='('+{0:'~',11:'-',12:'!'}[op]+acc+')'
   elif op==26:acc=str(v)
   elif op in (27,):stack.append(acc)
   elif op==28:stack.append(str(v))
   elif op==29:pop()
   elif op==30:x=pop();stack.extend([x,x])
   elif op in (59,60,61):stack.append(str(op-59))
   elif op==62:stack.append('self')
   elif op==46:acc='self'
   elif op in (57,58):
    x=(i.get('object_name') or (repr(i['string_hint']) if i.get('string_hint') else f'address_{i["object_target"]:04x}'))
    if op==57:acc=x
    else:stack.append(x)
   elif 64<=op<=127:
    group=(op-64)//16;slot=(op-64)%16;space=['global','local','temp','param'][slot%4];idx=f'{v}+({acc})' if slot>=8 else str(v);var=f'{space}[{idx}]'
    if group==0:
     value=f'value_{off:04x}';stmt=f'{value} = {var};'
     if slot%8<4:acc=value
     else:stack.append(value)
    elif group==1:
     x=acc if slot%8<4 else pop();stmt=f'{var} = {x};'
    else:
     stmt=f'{var}{"++" if group==2 else "--"};'
     value=f'value_{off:04x}';stmt+=f' {value} = {var};'
     if slot%8<4:acc=value
     else:stack.append(value)
   elif 49<=op<=56:
    var='self.'+i['property_hint'] if i.get('property_hint') else f'property[{v}]'
    if op==49:
     acc=f'value_{off:04x}';stmt=f'{acc} = {var};'
    elif op==50:stmt=f'{var} = {acc};'
    elif op==51:
     value=f'value_{off:04x}';stmt=f'{value} = {var};';stack.append(value)
    elif op==52:stmt=f'{var} = {pop()};'
    else:
     stmt=f'{var}{"++" if op in (53,55) else "--"};'
     value=f'value_{off:04x}';stmt+=f' {value} = {var};'
     if op in (53,54):acc=value
     else:stack.append(value)
   elif op in (23,24):stmt=f'if ({"!" if op==24 else ""}({acc})) goto L{i["targets"][0]:04x};'
   elif op==25:stmt=f'goto L{i["targets"][0]:04x};'
   elif op==36:stmt=f'return {acc};'
   elif op in (32,33,34,35):
    n=a[-1]//2;args=[pop() for _ in range(n)][::-1];argc=pop();target=(f'procedure_{i["targets"][0]:04x}' if op==32 else f'kernel_{v}' if op==33 else f'export0_{v}' if op==34 else f'export_{v}_{a[1]}');call=f'{target}({", ".join(args)})';acc=f'result_{off:04x}';stmt=f'{acc} = {call}; // argc={argc}'
   elif op in (37,42,43):
    words=a[-1]//2;items=[pop() for _ in range(words)][::-1];messages=[];q=0
    while q+1<len(items):
     sel=items[q];count=items[q+1]
     if not count.lstrip('-').isdigit():break
     count=int(count)
     if count<0 or q+2+count>len(items):break
     name=sels.get(int(sel),sel) if sel.lstrip('-').isdigit() else sel
     messages.append(f'{name}({", ".join(items[q+2:q+2+count])})');q+=2+count
    target=acc if op==37 else 'self' if op==42 else f'superclass_{v}'
    call=f'{target}.{{'+'; '.join(messages)+'}' if q==len(items) else f'send({target}, [{", ".join(items)}])'
    acc=f'result_{off:04x}';stmt=f'{acc} = {call};'
   elif op==40:acc=f'class_{v}'
   elif op==31:stmt=f'// allocate {v} temporary slots'
   elif op==44:stmt=f'// forward rest arguments from param[{v}] (dynamic stack effect not resolved)';stack.append('REST_ARGUMENTS')
   elif op==48:stack.append(previous)
   elif op==45:acc=f'address_of_variable({a})'
   elif op==63:stmt=f'// source line {v}'
   else:stmt=f'// unsupported symbolic operation {i["op"]} {a}'
   if stmt:out.append(f'  /* {off:04x} */ {stmt}')
  if stack:out.append('  // outgoing stack: '+', '.join(stack))
  out.append('  // outgoing acc: '+acc)
 return '\n'.join(out)+'\n'

def self_test():
 # Width, signed displacements, call PC base (after frame size), absolute operand encoding.
 assert len(NAMES)==128
 assert instruction(bytes.fromhex('2ffb'),0)['targets']==[-3] # bt -5 from PC2
 assert instruction(bytes.fromhex('300100'),0)['targets']==[4] # bnt +1 from PC3
 assert instruction(bytes.fromhex('40fcff04'),0)['targets']==[0] # call -4 from PC4
 assert instruction(bytes.fromhex('431204'),0)['args']==[18,4] # short kernel ID + fixed byte frame
 assert instruction(bytes.fromhex('42ff0008'),0)['args']==[255,8] # wide kernel ID + same fixed frame
 assert instruction(bytes.fromhex('35ff'),0)['args']==[-1]
 assert instruction(bytes.fromhex('72faff'),0)['args']==[-6] # relative lofs, signed16
 assert instruction(bytes.fromhex('7e3412'),0)['args']==[0x1234] # fixed16 source line
 try:instruction(bytes.fromhex('4c'),0)
 except ValueError:pass
 else:raise AssertionError('invalid opcode accepted')
 # Complete synthetic class block: class/object pointer +12, property selectors,
 # method count, selector IDs, zero terminator, code offsets.
 d=struct.pack('<HHHHHH',6,36,0x1234,0,18,4)+struct.pack('<4H',9,0,0x8000,0)+struct.pack('<4H',0,1,2,23)+struct.pack('<4H',1,60,0,40)+struct.pack('<HH',2,8)+bytes.fromhex('350148')+b'\0'
 got=parse_script(d,999,{60:'doit',23:'name'})
 assert got['objects'][0]['offset']==12
 assert got['objects'][0]['properties'][3]['selector']==23
 assert got['objects'][0]['methods']==[{'selector':60,'name':'doit','offset':40}]
 assert got['instructions'][0]['offset']==40
 # Reads must snapshot values: a stored accumulator can be used again after
 # the source slot has changed. Substituting a live variable would recalculate it.
 def symbolic_fixture(hexcode):
  data=bytes.fromhex(hexcode);instructions=[];pos=0
  while pos<len(data):
   inst=instruction(data,pos);instructions.append(inst);pos=inst['end']
  sample={'instructions':instructions,'functions':[], 'basic_blocks':[{'offset':0,'instructions':[i['offset'] for i in instructions]}]}
  return pseudocode(sample,{})
 text=symbolic_fixture('850036350504a500a50148')
 assert 'value_0000 = temp[0];' in text
 assert 'temp[0] = (value_0000 - 5);' in text
 assert 'temp[1] = (value_0000 - 5);' in text
 text=symbolic_fixture('67083501650848') # property stack read followed by write
 assert 'value_0000 = property[8];' in text
 assert 'outgoing stack: value_0000' in text
 text=symbolic_fixture('c100a50148') # increment global slot then store stable result
 assert 'global[0]++; value_0000 = global[0];' in text
 assert 'temp[1] = value_0000;' in text
 text=symbolic_fixture('3502910548') # indexed global read snapshots its index
 assert 'value_0002 = global[5+(2)];' in text
 return {'fixtures':14,'status':'passed'}

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--resources',type=Path,default=Path('work/original-assets/decoded/resources'));ap.add_argument('--output',type=Path,default=Path('work/bytecode/decoded'));ap.add_argument('--coverage',type=Path);ap.add_argument('--self-test',action='store_true');args=ap.parse_args()
 if args.self_test:print(json.dumps(self_test()));return 0
 root=Path(__file__).resolve().parents[2];out=args.output.resolve()
 if not any(out.is_relative_to(root/p) for p in ('work','artifacts/private')):ap.error('Original-code outputs must be under ignored work/ or artifacts/private/')
 lock=json.loads((root/'artifacts/original-game/decoded-asset-summary.json').read_text())
 expected={int(r['number']):r['sha256'] for r in lock['resources'] if r['type']=='script'}
 inputs={int(p.name.split('.')[1]):hashlib.sha256(p.read_bytes()).hexdigest() for p in args.resources.glob('script.*.bin')}
 if inputs!=expected:ap.error('Script inputs differ from locked website asset hashes; rebuild the original catalogue first')
 selector_file=args.resources/'vocabulary.997.bin'
 if hashlib.sha256(selector_file.read_bytes()).hexdigest()!='1adc0a33a4c7e79022b0c936b0613dcc89deb2a9ffe84f3e4539afec86601850':ap.error('Selector vocabulary hash mismatch')
 out.mkdir(parents=True,exist_ok=True);sels=selectors((args.resources/'vocabulary.997.bin').read_bytes());scripts=[];failures=[]
 for path in sorted(args.resources.glob('script.*.bin')):
  num=int(path.name.split('.')[1])
  try:scripts.append(parse_script(path.read_bytes(),num,sels))
  except (ValueError,struct.error,IndexError,AssertionError) as e:failures.append({'script':num,'error':str(e)})
 annotate_all(scripts,sels)
 (out/'selectors.json').write_text(json.dumps(sels,indent=2)+'\n')
 for s in scripts:
  stem=out/f'script-{s["number"]:03d}';stem.with_suffix('.json').write_text(json.dumps(s,indent=2)+'\n');labels={f['offset']:f['name'] for f in s['functions']};lines=[f'; script {s["number"]} sha256 {s["sha256"]}']
  for o in s['objects']:lines.append('; object '+json.dumps(o))
  for i in s['instructions']:
   if i['offset'] in labels:lines.append('\n'+labels[i['offset']]+':')
   hint=((' selector?='+i['selector_hint']) if 'selector_hint'in i else '')+((' object='+i['object_name']) if i.get('object_name') else '')
   lines.append(f'{i["offset"]:04x}: {i["bytes"]:18} {i["op"]:8} '+', '.join(str(a) for a in i['args'])+(' -> '+','.join(f'{t:04x}' for t in i['targets']) if i['targets'] else '')+hint)
  stem.with_suffix('.asm').write_text('\n'.join(lines)+'\n');stem.with_suffix('.pseudo.txt').write_text(pseudocode(s,sels))
 coverage={'schema':1,'source':lock['coverage']['source'],'selector_vocabulary_sha256':hashlib.sha256(selector_file.read_bytes()).hexdigest(),'tool_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'fixture_validation':self_test(), 'code_payload_bytes':sum(s['code_coverage']['code_payload_bytes'] for s in scripts),'instruction_bytes':sum(s['code_coverage']['instruction_bytes'] for s in scripts),'alignment_padding_bytes':sum(s['code_coverage']['alignment_padding_bytes'] for s in scripts),'instructions_not_reached_from_recovered_entries':sum(len(s['code_coverage']['not_reached_from_recovered_entries']) for s in scripts),'pseudocode_unknown_stack_references':sum(stem.read_text().count('incoming_stack_') for stem in out.glob('script-*.pseudo.txt')),'pseudocode_dynamic_rest_operations':sum(stem.read_text().count('dynamic stack effect not resolved') for stem in out.glob('script-*.pseudo.txt')),'evidence':'direct decoded website script bytes; no published decompiled source used as input','scummvm_commit':'2b5f9b5d95f267c87889746906148db6088130f8','script_count':len(scripts),'failures':failures,'instruction_count':sum(len(s['instructions']) for s in scripts),'object_count':sum(len(s['objects']) for s in scripts),'method_count':sum(len(o['methods']) for s in scripts for o in s['objects']),'function_count':sum(len(s['functions']) for s in scripts),'basic_block_count':sum(len(s['basic_blocks']) for s in scripts),'selectors':len(sels),'scripts':[{'number':s['number'],'sha256':s['sha256'],'size':s['size'],'instructions':len(s['instructions']),'objects':len(s['objects']),'methods':sum(len(o['methods']) for o in s['objects']),'functions':len(s['functions']),'code_coverage':s['code_coverage'],'issues':s['issues']} for s in scripts],'limits':['Disassembly and conservative block-local expression recovery; not complete structured source decompilation.','Stack values across basic-block joins remain explicit unknowns.','Dynamic rest arguments and runtime-dependent message targets require manual interpretation.','Numeric globals, locals and kernel IDs are not assigned speculative original names.','Instructions outside recovered entry-point reachability are listed; this does not prove they are dead code.', 'Arithmetic expressions retain SCI VM operations; execute with original 16-bit semantics, not Python or JavaScript arithmetic.', 'Signed PC-relative lofsa/lofss format confirmed by object and string target alignment for this bundle.']}
 (out/'coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')
 if args.coverage:args.coverage.write_text(json.dumps(coverage,indent=2)+'\n')
 print(json.dumps({k:v for k,v in coverage.items() if k!='scripts'},indent=2));return bool(failures or any(s['issues'] for s in scripts))
if __name__=='__main__':raise SystemExit(main())
