import sys
opCodeOf={"add":'00000',
            'sub':'00001',
            'mov':'00010',
            'mov1':'00011',
            'ld':'00100',
            'st':'00101',
            'mul':'00110',
            'div':'00111',
            'rs':'01000',
            'ls':'01001',
            'xor':'01010',
            'or':'01011',
            'and':'01100',
            'not':'01101',
            'cmp':'01110',
            'jmp':'01111',
            'jlt':'11100',
            'jgt':'11101',
            'je':'11111',
            'hlt':'11010'}

# Dictionary for register addresses in binary
registers={'R0':'000',
           'R1':'001',
           'R2':'010',
           'R3':'011',
           'R4':'100',
           'R5':'101',
           'R6':'110',
           'FLAGS':'111'}
# Dictionary for register addresses in binary
registers_value={'R0': 0,
           'R1':0,
           'R2':0,
           'R3':0,
           'R4':0,
           'R5':0,
           'R6':0,
           'FLAGS':0
           }
# Counting number of vars
reg3ins = ["add", "sub", "mul", "xor", "or", "and"] # type A
immins = ["mov", "rs", "ls"] # type B
reg2ins = ["mov1", "div", "not", "cmp"] # type C
memins = ["ld", "st"] # type D
jmpins = ["jmp", "jlt", "jgt", "je", "hlt"] # type E    
def input_read():
    inp_lines=sys.stdin.readlines()
    return inp_lines


def file_write(out_lst):
    for line in out_lst:
        print(line)

def mov(address1 , address2 , address3):
    reg1 = ""
    reg2 = ""
    reg3 = ""
    for r , v in registers.items():
        if(v == address1):
            reg1 = r
        if(v == address2):
            reg2 = r
        if(v == address3):
            reg3 = r
    registers_value[reg1] = registers_value[reg2] - registers_value[reg3]
def mov1(address1 , immediate):
    reg1 = ""
    for r , v in registers.items():
        if(v == address1):
            reg1 = r
            break
    registers_value[reg1] = immediate
def cmp(address1 ,address2):
    reg1 = ""
    reg2 = ""
    for r , v in registers.items():
        if(v == address1):
            reg1 = r
        if(v == address2):
            reg2 = r
    val1 = registers_value[reg1]
    val2 = registers_value[reg2]
    if( val1 == val2 ):
        registers_value['FLAGS'] = 1
    elif( val1 > val2 ):
        registers_value['FLAGS'] = 2
    else:
        registers_value['FLAGS'] = 4        

