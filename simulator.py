import sys


program_counter=0



def program_counter_update(program_counter):
    program_counter+=1
    binary=bin(program_counter)
    return program_counter


def input_read():
    inp_lines=sys.stdin.readlines()
    return inp_lines

def file_write(out_lst):
    for line in out_lst:
        print(line)


