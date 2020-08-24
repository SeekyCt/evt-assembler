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

    s = line.split()
    opname = s.pop(0).lower()
    assert opname in opcodesR, f"Unrecognised opcode '{opname}' on line {linenum}"
    cmd = opcodesR[opname]
    cmdn = len(s)
    assert cmdn < 0xffff, f"Too many operands on line {linenum}, must be under 0xffff"
    output += f"{hex((cmdn << 16) | cmd)}, "
    length += 4
    for i in range(0, cmdn):
        operand = s[i].strip()
        if operand[-1] == ',':
            operand = operand[:-1]

        if '.' in operand:
            # float function
            o = float(operand) * 1024 + typeBases['Float']

            # float to binary in unsigned int
            output += f"{hex(struct.unpack('>I', struct.pack('>i', int(o)))[0])}, "
        elif operand[0].isdigit():
            # let the unsigned int stay
            output += f"{operand}, "
        else:
            # signed int to unsigned
            if operand[0] == '-':
                if operand.startswith("0x"):
                    o = int(operand[2:], 16)
                else:
                    o = int(operand)
            else:
                # expression type macros
                _s = operand.split("(")
                t = _s[0]
                o = int(_s[1][:-1]) + typeBases[t] # remove )

            output += f"{hex(struct.unpack('>I', struct.pack('>i', o))[0])}, "

        length += 4

output = output[:-2]
output += "};"

print(output)
print(length)

if config.toFile:
    out.close()
Config.destroyStaticInstance()