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
        s = chr(ord('0') + n%2) + s
        n //= 2
    return s

def intToPC(n):
    s = ""
    for i in range(7):
        s = chr(ord('0') + n%2) + s
        n //= 2
    return s + ' '*8 # 8 spaces required by output for some reason

insCodeOf={'00000': "add",
           '00001':'sub',
           '00010':'mov',
           '00011':'mov1',
           '00100':'ld',
           '00101':'st',
           '00110':'mul',
           '00111':'div',
           '01000':'rs',
           '01001':'ls',
           '01010':'xor',
           '01011':'or',
           '01100':'and',
           '01101':'not',
           '01110':'cmp',
           '01111':'jmp',
           '11100':'jlt',
           '11101':'jgt',
           '11111':'je',
           '11010':'hlt'}

# List for register addresses in binary
registers = [0]*8
memory = [0]*128
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
    print(intToPC(oldPC), end = "")
    print(*[intToBin(i) for i in registers])

# Counting number of vars
reg3ins = ["add", "sub", "mul", "xor", "or", "and"] # type A
immins = ["mov", "rs", "ls"] # type B
reg2ins = ["mov1", "div", "not", "cmp"] # type C
memins = ["ld", "st"] # type D
jmpins = ["jmp", "jlt", "jgt", "je", "hlt"] # type E   

operatorOf = {
    "add": operator.add,
    "sub": operator.sub,
    "mul": operator.mul,
    "or": operator.__or__,
    "and": operator.__and__,
    "xor": operator.xor
}

print(operatorOf["xor"](4,4))

def validImmediate(reg): 
    return (reg >= 0) and (reg < 128)

def typeA(ins, reg1, reg2, reg3):
    global registers

    registers[reg1] = operatorOf[ins](registers[reg2], registers[reg3]) 
    if not validImmediate(registers[reg1]):
        registers[reg1] = 0
        registers[FLAGS] |= 8 # forcefully set overflow flag 
    else:
        registers[FLAGS] &= 119 # 127 - 8 

    next()

def typeB(ins, reg1, im1):
    global registers
    if ins=='mov':
        registers[reg1] = im1
    elif ins=='rs':
        registers[reg1] >>= im1
    else:
        registers[reg1] <<= im1
        registers[reg1] %= 128

    next()

def typeC(ins, reg1, reg2):
    global registers
    if ins=='mov1':
        registers[reg1] = registers[reg2]
    elif ins=='div':
        if registers[reg2] == 0:
            registers[reg1] = 0
            registers[FLAGS] |= 8
        else:
            registers[reg1] //= registers[reg2]
    elif ins=='not':
        registers[reg1] = 127 - registers[reg2]
    else:
        # cmp
        if registers[reg1] < registers[reg2]:
            registers[FLAGS] |= 4
            registers[FLAGS] &= 125 # 127 - 2
            registers[FLAGS] &= 126 # 127 - 1
        elif registers[reg1] == registers[reg2]:
            registers[FLAGS] &= 123 # 127 - 4
            registers[FLAGS] &= 125 # 127 - 2
            registers[FLAGS] |= 1
        else:
            registers[FLAGS] &= 123
            registers[FLAGS] |= 2
            registers[FLAGS] &= 126
    next()


def typeD(ins, reg1, mem1):
    global registers
    if ins=='ld':
        registers[reg1] = memory[mem1]
    else:
        memory[mem1] = registers[reg1]
    next()

# MAIN

binary = getBinary()
print(binary)

for i in range(len(binary)):
    memory[i] = binToInt(binary[i])

while executing:
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
            registers[FLAGS] |= 8 # forcefully set overflow flag 
        else:
            registers[FLAGS] &= 119 # 127 - 8 
        next()

    # type B
    elif ins in immins:
        reg1 = binToInt(current[6:9]) # nice ;)
        im1 = binToInt(current[9:])
        if ins=='mov':
            registers[reg1] = im1
        elif ins=='rs':
            registers[reg1] >>= im1
        else:
            registers[reg1] <<= im1
            registers[reg1] %= 128

        next()

    # type C
    elif ins in reg2ins:
        reg1 = binToInt(current[10:13])
        reg2 = binToInt(current[13:])
        if ins=='mov1':
            registers[reg1] = registers[reg2]
        elif ins=='div':
            if registers[reg2] == 0:
                registers[reg1] = 0
                registers[FLAGS] |= 8
            else:
                registers[reg1] //= registers[reg2]
                registers[FLAGS] &= 119
        elif ins=='not':
            registers[reg1] = 127 - registers[reg2]
        else:
            # cmp
            if registers[reg1] < registers[reg2]:
                registers[FLAGS] |= 4
                registers[FLAGS] &= 125 # 127 - 2
                registers[FLAGS] &= 126 # 127 - 1
            elif registers[reg1] == registers[reg2]:
                registers[FLAGS] &= 123 # 127 - 4
                registers[FLAGS] &= 125 # 127 - 2
                registers[FLAGS] |= 1
            else:
                registers[FLAGS] &= 123
                registers[FLAGS] |= 2
                registers[FLAGS] &= 126
        next()

    # type D
    elif ins in memins:
        reg1 = binToInt(current[6:9])
        mem1 = binToInt(current[9:])
        if ins=='ld':
            registers[reg1] = memory[mem1]
        else:
            memory[mem1] = registers[reg1]
        next()

    # type E
    else:
        mem1 = current[9:]
        if ins=='jmp':
            PC = mem1
        elif ins=='jlt':
            if registers[FLAGS] & 4:
                PC = mem1
        elif ins=='jgt':
            if registers[FLAGS] & 2:
                PC = mem1
        elif ins=='je':
            if registers[FLAGS] & 1:
                PC = mem1
        else:
            executing = False
        next()


    dumpState(old)
