import sys
import string
from pathlib import Path

def main():
    vmtrans_file = sys.argv[1]
    print(f'vmtrans_file: {vmtrans_file}')

    with open(vmtrans_file, 'r') as f:
        s = f.read()

    filepath = Path(sys.argv[1])

    def clean_string(string): #get rid of '//'
        s = string.split('\n')
        l = []
        for i in s:
            if not i == '' and not i.startswith('//'):
                l.append(i)
        return l
    s = clean_string(s)
    print(s)
    def read_string(string):
        string = string.split(' ')
        return string[-1]

    def push_constant(string):
        st = read_string(string)
        s = [f'@{st}']
        ls = s + ['D=A','@SP','AM=M+1','A=A-1','M=D']
        return ls

    def push_local(string):
        st = read_string(string)
        s = [f'@{st}']
        ls = ['@LCL','D=M'] + s + ['A=A+D','D=M','@SP','AM=M+1','A=A-1','M=D']
        return ls

    def pop_local(string):
        st = read_string(string)
        s = [f'@{st}']
        ls = ['@LCL','D=M'] + s + ['D=D+A','@R13','M=D','@SP','AM=M-1','D=M','@R13','A=M','M=D']
        return ls

    def push_argument(string):
        st = read_string(string)
        s = [f'@{st}']
        ls = ['@ARG','D=M'] + s + ['A=A+D','D=M','@SP','AM=M+1','A=A-1','M=D']
        return ls

    def pop_argument(string):
        st = read_string(string)
        s = [f'@{st}']
        ls = ['@ARG','D=M'] + s + ['D=D+A','@R13','M=D','@SP','AM=M-1','D=M','@R13','A=M','M=D']
        return ls

    def pop_this(string):
        st = read_string(string)
        s = [f'@{st}']
        ls = ['@THIS','D=M'] + s + ['D=D+A','@R13','M=D','@SP','AM=M-1','D=M','@R13','A=M','M=D']
        return ls

    def pop_that(string):
        st = read_string(string)
        s = [f'@{st}']
        ls = ['@THAT','D=M'] + s + ['D=D+A','@R13','M=D','@SP','AM=M-1','D=M','@R13','A=M','M=D']
        return ls

    def push_that(string):
        st = read_string(string)
        s = [f'@{st}']
        ls = ['@THAT','D=M'] + s + ['A=A+D','D=M','@SP','AM=M+1','A=A-1','M=D']
        return ls

    def push_this(string):
        st = read_string(string)
        s = [f'@{st}']
        ls = ['@THIS','D=M'] + s + ['A=A+D','D=M','@SP','AM=M+1','A=A-1','M=D']
        return ls

    def push_temp(string):
        st = read_string(string)
        i = int(st)
        s = [f'@{i+5}']
        ls = s + ['D=M','@SP','AM=M+1','A=A-1','M=D']
        return ls

    def pop_temp(string):
        st = read_string(string)
        i = int(st)
        s = [f'@{i+5}']
        ls = ['@SP','AM=M-1','D=M'] + s + ['M=D']
        return ls

    def push_pointer0(string): 
        ls = ['@THIS','D=M','@SP','A=M','M=D','@SP','M=M+1']
        return ls

    def push_pointer1(string):
        ls = ['@THAT','D=M','@SP','A=M','M=D','@SP','M=M+1']
        return ls

    def pop_pointer0(string): 
        ls = ['@SP','M=M-1','@THIS','M=D']
        return ls

    def pop_pointer1(string):
        ls = ['@SP','M=M-1','@THAT','M=D']
        return ls

    def pop_static(string):
        st = read_string(string)
        s = [f'@{st}']
        sa = f'@{filepath.stem}' + f'.{st}'
        ls = [sa,'D=M'] + s + ['D=D+A','@R13','M=D','@SP','AM=M-1','D=M','@R13','A=M','M=D']
        return ls 

    def push_static(string):
        st = read_string(string)
        s = [f'@{st}']
        sa = f'@{filepath.stem}' + f'.{st}'
        ls = [sa,'D=M'] + s + ['A=A+D','D=M','@SP','AM=M+1','A=A-1','M=D']
        return ls

    def add(string):
        add = ['@SP','AM=M-1','D=M','A=A-1','M=D+M']
        return add

    def sub(string):
        sub = ['@SP','AM=M-1','D=M','A=A-1','M=M-D']
        return sub

    count = 0
    def eq(string):
        nonlocal count
        eq = ['@SP','AM=M-1','D=M','A=A-1','M=M-D','@SP','A=M','A=A-1','D=M',f'@LABEL{count}','D;JEQ','@SP','A=M','A=A-1','M=0',f'@DONE{count}','0;JMP',f'(LABEL{count})','@SP','A=M','A=A-1','M=-1',f'(DONE{count})']
        count += 1
        return eq

    def lt(string):
        nonlocal count
        ltt = ['@SP','AM=M-1','D=M','A=A-1','M=M-D','@SP','A=M','A=A-1','D=M',f'@LABEL{count}','D;JLT','@SP','A=M','A=A-1','M=0',f'@DONE{count}','0;JMP',f'(LABEL{count})','@SP','A=M','A=A-1','M=-1',f'(DONE{count})']
        count += 1
        return ltt

    def gt(string):
        nonlocal count
        gtt = ['@SP','AM=M-1','D=M','A=A-1','M=M-D','@SP','A=M','A=A-1','D=M',f'@LABEL{count}','D;JGT','@SP','A=M','A=A-1','M=0',f'@DONE{count}','0;JMP',f'(LABEL{count})','@SP','A=M','A=A-1','M=-1',f'(DONE{count})']
        count += 1
        return gtt

    def neg(string):
        neggg = ['@SP','A=M-1','M=-M']
        return neggg

    def andd(string):
        andaa = ['@SP','AM=M-1','D=M','A=A-1','M=M&D']
        return andaa

    def orr(string):
        orrrr = ['@SP','AM=M-1','D=M','A=A-1','M=M|D']
        return orrrr

    def nott(string):
        nottttt = ['@SP','A=M-1','M=!M']
        return nottttt

    l_pp=[]
    for i in s:
        if i.startswith('push c'):
            pu_c = push_constant(i)
            l_pp.extend(pu_c)
            continue
        if i.startswith('pop l'):
            po_l = pop_local(i)
            l_pp.extend(po_l)
            continue 
        if i.startswith('push arg'):
            pu_arg = push_argument(i)
            l_pp.extend(pu_arg)
            continue
        if i.startswith('pop a'):
            po_a = pop_argument(i)
            l_pp.extend(po_a)
            continue   
        if i.startswith('pop this'):
            po_this = pop_this(i)
            l_pp.extend(po_this)
            continue
        if i.startswith('pop that'):
            po_that = pop_that(i)
            l_pp.extend(po_that)
            continue
        if i.startswith('pop temp'):
            po_temp = pop_temp(i)
            l_pp.extend(po_temp)
            continue
        if i.startswith('push temp'):
            pu_temp = push_temp(i)
            l_pp.extend(pu_temp)
            continue
        if i.startswith('push l'):
            pu_l = push_local(i)
            l_pp.extend(pu_l)
            continue
        if i.startswith('push that'):
            pu_that = push_that(i)
            l_pp.extend(pu_that)
            continue
        if i.startswith('push this'):
            pu_this = push_this(i)
            l_pp.extend(pu_this)
            continue
        if i == 'pop pointer 0':
            po_poin0 = pop_pointer0(i)
            l_pp.extend(po_poin0)
            continue
        if i == 'pop pointer 1':
            po_poin1 = pop_pointer1(i)
            l_pp.extend(po_poin1)
            continue
        if i == 'push pointer 0':
            pu_poin0 = push_pointer0(i)
            l_pp.extend(pu_poin0)
            continue
        if i == 'push pointer 1':
            pu_poin1 = push_pointer1(i)
            l_pp.extend(pu_poin1)
            continue
        if i.startswith('pop static'):
            po_static = pop_static(i)
            l_pp.extend(po_static)
            continue
        if i.startswith('push static'):
            pu_static = push_static(i)
            l_pp.extend(pu_static)
            continue
        if i == 'add':
            ad = add(i)
            l_pp = l_pp + ad
            continue
        if i == 'sub':
            su = sub(i)
            l_pp = l_pp + su 
            continue 
        if i == 'eq':
            eqa = eq(i)
            l_pp = l_pp + eqa 
            continue
        if i == 'lt':
            lta = lt(i)
            l_pp = l_pp + lta 
            continue
        if i == 'gt':
            gta = gt(i)
            l_pp = l_pp + gta
            continue
        if i == 'neg':
            nega = neg(i)
            l_pp = l_pp + nega
            continue
        if i == 'and':
            anda = andd(i)
            l_pp = l_pp + anda
            continue
        if i == 'or':
            ora = orr(i)
            l_pp = l_pp + ora
            continue
        if i == 'not':
            nota = nott(i)
            l_pp = l_pp + nota
    l_pp = l_pp + ['(END)','@END','0;JMP',]
    print(l_pp)
    # with open(vmtrans_file[:-3]+'.asm', 'w') as f:
        # f.write('\n'.join(l_pp))

if __name__ == '__main__':
    main()