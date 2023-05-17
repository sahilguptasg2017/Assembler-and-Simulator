import sys
# Dictionary for instruction set of opCodeOf in binary
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

# Counting number of vars
var_count = 0
instr_count = 0

varIndices = []
var_dict={}
labels = {}

reg3ins = ["add", "sub", "mul", "xor", "or", "and"] # type A
immins = ["mov", "rs", "ls"] # type B
reg2ins = ["mov1", "div", "not", "cmp"] # type C
memins = ["ld", "st"] # type D
jmpins = ["jmp", "jlt", "jgt", "je", "hlt"] # type E

# check if valid memory address
def isvalid(mem):
    if not all([i in "01" for i in mem]):
        return False
    return int(mem,2) < instr_count

# opcode to binary functions
def ins_typeA(ins, args, line_no):
    if(len(args) != 3):
        return f"Error on line {line_no+1}: Incorrect number of argumets in type A instruction" 
    if not all([i in registers for i in args]):
        return f"Error on line {line_no+1}: Incorrect register name in type A instruction \"{ins}\""

    if ins=='add':
        if "FLAGS" in args:
            return f"Error on line {line_no+1}: Illegal use of FLAGS"
        out_str=opCodeOf['add']
        out_str+='0'*2
        out_str+=registers[args[0]]
        out_str+=registers[args[1]]
        out_str+=registers[args[2]]
        return out_str
    elif ins=='sub':
        if "FLAGS" in args:
            return f"Error on line {line_no+1}: Illegal use of FLAGS"
        out_str=opCodeOf['sub']
        out_str+='0'*2
        out_str+=registers[args[0]]
        out_str+=registers[args[1]]
        out_str+=registers[args[2]]
        return out_str

    if "FLAGS" in args:
        return f"Error on line {line_no+1}: Illegal use of FLAGS"
    ins_str = opCodeOf[ins] + "00"
    ins_str += ''.join(registers[i] for i in args)
    return ins_str

def ins_typeB(ins, args, line_no):
    if(len(args) != 2):
        return f"Error on line {line_no+1}: Incorrect number of argumets in type B instruction"
    if args[0] not in registers:
        return f"Error on line {line_no+1}: Incorrect register name in type B instruction \"{ins}\""
    if "FLAGS" in args:
        return f"Error on line {line_no+1}: Illegal use of FLAGS"
    ins_str=opCodeOf[ins]+'0'
    ins_str+=registers[args[0]]

    if args[1][0] != '$':
        return f"Error on line {line_no+1}: Incorrect format for Immediate value."
    for i in args[1][1:]:
        if i not in '0123456789':
            return f"Error on line {line_no+1}: Incorrect format for Immediate value."

    nm = bin(int(args[1][1:]))[2:]
    if len(nm) > 7:
        return f"Error on line {line_no+1}: Immediate value larger than 7 bits."

    ins_str+= '0'*(7-len(nm))
    ins_str+= nm
    return ins_str

def ins_typeC(ins, args, line_no):
    if(len(args) != 2):
        return f"Error on line {line_no+1}: Incorrect number of argumets in type A instruction"
    if not all([i in registers for i in args]):
        return f"Error on line {line_no+1}: Incorrect register name in type A instruction \"{ins}\""
    if "FLAGS" in args and ins != "mov1":
        return f"Error on line {line_no+1}: Illegal use of FLAGS"
    if args[0] == 'FLAGS':
        return f"Error on line {line_no+1}: Illegal use of FLAGS"
    ins_str = opCodeOf[ins] + "00000"
    ins_str += ''.join(registers[i] for i in args)
    return ins_str

def ins_typeD(ins, args, line_no):
    if(len(args) != 2):
        return f"Error on line {line_no+1}: Incorrect number of argumets in type D instruction"
    if args[0] not in registers:
        return f"Error on line {line_no+1}: Incorrect register name in type D instruction \"{ins}\""
    ins_str = opCodeOf[ins] + '0'
    ins_str+=registers[args[0]]
    
    if(isvalid(args[1])):
        ins_str += '0'*(7-len(args[1])) + args[1]
    else:
        if args[1] not in var_dict:
            return f"Error on line {line_no+1}: Invalid variable name \"{args[1]}\""
        else:
            ins_str+='0'*(7-len(bin(var_dict[args[1]])[2:]))+bin(var_dict[args[1]])[2:]

    return ins_str

def ins_typeE(ins, args, line_no):
    if ins == 'hlt':
        return opCodeOf['hlt'] + '0'*11
    if(len(args) != 1):
        return f"Error on line {line_no+1}: Incorrect number of argumets in type E instruction"
    ins_str = opCodeOf[ins] + '0'*4
    if isvalid(args[0]):
        ins_str += '0'*(7-len(args[0])) + args[0]
    else:
        if args[0] not in labels:
            return f"Error on line {line_no+1}: Invalid label name \"{args[0]}\""
        ins_str+=labels[args[0]]
    return ins_str

# Function to read input from input file
def file_read():
    inp_lines=sys.stdin.readlines()
    return inp_lines

# Function to write output to output file
def file_write(out_lst):
    for line in out_lst:
        print(line)

# check if all vars are in front
inp_lines = file_read()

al_lst = []

def var_and_ins_counts():
    #inp_lines=file_read()                  # Opening and reading input file
    vc = 0
    ic = 0
    hasVar = [True]
    for i in range(len(inp_lines)):
        wrds = inp_lines[i].strip().split()
        if not wrds:
            continue
        if wrds[0] == 'var':
            if not hasVar[-1]:
                al_lst.append(f"Error on line {i+1}: variable name declared after instructions.")
            if len(wrds) != 2:
                al_lst.append(f"Error on line {i+1}: incorrect number of arguments in var command.")
            vc += 1
            varIndices.append(i)
        else:
            ic += 1
        hasVar.append(wrds[0] == 'var')
    if(ic > 127):
        al_lst.append(f"Instruction count greater than 127.")
    return (vc, ic)

var_count, instr_count = var_and_ins_counts()

memIndex = instr_count


# make var dict

for i in varIndices:
    nm = inp_lines[i].strip().split()[1]
    if nm in var_dict:
        al_lst.append(f"Error on line {i+1}: variable \"{nm}\" has already been declared.")
    var_dict[nm] = memIndex
    memIndex += 1


# make labels dict

ins_cnt = 0
for i in range(len(inp_lines)):
    line = inp_lines[i].strip().split()
    if not line:
        continue
    if line[0] == 'var':
        continue
    if line[0][-1] == ':':
        if line[0][:-1] in labels:
            al_lst.append(f"Error on line {i+1}: Label already exists")
        labels[line[0][:-1]] = '0'*(7-len(bin(ins_cnt)[2:]))+bin(ins_cnt)[2:]
    ins_cnt += 1

# main function
def main():
    out_lst=al_lst
    last_ins = ""
    ins = ""

    for i in range(len(inp_lines)):
        line = inp_lines[i]
        if ':' in line:
            line = ''.join(line.split(':')[1:]).strip().split()
        else:
            line = inp_lines[i].strip().split()
        if not line:
            continue
        if line[0] == 'var':
            continue
        if line[0] not in opCodeOf:
            out_lst.append(f"Error on line {i+1}: Invalid instruction name {line[0]}")
        ins = line[0]
        args = line[1:]
        line_no = i

        # look for correct mov 
        if ins=="mov":
            if all(i in registers for i in args):
                ins = "mov1"

        out_str = ""
        # add binary
        if ins in reg3ins:
            out_str += ins_typeA(ins, args, line_no)
        elif ins in immins:
            out_str += ins_typeB(ins, args, line_no)
        elif ins in reg2ins:
            out_str += ins_typeC(ins, args, line_no)
        elif ins in memins:
            out_str += ins_typeD(ins, args, line_no)
        else:
            out_str += ins_typeE(ins, args, line_no)

        out_lst.append(out_str + '')
        
    # Handling errors h and i
    if ins!="hlt":
         out_lst.append(f"Error: Missing hlt instruction or last instruction is not hlt")

    if any(["Error" in i for i in out_lst]):
        file_write([i for i in out_lst if "Error" in i])
    else:
        file_write(out_lst)

if __name__=="__main__":
    main()

# ORIGINAL CODE 

'''
for i in range(len(inp_lines)):
    line_count+=1
    # Storing the instruction in list
    line = inp_lines[i].strip()
    if not line:
        continue
    #adjusting for labels by dividing it on ":" symbol.
    if ":" in line:
        line=line[line.index(":")+1:]           
    words=line.split(" ")
    k=0
    while k<len(words):
        words[k]=words[k].strip()
        k+=1
    instruction=[]
    for t in words:   
        if t!='':
            instruction.append(t)
    # Reading, interpreting instruction and writing corresponding binary to stdout.txt
    out_str=""
    if instruction[0]!='var': 
            # error check of variable  
            if(instruction[0] not in opCodeOf.keys()):
                out_str=("Incorrect instruction name in line " + str(line_count))
                out_lst.append(f'{out_str}')
                continue


            if instruction[0]=='mov':
                # error of register
                if(instruction[1] not in registers.keys()):
                    out_str=("Incorrect Register name in line " + str(line_count))
                    out_lst.append(f'{out_str}')
                    continue

                if '$' in instruction[2]:
                    out_str+=opCodeOf['mov']
                    out_str+='0'
                    out_str+=registers[instruction[1]]
                    #this is only possible if value <= 127..
                    out_str+='0'*(7-len(bin(int(instruction[2][1:]))[2:]))
                    out_str+=bin(int(instruction[2][1:]))[2:]    
                    out_lst.append(f'{out_str}')
                else:
                    out_str+=opCodeOf['mov1']
                    out_str+='0'*5
                    out_str+=registers[instruction[1]]
                    out_str+=registers[instruction[2]]
                    out_lst.append(f'{out_str}')
            elif instruction[0]=='mul':
                # error check of register
                if(instruction[1] not in registers.keys() or instruction[2] not in registers.keys() or instruction[3] not in registers.keys() ):
                    out_str=("Incorrect Register name in line " + str(line_count))
                    out_lst.append(f'{out_str}')
                    continue
                out_str+=opCodeOf['mul']
                out_str+='0'*2
                out_str+=registers[instruction[1]]
                out_str+=registers[instruction[2]]
                out_str+=registers[instruction[3]]
                out_lst.append(f'{out_str}')
            elif instruction[0]=='st':
                out_str+=opCodeOf['st']    
                out_str+='0'
                out_str+=registers[instruction[1]]
                # error check of variable
                if(instruction[2] not in var_dict.keys()):
                    out_str=("Incorrect variable name in line " + str(line_count))
                    out_lst.append(f'{out_str}')
                    continue 
                out_str+='0'*(7-len(bin(var_dict[instruction[2]])[2:]))+bin(var_dict[instruction[2]])[2:]
                out_lst.append(f'{out_str}')
            elif instruction[0]=='hlt':
                out_str+=opCodeOf['hlt']
                out_str+=11*'0'
                out_lst.append(f'{out_str}')
                break
            elif instruction[0]=='add':
                if(instruction[1] not in registers.keys() or instruction[2] not in registers.keys() or instruction[3] not in registers.keys() ):
                    out_str=("Incorrect Register name in line " + str(line_count))
                    out_lst.append(f'{out_str}')
                    continue
                out_str+=opCodeOf['add']
                out_str+='0'*2
                out_str+=registers[instruction[1]]
                out_str+=registers[instruction[2]]
                out_str+=registers[instruction[3]]
                out_lst.append(f'{out_str}')
            elif instruction[0]=='sub':
                if(instruction[1] not in registers.keys() or instruction[2] not in registers.keys() or instruction[3] not in registers.keys() ):
                    out_str=("Incorrect Register name in line " + str(line_count))
                    out_lst.append(f'{out_str}')
                    continue
                out_str+=opCodeOf['sub']
                out_str+='0'*2
                out_str+=registers[instruction[1]]
                out_str+=registers[instruction[2]]
                out_str+=registers[instruction[3]]
                out_lst.append(f'{out_str}')
            elif instruction[0]=='ld':
                if(instruction[1] not in registers.keys()):
                    out_str=("Incorrect Register name in line " + str(line_count))
                    out_lst.append(f'{out_str}')
                    continue
                out_str+=opCodeOf['ld']
                out_str+='0'*1
                out_str+=registers[instruction[1]]
                out_str+='0'*(7-len(bin(var_dict[instruction[2]])[2:]))+bin(var_dict[instruction[2]])[2:]
                out_lst.append(f'{out_str}')
            elif instruction[0]=='div':
                if(instruction[1] not in registers.keys() or instruction[2] not in registers.keys()):
                    out_str=("Incorrect Register name in line " + str(line_count))
                    out_lst.append(f'{out_str}')
                    continue
                out_str+=opCodeOf['div']
                out_str+='0'*5
                out_str+=registers[instruction[1]]
                out_str+=registers[instruction[2]]
                out_lst.append(f'{out_str}')
            elif instruction[0]=='rs':
                if(instruction[1] not in registers.keys()):
                    out_str=("Incorrect Register name in line " + str(line_count))
                    out_lst.append(f'{out_str}')
                    continue
                out_str+=opCodeOf['rs']
                out_str+='0'*1
                out_str+=registers[instruction[1]]
                out_str+=bin(int(instruction[2][1:]))[2:]
                out_lst.append(f'{out_str}')
            elif instruction[0]=='ls':
                if(instruction[1] not in registers.keys()):
                    out_str=("Incorrect Register name in line " + str(line_count))
                    out_lst.append(f'{out_str}')
                    continue
                out_str+=opCodeOf['ls']
                out_str+='0'*1
                out_str+=registers[instruction[1]]
                out_str+=bin(int(instruction[2][1:]))[2:]    
                out_lst.append(f'{out_str}')
            elif instruction[0]=='xor':
                if(instruction[1] not in registers.keys() or instruction[2] not in registers.keys() or instruction[3] not in registers.keys() ):
                    out_str=("Incorrect Register name in line " + str(line_count))
                    out_lst.append(f'{out_str}')
                    continue
                out_str+=opCodeOf['xor']
                out_str+='0'*2
                out_str+=registers[instruction[1]]
                out_str+=registers[instruction[2]]
                out_str+=registers[instruction[3]]
                out_lst.append(f'{out_str}')
            elif instruction[0]=='or':
                if(instruction[1] not in registers.keys() or instruction[2] not in registers.keys() or instruction[3] not in registers.keys() ):
                    out_str=("Incorrect Register name in line " + str(line_count))
                    out_lst.append(f'{out_str}')
                    continue
                out_str+=opCodeOf['or']    
                out_str+='0'*2
                out_str+=registers[instruction[1]]
                out_str+=registers[instruction[2]]
                out_str+=registers[instruction[3]]
                out_lst.append(f'{out_str}')
            elif instruction[0]=='and':
                if(instruction[1] not in registers.keys() or instruction[2] not in registers.keys() or instruction[3] not in registers.keys() ):
                    out_str=("Incorrect Register name in line " + str(line_count))
                    out_lst.append(f'{out_str}')
                    continue
                out_str+=opCodeOf['and']
                out_str+='0'*2
                out_str+=registers[instruction[1]]
                out_str+=registers[instruction[2]]
                out_str+=registers[instruction[3]]
                out_lst.append(f'{out_str}')
            elif instruction[0]=='not':
                if(instruction[1] not in registers.keys() or instruction[2] not in registers.keys()):
                    out_str=("Incorrect Register name in line " + str(line_count))
                    out_lst.append(f'{out_str}')
                    continue
                out_str+=opCodeOf['not']
                out_str+='0'*5
                out_str+=registers[instruction[1]]
                out_str+=registers[instruction[2]]  
                out_lst.append(f'{out_str}')
            elif instruction[0]=='cmp':
                if(instruction[1] not in registers.keys() or instruction[2] not in registers.keys()):
                    out_str=("Incorrect Register name in line " + str(line_count))
                    out_lst.append(f'{out_str}')
                    continue
                out_str+=opCodeOf['cmp']
                out_str+='0'*5
                out_str+=registers[instruction[1]]
                out_str+=registers[instruction[2]]
                out_lst.append(f'{out_str}')
            elif instruction[0]=='jmp':
                out_str+=opCodeOf['cmp']
                out_str+='0'*4
                out_str+='0'*(7-len(bin(var_dict[instruction[2]])[2:]))+bin(var_dict[instruction[2]])[2:]
                out_lst.append(f'{out_str}')
            elif instruction[0]=='jlt':
                out_str+=opCodeOf['jlt']
                out_str+='0'*4
                out_str+='0'*(7-len(bin(var_dict[instruction[2]])[2:]))+bin(var_dict[instruction[2]])[2:]
                out_lst.append(f'{out_str}')
            elif instruction[0]=='jgt':
                out_str+=opCodeOf['jgt']
                out_str+='0'*4
                out_str+='0'*(7-len(bin(var_dict[instruction[2]])[2:]))+bin(var_dict[instruction[2]])[2:]
                out_lst.append(f'{out_str}')        
            elif instruction[0]=='je':
                out_str+=opCodeOf['je']
                out_str+='0'*4
                out_str+='0'*(7-len(bin(var_dict[instruction[2]])[2:]))+bin(var_dict[instruction[2]])[2:]
                out_lst.append(f'{out_str}')

'''

