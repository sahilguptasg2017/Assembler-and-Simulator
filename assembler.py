# Dictionary for instruction set of operations in binary
operations={"add":'00000',
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

# Opening and reading input file
inp_file=open(r"stdin.txt","r+")
inp_lines=inp_file.readlines()
inp_file.close()

# Counting number of vars
var_count=0
for line in inp_lines:
    if 'var' in line:
        var_count+=1
        
# Counting number of instructions
instr_count=-var_count   
for line in inp_lines:
    if line!='\n':
        instr_count+=1

# Storing position allocation for each variable in var_dict
var_dict={}
for line in inp_lines:
    if 'var' in line:
        line=line.replace(" ","")
        var_dict[line[3]]=instr_count
        instr_count+=1

out_lst=[]
for line in inp_lines:
    # Storing the instruction in list
    if line!='\n':
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
                if instruction[0]=='mov':
                    if '$' in instruction[2]:
                        out_str+=operations['mov']
                        out_str+='0'
                        out_str+=registers[instruction[1]]
                        out_str+='0'*(7-len(bin(int(instruction[2][1:]))[2:]))
                        out_str+=bin(int(instruction[2][1:]))[2:]    
                        out_lst.append(f'{out_str}\n')
                    else:
                        out_str+=operations['mov1']
                        out_str+='0'*5
                        out_str+=registers[instruction[1]]
                        out_str+=registers[instruction[2]]
                        out_lst.append(f'{out_str}\n')
                elif instruction[0]=='mul':
                    out_str+=operations['mul']
                    out_str+='0'*2
                    out_str+=registers[instruction[1]]
                    out_str+=registers[instruction[2]]
                    out_str+=registers[instruction[3]]
                    out_lst.append(f'{out_str}\n')
                elif instruction[0]=='st':
                    out_str+=operations['st']    
                    out_str+='0'
                    out_str+=registers[instruction[1]]
                    out_str+='0'*(7-len(bin(var_dict[instruction[2]])[2:]))+bin(var_dict[instruction[2]])[2:]
                    out_lst.append(f'{out_str}\n')
                elif instruction[0]=='hlt':
                    out_str+=operations['hlt']
                    out_str+=11*'0'
                    out_lst.append(f'{out_str}\n')
                    break
                elif instruction[0]=='add':
                    out_str+=operations['add']
                    out_str+='0'*2
                    out_str+=registers[instruction[1]]
                    out_str+=registers[instruction[2]]
                    out_str+=registers[instruction[3]]
                    out_lst.append(f'{out_str}\n')
                elif instruction[0]=='sub':
                    out_str+=operations['sub']
                    out_str+='0'*2
                    out_str+=registers[instruction[1]]
                    out_str+=registers[instruction[2]]
                    out_str+=registers[instruction[3]]
                    out_lst.append(f'{out_str}\n')
                elif instruction[0]=='ld':
                    out_str+=operations['ld']
                    out_str+='0'*1
                    out_str+=registers[instruction[1]]
                    out_str+='0'*(7-len(bin(var_dict[instruction[2]])[2:]))+bin(var_dict[instruction[2]])[2:]
                    out_lst.append(f'{out_str}\n')
                elif instruction[0]=='div':
                    out_str+=operations['div']
                    out_str+='0'*5
                    out_str+=registers[instruction[1]]
                    out_str+=registers[instruction[2]]
                    out_lst.append(f'{out_str}\n')
                elif instruction[0]=='rs':
                    out_str+=operations['rs']
                    out_str+='0'*1
                    out_str+=registers[instruction[1]]
                    out_str+=bin(int(instruction[2][1:]))[2:]
                    out_lst.append(f'{out_str}\n')
                elif instruction[0]=='ls':
                    out_str+=operations['ls']
                    out_str+='0'*1
                    out_str+=registers[instruction[1]]
                    out_str+=bin(int(instruction[2][1:]))[2:]    
                    out_lst.append(f'{out_str}\n')
                elif instruction[0]=='xor':
                    out_str+=operations['xor']
                    out_str+='0'*2
                    out_str+=registers[instruction[1]]
                    out_str+=registers[instruction[2]]
                    out_str+=registers[instruction[3]]
                    out_lst.append(f'{out_str}\n')
                elif instruction[0]=='or':
                    out_str+=operations['or']    
                    out_str+='0'*2
                    out_str+=registers[instruction[1]]
                    out_str+=registers[instruction[2]]
                    out_str+=registers[instruction[3]]
                    out_lst.append(f'{out_str}\n')
                elif instruction[0]=='and':
                    out_str+=operations['and']
                    out_str+='0'*2
                    out_str+=registers[instruction[1]]
                    out_str+=registers[instruction[2]]
                    out_str+=registers[instruction[3]]
                    out_lst.append(f'{out_str}\n')
                elif instruction[0]=='not':
                    out_str+=operations['not']
                    out_str+='0'*5
                    out_str+=registers[instruction[1]]
                    out_str+=registers[instruction[2]]  
                    out_lst.append(f'{out_str}\n')
                elif instruction[0]=='cmp':
                    out_str+=operations['cmp']
                    out_str+='0'*5
                    out_str+=registers[instruction[1]]
                    out_str+=registers[instruction[2]]
                    out_lst.append(f'{out_str}\n')
                elif instruction[0]=='jmp':
                    out_str+=operations['cmp']
                    out_str+='0'*4
                    out_str+='0'*(7-len(bin(var_dict[instruction[2]])[2:]))+bin(var_dict[instruction[2]])[2:]
                    out_lst.append(f'{out_str}\n')
                elif instruction[0]=='jlt':
                    out_str+=operations['jlt']
                    out_str+='0'*4
                    out_str+='0'*(7-len(bin(var_dict[instruction[2]])[2:]))+bin(var_dict[instruction[2]])[2:]
                    out_lst.append(f'{out_str}\n')
                elif instruction[0]=='jgt':
                    out_str+=operations['jgt']
                    out_str+='0'*4
                    out_str+='0'*(7-len(bin(var_dict[instruction[2]])[2:]))+bin(var_dict[instruction[2]])[2:]
                    out_lst.append(f'{out_str}\n')        
                elif instruction[0]=='je':
                    out_str+=operations['je']
                    out_str+='0'*4
                    out_str+='0'*(7-len(bin(var_dict[instruction[2]])[2:]))+bin(var_dict[instruction[2]])[2:]
                    out_lst.append(f'{out_str}\n')

# Opening output file and writing data to it given if no errors
out_file=open(r"stdout.txt","w")
for line in out_lst:
    out_file.write(line)
out_file.close()

