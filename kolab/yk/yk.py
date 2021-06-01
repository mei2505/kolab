import sys
import pegtree as pg
import csv

peg = pg.grammar('yk.tpeg')
parse = pg.generate(peg)

VAR = 'ABCDEFEGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def replace_as_special_parameter(s, mapped):
    if s in mapped:
        return mapped[s]
    x = '<' + VAR[len(mapped)] +'>' #辞書
    mapped[s] = x
    return x

def convert_nothing(tok, doc, mapped):
    s = str(tok)
    if s == ';':  # ; だけはセミコロンに変える
        return '<sep>'
    return s

def convert_all(tok, doc, mapped):
    tag = tok.getTag()
    s = str(tok)
    if tag == 'Name':
        if s in doc:  # 変数名の特殊記号化
            return replace_as_special_parameter(s, mapped)
        else:
            if s.startswith('.'):
                s = '. ' + s[1:]
            return s
    if tag == 'Value' and s in doc: # 値リテラルの特殊記号化
        return replace_as_special_parameter(s, mapped)
    return convert_nothing(tok, doc, mapped)

def make(code, doc0, convert=convert_all):
    #print('BEFORE', code, doc)
    mapped = {}
    doc = []
    flag=0
    for tok in parse(doc0):
        s = str(tok)
        if tok.getTag() == 'Raw':
            q = f"'{s}'"
            q2 = f'"{s}"'
            if q in code:
                #print(f'`{s}` => {q}')
                doc.append(q)
                flag=1
                continue
            if q2 in code:
                #print(f'`{s}` => {q2}')
                doc.append(q2)
                flag=1
                continue
            print('@', s, code)
        doc.append(s)
    #doc = [str(tok) for tok in parse(doc)]
    ws = [convert(tok, doc, mapped) for tok in parse(code)]
    code = ' '.join(ws)
    ws = [mapped[tok] if tok in mapped else tok for tok in doc if tok.strip() != '']
    doc = ' '.join(ws)
    # if flag == 1:
    #     print('AFTER ', code, doc)
    return code, doc

# make('open(a, "file.txt", "w")', '書き込みモードでファイル"file.txt"を開く')
# make('a+b', 'aにbを足した値')
# make('a[-1]', 'aの末尾')
# make('while fib[-1] < 4000000:', 'fibの末尾要素が4000000未満の間繰り返し')
# make('while fib[-1] < sin(x)', 'fibの末尾要素が_sin(x)未満の間、繰り返し')
# make("data['名前'].values", "dataの'名前'カラムの配列")
# make('temp=a;a=b;b=temp', 'aとbを入れ替える')

make('if a> 0: <blk>print(a)</blk>', 'もし`a`が正の数ならば`a`を表示する', convert_all)
make('if a> 0: <blk>print(a)</blk>', 'もしaが正の数ならばaを表示する', convert_nothing)


def read_tsv(filename):
    with open(filename) as f:
        with open('result_yk.tsv', 'w') as f2:
            reader = csv.reader(f, delimiter='\t')
            writer = csv.writer(f2, delimiter='\t')

            for row in reader:
                code, doc = make(row[0], row[1])
                writer.writerow([code, doc])

if __name__ == '__main__':
    for f in sys.argv[1:]:
        read_tsv(f)
