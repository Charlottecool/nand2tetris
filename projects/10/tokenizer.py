from pathlib import Path
from utils import XML, Ref


def tokenize(tokenizer_file:Path):
    
    print(f'tokenizer_file:{tokenizer_file}')

    raw_text = Path(tokenizer_file).read_text()
    text_ref = Ref(raw_text)
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
        
        #debug
        import pdb;pdb.set_trace()

        raise Exception(f'failed to eat any tokens this time. remaining text: "{text_ref.value}"')

    #save the file
    b = tokenizer_file.with_stem('_' + tokenizer_file.stem + 'T').with_suffix('.xml')
    f = str(root)
    b.write_text(f)

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
    return XML('stringConstant', [string])

import subprocess
def check_tokenizer(path:Path):
    my_xml = path.with_stem('_' + path.stem + 'T').with_suffix('.xml')
    their_xml = path.with_stem(path.stem + 'T').with_suffix('.xml')

    print(f'comparing {their_xml} to {my_xml}')
    res = subprocess.run(['bash', '../../tools/TextComparer.sh', their_xml, my_xml])


