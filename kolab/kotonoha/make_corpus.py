import sys
import random
import kolab.pj.piece as piece
import collections

#tokenize_pj = piece.load_tokenizer('aoj8k.model')
tokenize_pj = piece.load_tokenizer()


def read_corpus(filename):
    pj = ''
    D = {}
    c = 0
    with open(filename) as f:
        for line in f.readlines():
            if line.startswith('#'):
                pj = line[1:].strip()
            else:
                if pj == '':
                    continue
                c += 1
                if pj not in D:
                    D[pj] = line.strip()
    return D


def vocab_update(tokens, vocab):
    for tok in tokens:
        vocab.add(tok)
    return ' '.join(tokens)+'\n'


def vocab_check(tokens, vocab):
    for tok in tokens:
        if tok not in vocab:
            if tok.isdigit():
                tok = '1'
            else:
                tok = 'unk'
    return ' '.join(tokens)+'\n'


def write_corpus(D, prefix='data'):
    D = [(ja, py) for ja, py in D.items()]
    random.shuffle(D)
    train_size = int(len(D) * 0.8)
    valid_size = (len(D) - train_size)//2
    test_size = len(D) - train_size - valid_size
    print(f'train: {train_size} valid: {valid_size}')
    vocpj = set()
    vocpy = set()
    with open(f'{prefix}/train.ja', 'w') as wja:
        with open(f'{prefix}/train.py', 'w') as wpy:
            for ja, py in D[:train_size]:
                wja.write(vocab_update(tokenize_pj(ja), vocpj))
                wpy.write(vocab_update((py).split(' '), vocpy))
            wja.write('未定義\n')
            wpy.write('unk\n')
    with open(f'{prefix}/valid.ja', 'w') as wja:
        with open(f'{prefix}/valid.py', 'w') as wpy:
            for ja, py in D[train_size:train_size+valid_size]:
                wja.write(vocab_check(tokenize_pj(ja), vocpj))
                wpy.write(vocab_check((py).split(' '), vocpy))
    with open(f'{prefix}/test.ja', 'w') as wja:
        with open(f'{prefix}/test.py', 'w') as wpy:
            for ja, py in D[train_size:train_size+valid_size]:
                wja.write(vocab_check(tokenize_pj(ja), vocpj))
                wpy.write(vocab_check((py).split(' '), vocpy))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        D = read_corpus(sys.argv[1])
        write_corpus(D)
