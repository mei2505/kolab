
import sys
import random
from pegtree.visitor import ParseTreeVisitor
from pegtree import ParseTree
import pegtree as pg

from pj import lemma, Lemma

from logging import getLogger
logger = getLogger(__name__)

EMPTY = tuple()

# オプション

OPTION = {
    'Simple': False,  # シンプルな表現を優先する
    'Block': False,  # Expressionに <e> </e> ブロックをつける
    'ReversePolish': True,  # 膠着語の場合はTrue
    'EnglishFirst': False,  # 英訳の精度を優先する
    'ShuffleSynonym': True,  # 同音異議語をシャッフルする
    'MultipleSentence': True,  # 複数行モード
    'ShuffleOrder': True,  # もし可能なら順序も入れ替える
    'Verbose': True,  # デバッグ出力あり
}

RandomIndex = 0


def randomize():
    global RandomIndex
    if OPTION['ShuffleSynonym']:
        RandomIndex = random.randint(1, 1789)


def random_index(arraysize: int, seed):
    if OPTION['ShuffleSynonym']:
        return (RandomIndex + seed) % arraysize
    return 0


def alt(s: str):
    if '|' in s:
        ss = s.split('|')
        if OPTION['EnglishFirst']:
            return ss[-1]  # 最後が英語
        return ss[random_index(len(ss), len(s))]
    return s


def shuffle(x, y):
    if OPTION['ShuffleSynonym']:
        return x if random.random() < 0.6 else y
    return x

# 自然言語フレーズ


RESULT = 'P結果'
EOS = 'E。'


class NExpr(object):

    def asType(self, typefix):
        return self

    def apply(self, mapped):
        return self

    def __repr__(self):
        return str(self)


class NPiece(NExpr):
    piece: str

    def __init__(self, piece):
        self.piece = piece

    def asType(self, typefix):
        return NPred(self.piece, typefix)

    def __str__(self):
        return self.piece

    def emit(self, typefix, buffer=None):
        return alt(self.piece)


# class NChoice(NExpr):
#     choices: tuple

#     def __init__(self, *choices):
#         self.choices = choices

#     def asType(self, typefix):
#         return NChoice(*[c.asType(typefix) for c in self.choices])

#     def apply(self, mapped):
#         return NChoice(*[c.apply(mapped) for c in self.choices])

#     def __str__(self):
#         return '[' + '|'.join(map(str, self.choices)) + ']'

#     def emit(self, typefix, buffer=None):
#         if OPTION['ShuffleSynonym']:
#             index = random.randrange(0, len(self.choices))
#             return self.choices[index].emit(typefix, buffer)
#         return self.choices[0].emit(typefix, buffer)


class NTuple(NExpr):
    elements: tuple

    def __init__(self, *elements):
        self.elements = tuple(toNExpr(e) for e in elements)

    def asType(self, typefix):
        return NTuple(*[c.asType(typefix) for c in self.elements])

    def apply(self, mapped):
        return NTuple(*[c.apply(mapped) for c in self.elements])

    def __str__(self):
        return '(' + ','.join(map(str, self.elements)) + ')'

    def emit(self, typefix, buffer=None):
        return '(' + ','.join(map(lambda e: e.emit(typefix, buffer), self.elements)) + ')'


class NPred(NExpr):
    prefix: tuple
    verb: str
    ret: str
    typefix: str

    def __init__(self, prefix, verb, ret, typefix):
        self.prefix = prefix
        self.verb = verb
        self.ret = ret
        self.typefix = typefix

    def __str__(self):
        if self.ret == '':
            return str(self.verb)
        return f'({self.verb} : {self.ret})'

    def emit(self, typefix, buffer=None):
        ss = []
        for e in self.prefix:
            ss.append(e.emit(EOS, buffer))
        tok = lemma(alt(self.verb))
        if tok.lemmatype == 'N':
            s = str(tok)
        elif typefix == EOS:
            s = tok.emit(typefix)
        else:
            if len(self.typefix)+1 > len(typefix):
                typefix = typefix[0] + alt(self.typefix)
            s = tok.emit(typefix)
        ss.append(s)
        return ''.join(ss)


class NLiteral(NExpr):
    value: str
    ret: str

    def __init__(self, value: str, ret=None):
        self.value = value
        if ret is None:
            if value.startswith('"') or value.startswith("'"):
                ret = 'str'
            elif value.isdigit():
                ret = 'int'
        self.ret = ret

    def __str__(self):
        return self.value

    def emit(self, typefix, buffer=None):
        if not typefix.startswith('P') or typefix == RESULT:
            return self.value
        prefix = typefix[1:]
        if prefix in ['結果', '値']:
            return self.value
        return f'{prefix} {self.value}'


class NParam(NExpr):
    symbol: str
    index: int
    typefix: str
    bound: NExpr

    def __init__(self, symbol, index, typefix='', bound=None):
        self.symbol = symbol
        self.index = index
        self.typefix = typefix
        self.bound = bound

    def apply(self, mapped):
        if self.index in mapped:
            bound = mapped[self.index]
            return NParam(self.symbol, self.index, self.typefix, bound)
        return self

    def __str__(self):
        return ALPHA[self.index]

    def emit(self, typefix, buffer=None):
        if self.bound is None:
            return self.symbol
        typefix = RESULT if self.typefix == '' else 'P' + self.typefix
        return self.bound.emit(typefix, buffer)


def toNExpr(e):
    if isinstance(e, NExpr):
        return e
    if isinstance(e, CValue):
        return NLiteral(e.value)
    return NPiece(str(e))


class NChunk(NExpr):
    pieces: tuple
    suffix: str

    def __init__(self, suffix, *pieces):
        self.pieces = [toNExpr(p) for p in pieces]
        self.suffix = suffix

    def apply(self, mapped):
        pieces = [e.apply(mapped) for e in self.pieces]
        return NChunk(self.suffix, *pieces)

    def __str__(self):
        ss = []
        for p in self.pieces:
            ss.append(str(p))
        ss.append(self.suffix)
        return '{{ ' + ''.join(ss) + ' }}'

    def emit(self, typefix, buffer=None):
        ss = []
        for p in self.pieces:
            ss.append(p.emit(typefix, buffer))
        ss.append(self.suffix)
        return ''.join(ss)


class NPhrase(NExpr):
    pieces: tuple
    options: tuple
    ret: str  # 返り値の種類

    def __init__(self, *pieces):
        self.pieces = [toNExpr(p) for p in pieces]
        self.options = EMPTY
        self.ret = None

    def asType(self, ret):
        self.ret = ret
        return self

    def apply(self, mapped):
        pred = NPhrase(*[e.apply(mapped) for e in self.pieces])
        pred.options = mapped.get('options', EMPTY)
        pred.ret = self.ret
        return pred

    def __str__(self):
        ss = []
        for p in self.pieces:
            ss.append(str(p))
        return ' '.join(ss)

    def emit(self, typefix, buffer=None):
        ss = []
        if OPTION['Block']:
            ss.append('<e>')
        if len(self.options) > 2 and OPTION['ShuffleOrder']:
            os = list(self.options)
            random.shuffle(os)
            self.options = tuple(os)

        for p in self.options:
            if buffer is None:
                ss.append(p.emit(shuffle('T、', 'A、')))
            else:
                buffer.append(p.emit(EOS))

        for p in self.pieces:
            ss.append(p.emit(typefix, buffer))

        if OPTION['Block']:
            if buffer is not None:
                ss.extend(buffer)
                buffer.clear()
            ss.append('</e>')
        return ' '.join(ss)


# コード表現

ALPHA = [chr(c) for c in range(ord('A'), ord('Z')+1)] + ['?']

STATIC_MODULE = {
    'math', 'pd', 'sys', 'os'
}


def toCExpr(value):
    return value if isinstance(value, CExpr) else CValue(value)


def cmatch(cpat, code, mapped: dict):
    if cpat.__class__ is not code.__class__:
        return False
    if cpat.name != code.name or len(cpat.params) != len(code.params):
        return False
    for e, e2 in zip(cpat.params, code.params):
        # print(':: ', type(e), e, type(e2), e2)
        if isinstance(e, CMetaVar):
            if e.index in mapped:
                if str(mapped[e.index]) != str(e2):
                    return False
                else:
                    continue
            mapped[e.index] = e2
            continue
        if isinstance(e, CValue) and isinstance(e2, CValue):
            if e.value != e2.value:
                return False
            continue
        if not cmatch(e, e2, mapped):
            return False
    for opat in cpat.options:
        option = code.getoption(opat.name)
        if option is None:
            return False
        if not cmatch(opat, option, mapped):
            return False
    if len(code.options) > 0:
        os = []
        for option in code.options:
            opat = cpat.getoption(option.name)
            if opat is None:
                os.append(option)
        mapped['options'] = os
    return True


class CExpr(object):  # Code Expression
    name: str
    params: tuple

    def __init__(self, name='', params=EMPTY):
        self.name = name
        self.params = params
        self.options = EMPTY

    def format(self):
        return f'undefined({self.__class__.__name__})'

    def __repr__(self):
        return self.format().format(*(self.params+self.options))

    def __lt__(self, a):
        return id(self) < id(a)

    def __len__(self):
        return len(self.params)

    def __getitem__(self, index):
        return self.params[index]

    def getoption(self, name):
        for option in self.options:
            if name == option.name:
                return option
        return None

    def match(self, model) -> NExpr:
        name = self.name
        # print('matching', name)
        if len(self.params) > 0:  # レシーバの型を調べる
            recv = self.params[0].match(model)
            if hasattr(recv, 'ret') and recv.ret is not None:
                lname = f'{recv.ret}.{name}'
                # print('@レシーバの型', recv.ret, lname)
                if lname in model.rules:
                    name = lname
        while name not in model.rules and '.' in name:
            loc = name.find('.')
            name = name[loc+1:]
        if name in model.rules:
            for _, pat, pred in model.rules[name]:
                mapped = {}
                # print(f'trying {name}.. ', pat, type(self), self)
                if cmatch(pat, self, mapped):
                    for key in mapped.keys():
                        if key == 'options':
                            mapped[key] = [e.match(model) for e in mapped[key]]
                        else:
                            mapped[key] = mapped[key].match(model)
                    return pred.apply(mapped)
            # print(f'unmatched: {name}', str(self), type(self))
            if len(self.params) > 0:  # パラメータ圧縮する print(1,2,3) -> print(1,(2,3))
                paramsize = max(size for size, _, _ in model.rules[name])
                # print('減らす', name, paramsize,
                #       self.params[:paramsize-1], self.params[paramsize-1:])
                if len(self.params) > paramsize > 0:
                    ss = list(self.params[:paramsize-1])
                    ss.append(CSeq(self.params[paramsize-1:]))
                    self.params = tuple(ss)
                    return self.match(model)
        return self.unmatched(model)

    def unmatched(self, model) -> NExpr:
        logger.debug('undefined? ' + str(type(self)) + ' ' + str(self))
        # print('unmatched? ' + str(type(self)) + ' ' + str(self))
        return NPiece(str(self))


class CMetaVar(CExpr):
    index: int
    original_name: str

    def __init__(self, index: int, original_name: str):
        CExpr.__init__(self)
        self.index = index
        self.original_name = original_name

    def format(self):
        return repr(self)

    def __repr__(self):
        return ALPHA[self.index]


class CValue(CExpr):
    value: object

    def __init__(self, value):
        CExpr.__init__(self)
        self.value = value

    def __repr__(self):
        if isinstance(self.value, str):
            return repr(self.value)  # FIXME
        return str(self.value)

    def format(self):
        return repr(self)

    def match(self, model) -> NExpr:
        return NLiteral(str(self))


def stem_name(name: str):
    if name[-1].isdigit():
        return stem_name(name[:-1])
    return name


class CVar(CExpr):

    def __init__(self, name):
        CExpr.__init__(self, name)

    def format(self):
        return self.name

    def __repr__(self):
        return self.name

    def unmatched(self, model) -> NExpr:
        name = str(self.name)
        ret = stem_name(name)
        if ret in model.names:
            return NLiteral(name, ret)
        return NLiteral(name)


class CBinary(CExpr):

    def __init__(self, left, op, right):
        CExpr.__init__(self, op, (toCExpr(left), toCExpr(right)))

    def format(self):
        return f'{{}} {self.name} {{}}'


class CAnd(CExpr):

    def __init__(self, left, right):
        CExpr.__init__(self, 'and', (toCExpr(left), toCExpr(right)))

    def format(self):
        return f'{{}} and {{}}'

    def match(self, model) -> NExpr:
        left = self.params[0].match(model)
        right = self.params[1].match(model)
        return NPhrase(left, NPiece('かつ'), right)


class COr(CExpr):

    def __init__(self, left, right):
        CExpr.__init__(self, 'or', (toCExpr(left), toCExpr(right)))

    def format(self):
        return f'{{}} or {{}}'

    def match(self, model) -> NExpr:
        left = self.params[0].match(model)
        right = self.params[1].match(model)
        return NPhrase(left, NPiece('または'), right)


class CUnary(CExpr):

    def __init__(self, op, expr):
        CExpr.__init__(self, op, (toCExpr(expr),))

    def format(self):
        return f'{self.name} {{}}'


class CNot(CExpr):

    def __init__(self, expr):
        CExpr.__init__(self, 'not', (toCExpr(expr),))

    def format(self):
        return f'not {{}}'

    def match(self, model) -> NExpr:
        value = self.params[0].match(model)
        return NPhrase(value, NPred(EMPTY, 'ない', '', ''))


class COption(CExpr):

    def __init__(self, name: str, value: CExpr):
        CExpr.__init__(self, name, (toCExpr(value),))

    def format(self):
        return f'{self.name} = {{}}'

    def unmatched(self, model) -> NExpr:
        name = alt(model.names[self.name]
                   ) if self.name in model.names else self.name
        value = self.params[0].match(model)
        if OPTION['MultipleSentence']:
            return NPhrase(name, 'は', value, 'に', NPred(EMPTY, 'する', '', ''))
        else:
            return NPhrase(value, 'を', name, 'と', NPred(EMPTY, 'する', '', ''))


class CApp(CExpr):

    def __init__(self, name: str, *es):
        CExpr.__init__(self, name, tuple(toCExpr(e)
                                         for e in es if not isinstance(e, COption)))
        if len(es) != len(self.params):
            self.options = tuple(toCExpr(e)
                                 for e in es if isinstance(e, COption))

    def format(self):
        ss = []
        ss.append(self.name)
        ss.append('(')
        n = len(self.params)+len(self.options)
        if n > 0:
            ps = [',', '{}'] * (n)
            ss.extend(ps[1:])
        ss.append(')')
        return ' '.join(ss)


class OOP(object):
    pass


class CMethod(CExpr, OOP):

    def __init__(self, name: str, *es):
        CExpr.__init__(self, name, tuple(toCExpr(e)
                                         for e in es if not isinstance(e, COption)))
        if len(es) != len(self.params):
            self.options = tuple(toCExpr(e)
                                 for e in es if isinstance(e, COption))

    def format(self):
        ss = ['{}', '.']
        ss.append(self.name)
        ss.append('(')
        n = len(self.params)+len(self.options)
        if n > 1:
            ps = [',', '{}'] * (n-1)
            ss.extend(ps[1:])
        ss.append(')')
        return ' '.join(ss)


class CField(CExpr, OOP):

    def __init__(self, recv: CExpr, name: str):
        CExpr.__init__(self, name, (toCExpr(recv),))

    def format(self):
        return f'{{}} . {self.name}'


class CTuple(CExpr):

    def __init__(self, *es):
        CExpr.__init__(self, "(,)", tuple(toCExpr(e) for e in es))

    def format(self):
        ss = []
        ss.append('(')
        n = len(self.params)
        if n == 1:
            ss.extend(['{}', ','])
        else:
            ps = [',', '{}'] * (n)
            ss.extend(ps[1:])
        ss.append(')')
        return ' '.join(ss)


class CList(CExpr):

    def __init__(self, *es):
        CExpr.__init__(self, "[,]", tuple(toCExpr(e) for e in es))

    def format(self):
        ss = []
        ss.append('[')
        n = len(self.params)
        if n > 0:
            ps = [',', '{}'] * (n)
            ss.extend(ps[1:])
        ss.append(']')
        return ' '.join(ss)


class CSeq(CExpr):

    def __init__(self, es):
        CExpr.__init__(self, "", es)

    def format(self):
        ss = []
        n = len(self.params)
        if n > 0:
            ps = [',', '{}'] * (n)
            ss.extend(ps[1:])
        return ' '.join(ss)

    def match(self, model):
        ss = []
        for e in self.params:
            ss.append(NPiece('、'))
            ss.append(e.match(model))
        return NPhrase(*ss[1:])


class CData(CExpr):

    def __init__(self, *es):
        CExpr.__init__(self, "{,}", tuple(toCExpr(e) for e in es))

    def format(self):
        ss = []
        ss.append('{')
        for i in range(0, len(self.params), 2):
            ss.extend(['{}', '=', '{}', ','])
        ss.append('}')
        return ' '.join(ss)


class CIndex(CExpr, OOP):

    def __init__(self, recv, index):
        CExpr.__init__(self, "[]", (toCExpr(recv), toCExpr(index)))

    def format(self):
        return f'{{}} [ {{}} ]'


class CEmpty(CExpr, OOP):

    def __init__(self):
        CExpr.__init__(self, "")

    def format(self):
        return ''


CEMPTY = CEmpty()


class CSlice(CExpr):

    def __init__(self, recv, start=CEMPTY, stop=CEMPTY, step=CEMPTY):
        CExpr.__init__(self, "[]", (toCExpr(recv),
                                    toCExpr(start),  toCExpr(stop), toCExpr(step)))

    def format(self):
        return f'{{}} [ {{}} : {{}} : {{}}]'


##
peg = pg.grammar('kotoha.tpeg')
parser = pg.generate(peg)
snipet_parser = pg.generate(peg, start='Snipet')


def traverse_symbols(tree, ss):
    for _, child in tree.subs():
        tag = child.getTag()
        if tag == 'NSymbol':
            ss.append(str(child))
        if tag == 'NParam':
            ss.append(str(child[0]))
        if tag == 'NChunk':
            traverse_symbols(child, ss)


class Reader(ParseTreeVisitor):
    rules: dict
    indexes: dict
    newnames: set

    def __init__(self, rules):
        ParseTreeVisitor.__init__(self)
        self.rules = rules
        self.symbols = EMPTY
        self.names = {
            's': '文字列', 'c': '文字',
            'n': '整数', 'f': 'ファイル',
        }
        self.modules = STATIC_MODULE
        self.synonyms = {}
        self.newnames = set()

    def isRuleMode(self):
        return self.symbols is not EMPTY

    def acceptSource(self, tree):
        for t in tree:
            self.visit(t)

    def acceptAssignment(self, tree):
        left = self.visit(tree.left)  # xをyとする
        right = self.visit(tree.right)
        return CBinary(left, '=', right)

    def acceptSelfAssignment(self, tree):
        name = str(tree.name)
        left = self.visit(tree.left)
        right = self.visit(tree.right)
        return CBinary(left, name, right)

    def acceptInfix(self, tree):
        name = str(tree.name)
        left = self.visit(tree.left)
        right = self.visit(tree.right)
        return CBinary(left, name, right)

    def acceptAnd(self, tree):
        left = self.visit(tree.get('left'))
        right = self.visit(tree.get('right'))
        return CAnd(left, right)

    def acceptOr(self, tree):
        left = self.visit(tree.get('left'))
        right = self.visit(tree.get('right'))
        return COr(left, right)

    def acceptUnary(self, tree):
        name = str(tree.name)
        expr = self.visit(tree.expr)
        return CUnary(name, expr)

    def acceptNot(self, tree):
        expr = self.visit(tree[0])
        return CNot(expr)

    def acceptApplyExpr(self, tree):
        name = str(tree.name)
        params = self.visit(tree.params)
        return CApp(name, *params)

    def acceptArguments(self, tree):
        return [self.visit(e) for e in tree]

    def acceptOption(self, tree):
        value = self.visit(tree[1])
        return COption(str(tree[0]), value)

    def acceptMethodExpr(self, tree):
        recv = self.visit(tree.recv)
        name = str(tree.name)
        params = self.visit(tree.params)
        if isinstance(recv, CVar):
            if self.isRuleMode() and recv.name.startswith('_'):
                return CApp(recv.name[1:] + '.' + name, *params)
            if recv.name in self.modules:
                return CApp(recv.name + '.' + name, *params)
        return CMethod(name, *([recv]+params))

    def acceptGetExpr(self, tree):
        recv = self.visit(tree.recv)
        name = str(tree.name)
        if isinstance(recv, CVar):
            if self.isRuleMode() and recv.name.startswith('_'):
                recv.name = recv.name[1:] + '.' + name
                return recv
            if recv.name in self.modules or '.' in recv.name:
                recv.name += '.' + name
                return recv
        return CField(recv, name)  # Fixme

    def acceptIndexExpr(self, tree):
        recv = self.visit(tree.recv)
        index = self.visit(tree.index)
        return CIndex(recv, index)  # Fixme

    def acceptName(self, tree):
        s = str(tree)
        if self.isRuleMode():
            if s in self.symbols:
                if s not in self.indexes:
                    self.indexes[s] = len(self.indexes)
                return CMetaVar(self.indexes[s], s)
        return CVar(s)

    def acceptString(self, tree):
        s = str(tree)
        if s.startswith("'") and s.endswith("'"):
            s = s[1:-1].encode('unicode-escape').decode('unicode-escape')
        if s.startswith('"') and s.endswith('"'):
            s = s[1:-1].encode('unicode-escape').decode('unicode-escape')
        return CValue(s)

    def acceptInt(self, tree):
        s = str(tree)
        return CValue(int(s))

    def acceptDouble(self, tree):
        s = str(tree)
        return CValue(float(s))

    def acceptTrueExpr(self, tree):
        return CValue(True)

    def acceptFalseExpr(self, tree):
        return CValue(False)

    def acceptNull(self, tree):
        return CValue(None)

    def acceptList(self, tree):
        es = [self.visit(t) for t in tree]
        return CList(*es)

    def acceptTuple(self, tree):
        es = [self.visit(t) for t in tree]
        return CTuple(*es)

    def acceptList(self, tree):
        es = [self.visit(t) for t in tree]
        return CList(*es)

    def acceptUndefined(self, tree):
        logger.warning(f'@undefined {repr(tree)}')
        s = str(tree)
        return CValue(s)

    def acceptNRule(self, tree):
        code = tree[0]
        doc = tree[1]
        self.symbols = []
        traverse_symbols(doc, self.symbols)
        self.indexes = {}
        cpat = self.visit(code)
        if str(doc).strip() == 'symbol':
            name = cpat.name
            symbol = str(cpat.params[0])[1:-1]
            self.names[name] = symbol
            return
        if str(doc).strip() == 'module':
            name = cpat.name
            self.modules.add(name)
            return
        pred = self.visit(doc)
        self.add_rule(cpat, len(self.indexes), pred)
        self.symbols = EMPTY

    def add_rule(self, cpat: CExpr, size, pred: NExpr):
        name = cpat.name
        assert name != ''
        if len(cpat.params) > 0 and isinstance(cpat.params[0], CMetaVar):
            ns = cpat.params[0].original_name
            if len(ns) > 1:
                lname = f'{ns}.{name}'
                if lname not in self.rules:
                    self.rules[lname] = []
                # print('adding', lname, (size, cpat, pred))
                self.rules[lname].append((size, cpat, pred))
                if name not in self.rules or ns in self.newnames:
                    self.newnames.add(ns)
                else:
                    # print(f'{lname}のみ登録', cpat, pred)
                    return
        if name not in self.rules:
            self.rules[name] = []
        # print('adding', name, (size, cpat, pred))
        self.rules[name].append((size, cpat, pred))

    def acceptNSymbolDef(self, tree):
        name = str(tree[0])
        symbol = str(tree[1])[1:-1]
        if tree[0] == 'Noun':
            self.synonyms[name] = symbol
        else:
            self.names[name] = symbol

    def acceptNImport(self, tree):
        name = str(tree[0 if len(tree) == 1 else 0])
        self.modules.add(name)
        STATIC_MODULE.add(name)

    def acceptNExample(self, tree):
        # ce = self.visit(tree[0])
        logger.debug('example', str(tree))

    def acceptNDocument(self, tree):
        ss = []
        for t in tree:
            ss.append(self.visit(t))
        # print(ss)
        return NPhrase(*ss)

    def acceptNChunk(self, tree):
        ss = []
        for t in tree[:-1]:
            ss.append(self.visit(t))
        suffix = str(tree[-1])
        return NChunk(suffix, *ss)

    def acceptNPred(self, tree):
        ret = ''
        typefix = ''
        prefix = EMPTY
        if tree[-1] == 'NType':
            ntype = tree[-1][0]
            if ntype == 'NSymbol':
                ret = str(ntype)
            else:
                ret = str(ntype[0])
                typefix = str(ntype[1])
            pred = str(tree[-2])
            if len(tree) > 2:
                prefix = tuple(self.visit(t) for t in tree[:-2])
        else:
            pred = str(tree[-1])
            ret = 'bool' if pred.endswith('かどうか') else ''
            prefix = tuple(self.visit(t) for t in tree[:-1])
        if typefix == '':
            typefix = self.names.get(ret, '結果')
        pred = self.synonyms.get(pred, pred)
        return NPred(prefix, pred, ret, typefix)

    def acceptNSymbol(self, tree):
        s = str(tree)
        if s in self.indexes:
            p = NParam(s, self.indexes[s])
            if s[-1].isdigit():
                s = s[:-1]
            if s in self.names:
                p.typefix = self.names[s]
            return p
        return NPiece(s)

    def acceptNParam(self, tree):
        piece = self.visit(tree[0])
        typefix = str(tree[1])
        if isinstance(piece, NParam):
            piece.typefix = typefix
            return piece
        return piece

    def acceptNSynonym(self, tree):
        ss = [str(t) for t in tree]
        if len(ss) == 1:
            if ss[0] in self.synonyms:
                return NPiece(self.synonyms[ss[0]])
            return NPiece(ss[0]+'|')
        return NPiece('|'.join(ss))

    def acceptNTuple(self, tree):
        ss = [str(t) for t in tree]
        return NTuple(*[NPiece(str(t)) for t in ss])

    def acceptNLiteral(self, tree):
        symbol = str(tree)
        return NLiteral(symbol)

    def acceptNPiece(self, tree):
        s = str(tree)
        if s in self.synonyms:
            return NPiece(s)
        return NPiece(s)

    def accepterr(self, tree):
        print(repr(tree))
        raise InterruptedError


class KotohaModel(object):
    rules: dict
    names: dict
    reader: Reader

    def __init__(self):
        self.rules = {}
        self.reader = Reader(self.rules)
        self.names = {}

    def load(self, *files):
        for file in files:
            with open(file) as f:
                source = f.read()
                tree = parser(source, urn=file)
                self.reader.visit(tree)
        for key in self.rules:
            d = self.rules[key]
            if len(d) > 1:
                self.rules[key] = sorted(d)
        self.names = self.reader.names

    def translate(self, expression, suffix=''):
        randomize()
        try:
            tree = snipet_parser(expression)
            # print(repr(tree))
            code = self.reader.visit(tree)
            # print(type(code), code)
            pred = code.match(self)
            if OPTION['MultipleSentence']:
                buffer = []
                main = pred.emit(suffix, buffer)
                if len(buffer) > 0:
                    main += 'その際、' + (' '.join(buffer))
                return code, main
            return code, pred.emit(suffix)
        except InterruptedError:
            return expression, 'err'

    def generate(self, w, *files):
        for file in files:
            with open(file) as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == '' or line.startswith('#'):
                        continue
                    if '\t' in line:
                        line = line.split('\t')[0]
                    code, doc = self.translate(line, suffix=EOS)
                    print(code, '\t', doc, file=w)


if __name__ == '__main__':
    model = KotohaModel()
    argv = sys.argv[1:]
    rule_files = []
    input_files = []
    tsvfile = sys.stdout
    for s in sys.argv[1:]:
        if s.endswith('.py'):
            if s.endswith('rule.py'):
                rule_files.append(s)
            else:
                input_files.append(s)
        if s.endswith('.tsv'):
            tsvfile = open(s, 'w')
        if s.endswith('=True'):
            key, _ = s.split('=')
            if key in OPTION:
                OPTION[key] = True
            else:
                logger.warning(f'unknown option: {key}')
        if s.endswith('=False'):
            key, _ = s.split('=')
            if key in OPTION:
                OPTION[key] = False
            else:
                logger.warning(f'unknown option: {key}')
    model.load(*rule_files)
    if len(input_files) > 0:
        model.generate(tsvfile, *input_files)
    else:
        import readline
        try:
            while True:
                line = input('Snipet >>> ')
                if line == '':
                    print('Bye')
                    sys.exit(0)
                code, doc = model.translate(line, suffix=EOS)
                print(code, '\t#', doc)
        except EOFError:
            print('Bye')
