
from pegtree.visitor import ParseTreeVisitor
from pegtree import ParseTree
import pegtree as pg

from logging import getLogger
logger = getLogger(__name__)

ALPHA = [chr(c) for c in range(ord('A'), ord('Z')+1)] + ['?']
EMPTY = tuple()


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
        if option:
            ps = [',', '{}'] * (len(self.params)+len(self.options))
        else:
            ps = [',', '{}'] * len(self.params)
        if len(ps) > 0:
            ss.extend(ps[1:])
        ss.append(')')
        return ' '.join(ss)


# e = CApp('print', 1, COption('end', ''))
# print(e)

####################################################

RESULT = '結果'
EOS = '。'


def emitVerbalSentence(sentence, typefix):
    if typefix.endswith(EOS):
        if len(typefix) > 1:
            return f'{sentence}、そして {typefix[:-1]} とする。'
        else:
            return sentence + EOS
    return sentence


class NExpr(object):

    def append(self, e):
        return NChoice(self, e)

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

    def append(self, e: NExpr):
        return NChoice(*(self.choices + (e,)))

    def asType(self, typefix):
        return NChoice(*[c.asType(typefix) for c in self.choices])

    def apply(self, mapped):
        return NChoice(*[c.apply(mapped) for c in self.choices])

    def __str__(self):
        return '{' + '|'.join(map(str, self.choices)) + '}'

    def emit(self, typefix):
        return self.choices[0].emit(typefix)


class NPiece(NExpr):
    piece: str

    def __init__(self, piece):
        self.piece = piece

    def __str__(self):
        return self.piece

    def emit(self, typefix):
        return self.piece


class NPred(NExpr):
    verb: str
    typefix: str   # '' のときは、名詞

    def __init__(self, verb, typefix=''):
        assert isinstance(verb, str), type(verb)
        self.verb = str(verb)
        self.typefix = typefix

    def asType(self, typefix):
        return NPred(self.verb, typefix) if typefix != self.typefix else self

    def __str__(self):
        if self.typefix == '':
            return self.verb
        return f'{self.verb} #{self.typefix}'

    def emit(self, typefix):
        if typefix == RESULT and self.typefix != '':
            typefix = self.typefix
        return self.verb + f' #{typefix}'


class NLiteral(NExpr):
    value: str

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def emit(self, typefix):
        if typefix == RESULT:
            return self.value
        return f'{typefix} {self.value}'


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

    def emit(self, typefix):
        if self.bound is None:
            return self.symbol
        return self.bound.emit(RESULT if self.typefix == '' else self.typefix)


def toNExpr(e):
    if isinstance(e, NExpr):
        return e
    if isinstance(e, CValue):
        return NLiteral(e.value)
    return NPiece(str(e))


class NPhrase(NExpr):
    pieces: tuple[NExpr]
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

    def emit(self, typefix):
        ss = []
        if len(self.options) > 0:
            for p in self.options:
                ss.append(p.emit(''))
        for p in self.pieces:
            ss.append(p.emit(typefix))
        return ' '.join(ss)


#e = NPhrase('A', 'を', 'B', 'で', NPred('置き換える')).asType('文字列')
# print(e.emit('ファイル名'))


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


class Matcher(object):
    rules: dict

    def __init__(self):
        self.rules = {}

    def add_rule(self, cpat: CExpr, pred: NExpr):
        name = cpat.name
        if name != '':
            if name not in self.rules:
                self.rules[name] = []
            self.rules[name].append((cpat, pred))
        else:
            logger.warning('@fixme', cpat, pred)

    def match(self, ce: CExpr) -> NExpr:
        name = ce.name
        if name not in self.rules and '.' in name:
            loc = name.find('.')
            name = name[loc+1:]
        if name in self.rules:
            for pat, pred in self.rules[name]:
                mapped = {}
                #print('trying .. ', pat, type(ce), ce)
                if cmatch(pat, ce, mapped):
                    for key in mapped.keys():
                        if key == 'options':
                            mapped[key] = [self.match(e) for e in mapped[key]]
                        else:
                            mapped[key] = self.match(mapped[key])
                    return pred.apply(mapped)
            logger.warning('unmatched: ' + str(ce))
        return NLiteral(str(ce))


m = Matcher()

##

peg = pg.grammar('kotoha.tpeg')
parser = pg.generate(peg)
eparser = pg.generate(peg, start='Expression')


def symbols(tree):
    ss = []
    print(tree)
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

    def __init__(self):
        ParseTreeVisitor.__init__(self)
        self.rules = m.rules
        self.symbols = EMPTY

    def load_rule(self, file):
        with open(file) as f:
            source = f.read()
            tree = parser(source, urn=file)
            self.visit(tree)

    def translate(self, expression, suffix=''):
        tree = eparser(expression)
        code = self.visit(tree)
        #print(type(code), code)
        pred = m.match(code)
        return code, pred.emit(suffix)

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
        pred = self.visit(doc)
        m.add_rule(cpat, pred)
        # print(">>> ", str(cpat), '##', str(pred), '@', repr(self.symbols), repr(self.indexes))

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
            return CApp(recv.name + '.' + name, *params)
        return CMethod(name, *((recv,)+params))  # Fixme

    def acceptGetExpr(self, tree):
        recv = self.visit(tree.recv)
        if isinstance(recv, CVar):
            recv.name += '.' + str(tree.name)
            return recv
        return CField(recv, str(tree.name))  # Fixme

    def acceptName(self, tree):
        s = str(tree)
        if s in self.symbols:
            if s not in self.indexes:
                self.indexes[s] = len(self.indexes)
            return CIndex(self.indexes[s])
        return CVar(s)

    def acceptString(self, tree):
        s = str(tree)
        if s.startswith("'") and s.endswith("'"):
            s = s[1:-1].encode().decode('unicode-escape')
        if s.startswith('"') and s.endswith('"'):
            s = s[1:-1].encode().decode('unicode-escape')
        return CValue(s)

    def acceptInt(self, tree):
        s = str(tree)
        return CValue(int(s))

    def acceptDouble(self, tree):
        s = str(tree)
        return CValue(float(s))

    def acceptUndefined(self, tree):
        print('@undefined', repr(tree))
        s = str(tree)
        return CValue(s)

    def acceptDocument(self, tree):
        ret = ''
        ss = []
        for t in tree:
            if t.getTag() == 'Return':
                ret = str(t).strip()
            else:
                ss.append(self.visit(t))
        e = NPhrase(*ss)
        if ret != '':
            return e.asType(ret)
        return e

    def acceptSymbol(self, tree):
        s = str(tree)
        if s in self.indexes:
            return NParam(s, self.indexes[s])
        return NPiece(s)

    def acceptParam(self, tree):
        piece = self.visit(tree[0])
        typefix = str(tree[1])
        if isinstance(piece, NParam):
            piece.typefix = typefix
            return piece
        return piece

    def acceptVerb(self, tree):
        e = NPred(str(tree[0]))
        for t in tree[1:]:
            e = e.append(NPred(str(t)))
        return e

    def acceptLiteral(self, tree):
        return NLiteral(str(tree))

    def acceptPiece(self, tree):
        return NPiece(str(tree))


Kotoha = Reader()

Kotoha.load_rule('rule.py')
pair = Kotoha.translate('x % 2 != 0')
print(*pair)

pair = Kotoha.translate('open("file.txt", encoding="sjis")', "ファイル" + EOS)
#pair = Kotoha.translate('open("file.txt")', "ファイル")
print(*pair)

pair = Kotoha.translate('print(x, end="")')
print(*pair)

pair = Kotoha.translate('print(x+1, end="")')
print(*pair)
