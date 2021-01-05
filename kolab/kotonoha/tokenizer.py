import sys
import random
import sentencepiece as spm

sp = spm.SentencePieceProcessor()
sp.Load("prog8k.model")


def tokenize_pj(s):
    tokens = sp.EncodeAsPieces(s)
    if len(tokens) > 0:
        if tokens[0] == '▁':
            tokens.pop(0)
        else:
            tokens[0] = tokens[0][1:]
    return tokens


def read_corpus(filename):
    pj = ''
    D = {}
    with open(filename) as f:
        for line in f.readlines():
            if line.startswith('#'):
                pj = line[1:].strip()
            else:
                if pj == '':
                    continue
                if pj not in D:
                    D[pj] = line.strip()
    return D


def write_corpus(D, prefix='tefu417'):
    D = [(ja, py) for ja, py in D.items()]
    random.shuffle(D)
    train_size = int(len(D) * 0.8)
    valid_size = (len(D) - train_size)//2
    test_size = len(D) - train_size - valid_size
    with open(f'{prefix}/train.ja', 'w') as wja:
        with open(f'{prefix}/train.py', 'w') as wpy:
            for ja, py in D[:train_size]:
                wja.write(' '.join(tokenize_pj(ja)) + '\n')
                wpy.write(py + '\n')
    with open(f'{prefix}/valid.ja', 'w') as wja:
        with open(f'{prefix}/valid.py', 'w') as wpy:
            for ja, py in D[train_size:train_size+valid_size]:
                wja.write(' '.join(tokenize_pj(ja)) + '\n')
                wpy.write(py + '\n')
    with open(f'{prefix}/test.ja', 'w') as wja:
        with open(f'{prefix}/test.py', 'w') as wpy:
            for ja, py in D[train_size:train_size+valid_size]:
                wja.write(' '.join(tokenize_pj(ja)) + '\n')
                wpy.write(py + '\n')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        D = read_corpus(sys.argv[1])
        write_corpus(D)
