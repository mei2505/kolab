
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

ReversePolish = True  # 膠着語の場合はTrue
ShuffleSynonym = True  # NChoiceの表現をシャッフルする
ShuffleOrder = True
MultipleSentence = True


def shuffle(x, y):
    if ShuffleSynonym:
        return x if random.random() < 0.6 else y
    return x


def alt(s: str):
    if '|' in s:
        ss = s.split('|')
        if ShuffleSynonym:
            random.shuffle(ss)
        return ss[0]
    return s

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


class NChoice(NExpr):
    choices: tuple[NExpr]

    def __init__(self, *choices):
        self.choices = choices

    def asType(self, typefix):
        return NChoice(*[c.asType(typefix) for c in self.choices])

    def apply(self, mapped):
        return NChoice(*[c.apply(mapped) for c in self.choices])

    def __str__(self):
        return '[' + '|'.join(map(str, self.choices)) + ']'

    def emit(self, typefix, buffer=None):
        if ShuffleSynonym:
            index = random.randrange(0, len(self.choices))
            return self.choices[index].emit(typefix, buffer)
        return self.choices[0].emit(typefix, buffer)


class NPiece(NExpr):
    piece: str

    def __init__(self, piece):
        self.piece = piece

    def asType(self, typefix):
        return NPred(self.piece, typefix)

    def __str__(self):
        return self.piece

    def emit(self, typefix, buffer=None):
        return self.piece


class NPred(NExpr):
    lemma: Lemma
    typefix: str

    def __init__(self, verb, typefix=''):
        self.lemma = lemma(verb)
        self.typefix = typefix

    def __str__(self):
        if self.typefix == '':
            return str(self.lemma)
        return f'{self.lemma} as {self.typefix}'

    def emit(self, typefix, buffer=None):
        if typefix != EOS and self.lemma.lemmatype == 'N':
            return str(self.lemma)
        if typefix == EOS:
            return self.lemma.emit(typefix)
        if len(self.typefix)+1 > len(typefix):
            typefix = typefix[0] + self.typefix
        return self.lemma.emit(typefix)


class NLiteral(NExpr):
    value: str

    def __init__(self, value):
        self.value = value

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


class NPhrase(NExpr):
    pieces: tuple
    options: tuple

    def __init__(self, *pieces):
        self.pieces = [toNExpr(p) for p in pieces]
        self.options = EMPTY

    def asType(self, ret):
        return NPhrase(*[e.asType(ret) for e in self.pieces])

    def apply(self, mapped):
        pred = NPhrase(*[e.apply(mapped) for e in self.pieces])
        pred.options = mapped.get('options', EMPTY)
        return pred

    def __str__(self):
        ss = []
        for p in self.pieces:
            ss.append(str(p))
        return ' '.join(ss)

    def emit(self, typefix, buffer=None):
        ss = []
        if len(self.options) > 2 and ShuffleOrder:
            os = list(self.options)
            random.shuffle(os)
            self.options = tuple(os)

        for p in self.options:
            if buffer is None:
                ss.append(p.emit(shuffle('T、', 'A、')))
            else:
                buffer.append(p.emit('E。'))

        for p in self.pieces:
            ss.append(p.emit(typefix, buffer))
        return ' '.join(ss)


# コード表現

ALPHA = [chr(c) for c in range(ord('A'), ord('Z')+1)] + ['?']

STATIC_MODULE = {
    'math', 'pd', 'sys', 'os'
}


def toCExpr(value):
    return value if isinstance(value, CExpr) else CValue(value)


class CExpr(object):  # Code Expression
    name: str
    params: tuple

    def __init__(self, name='', params=EMPTY):
        self.name = name
        self.params = params
        self.options = EMPTY

    def format(self, option=True):
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


class CIndex(CExpr):
    index: object

    def __init__(self, index):
        CExpr.__init__(self)
        self.index = index

    def format(self, option=True):
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

    def format(self, option=True):
        return repr(self)


class CVar(CExpr):

    def __init__(self, name):
        CExpr.__init__(self, name)

    def format(self, option=True):
        return self.name

    def __repr__(self):
        return self.name


class CBinary(CExpr):

    def __init__(self, left, op, right):
        CExpr.__init__(self, op, (toCExpr(left), toCExpr(right)))

    def format(self, option=True):
        return f'{{}} {self.name} {{}}'


class COption(CExpr):

    def __init__(self, name: str, value: CExpr):
        CExpr.__init__(self, name, (toCExpr(value),))

    def format(self, option=True):
        return f'{self.name} = {{}}'


class CApp(CExpr):

    def __init__(self, name: str, *es):
        CExpr.__init__(self, name, tuple(toCExpr(e)
                                         for e in es if not isinstance(e, COption)))
        if len(es) != len(self.params):
            self.options = tuple(toCExpr(e)
                                 for e in es if isinstance(e, COption))

    def format(self, option=True):
        ss = []
        ss.append(self.name)
        ss.append('(')
        n = len(self.params)+len(self.options)
        if n > 0:
            ps = [',', '{}'] * (n)
            ss.extend(ps[1:])
        ss.append(')')
        return ' '.join(ss)


class CMethod(CExpr):

    def __init__(self, name: str, *es):
        CExpr.__init__(self, name, tuple(toCExpr(e)
                                         for e in es if not isinstance(e, COption)))
        if len(es) != len(self.params):
            self.options = tuple(toCExpr(e)
                                 for e in es if isinstance(e, COption))

    def format(self, option=True):
        ss = ['{}', '.']
        ss.append(self.name)
        ss.append('(')
        n = len(self.params)+len(self.options)
        if n > 1:
            ps = [',', '{}'] * (n-1)
            ss.extend(ps[1:])
        ss.append(')')
        return ' '.join(ss)


##
peg = pg.grammar('kotoha.tpeg')
parser = pg.generate(peg)
eparser = pg.generate(peg, start='Snipet')


def symbols(tree):
    ss = []
    for _, child in tree.subs():
        tag = child.getTag()
        if tag == 'Name' or tag == 'Symbol':
            ss.append(str(child))
        if tag == 'Param':
            ss.append(str(child[0]))
    return ss


class Reader(ParseTreeVisitor):
    rules: dict
    indexes: dict

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

    def isRuleMode(self):
        return self.symbols is not EMPTY

    def acceptSource(self, tree):
        for t in tree:
            self.visit(t)

    def acceptRule(self, tree):
        code = tree[0]
        doc = tree[1]
        self.symbols = set(symbols(doc))
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
        if name != '':
            if name not in self.rules:
                self.rules[name] = []
            self.rules[name].append((size, cpat, pred))
            #print('rule', (size, cpat, pred))
        else:
            logger.warning('@fixme', cpat, pred)

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
            if self.isRuleMode() or recv.name in STATIC_MODULE:
                return CApp(recv.name + '.' + name, *params)
        return CMethod(name, *([recv]+params))

    def acceptGetExpr(self, tree):
        recv = self.visit(tree.recv)
        if isinstance(recv, CVar):
            if self.isRuleMode() or recv.name in STATIC_MODULE:
                recv.name += '.' + str(tree.name)
                return recv
        return CField(recv, str(tree.name))  # Fixme

    def acceptName(self, tree):
        s = str(tree)
        if self.isRuleMode():
            if s in self.symbols:
                if s not in self.indexes:
                    self.indexes[s] = len(self.indexes)
                return CIndex(self.indexes[s])
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

    def acceptUndefined(self, tree):
        logger.warning(f'@undefined {repr(tree)}')
        s = str(tree)
        return CValue(s)

    def acceptMetaData(self, tree):
        lines = str(tree).split('\n')
        for line in lines:
            ss = line.split(' ')
            if len(ss) > 2:
                self.synonyms[ss[1]] = tuple(lemma(t) for t in ss[1:])
                # print(ss[1], self.synonyms[ss[1]])

    def acceptDocument(self, tree):
        ret = ''
        ss = []
        for t in tree:
            if t.getTag() == 'Return':
                ret = str(t).strip()
                # if ret == '':
                #     ret = EOS
                # print(repr(t), ret)
            else:
                ss.append(self.visit(t))
        if ReversePolish:
            ss[-1] = ss[-1].asType(ret)
        else:
            ss[-1] = ss[-1].asType(ret)
        e = NPhrase(*ss)
        return e

    def acceptSymbol(self, tree):
        s = str(tree)
        if s in self.indexes:
            p = NParam(s, self.indexes[s])
            if s[-1].isdigit():
                s = s[:-1]
            if s in self.names:
                p.typefix = alt(self.names[s])
            return p
        return NPiece(s)

    def acceptParam(self, tree):
        piece = self.visit(tree[0])
        typefix = str(tree[1])
        if isinstance(piece, NParam):
            piece.typefix = typefix
            return piece
        return piece

    def acceptSynonyms(self, tree):
        ss = [str(t) for t in tree]
        if len(ss) == 1:
            if ss[0] in self.synonyms:
                ss = [NPiece(str(t)) for t in self.synonyms[ss[0]]]
                return NChoice(*ss)
        return NChoice(*[NPiece(str(t)) for t in ss])

    def acceptLiteral(self, tree):
        return NLiteral(str(tree))

    def acceptPiece(self, tree):
        s = str(tree)
        if s in self.synonyms:
            ss = [NPiece(str(t)) for t in self.synonyms[s]]
            return NChoice(*ss)
        return NPiece(s)

    def accepterr(self, tree):
        print(repr(tree))
        sys.exit(0)


# Matcher

def cmatch(cpat, code, mapped: dict):
    if cpat.__class__ is not code.__class__:
        return False
    if cpat.name != code.name or len(cpat.params) != len(code.params):
        return False
    for e, e2 in zip(cpat.params, code.params):
        #print(':: ', type(e), e, type(e2), e2)
        if isinstance(e, CIndex):
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
        if not opat.match(option, mapped):
            return False
    if len(code.options) > 0:
        os = []
        for option in code.options:
            opat = cpat.getoption(option.name)
            if opat is None:
                os.append(option)
        mapped['options'] = os
    return True


def NOption(name, value: NExpr):
    if MultipleSentence:
        return NPhrase(name, 'は', value, 'に', NPred('する'))
    else:
        return NPhrase(name, 'を', value, 'に', NPred('する'))


class KotohaModel(object):
    rules: dict
    reader: Reader

    def __init__(self):
        self.rules = {}
        self.reader = Reader(self.rules)

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

    def match(self, ce: CExpr) -> NExpr:
        name = ce.name
        if name not in self.rules and '.' in name:
            loc = name.find('.')
            name = name[loc+1:]
        if name in self.rules:
            for _, pat, pred in self.rules[name]:
                mapped = {}
                # print('trying .. ', pat, type(ce), ce)
                if cmatch(pat, ce, mapped):
                    for key in mapped.keys():
                        if key == 'options':
                            mapped[key] = [self.match(e) for e in mapped[key]]
                        else:
                            mapped[key] = self.match(mapped[key])
                    return pred.apply(mapped)
            logger.debug('unmatched: ' + str(ce))
        if len(ce.params) > 0:
            logger.debug('undefined? ' + str(type(ce)) + ' ' + str(ce))
        if isinstance(ce, CVar) or isinstance(ce, CValue):
            return NLiteral(str(ce))
        if isinstance(ce, COption) and ce.name in self.reader.names:
            name = alt(self.reader.names[ce.name])
            return NOption(name, self.match(ce.params[0]))
        return NPiece(str(ce))

    def translate(self, expression, suffix=''):
        tree = eparser(expression)
        code = self.reader.visit(tree)
        #print(type(code), code)
        pred = self.match(code)
        if MultipleSentence:
            buffer = []
            main = pred.emit(suffix, buffer)
            if len(buffer) > 0:
                main += 'そのとき、' + (' '.join(buffer))
            return code, main
        return code, pred.emit(suffix)

    def generate(self, *files):
        for file in files:
            with open(file) as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == '' or line.startswith('#'):
                        continue
                    code, doc = self.translate(line, suffix=EOS)
                    print(code, '\t#', doc)


if __name__ == '__main__':
    model = KotohaModel()
    rule_files = [s for s in sys.argv[1:] if s.endswith('rule.py')]
    input_files = [s for s in sys.argv[1:] if not s.endswith('rule.py')]
    model.load(*rule_files)
    if len(input_files) > 0:
        model.generate(*input_files)
    else:
        import readline
        while True:
            line = input('Expression >>> ')
            if line == '':
                sys.exit(0)
            code, doc = model.translate(line, suffix=EOS)
            print(code, '\t#', doc)
