import sys
from pathlib import Path
from utils import XML, Ref
from tokenizer import tokenize, check_tokenizer


if __name__ == '__main__':
    tokenizer_path = Path(sys.argv[1])
    if tokenizer_path.is_file() and tokenizer_path.suffix == '.jack':
        tokenize(tokenizer_path)
        check_tokenizer(tokenizer_path)
    elif tokenizer_path.is_dir():
        for each in tokenizer_path.glob('*.jack'):
            tokenize(each)
            check_tokenizer(each)
