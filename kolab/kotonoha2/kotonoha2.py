from os import get_exec_path
import string

ALPHA = [ chr(c) for c in range(ord('A'), ord('Z')+1) ] + ['?']
EMPTY = tuple()

class CExpr(object):  #Code Expression

    def key(self):
        return None

    def get_format(self):
        return 'undefined'

    def get_params(self):
        return EMPTY
    
    def __repr__(self):
        return self.get_format()(*[repr(e) for e in self.get_params()])

class CValue(CExpr):
    value: object

    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return str(self.value)

def toCExpr(value):
    return value if isinstance(value, CExpr) else CValue(value)

class CVar(CExpr):
    name: object

    def key(self):
        return self.name

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return self.name


class CIndex(CExpr):
    index: int

    def key(self):
        return None

    def __init__(self, index):
        self.index = index
    
    def __repr__(self):
        return ALPHA[self.index]

class CBinary(CExpr):
    left: CExpr
    right: CExpr
    op: str

    def __init__(self, left, op, right):
        self.left = toCExpr(left)
        self.op = op
        self.right = toCExpr(right)

    def __repr__(self):
        return f'{repr(self.left)} {self.op} {repr(self.right)}'

    def key(self):
        return self.op

    def get_format(self):
        return ' '.join(['{}', self.op, '{}'])

    def get_params(self):
        return (self.left, self.right)

class COption(CExpr):
    name: str
    value: CExpr

    def __init__(self, name: str, value):
        self.name = name
        self.value = toCExpr(value)

    def __repr__(self):
        return f'{self.name} = {self.value}'

    def key(self):
        return self.name

    def get_format(self):
        return ' '.join([self.name, '=', '{}'])

    def get_params(self):
        return (self.value,)

class CApp(CExpr):
    name: str
    es: list[CExpr]

    def __init__(self, name: str, *es):
        self.name = name
        self.es = tuple(toCExpr(e) for e in es)

    def __repr__(self):
        ss = []
        ss.append(self.name)
        ss.append('(')
        for i, e in enumerate(self.es):
            if i > 0:
                ss.append(',')
            ss.append(str(e))
        ss.append(')')
        return ' '.join(ss)
    
    def key(self):
        return self.name

    def get_format(self):
        ss = []
        ss.append(self.name)
        ss.append('(')
        for i, e in enumerate(self.es):
            if isinstance(e, COption):
                break
            if i > 0:
                ss.append(',')
            ss.append(repr(e))
        ss.append(')')
        return ' '.join(ss)

    def get_params(self):
        ss = []
        for e in self.es:
            if isinstance(e, COption):
                break
            ss.append(e)
        return ss


e = CApp('print', 1, COption('end', ''))
print(e)

####################################################

RESULT = '結果'

class NExpr(CExpr):

    def append(self, e):
        return NChoice(self, e)

    def asType(self, ret):
        return self

    def apply(self, mapped):
        return self

class NChoice(NExpr):
    choices: tuple[NExpr]

    def __init__(self, *choices):
        self.choices = choices

    def append(self, e: NExpr):
        return NChoice(*(self.choices + (e,)))

    def asType(self, ret):
        return NChoice(*[c.asType(ret) for c in self.choices])

    def apply(self, mapped):
        return NChoice(*[c.apply(mapped) for c in self.choices])

    def __str__(self):
        return '{' + '|'.join(self.choices) + '}'

    def emit(self, suffix):
        return self.choices[0].emit(suffix)

class NPiece(NExpr):
    piece: str
    def __init__(self, piece):
        self.piece = piece

    def __str__(self):
        return self.piece

    def emit(self, suffix):
        return self.piece

class NVerb(NExpr):
    verb: str
    ret: str

    def __init__(self, verb, ret = ''):
        assert isinstance(verb, str), type(verb)
        self.verb = str(verb)
        self.ret = ret

    def asType(self, ret):
        return NVerb(self.verb, ret)

    def __str__(self):
        if self.ret == '':
            return self.verb
        return f'{self.verb}# {self.ret}'

    def emit(self, suffix):
        if suffix == RESULT and self.ret != '':
            suffix = self.ret
        return self.verb + f'# {suffix}'

class NValue(NPiece):
    def emit(self, suffix):
        return f'{suffix} {self.piece}'

class NParam(NExpr):
    symbol: str
    index: int
    kind: str
    bound: NExpr

    def __init__(self, symbol, index, kind='', bound = None):
        self.symbol = symbol
        self.index = index
        self.kind = kind
        self.bound = bound

    def apply(self, mapped):
        if self.index in mapped:
            bound = mapped[self.index]
            return NParam(self.symbol, self.index, self.kind, bound)
        return self

    def __str__(self):
        return ALPHA[self.index]

    def emit(self, suffix):
        if self.bound is None:
            return self.symbol
        return self.bound.emit(RESULT if self.kind == '' else self.kind)

def toNExpr(e):
    if isinstance(e, NExpr):
        return e
    if isinstance(e, CValue):
        return NValue(e.value)
    return NPiece(str(e))

class NPredicate(NExpr):
    pieces: tuple[NExpr]

    def __init__(self, *pieces):
        self.pieces = [toNExpr(p) for p in pieces]
 
    def asType(self, ret):
        return NPredicate(*[e.asType(ret) for e in self.pieces])

    def apply(self, mapped):
        return NPredicate(*[e.apply(mapped) for e in self.pieces])

    def __str__(self):
        ss = []
        for p in self.pieces:
            ss.append(str(p))
        return ' '.join(ss)

    def emit(self, suffix):
        ss = []
        for i, p in enumerate(self.pieces):
            ss.append(p.emit(suffix))
        return ' '.join(ss)

e = NPredicate('A', 'を', 'B', 'で', NVerb('置き換える')).asType('文字列')
print(e.emit('ファイル名'))


### Matcher

import itertools
def combi(clist):
    ss = [EMPTY]
    for i in range(1, min(len(clist)+1, 3)):
        for v in itertools.combinations(clist, i):
            ss.append(v)
    return ss[::-1]

def make_pattern(ce: CExpr, masked, mapped):
    ss = []
    for p in ce.get_params():
        if isinstance(p, CValue) and p.value in masked:
            ss.append(p.value)
        # elif ce.has_masked(masked):
        #     ss.append(make_pattern(ce, masked, mapped))
        else:
            index = len(mapped)
            mapped[index] = p
            ss.append(ALPHA[index])
    return ce.get_format().format(*ss)

class Matcher(object):

    def __init__(self):
        self.keys = {}
        self.patterns = {}
    
    def match(self, ce: CExpr) -> NExpr:
        key = ce.key()
        for mask in combi(self.keys.get(key, EMPTY)):
            mapped = {}
            pat = make_pattern(ce, mask, mapped)
            print(mask, pat)
            if pat in self.patterns:
                for key in mapped:
                    print('@', mapped)
                    mapped[key] = self.match(mapped[key])
                return self.patterns[pat].apply(mapped)
        return NPiece(str(ce))

m = Matcher()

##

import pegtree as pg
from pegtree import ParseTree
from pegtree.visitor import ParseTreeVisitor
peg = pg.grammar('kotonoha2.tpeg')
parser = pg.generate(peg)

def expression_key(tree):
    if tree.has('name'):
        return tree.getToken('name')
    return None

def expression_value(tree):
    tag = tree.getTag()
    if tag == 'Name' or tag == 'Symbol':
        return str(tree)
    # if tag == 'Int':
    #     s = str(tree).replace('_', '')
    #     if s.startswith('0b') or s.startswith('0B'):
    #         return str(int(s[2:], 2))
    #     return str(int(s))
    # if tag == 'String':
    #     s = str(tree)
    #     if s.startswith('"') and s.endswith('"'):
    #         s = s[1:-1]
    #     if s.startswith('\'') and s.endswith('\''):
    #         s = s[1:-1]
    #     return '"'+s.encode().decode('unicode-escape')+"'"
    return None

def find_values(tree: ParseTree, values: dict):
    if len(tree) == 0:
        v = expression_value(tree)
        if v is not None:
            values[v] = len(values)
    else:
        for label, child in tree.subs():
            find_values(child, values)


class Reader(ParseTreeVisitor):
    key_consts: dict
    patterns: dict

    indexes: dict
    consts: dict
    mapped: dict

    def __init__(self):
        ParseTreeVisitor.__init__(self)
        self.key_consts = m.keys
        self.patterns = m.patterns

    def load(self, file):
        with open(file) as f:
            source = f.read()
            tree = parser(source, urn=file)
            self.visit(tree)

    def acceptSource(self, tree):
        for t in tree:
            self.visit(t)
        
    def acceptRule(self, tree):
        expr = tree[0]
        doc = tree[1]
        key = expression_key(expr)
        self.indexes = {}
        find_values(tree[1], self.indexes)
        #print(doc, self.indexes)
        #print(repr(expr))
        if key in self.key_consts:
            self.consts = set(self.key_consts[key])
        else:
            self.consts = set()
        self.mapped = {}
        code = self.visit(expr)
        if len(self.consts) > 0:
            #print('const', key, tuple(self.consts))
            self.key_consts[key] = tuple(self.consts)
        self.indexes = self.mapped
        pred = self.visit(doc)
        self.patterns[str(code)] = pred
        print(str(code), '##', pred)
    
    def acceptInfix(self, tree):
        name = tree.name
        left = self.visit(tree.left)
        right = self.visit(tree.right)
        return CBinary(left, name, right)

    def acceptApplyExpr(self, tree):
        name = str(tree.name)
        params = self.visit(tree.params)
        return CApp(name, *params)

    def acceptArguments(self, tree):
        return [self.visit(e) for e in tree]

    def acceptName(self, tree):
        s = str(tree)
        if s in self.indexes:
            if s not in self.mapped:
                self.mapped[s] = len(self.mapped)
            return CIndex(self.mapped[s])
        return CVar(s)

    def acceptString(self, tree):
        s = str(tree)
        if s.startswith("'") and s.endswith("'"):
            s = '"' + s[1:-1].replace("'", "\\'") + '"'
        self.consts.add(s)
        return CValue(s)

    def acceptUndefined(self, tree):
        s = str(tree)
        self.consts.add(s)
        return CValue(s)
    
    def acceptDocument(self, tree):
        ret = ''
        ss = []
        for t in tree:
            if t.getTag() == 'Return':
                ret = str(t).strip()
            else:
                ss.append(self.visit(t))
        e = NPredicate(*ss)
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
        kind = str(tree[1])
        if isinstance(piece, NParam):
            piece.kind = kind
            return piece
        return kind

    def acceptVerb(self, tree):
        e = NVerb(str(tree[0]))
        for t in tree[1:]:
            e = e.append(NVerb(str(t)))
        return e

Reader().load('rule.py')

e = CBinary(CBinary(CVar('x'), '%', CValue('3')), '==', CValue('0'))
print(e)
pred = m.match(e)
print(pred)
