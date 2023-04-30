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
file_1=open(r"stdout.txt","w")
y=x.readlines()
#file_1.write(y)
count=0

for n in y:
    if 'var' in n:
        count+=1
#file_1.write(count)        
        
count1=-count

for u in y:
    if u!='\n':
        count1+=1
#file_1.write(count1) 

d={}

for r in y:
    if 'var' in r:
        r=r.replace(" ","")
        #file_1.write(r)
        d[r[3]]=count1
        count1+=1        
#file_1.write(d)

for i in y:
    s=""
    if i!='\n':
        z1=i.split(" ")
        k=0
        while k<len(z1):
            z1[k]=z1[k].strip()
            k+=1
     #   file_1.write(z1)
        z=[]
        for t in z1:   
            if t!='':
                z.append(t)

 #       file_1.write(z)
        n=0
        if z[0]!='var':
                if z[0]=='mov':
                    if '$' in z[2]:
                        s+=operations['mov']
                        s+='0'
                        s+=registers[z[1]]
                        s+='0'*(7-len(bin(int(z[2][1:]))[2:]))
                        s+=bin(int(z[2][1:]))[2:]    
                        file_1.write(f'{s}\n')
                    else:
                        s+=operations['mov1']
                        s+='0'*5
                        s+=registers[z[1]]
                        s+=registers[z[2]]
                        file_1.write(f'{s}\n')
                elif z[0]=='mul':
                    s+=operations['mul']
                    s+='0'*2
                    s+=registers[z[1]]
                    s+=registers[z[2]]
                    s+=registers[z[3]]
                    file_1.write(f'{s}\n')
                elif z[0]=='st':
                    s+=operations['st']    
                    s+='0'
                    s+=registers[z[1]]
                    s+='0'*(7-len(bin(d[z[2]])[2:]))+bin(d[z[2]])[2:]
                    file_1.write(f'{s}\n')
                elif z[0]=='hlt':
                    s+=operations['hlt']
                    s+=11*'0'
                    file_1.write(f'{s}\n')
                    break
                elif z[0]=='add':
                    s+=operations['add']
                    s+='0'*2
                    s+=registers[z[1]]
                    s+=registers[z[2]]
                    s+=registers[z[3]]
                    file_1.write(f'{s}\n')
                elif z[0]=='sub':
                    s+=operations['sub']
                    s+='0'*2
                    s+=registers[z[1]]
                    s+=registers[z[2]]
                    s+=registers[z[3]]
                    file_1.write(f'{s}\n')
                elif z[0]=='ld':
                    s+=operations['ld']
                    s+='0'*1
                    s+=registers[z[1]]
                    s+='0'*(7-len(bin(d[z[2]])[2:]))+bin(d[z[2]])[2:]
                    file_1.write(f'{s}\n')
                elif z[0]=='div':
                    s+=operations['div']
                    s+='0'*5
                    s+=registers[z[1]]
                    s+=registers[z[2]]
                    file_1.write(f'{s}\n')
                elif z[0]=='rs':
                    s+=operations['rs']
                    s+='0'*1
                    s+=registers[z[1]]
                    s+=bin(int(z[2][1:]))[2:]
                    file_1.write(f'{s}\n')
                elif z[0]=='ls':
                    s+=operations['ls']
                    s+='0'*1
                    s+=registers[z[1]]
                    s+=bin(int(z[2][1:]))[2:]    
                    file_1.write(f'{s}\n')
                elif z[0]=='xor':
                    s+=operations['xor']
                    s+='0'*2
                    s+=registers[z[1]]
                    s+=registers[z[2]]
                    s+=registers[z[3]]
                    file_1.write(f'{s}\n')
                elif z[0]=='or':
                    s+=operations['or']    
                    s+='0'*2
                    s+=registers[z[1]]
                    s+=registers[z[2]]
                    s+=registers[z[3]]
                    file_1.write(f'{s}\n')
                elif z[0]=='and':
                    s+=operations['and']
                    s+='0'*2
                    s+=registers[z[1]]
                    s+=registers[z[2]]
                    s+=registers[z[3]]
                    file_1.write(f'{s}\n')
                elif z[0]=='not':
                    s+=operations['not']
                    s+='0'*5
                    s+=registers[z[1]]
                    s+=registers[z[2]]  
                    file_1.write(f'{s}\n')
                elif z[0]=='cmp':
                    s+=operations['cmp']
                    s+='0'*5
                    s+=registers[z[1]]
                    s+=registers[z[2]]
                    file_1.write(f'{s}\n')
                elif z[0]=='jmp':
                    s+=operations['cmp']
                    s+='0'*4
                    s+='0'*(7-len(bin(d[z[2]])[2:]))+bin(d[z[2]])[2:]
                    file_1.write(f'{s}\n')
                elif z[0]=='jlt':
                    s+=operations['jlt']
                    s+='0'*4
                    s+='0'*(7-len(bin(d[z[2]])[2:]))+bin(d[z[2]])[2:]
                    file_1.write(f'{s}\n')
                elif z[0]=='jgt':
                    s+=operations['jgt']
                    s+='0'*4
                    s+='0'*(7-len(bin(d[z[2]])[2:]))+bin(d[z[2]])[2:]
                    file_1.write(f'{s}\n')        
                elif z[0]=='je':
                    s+=operations['je']
                    s+='0'*4
                    s+='0'*(7-len(bin(d[z[2]])[2:]))+bin(d[z[2]])[2:]
                    file_1.write(f'{s}\n')
                    


                    








