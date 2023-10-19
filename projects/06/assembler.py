import sys
import string

num='0123456789'
def main():
    assembly_file = sys.argv[1]
    print(f'assemplying file: {assembly_file}')

    #read in the content of the file
    with open(assembly_file, 'r') as f:
        s = f.read()
    li = []
    lis = []
    lise = []
    s = s.split('\n')
    def cstrip(string):
        l = []
        string = string.split(' ')
        for i in string:
            if not i == '' and not i.startswith('//'):
                l.append(i)
                stri = l[0]
        return stri

    def striplist(list): #ger rid of all '//' after c_ins
        lisfinal = []
        for i in lis:
            if i.startswith('@'):
                lisfinal.append(i)
            if '//' in i:
                i = cstrip(i)
                lisfinal.append(i)
        return lisfinal

    for i in s: #get rid of //line
        if not i.startswith('//'):
            li.append(i)
    for i in li: #get rid of extra elements
        if i !='' and i != '\t':
            i = i.strip()
            lis.append(i)
    # print(lis)  #list without '//'

    a = ''.join(lis) #choose regular or L version of asm
    # print(a)
    if '//' in a:
        fin = striplist(lis)
    else:
        fin = lis    
    # print(fin) #list include (symbol) and @variable
    #organize '@symbol' syntax 
    address = 0
    l_count = []
    lis_copy = lis
    # print(lis_copy)
    for i in lis_copy: #get (symbol) location
        if i.startswith('('):
            a = i
            l_count.append(address)
        else:
            address += 1
    # print(l_count)
    a_value = ['@'+str(i) for i in l_count] #list of value of (symbol)
    # print(a_value)
    l_symbol = [i[1:-1] for i in lis if i.startswith('(')]
    # print(l_symbol) #list of (symbol)
    l_symbol = ['@' + i for i in l_symbol]
    symbol = zip(l_symbol,a_value)
    symbol_dict = dict(symbol)
    # print(symbol_dict) #dictionay of {'@symbol':'@value'}

    # replace R0...
    symboldict = {'@R0':'@0','@R1':'@1','@R2':'@2','@R3':'@3','@R4':'@4','@R5':'@5','@R6':'@6','@R7':'@7','@R8':'@8','@R9':'@9','@R10':'@10','@R11':'@11','@R12':'@12','@R13':'@13','@R14':'@14','@R15':'@15','@SCREEN':'@16384','@KBD':'@24576','@SP':'@0','@LCL':'@1','@ARG':'@2','@THIS':'@3','@THAT':'@4'}
    repfin = [symboldict[x] if x in symboldict else x for x in fin]
    # print(repfin) # list of '@variable in symboldict.values()'
    repsym = [symbol_dict[x] if x in symbol_dict else x for x in repfin]
    for i in repsym:     #filter (content)
        if i.startswith('('):
            repsym.remove(i)
    # print(repsym) #list get rid of (symbol) but with @variale

    count_sym = [i for i in range(16,300000) if i!= 16384 and 1 != 24576]
    count_l = [i for i in count_sym if i not in a_value]
    lva = []
    no_dub = set()
    for i in repsym:
        if i.startswith('@') and i[1].isalpha():
            if i not in no_dub:
                no_dub.add(i)
                lva.append(i)             
    # print('lva=',lva)     
    num_v = len(lva)
    cut_l = ['@' + str(i) for i in count_l[:num_v]]
    # print(cut_l)
    final = zip(lva,cut_l)
    finaldic = dict(final)
    # print(finaldic)
    def merge_two_dicts(x, y):
        z = x.copy()   # start with keys and values of x
        z.update(y)    # modifies z with keys and values of y
        return z
    d = merge_two_dicts(symbol_dict,finaldic)
    # print(d)
    dd = merge_two_dicts(d,symboldict)
    # print(dd)
    # print(len(dd))
    final_list = [dd[x] if x in dd else x for x in repsym]
    # print(final_list) #len=23
    # print(len(final_list))

    def trans_a(string):
        ta = str.maketrans('@','0')
        numa = string[0].translate(ta)
        numb='{0:15b}'.format(int(string[1:]))
        numb=numb.replace(' ','0')
        return numa+numb
    # print(trans_a('@17'))

    compz = '0101010'
    compo = '0111111'
    c_negone = '0111010'
    compd = '0001100'
    compa = '0110000'
    compm = '1110000'
    c_notd = '0001101'
    c_nota = '0110001'
    c_notm = '1110001'
    c_negd = '0001111'
    c_nega = '0110011'
    c_negm = '1110011'
    c_dpone = '0011111'
    c_apone = '0110111'
    c_mpone = '1110111'
    c_dmone = '0001110'
    c_amone = '0110010'
    c_mmone = '1110010'
    compdpa = '0000010'
    compdpm = '1000010'
    compdma = '0010011'
    compdmm = '1010011'
    compamd = '0000111'
    compmmd = '1000111'
    c_danda = '0000000'
    c_dandm = '1000000'
    c_dora = '0010101'
    c_dorm = '1010101'

    destm = '001'
    destd = '010'
    destmd = '011'
    desta = '100'
    destam = '101'
    destad = '110'
    destamd = '111'

    jgt = '001'
    jeq = '010'
    jge = '011'
    jlt = '100'
    jne = '101'
    jle = '110'
    jmp = '111'

    def trans_nojump(string):
        dest,comp = string.split('=')
        if dest == 'D' and comp =='A':
            new = '111' + compa + destd + '000'
        if dest == 'D' and comp == 'D+A':
            new = '111' + compdpa + destd + '000'
        if dest == 'M' and comp == 'D':
            new = '111' + compd + destm +'000'
        if dest == 'D' and comp == 'M':
            new = '111' + compm + destd +'000'
        if dest == 'D' and comp == 'D-M':
            new = '111' + compdmm + destd +'000'
        if dest == 'A' and comp == 'M':
            new = '111' + compm + desta +'000'
        if dest == 'M' and comp == '-1':
            new = '111' + c_negone + destm + '000'
        if dest == 'MD' and comp == 'M-1':
            new = '111' + c_mmone + destmd + '000'
        if dest == 'AM' and comp == 'M-1':
            new = '111' + c_mmone + destam + '000'
        if dest == 'A' and comp == 'A-1':
            new = '111' + c_amone + desta + '000'  
        if dest == 'D' and comp == 'M-D':
            new = '111' + compmmd + destd + '000'   
        if dest == 'M' and comp == '0':
            new = '111' + compz + destm + '000' 
        if dest == 'A' and comp == 'M-1':
            new = '111' + c_mmone + desta + '000'
        if dest == 'A' and comp == 'M-D':
            new = '111' + compmmd +desta +'000'
        if dest == 'M' and comp == 'D+1':
            new = '111' + c_dpone +destm +'000'
        if dest == 'AM' and comp == 'D-1':
            new = '111' + c_dmone +destam +'000'
        if dest == 'AM' and comp == 'M+1':
            new = '111' + c_mpone +destam +'000'
        if dest == 'D' and comp == 'D+M':
            new = '111' + compdpm +destd +'000'
        if dest == 'MD' and comp == 'M+1':
            new = '111' + c_mpone +destmd +'000'
        if dest == 'A' and comp == 'M+1':
            new = '111' + c_mpone +desta +'000'
        if dest == 'A' and comp == 'A+1':
            new = '111' + c_apone +desta +'000'
        if dest == 'A' and comp == 'D+A':
            new = '111' + compdpa +desta +'000'
        if dest == 'M' and comp == 'M-D':
            new = '111' + compmmd +destm +'000'
        if dest == 'M' and comp == 'M+1':
            new = '111' + c_mpone +destm +'000'
        if dest == 'M' and comp == '!M':
            new = '111' + c_notm +destm +'000'
        if dest == 'M' and comp == 'D+M':
            new = '111' + compdpm +destm +'000'
        if dest == 'D' and comp == 'D-1':
            new = '111' + c_dmone +destd +'000'
        if dest == 'M' and comp == '1':
            new = '111' + compo +destm +'000'
        if dest == 'M' and comp == 'D&M':
            new = '111' + c_dandm +destm +'000'
        if dest == 'M' and comp == 'D|M':
            new = '111' + c_dorm +destm +'000'
        if dest == 'D' and comp == '!M':
            new = '111' + c_notm +destd +'000'
        if dest == 'AD' and comp == 'A+1':
            new = '111' + c_apone +destad +'000'
        return new

    def trans_onlyjump(string):
        comp,jump = string.split(';')
        if comp == 'D' and jump == 'JGT':
            num = '111' + compd + '000' +  jgt
        if comp == '0' and jump == 'JMP':
            num = '111' + compz +'000' + jmp
        if comp == 'D' and jump == 'JLE':
            num = '111' + compd +'000' + jle  
        if comp == 'D' and jump == 'JNE':
            num = '111' + compd +'000' + jne 
        if comp == 'D' and jump == 'JGE':
            num = '111' + compd +'000' + jge
        return num

    for i in final_list: #tranfer @num
        if i.startswith('@'):
            i = trans_a(i)
        if '=' in i:
            i = trans_nojump(i)
        if ';' in i:
            i = trans_onlyjump(i)
        lise.append(i)
    print(lise)

    with open(assembly_file[:-4]+'.hack', 'w') as f:
        f.write('\n'.join(lise))





if __name__ == '__main__':
    main()