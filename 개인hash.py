# 오류 있음.. 먼지는 잘 모르겠음.
from hashlib import sha256 as sha
import codecs


isLittleEndian = True # x86계열 CPU를 리트 - 엔디안(little-end)


#little-endian big-denian 변경

def transEndian(bits) :
    decode_hex = codecs.getdecoder('hex_codec')
    binn = decode_hex(bits)[0]
    ret = codecs.encode(binn[::-1],'hex_codec')
    
    return ret.decode()

def getTarget(bits):
    if isLittleEndian :
        bits = transEndian(bits)
        
    print('Bits = Ox' +bits)
    
    bit1 = 'Ox'+bits[:2]
    bit2 = 'Ox'+bits[2:]
    
    sft = (int(bit1, 16)-3)*8
    base = int(bit2,16)
    
    ret = base << sft 
    target = hex(ret)
    
    print('Target = ', target)    

    
Bits = 'f29441a'
getTarget(Bits)



