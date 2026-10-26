from pathlib import Path
import argparse
import bz2
import hashlib
import json
import struct
import zlib

BASE = 0x10000000
FAMILY = 0xe48bff56
FLASH_SIZE = 0x1000000
CONFIG = 0x4a000
SCRIPT = 0x4a100
SYSTEM = 0x52000
STORAGE = 0x3e0000
COLLECTION = 0x400000

def read_uf2(path):
    data = path.read_bytes()
    assert len(data) % 512 == 0, 'Truncated UF2'
    blocks = {}
    count = len(data)//512
    for i in range(count):
        block = data[i*512:(i+1)*512]
        m0,m1,flags,address,size,index,total,family = struct.unpack_from('<8I', block)
        assert (m0,m1,struct.unpack_from('<I',block,508)[0]) == (0x0a324655,0x9e5d5157,0x0ab16f30)
        assert flags == 0x2000 and family == FAMILY and size == 256
        assert index == i and total == count
        assert address % 256 == 0 and BASE <= address <= BASE+FLASH_SIZE-256
        offset = address-BASE
        assert offset not in blocks, 'Duplicate flash block'
        blocks[offset] = block[32:288]
    return blocks

def materialize(blocks):
    flash = bytearray(b'\xff'*FLASH_SIZE)
    for offset, payload in blocks.items():
        flash[offset:offset+256] = payload
    return flash

def bytecode_length(script):
    assert script[:4] == b'JSS4'
    offset = struct.unpack_from('<H',script,4)[0]
    count = struct.unpack_from('<H',script,offset)[0]
    return offset+2+2*count

def validate_script(script):
    assert len(script) == bytecode_length(script) <= SYSTEM-SCRIPT
    roots=struct.unpack_from('<64H',script,6)
    hash_offset=struct.unpack_from('<H',script,4)[0]
    assert roots[0]>=134 and all(0<=offset<hash_offset for offset in roots)
    assert all(roots[2+2*i] for i in range(31)), 'Missing physical press handler'

def validate_data(flash):
    assert flash[CONFIG:CONFIG+5] == bytes([0,0,0,1,0])
    assert flash[CONFIG+32] in (0,1), 'Unexpected top S mapping'
    assert flash[CONFIG+33] == 1, 'Lower S must map to left S'
    assert flash[CONFIG+32+26:CONFIG+32+28] == b'\0\0'
    magic,count,reverse,_ = struct.unpack_from('<IHBB',flash,COLLECTION)
    assert magic == 0x3443534a and count == 12 and reverse == 1
    textsize,textptr = struct.unpack_from('<II',flash,COLLECTION+8)
    timestamp = struct.unpack_from('<I',flash,COLLECTION+32)[0]
    assert timestamp == struct.unpack_from('<I',flash,textptr-BASE+textsize)[0]
    names=[]
    expected=[('emily-symbols',1),('abby-left-hand-modifiers.json',1),('emily-modifiers.json',1),
              ('jeff-phrasing',1),('jeff-numbers',0),('lapwing-javelin-additions.json',1),
              ('lapwing-semi-modal-movement.json',0),('lapwing-commands.json',1),
              ('lapwing-numbers.json',1),('lapwing-uk-additions.json',1),
              ('lapwing-proper-nouns.json',1),('lapwing-base.json',1)]
    for i in range(count):
        pointer=struct.unpack_from('<I',flash,COLLECTION+36+i*4)[0]-BASE
        enabled,maximum,kind,options=struct.unpack_from('<4B',flash,pointer)
        if kind in (0,1):
            n=struct.unpack_from('<I',flash,pointer+4)[0]-BASE
            name=flash[n:flash.index(b'\0',n)].decode()
        else: name={3:'jeff-numbers',4:'jeff-phrasing',5:'emily-symbols'}[kind]
        names.append((name,enabled))
    assert names == expected
    return names

def package(builder, hardware, script_path, source_path, output, top_s_as_s=False):
    blocks=read_uf2(builder)
    flash=materialize(blocks)
    validate_data(flash)
    binary=hardware.read_bytes()
    assert 256 < len(binary) <= CONFIG
    stack,entry=struct.unpack_from('<II',binary,256)
    assert 0x20000000 <= stack <= 0x20042000
    assert BASE+256 <= (entry&~1) < BASE+len(binary) and entry&1
    code=script_path.read_bytes()
    validate_script(code)
    source=source_path.read_text(encoding='utf8').replace('\r\n','\n')
    stored=b'\0'+bz2.compress(source.encode('utf8'))
    storage_size=len(stored)
    def replace(start,stop,payload):
        assert len(payload) <= stop-start and start%256 == stop%256 == 0
        region=payload+b'\xff'*(stop-start-len(payload))
        for offset in range(start,stop,256): blocks[offset]=region[offset-start:offset-start+256]
    config_page=bytearray(flash[CONFIG:SCRIPT])
    config_page[32]=1 if top_s_as_s else 0
    replace(CONFIG,SCRIPT,config_page)
    replace(0,CONFIG,binary)
    replace(SCRIPT,SYSTEM,code)
    # Store the supplied raw JSS in the official type-0/bzip2 format.
    storage=struct.pack('<II',zlib.crc32(code),storage_size)+stored
    replace(STORAGE,COLLECTION,storage)
    final=materialize(blocks)
    validate_data(final)
    assert final[SYSTEM:STORAGE] == flash[SYSTEM:STORAGE]
    assert final[COLLECTION:] == flash[COLLECTION:]
    assert final[CONFIG:SCRIPT] == config_page
    result=bytearray()
    for index,(offset,payload) in enumerate(sorted(blocks.items())):
        block=struct.pack('<8I',0x0a324655,0x9e5d5157,0x2000,BASE+offset,256,index,len(blocks),FAMILY)
        result += block+payload+bytes(220)+struct.pack('<I',0x0ab16f30)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_bytes(result)
    assert materialize(read_uf2(output)) == final
    digest=hashlib.sha256(result).hexdigest()
    output.with_suffix('.sha256').write_text(f'{digest}  {output.name}\n')
    report={'file':output.name,'bytes':len(result),'sha256':digest,'hardware_bytes':len(binary),
            'script_bytes':len(code),'dictionaries':validate_data(final),'flashed':False}
    print(json.dumps(report,indent=2))
    return report

if __name__ == '__main__':
    p=argparse.ArgumentParser(description='Combine a matching Javelin data image with Steno V3 hardware and a validated 31-button script. Does not flash.')
    p.add_argument('--builder',required=True,type=Path)
    p.add_argument('--hardware',required=True,type=Path)
    p.add_argument('--script',required=True,type=Path)
    p.add_argument('--source',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--top-s-as-s',action='store_true',help='Map the upper S to S; omit for layout v1 top-number behavior')
    a=p.parse_args()
    package(a.builder,a.hardware,a.script,a.source,a.output,a.top_s_as_s)
