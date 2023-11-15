import sys
from pathlib import Path
from utils import XML, Ref


def main(tokenizer_file:Path):
    

    print(f'tokenizer_file:{tokenizer_file}')

    # with open(tokenizer_file,'r') as f:
    #   s = f.read()
    raw_text = Path(tokenizer_file).read_text()
    #print(raw_text)


    text_ref = Ref(raw_text)

    # print('text_ref=',text_ref)
    # print(type(text_ref))

    root = XML('tokens', [])


    while len(text_ref.value) > 0:
        if eat_singlelinecomment(text_ref):
            continue
        if eat_blockcomment(text_ref):
            continue
        if eat_whitespace(text_ref):
            #don't add whitespace to xml. just skip it
            continue
        if (result := eat_keyword(text_ref)) is not None:
            root.append_child(result)
            continue
        if (result := eat_symbol(text_ref)) is not None:
            root.append_child(result)
            continue
        if (result := eat_identifier(text_ref)) is not None:
            root.append_child(result)
            continue
        if (result := eat_integerConstant(text_ref)) is not None:
            root.append_child(result)
            continue
        if (result := eat_StringConstant(text_ref)) is not None:
            root.append_child(result)
            continue
        #other eat functions for other tokens
        import pdb;pdb.set_trace()

        raise Exception(f'failed to eat any tokens this time. remaining text: "{text_ref.value}"')

    b = tokenizer_file.with_stem('_' + tokenizer_file.stem + 'T').with_suffix('.xml')
    f = str(root)
    b.write_text(f)











    # filepath = Path(sys.argv[1])

    # def get_string(string): #get substring from a line
    #   s = string.split('"')
    #   return s[1]

    # def keyword(l):
    #   for i in l:
    #       if 'class' or 'constructor' or 'function' or 'method' or 'field' or 'static' or 'var' or 'int' or 'char' or 'boolean' or 'void' or 'true' or 'false' or 'null' or 'this' or 'let' or 'do' or 'if' or 'else' or 'while' or 'return' in i:
    #       return ('<keyword>',i,'</keyword>')
    #????def tokenType(list): #Returns the type of the current token.
    # for i in or_s:
    #   i = keyword(i)
    #   if '{' or '}' or '(' or ')' or '[' or ']' or '.' or ',' or ';' or '+' or '-' or '*' or '/' or '&' or '|' or '<' or '>' or '=' or '~' in i:
    #       print('symbol')
    #       #return SYMBOL
    #   if num_there(i) is True:
    #       print('int_const')
    #       #return INT_CONST
    #   if '"' in i:
    #       print('string_const')
    #       #return STRING_CONST
    #   else: 
    #       print('identifier')
    #       #return
    # print(or_s)

keywords = {'class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return'}
def eat_keyword(string_ref:Ref[str]) -> XML|None:
    for keyword in keywords:
        if string_ref.value.startswith(keyword) and (len(string_ref.value) == len(keyword) or not string_ref.value[len(keyword)].isalnum()):
            #update the string to get rid of the keyword from the start of it
            string_ref.value = string_ref.value[len(keyword):]
            #return the xml object for that keyword
            return XML('keyword', [keyword])

def eat_whitespace(string_ref:Ref[str]) -> bool|None:
    if string_ref.value.startswith(' ') or string_ref.value.startswith('\n') or string_ref.value.startswith('\t'):
        string_ref.value = string_ref.value[1:]
        return not None

symbols = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~'}
def eat_symbol(string_ref:Ref[str]) -> XML|None:
    for symbol in symbols:
        if string_ref.value.startswith(symbol):
            #update the string to get rid of the symbol from the start of it
            string_ref.value = string_ref.value[len(symbol):]
            #return the xml object for that keyword
            return XML('symbol', [symbol])

def eat_identifier(string_ref:Ref[str]) -> XML|None:
    if string_ref.value[0].isdigit():
        return None
    
    # "apple"
    i = 0
    while i < len(string_ref.value) and (string_ref.value[i].isalnum() or string_ref.value.startswith('_')):
        i += 1
    if i == 0:
        return None
    identifier = string_ref.value[:i]
    string_ref.value = string_ref.value[i:]
    return XML('identifier', [identifier])

def eat_singlelinecomment(string_ref:Ref[str])-> bool|None: #get rid of all // lines
    if not string_ref.value.startswith('//'):
        return None
    lines = string_ref.value.split('\n',1)
    string_ref.value = lines[1]
    return True

def eat_blockcomment(string_ref:Ref[str])-> bool|None: #get rid of all /** lines
    if not string_ref.value.startswith('/*') :
        return None
    lines = string_ref.value.split('*/',1)
    string_ref.value = lines[1]
    return True
   
def eat_integerConstant(string_ref:Ref[str])-> bool|None: #eat all the integers
    i = 0
    while i < len(string_ref.value) and string_ref.value[i].isdigit():
        i += 1
    if i == 0:
        return None
    integer = string_ref.value[:i]
    string_ref.value = string_ref.value[i:]
    return XML('integerConstant', [integer])

def eat_StringConstant(string_ref:Ref[str])-> bool|None: #eat all the strings
    if not string_ref.value.startswith('"'):
        return None
    strings = string_ref.value.split('"',2)
    string_ref.value = strings[2]
    string = strings[1]
    return XML('StringConstant', [string])

if __name__ == '__main__':
    tokenizer_path = Path(sys.argv[1])
    if tokenizer_path.is_file() and tokenizer_path.suffix == '.jack':
        main(tokenizer_path)
    elif tokenizer_path.is_dir():
        for each in tokenizer_path.glob('*.jack'):
            main(each)
