import sentencepiece as spm
import pathlib


def iter_alpha(tokens):
    prev = ''
    for tok in tokens:
        if tok.startswith('▁'):
            tok = tok[1:]
        if len(tok) == 0:
            continue
        if tok.isascii() and tok.isalpha():
            prev += tok
        else:
            if prev != '':
                yield prev
                prev = ''
            yield tok

    if prev != '':
        yield prev


def join_alpha(tokens):
    return [tok for tok in iter_alpha(tokens)]


def load_tokenizer(model: str = None):
    import sentencepiece as spm
    if model is None:
        model = str(pathlib.Path(__file__).parent.resolve() / 'prog8k.model')
    sp = spm.SentencePieceProcessor()
    sp.Load(model)

    def tokenize(s: str) -> list[str]:
        tokens = sp.EncodeAsPieces(s)
        if len(tokens) > 0:
            if tokens[0] == '▁':
                tokens.pop(0)
            else:
                tokens[0] = tokens[0][1:]
        return tokens

    def tokenize2(s: str) -> list[str]:
        tokens = sp.EncodeAsPieces(s)
        return join_alpha(tokens)

    return tokenize2


#p = load_tokenizer()
#print(p('_add ( A . leftwindow ) をAのleft2にする'))
