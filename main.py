import struct
from config import Config
from opcodes import opcodes, opcodesR

typeBases = {
    'Address': -270000000,
    'Float': -240000000,
    'UF': -210000000,
    'UW': -190000000,
    'GSW': -170000000,
    'LSW': -150000000,
    'GSWF': -130000000,
    'LSWF': -110000000,
    'GF': -90000000,
    'LF': -70000000,
    'GW': -50000000,
    'LW': -30000000
}

config = Config.getStaticInstance()
output = bytearray()
linenum = 0
infile = open(config.inPath)
for line in infile.readlines():
    linenum += 1

    if line[0] == '8': # Remove address labels
        line = line[10:]
    line = line.split("#")[0].strip() # Remove comments
    if len(line) == 0:
        continue

    split = line.split()
    opname = split.pop(0).lower()
    assert opname in opcodesR, f"Unrecognised opcode '{opname}' on line {linenum}"
    cmd = opcodesR[opname]
    cmdn = len(split)
    assert cmdn < 0xffff, f"cmdn out of range on line {linenum}"
    output += int.to_bytes(cmdn, 2, 'big')
    output += int.to_bytes(cmd, 2, 'big')
    
    for i in range(0, cmdn):
        operand = split[i].strip()
        if operand[-1] == ',':
            operand = operand[:-1]

        if operand.startswith('0x'):
            # hex immediate
            val = int(operand, 16)
        else:
            if '.' in operand:
                # float conversion
                val = int(float(operand) * 1024 + typeBases['Float'])
            else:
                if operand[0] == '-' or operand[0].isdigit():
                    # signed int immediate
                    val = int(operand)
                else:
                    # expression type macros
                    splitOperand = operand.split("(")
                    macro = splitOperand[0]
                    assert macro in typeBases, f"Unable to parse operand '{operand}' on line {linenum}"
                    assert not macro in ['Address', 'Float'], f"Address and Float are not meant to be used as expression macros (line {linenum})"
                    val = typeBases[macro] + int(splitOperand[1][:-1]) # remove )
            if val < 0:
                val = struct.unpack('>I', struct.pack('>i', val))[0]
        assert 0 <= val <= 0xffffffff, f"Operand '{operand}' out of range on line {linenum}"
        output += int.to_bytes(val, 4, 'big')
infile.close()

if config.binary:
    if config.toFile:
        outfile = open(config.outPath, 'wb')
        outfile.write(output)
        outfile.close()
    else:
        n = 0
        for i in range(0, len(output), 4):
            n += 1
            word = ""
            for j in range(0, 4):
                word += f"{output[i + j]:02x}"
            print(f"{word} ", end="")
            if n == 8:
                n = 0
                print("")
else:
    s = f"unsigned int {config.symbol}[] = {{"
    for i in range(0, len(output), 4):
        word = ""
        for j in range(0, 4):
            word += f"{output[i + j]:02x}"
        s += f"0x{word}, "
    s = s[:-2] + "};"

    if config.toFile:
        outfile = open(config.outPath, 'w')
        outfile.write(s)
        outfile.close()
    else:
        print(s)
print(f"\nAssembled script with length {hex(len(output))} bytes")

Config.destroyStaticInstance()