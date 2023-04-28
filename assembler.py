#!/usr/bin/env python

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

registers={'R0':'000',
           'R1':'001',
           'R2':'010',
           'R3':'011',
           'R4':'100',
           'R5':'101',
           'R6':'110',
           'FLAGS':'111'}

x=open(r"stdin.txt","r+")
y=x.readlines()
print(y)

for i in y:
    s=""
    if i!='\n':
        z=i.split(" ")
        k=0
        while k<len(z):
            z[k]=z[k].strip()
            k+=1
        print(z)
        n=0
        if z[0]!='var':
                if z[0]=='mov':
                    if '$' in z[2]:
                        s+=operations['mov']
                        s+='0'
                        s+=registers[z[1]]
                        if len((bin(z[2][1:]))[2:])<7:
                            s+='0'*(7-len((bin(z[2][1:]))[2:]))
                            s+=(bin((z[2])[1:]))[2:]
                            print(f's\n')
                        else:
                            s+=(bin((z[2])[1:]))[2:]
                            print(s+"\n")    
                    else:
                        s+=operations['mov1']
                        s+='0'*5
                        s+=registers[z[1]]
                        s+=registers[z[2]]
                        print(s+"\n")
                elif z[0]=='mul':
                    s+=operations['mul']
                    s+='0'*2
                    s+=registers[z[1]]
                    s+=registers[z[2]]
                    s+=registers[z[3]]
                    print(s+"\n")
                elif z[0]=='st':
                    s+=operations['st']    
                    s+='0'
                    s+=registers[z[1]]
                    s+='0'*(16-len(s))
                    print(s+"\n")
                        
                   

    