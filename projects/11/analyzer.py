import sys
from pathlib import Path
from tokenizer import tokenize, check_tokenizer
from CompilationEngine import compile, check_compiler



if __name__ == '__main__':
    tokenizer_path = Path(sys.argv[1])
    if tokenizer_path.is_file() and tokenizer_path.suffix == '.jack':
        tokenize(tokenizer_path)
        check_tokenizer(tokenizer_path)
        inpath = tokenizer_path.with_stem('_' + tokenizer_path.stem + 'T').with_suffix('.xml')
        outpath = tokenizer_path.with_stem('_' + tokenizer_path.stem).with_suffix('.xml')
        compile(inpath, outpath)
        check_compiler(tokenizer_path)
    elif tokenizer_path.is_dir():
        for each in tokenizer_path.glob('*.jack'):
            tokenize(each)
            check_tokenizer(each)
            inpath = each.with_stem('_' + each.stem + 'T').with_suffix('.xml')
            outpath = each.with_stem('_' + each.stem).with_suffix('.xml')
            compile(inpath, outpath)
            check_compiler(each)
