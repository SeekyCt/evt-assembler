import sys, struct
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
if config.toFile:
    out = open(config.outPath, 'w')

output = "unsigned int script[] = {"

f = open(config.inPath)
length = 0
linenum = 0
for line in f.readlines():
    linenum += 1

    # Remove address labels, comments, strip whitespace and ignore blank lines
    if line[0] == '8':
        line = line[10:]
    line = line.split("#")[0].strip()
    if len(line) == 0:
        continue

    # Split operands, strip whitespace and commas
    s = line.split()
    for i in range(0, len(s)):
        s[i] = s[i].strip()
        if s[i][-1] == ',':
            s[i] = s[i][:-1]

    # halfword cmdn
    # halfword cmd
    opname = s[0].lower()
    assert opname in opcodesR, f"Unrecognised opcode '{opname}' on line {linenum}"
    cmd = opcodesR[opname]
    cmdn = len(s) - 1
    assert cmdn < 0xffff, f"Too many operands on line {linenum}, must be under 0xffff"
    output += f"{hex((cmdn << 16) | cmd)}, "
    length += 4

    # word[cmdn] data
    for i in range(1, cmdn + 1):
        operand = s[i]

        if operand[0].isdigit():
            if '.' in operand:
                # float function
                o = float(operand) * 1024 + typeBases['float']

                # float to binary in unsigned int
                output += f"{hex(struct.unpack('>I', struct.pack('>f', )[0]))}, "
            else:
                # let the unsigned int stay
                output += f"{operand}, "
        elif operand[0] == '-':
            # signed int to unsigned
            if operand.startswith("0x"):
                o = int(operand[2:], 16)
            else:
                o = int(operand)
            output += f"{hex(struct.unpack('>I', struct.pack('>i', o))[0])}, "
        else:
            print(f"function op: {operand}")            


        length += 4


output = output[:-2]
output += "};"

print(output)

if config.toFile:
    out.close()
Config.destroyStaticInstance()