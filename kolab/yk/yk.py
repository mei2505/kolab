import pegtree as pg

peg = pg.grammar('yk.tpeg')
parse = pg.generate(peg)

def replace_as_special_parameter(s, mapped):
    if s in mapped:
        return mapped[s]
    x = f'<x{len(mapped)}>'
    mapped[s] = x
    return x

def convert_token(tok, doc, mapped):
    tag = tok.getTag()
    s = str(tok)
    if tag == 'Name' and s in doc:
        return replace_as_special_parameter(s, mapped)
    if tag == 'Value' and s in doc:
        return replace_as_special_parameter(s, mapped)
    return str(tok)

def make(code, doc):
    doc = [str(tok) for tok in parse(doc)]
    mapped = {}
    ws = [convert_token(tok, doc, mapped) for tok in parse(code)]
    code = ' '.join(ws)
    ws = [mapped[tok] if tok in mapped else tok for tok in doc]
    doc = ' '.join(ws)
    print(code, doc)

make('open(a, "file.txt", "w")', '書き込みモードでファイル"file.txt"を開く')
make('a+b', 'aにbを足した値')

make('書き込みモードでファイル"file.txt"を開く', 'a')
make('temp=a<sep>a=b<sep>b=temp', 'aとbを入れ替える')
