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

x=open(r"C:\Sahil\Python\CSE112-Assignment\input.txt","r+")
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
        while n<len(z):
            if z[0]=='mov':
                if '$' in z[2]:
                    s+=operations['mov']
                    n+=1
                else:
                    s+=operations['mov1']
                    n+=1
<<<<<<< HEAD
                

            n+=1        
=======
            else:                
                s+=operations[z[0]]
                n += 1
>>>>>>> 4a76f950f2a5be73a8541cd451f3f4cfa54b9ac8




                

