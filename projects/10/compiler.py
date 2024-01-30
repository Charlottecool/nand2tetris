from pathlib import Path
from utils import XML, Ref

def compile(path:Path):
    print(f'compiler_file:{path}')

    #load tokens xml
    b = path.with_stem('_' + path.stem + 'T').with_suffix('.xml')
    text = b.read_text()
    xml = XML.from_string(text)
    tokens = xml.children
    print('tokens=',tokens) #tokenizer_file
    return

def CompileClass():
    pass 

def CompileClassVarDec():
    pass  

def compileParameterList():
    pass 

def CompileVarDec():
    pass

def compileStatements():
    pass

def compileDo():
    pass

def compileLet():
    pass

def compileWhile():
    pass

def compileReturn():
    pass 

def compileIf():
    pass

def CompileExpression():
    pass 

def CompileTerm():
    pass

def CompileExpressionList():
    pass


def check_compiler(path:Path):
    pass
    return

