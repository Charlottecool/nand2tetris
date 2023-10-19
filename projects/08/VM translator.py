import sys
import string
from pathlib import Path

def main():
    vmtrans_file = sys.argv[1]
    print(f'vmtrans_file: {vmtrans_file}')
    filepath = Path(sys.argv[1])
    #filename = sys.argv[1]
    #print('filename =',filename) ???
    if not filepath.is_dir():
        #handle single file,dont insert bootstapcode
        files = [filepath]
        outpath = filepath.with_suffix('.asm')
        INCLUDE_BOOTSTRAP = False
    else:
        #handle folder 
        files = [*filepath.glob('*.vm')]
        outpath = filepath / f'{filepath.name}.asm'
        INCLUDE_BOOTSTRAP = True

    def clean_string(string): #get rid of '//'
        s = string.split('\n')
        l = []
        for i in s:
            if not i == '' and not i.startswith('//'):
                l.append(i.rstrip())
        return l
    
    # print(li)
    def read_string(string):
        string = string.split(' ')
        return string[-1]

    def push_constant(string):
        # 
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
        ls = ['@SP','M=M-1','A=M','D=M','@THIS','M=D']
        return ls

    def pop_pointer1(string):
        ls = ['@SP','M=M-1','A=M','D=M','@THAT','M=D']
        return ls

    def pop_static(string,filename):
        st = read_string(string)
        s = [f'@{st}']
        sa =f'@{filename.stem}' + f'.{st}'
        ls = ['@SP','M=M-1','A=M','D=M'] + [sa,'M=D'] 
        return ls 

    def push_static(string,filename):
        st = read_string(string)
        s = [f'@{st}']
        sa = f'@{filename.stem}' + f'.{st}'
        ls = [sa,'D=M'] + ['@SP','A=M','M=D','@SP','M=M+1'] 
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

    def label(string):
        lii = []
        s = string.split(' ')
        lii.append(s[1].rstrip('\n'))
        liii = []
        for i in lii:
            i = f'({i})'
            liii.append(i)
        return liii
    
    def goto(string):
        l = []
        s = string.split(' ')
        l.append(s[1].rstrip('\n'))
        lis = []
        for i in l:
            i = f'@{i}'
            lis.append(i)
        lis = lis + ['0;JMP']
        return lis


    def if_goto(string):
        l = []
        s = string.split(' ')
        l.append(s[1].rstrip('\n'))
        lis = []
        for i in l:
            i = f'@{i}'
            lis.append(i)
        lis = ['@SP','M=M-1','A=M','D=M'] + lis + ['D;JNE']
        return lis

    def func_label(string):                   
        sa = string[9:-2]
        ss = ['('+sa+')']
        nums = int(string[-1])
        l = [j for i in range(nums) for j in push_constant('0')]
        li = ss + l
        return li

    def ret(string):
        l = ['@LCL','D=M','@FRAME','M=D',
            '@FRAME','D=M','@5','D=D-A','A=D','D=M','@RET','M=D',
            '@SP','M=M-1','A=M','D=M','@ARG','A=M','M=D',
            '@ARG','D=M+1','@SP','M=D',
            '@FRAME','D=M','@1','D=D-A','A=D','D=M','@THAT','M=D',
            '@FRAME','D=M','@2','D=D-A','A=D','D=M','@THIS','M=D',
            '@FRAME','D=M','@3','D=D-A','A=D','D=M','@ARG','M=D',
            '@FRAME','D=M','@4','D=D-A','A=D','D=M','@LCL','M=D',
            '@RET','A=M','0;JMP']
        return l

    def call_fun(string):
        nonlocal count
        n = int(string[-1])
        sn = [f'@{string[-1]}']
        sa = string[5:-2]
        ss = ['('+sa+')']
        ret_add = [f'(RETURN{count})']
        l = [f'@RETURN{count}','D=A','@SP','A=M','M=D','@SP','M=M+1',
            '@LCL','D=M','@SP','A=M','M=D','@SP','M=M+1',
            '@ARG','D=M','@SP','A=M','M=D','@SP','M=M+1',
            '@THIS','D=M','@SP','A=M','M=D','@SP','M=M+1',
            '@THAT','D=M','@SP','A=M','M=D','@SP','M=M+1',
            '@SP','D=M','@5','D=D-A'] + sn +['D=D-A','@ARG','M=D',
            '@SP','D=M','@LCL','M=D',f'@{sa}','0,JMP'] + ret_add
        count += 1
        return l

    resu = call_fun('call Sys.init 0')

    l_pp=[]

    if INCLUDE_BOOTSTRAP:
        l_pp = l_pp + ['@256','D=A','@SP','M=D']
        l_pp = l_pp + resu

        
    for file in files:
        with open(file, 'r') as f:
            s = f.read()
        s = clean_string(s)
        li = []
        for i in s:
            i = i.split('//')
            li.append(i[0].rstrip())
        
        for i in li:
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
                po_static = pop_static(i,file)
                l_pp.extend(po_static)
                continue
            if i.startswith('push static'):
                pu_static = push_static(i,file)
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
                continue
            if i.startswith('label'):
                la = label(i)
                l_pp = l_pp + la
                continue
            if i.startswith('if-goto'):
                ifgo = if_goto(i)
                l_pp = l_pp + ifgo 
                continue
            if i.startswith('goto'):
                gt = goto(i)
                l_pp = l_pp + gt
                continue
            if i.startswith('function '):
                fun = func_label(i)
                l_pp = l_pp + fun
                continue
            if i.startswith('return'):
                retu = ret(i)
                l_pp = l_pp + retu
                continue
            if i.startswith('call'):
                callf = call_fun(i)
                l_pp = l_pp + callf

    # print(l_pp)
    print(f'wrote to {outpath}')
    with open(outpath, 'w') as f:
        f.write('\n'.join(l_pp))

if __name__ == '__main__':
    main()