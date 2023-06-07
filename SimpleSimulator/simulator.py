import sys
import operator

def binToInt(s):
    exp = 1
    ans = 0
    while s:
        ans += (exp if s[-1] == '1' else 0)
        exp *= 2
        s = s[:-1]
    return ans

def intToBin(n):
    s = ""
    for i in range(16):
        s = chr(ord('0') + n % 2) + s
        n //= 2
    return s

def intToPC(n):
    s = ""
    for i in range(7):
        s = chr(ord('0') + n % 2) + s
        n //= 2
    return s + ' ' * 8  # 8 spaces required by output for some reason

def intToByte(n):
    s = ""
    for i in range(8):
        s = chr(ord('0') + n % 2) + s
        n //= 2
    return s

insCodeOf = {'00000': "add",
             '00001': 'sub',
             '00010': 'mov',
             '00011': 'mov1',
             '00100': 'ld',
             '00101': 'st',
             '00110': 'mul',
             '00111': 'div',
             '01000': 'rs',
             '01001': 'ls',
             '01010': 'xor',
             '01011': 'or',
             '01100': 'and',
             '01101': 'not',
             '01110': 'cmp',
             '01111': 'jmp',
             '11100': 'jlt',
             '11101': 'jgt',
             '11111': 'je',
             '11010': 'hlt',
             # FLOATING POINT INSTRUCTIONS
             '10000': 'addf',
             '10001': 'subf',
             '10010': 'movf',
             # BONUS
             '10011': 'nop'}

# List for register addresses in binary
registers = [0] * 8
memory = [0] * 128
FLAGS = 7

PC = 0
executing = True

def next():
    global PC
    PC += 1

def getBinary():
    inp = sys.stdin.readlines()
    finale = [i.strip() for i in inp]
    return finale

def dumpState(oldPC):
    print(intToPC(oldPC), end="")
    print(*[intToBin(i) for i in registers])

# Counting number of vars
reg3ins = ["add", "sub", "mul", "xor", "or", "and", "addf", "subf"]  # type A
immins = ["mov", "rs", "ls"]  # type B
reg2ins = ["mov1", "div", "not", "cmp"]  # type C
memins = ["ld", "st"]  # type D
jmpins = ["jmp", "jlt", "jgt", "je", "hlt"]  # type E
movfins = ["movf"]

# FLOATING POINT INSTRUCTIONS
def binToFloat(bn):
    # BIAS IS 3
    if all([i == '0' for i in bn]):
        return 0
    expPower = binToInt(bn[:3]) - 3
    # MANTISSA
    expBase = 1 + binToInt(bn[3:])/(1 << 5)
    return expBase**(expPower)

def floatToBin(flt):
    # BIAS
    if flt <= 0:
        return 0
    fExp = 3
    if flt < 1.0:
        while flt < 1.0:
            flt *= 2
            fExp -= 1
    elif flt >= 2.0:
        while flt >= 2.0:
            flt /= 2
            fExp += 1
    # OVERFLOW
    if fExp < 0 or fExp > 7:
        # 1 for overflow
        return 0
    else:
        flt -= 1
        flt *= 32
        flt = int(flt)
        # bitshifted by 5 for the format
        return ((fExp << 5) + flt)

def addf(a, b):
    f1 = binToFloat(intToByte(a))
    f2 = binToFloat(intToByte(b))
    return floatToBin(f1 + f2)

def subf(a, b):
    f1 = binToFloat(intToByte(a))
    f2 = binToFloat(intToByte(b))
    return floatToBin(f1 - f2)

def movf(a, imm1):
    registers[a] = imm1
    return 0

operatorOf = {
    "add": operator.add,
    "sub": operator.sub,
    "mul": operator.mul,
    "or": operator.__or__,
    "and": operator.__and__,
    "xor": operator.xor,
    "addf": addf,
    "subf": subf 
}



def validImmediate(reg):
    return 0 <= reg < 128
# MAIN

binary = getBinary()




for i in range(len(binary)):
    memory[i] = binToInt(binary[i])

while executing:
    if PC >= len(binary):
        break
    flagsWasSet = False
    old = PC
    current = binary[PC]
    opc = current[:5]
    ins = insCodeOf[opc]

    # type A
    if ins in reg3ins:
        r1 = binToInt(current[7:10])
        r2 = binToInt(current[10:13])
        r3 = binToInt(current[13:])
        registers[r1] = operatorOf[ins](registers[r2], registers[r3])
        if not validImmediate(registers[r1]):
            registers[r1] = 0
            # registers[FLAGS] |= 8  # forcefully set overflow flag
            registers[FLAGS] = 8  # REVIEW THIS
            flagsWasSet = True
        next()

    # type B
    elif ins in immins:
        reg1 = binToInt(current[6:9])  # nice ;)
        im1 = binToInt(current[9:])
        if ins == 'mov':
            registers[reg1] = im1
        elif ins == 'rs':
            registers[reg1] >>= im1
        else:
            registers[reg1] <<= im1
            registers[reg1] %= 128

        next()

    # type C
    elif ins in reg2ins:
        reg1 = binToInt(current[10:13])
        reg2 = binToInt(current[13:])
        if ins == 'mov1':
            registers[reg1] = registers[reg2]
        elif ins == 'div':
            if registers[reg2] == 0:
                registers[reg1] = 0
                # registers[FLAGS] |= 8
                registers[FLAGS] |= 8
                # REVIEW THIS
                flagsWasSet = True
            else:
                registers[reg1] //= registers[reg2]
        elif ins == 'not':
            registers[reg1] = ((1 << 16) - 1) - registers[reg2]
        else:
            # cmp
            flagsWasSet = True
            if registers[reg1] < registers[reg2]:
                registers[FLAGS] = 4
            elif registers[reg1] == registers[reg2]:
                registers[FLAGS] = 1
            else:
                registers[FLAGS] = 2
        next()

    # type D
    elif ins in memins:
        reg1 = binToInt(current[6:9])
        mem1 = binToInt(current[9:])
        if ins == 'ld':
            registers[reg1] = memory[mem1]
        else:
            memory[mem1] = registers[reg1]
        next()

    # type E
    elif ins in jmpins:
        mem1 = binToInt(current[9:])
        if ins == 'jmp':
            PC = mem1 - 1
        elif ins == 'jlt':
            if registers[FLAGS] & 4:
                PC = mem1 - 1
        elif ins == 'jgt':
            if registers[FLAGS] & 2:
                PC = mem1 - 1
        elif ins == 'je':
            if registers[FLAGS] & 1:
                PC = mem1 - 1
        elif ins == 'nop':
            pass
        else:
            executing = False
        next()

    # movf
    else:
        reg1 = binToInt(current[5:8])
        imm1 = binToInt(current[8:])
        registers[reg1] = imm1
        next()

    if not flagsWasSet: 
        registers[FLAGS] = 0

    dumpState(old)

for i in range(128):
    print(intToBin(memory[i]))     
