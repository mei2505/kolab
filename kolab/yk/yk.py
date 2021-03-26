import pegtree as pg

peg = pg.grammar('yk.tpeg')
parse = pg.generate(peg)

VAR = 'ABCDEFEGHIJKLMNOPQRSTUVWXYZ'

def replace_as_special_parameter(s, mapped):
    if s in mapped:
        return mapped[s]
    x = '<' + VAR[len(mapped)] +'>' #辞書
    #x = f'<x{len(mapped)}>'  #辞書
    mapped[s] = x
    return x

def convert_token(tok, doc, mapped):
    tag = tok.getTag()
    s = str(tok)
    if tag == 'Name' and s in doc:  # 変数名の特殊記号化
        return replace_as_special_parameter(s, mapped)
    if tag == 'Value' and s in doc: # 値リテラルの特殊記号化
        return replace_as_special_parameter(s, mapped)
    return str(tok)

def make(code, doc, convert=convert_token):
    print('BEFORE', code, doc)
    doc = [str(tok) for tok in parse(doc)]
    mapped = {}
    ws = [convert(tok, doc, mapped) for tok in parse(code)]
    code = ' '.join(ws)
    ws = [mapped[tok] if tok in mapped else tok for tok in doc]
    doc = ' '.join(ws)
    print('AFTER ', code, doc)
    return code, doc

#make('open(a, "file.txt", "w")', '書き込みモードでファイル"file.txt"を開く')
#make('temp=a<sep>a=b<sep>b=temp', 'aとbを入れ替える')
#make('a+b', 'aにbを足した値')
#make('a[-1]', 'aの末尾')
#make('while fib[-1] < 4000000:', 'fibの末尾要素が4000000未満の間繰り返し')
make('while fib[-1] < sin(x)', 'fibの末尾要素が_sin(x)未満の間、繰り返し')
make("data['名前'].values", "dataの'名前'カラムの配列")
