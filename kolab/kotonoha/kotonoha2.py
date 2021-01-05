import sys
import csv
import pathlib
import pegtree as pg
from collections import Counter
from pegtree import ParseTree

from kolab.kotonoha.visitor import TransCompiler
from kolab.kotonoha.pycode import PythonCode

from logging import getLogger
logger = getLogger(__name__)

# 文字列操作

hiragana = "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをん"


def containsHira(s):
    for c in s:
        if 'ぁ' <= c and c <= 'ん':
            return True
    return False


def chunk(s):
    # nested = 0
    # found = False
    # for i in range(len(s)):
    #     if s.startswith("{{", i):
    #         nested += 1
    #     elif s.startswith("}}", i):
    #         nested -= 1
    #     elif nested == 0 and s[i] in "にをがで":
    #         found = True
    #         break
    #     else:
    #         pass
    # if found:
    #     return '{{' + s + '}}'
    return s


THEN = {
    'く': 'き', 'す': 'し', 'つ': 'ち', 'ぬ': 'に', 'む': 'み',
    'う': 'い', 'ぐ': 'ぎ', 'ぶ': 'び', 'た': 'て', 'だ': 'で'
}


def and_then(s):
    if s.endswith('かどうか'):
        s = s[:-4]
    if s.endswith('い'):   # 美しい ない
        return s[:-1] + 'く'
    if s.endswith('する'):  # 含まれる  高め
        return s[:-2] + 'して'
    if s.endswith('る'):  # 含まれる  高め
        return s[:-1]
    if s[-1] in THEN:
        return s[:-1] + THEN[s[-1]]
    return s


NAI = {
    'く': 'か', 'す': 'さ', 'つ': 'た', 'ぬ': 'な', 'む': 'ま',
    'う': 'わ', 'ぐ': 'が', 'ぶ': 'ば', 'た': 'て', 'だ': 'で'
}


def not_nai(s):  # ないは自分でつける
    if s.endswith('かどうか'):
        s = s[:-4]
    if s.endswith('い'):   # 美しい ない
        return s[:-1] + 'く'
    if s.endswith('する'):  # 使用する
        return s[:-2] + 'し'
    if s.endswith('る'):  # 含まれる  高め
        return s[:-1]
    if s[-1] in NAI:
        return s[:-1] + NAI[s[-1]]
    return s + 'で'


def and_noun(s):  # +とき
    if s.endswith('かどうか'):
        s = s[:-4]
        # 大きい　含まれる　含まれた
        if s[-1] in "いるた":
            return s
    if s[-1] in 'いるた':  # する
        return s
    if s[-1] in NAI:
        return s
    return s + 'の'


# PJ

base = pathlib.Path(__file__).parent.resolve()

PARAMS = ('{}', '{0}', '{1}', '{2}', '{3}', '{4}', '{5}')


def check_pair(key, value, env):
    if 'A' in value:
        value = value.replace('A', '{0}')
        value = value.replace('B', '{1}')
        value = value.replace('C', '{2}')
        value = value.replace('D', '{3}')
        value = value.replace('E', '{4}')
        value = value.replace('F', '{5}')

    localkey = sum(value.count(x) for x in PARAMS)
    value = value.strip()
    if '@' in key:
        key, localkey = key.split('@')
    if '#' in key:
        key, localkey = key.split('#')
    if key not in env:
        env[key] = {}
    entry = env[key]
    if localkey in entry and entry[localkey] == value:
        logger.warning(f'duplicated key: {key}#{localkey}')
    entry[localkey] = value
    # print(value, and_then(value), and_noun(value)+'とき', not_nai(value))


def read_corpus(module, env={}, experimental=False):
    file = module
    if not module.endswith('.csv'):
        if '/' in module:
            file = f'{base}/{module}.csv'
        else:
            file = f'{base}/python-corpus/{module}.csv'
    with open(file) as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2 and row[1] != '':
                if row[0].startswith('#'):
                    continue
                if experimental and len(row) >= 3:
                    check_pair(row[0], row[2], env)
                else:
                    check_pair(row[0], row[1], env)


PYTHON = {}

TYPES = {
    'List': 'list', 'Set': 'set', 'Int': 'int', 'QString': 'str',
    'True': 'bool', 'False': 'bool', 'Float': 'float', 'Double': 'float',
}


def guess_type(tree, default_type=''):
    tag = tree.getTag()
    if tag in TYPES:
        return TYPES[tag]
    return default_type


py = 'py'
ja = 'ja'


class Camma(object):
    tree: ParseTree

    def __init__(self, tree):
        self.tree = tree


class TreeApp(object):
    tree: ParseTree

    def __init__(self, tree):
        self.tree = tree

    def conv(self, s):
        return s


class AndThen(TreeApp):
    def __init__(self, tree):
        TreeApp.__init__(self, tree)

    def conv(self, s):
        return and_then(s)


class NounPrefix(TreeApp):
    def __init__(self, tree):
        TreeApp.__init__(self, tree)

    def conv(self, s):
        return and_noun(s)


class NaiPrefix(TreeApp):
    def __init__(self, tree, suffix=''):
        TreeApp.__init__(self, tree)
        self.suffix = suffix

    def conv(self, s):
        return not_nai(s)+self.suffix


class Index(TreeApp):
    def __init__(self, tree, suffix=''):
        TreeApp.__init__(self, tree)
        self.suffix = suffix

    def conv(self, s):
        if s == '0':
            return '先頭'+self.suffix
        if s == '-1':
            return '末尾'+self.suffix
        if s.isdigit():
            if s.startswith('-'):
                return f'末尾から{s[1:]}番目'+self.suffix
            return f'{s}番目'+self.suffix
        if not containsHira(s):
            return f'{s}番目'+self.suffix
        return s+self.suffix  # 加えた値


UNK = []


class Kotonoha(TransCompiler):
    parser: object
    pycode: PythonCode

    def __init__(self, grammar='../pegtree/puppy2.tpeg'):
        TransCompiler.__init__(self)
        peg = pg.grammar(grammar)
        self.parser = pg.generate(peg)
        self.pycode = PythonCode(grammar)
        self.env = {}

    def load(self, modules, experimental=False):
        for module in modules.split(':'):
            read_corpus(module, self.env, experimental)

    def parse(self, source):
        return self.parser(source)

    def compile(self, source):
        if len(self.env) == 0:
            self.load('python3:builtin:random')
        tree = self.parser(source)
        self.pycode.init()
        self.buffers = []
        self.indent = 0
        self.level = 0
        try:
            self.pushenv()
            self.visit(tree)
        finally:
            self.popenv()
        return ''.join(self.buffers)

    # Sentence

    def extend(tree):
        if isinstance(tree, ParseTree):
            return [tree]

    def pushSentence(self, key, *tree):
        self.level = 0
        self.pushBOS('# ')
        self.pushExpression(key, *tree)

    def pushExpression(self, key, *tree):
        prefix = ''
        defined = self.getenv(key)
        param_size = len(tree)
        params = []
        for t in tree:
            if isinstance(t, ParseTree):
                if t == 'Option':
                    prefix = self.parseOption(key, defined, t)
                    param_size -= 1
                else:
                    params.append(self.stringfy(t))
            elif isinstance(t, Camma):
                params.append('、'.join([self.stringfy(e) for e in t.tree]))
            elif isinstance(t, TreeApp):
                params.append(t.conv(self.stringfy(t.tree)))
            else:
                params.append(str(t))
        try:
            if param_size not in defined:
                param_max = max(x for x in defined.keys()
                                if isinstance(x, int))
                if len(params) > param_max:
                    params = params[:param_max-1] + \
                        ['、'.join(params[param_max-1:])]
                    param_size = param_max
                else:
                    param_max = min(x for x in defined.keys()
                                    if isinstance(x, int))
                    params = params + ['[MASK]'] * (param_max-len(params))
                    param_size = param_max
            self.push(prefix + defined[param_size].format(*params))
        except ValueError:
            print(f'@FIXME ValueError key={key}', defined, tree, file=sys.stderr)
            self.push('[MASK]')
        except:
            print(f'@FIXME key={key}', defined, tree, file=sys.stderr)
            self.push('[MASK]')

    def parseOption(self, funcname, defined, tree):
        ss = []
        #print('@', repr(tree))
        for t in tree.getSubNodes():
            key = str(t.name)+'='
            longkey = key+str(t.value).replace('"', "'")
            if longkey in defined:
                ss.append(defined[longkey])
            elif key in defined:
                ss.append(defined[key].format(self.stringfy(t.value)))
            elif self.hasenv(longkey):
                ldefined = self.getenv(longkey)
                ss.append(ldefined[0])
            elif self.hasenv(key):
                ldefined = self.getenv(key)
                ss.append(ldefined[1].format(self.stringfy(t.value)))
            else:
                ldefined = self.getenv('=O')
                ss.append(ldefined[2].format(
                    self.rename(str(t.name)), self.stringfy(t.value)))
        return ''.join(ss)

    def stringfy(self, tree):
        if self.level < 5 and isinstance(tree, ParseTree):
            stored_buffer = self.buffers
            stored_level = self.level
            self.buffers = []
            self.level += 1
            self.visit(tree)
            s = ''.join(self.buffers)
            self.buffers = stored_buffer
            self.level = stored_level
            if self.level > 1:
                s = chunk(s)
            return s
        else:
            return self.codify(tree)

    def codify(self, tree):
        return self.pycode.stringfy(tree)

    # Source

    def acceptSource(self, tree):
        trees = tree.getSubNodes()
        for t in trees:
            self.visit(t)

    def acceptBlock(self, tree):
        self.indent += 1
        self.acceptSource(tree)
        self.indent -= 1

    def acceptDocument(self, tree):
        pass

    # Statement

    def acceptPass(self, tree):
        self.pushSentence('pass')

    def acceptAssert(self, tree):
        self.pushSentence('assert', NaiPrefix(tree.cond))

    # if a > 0: pass

    def acceptIfExpr(self, tree):
        self.pushExpression('if', NounPrefix(tree.cond),
                            tree.then, tree.get('else'))

    def acceptIf(self, tree):
        self.pushSentence('if', NounPrefix(tree.cond))
        self.visit(tree.get('then'))
        if tree.has('elif'):
            for t in tree.get('elif').getSubNodes():
                self.visit(t)
        if tree.has('else'):
            self.visit(tree.get('else'))

    def acceptElif(self, tree):
        self.pushSentence('elif', NounPrefix(tree.cond))
        self.visit(tree.get('then'))

    def acceptElse(self, tree):
        self.pushSentence('else')
        self.visit(tree[0])

    def acceptWhile(self, tree):
        if tree.cond == 'True':
            self.pushSentence('while')
        else:
            self.pushSentence('while', NounPrefix(tree.cond))
        self.visit(tree.body)

    def acceptTry(self, tree):
        self.pushSentence('try')
        self.visit(tree.body)
        if tree.has('except'):
            for e in tree.get('except'):
                self.visit(e)
        if tree.has('else'):
            self.visit(tree.get('else'))
        if tree.has('finally'):
            self.visit(tree.get('finally'))

    def acceptExcept(self, tree):
        if tree.has('cond'):
            if tree.has('as'):
                self.pushSentence('except', tree.cond, tree.get('as'))
            else:
                self.pushSentence('except', tree.cond)
        else:
            self.pushSentence('except')
        self.visit(tree.body)

    def acceptFinally(self, tree):
        self.pushSentence('finally')
        self.visit(tree[0])

    def acceptWith(self, tree):
        self.pushSentence('=W', tree.name, tree.expr)
        self.visit(tree.body)

    # break

    def acceptBreak(self, tree):
        self.pushSentence('break')

    # continue
    def acceptContinue(self, tree):
        self.pushSentence('continue')

    def acceptFor(self, tree):
        self.pushSentence('for', Camma(tree.each), tree.list)
        self.visit(tree.body)

    def acceptImportDecl(self, tree):
        name = str(tree.name)
        self.pushSentence('import', name)

    def acceptVarDecl(self, tree):
        self.pushSentence('=', tree.name, tree.expr)

    def acceptAssignment(self, tree):
        self.pushSentence('=A', tree.left, tree.right)

    def acceptMultiAssignment(self, tree):
        if len(tree.left) == 2 and len(tree.right) == 2:
            A = str(tree.left[0])
            B = str(tree.left[1])
            AA = str(tree.right[0])
            BB = str(tree.right[1])
            if A == BB and B == AA:
                self.pushSentence('=SWAP', tree.left[0], tree.left[1])
                return
        if tree.right == 'Tuple':
            self.pushSentence('=', Camma(tree.left), Camma(tree.right))
            # self.pushStatement('=', tree.left, tree.right)
        else:
            self.pushSentence('=D', Camma(tree.left), tree.right)

    # a += 1
    def acceptSelfAssignment(self, tree):
        name = str(tree.name)
        self.pushSentence(name, tree.left, tree.right)

    def acceptDelete(self, tree):
        self.pushSentence('del', tree.expr)

    def acceptExpression(self, tree):
        self.pushSentence('', tree[0])

    # def f(a,b):
    def acceptFuncDecl(self, tree):
        name = str(tree.name)
        try:
            self.pushenv()
            self.pushSentence('def', name, tree.params)
            self.visit(tree.body)
        finally:
            self.popenv()

    def acceptFuncParam(self, tree):
        ss = []
        for t in tree:
            name = str(t.name)
            self.setenv(name, {0: self.rename(name)})
            ss.append(self.rename(name))
        if len(ss) > 0:
            self.push('、'.join(ss)+'をパラメータとして')
        else:
            self.push('パラメータなしとして')

    def acceptReturn(self, tree):
        if tree.has('expr'):
            self.pushSentence('return', tree.expr)
        else:
            self.pushSentence('return')

    def acceptRaise(self, tree):
        self.pushSentence('raise', tree.expr)

    def acceptFuncExpr(self, tree):
        try:
            self.pushenv()
            self.pushExpression('lambda', tree.params, tree.body)
        finally:
            self.popenv()

    # Expression

    def acceptName(self, tree):
        name = str(tree)
        defined = self.getenv(name)
        if 0 in defined:
            self.push(defined[0])
        else:
            name = self.pycode.index_name(name)
            self.push(name)

    def rename(self, name):
        defined = self.getenv(name)
        if 0 in defined:
            return defined[0]
        return name

    # [#ApplyExpr 'a']

    def acceptApplyExpr(self, tree):
        name = str(tree.name)
        if self.hasenv(name):
            defined = self.getenv(name)
            ps = [p for p in tree.params]
            self.pushExpression(name, *ps)
        else:
            UNK.append(name)
            self.push(self.codify(tree))

    def rename(self, tree, suffix=''):
        return str(tree) + suffix

    def acceptMethodExpr(self, tree):
        # print('@recv', recv)
        name = str(tree.name)
        key = f'.{name}'
        module_key = self.rename(tree.recv, key)
        if self.hasenv(module_key):
            ps = [p for p in tree.params]
            self.pushExpression(module_key, *ps)
        elif self.hasenv(key):
            ps = [tree.recv] + [p for p in tree.params]
            self.pushExpression(key, *ps)
        else:
            UNK.append(module_key)
            UNK.append(key)
            self.push(self.codify(tree))

    #  o.name
    def acceptGetExpr(self, tree):
        name = str(tree.name)
        key = f'.{name}'
        module_key = self.rename(tree.recv, key)
        if self.hasenv(module_key):  # math.pi
            self.pushExpression(module_key)
        elif self.hasenv(key):  # .x
            self.pushExpression(key, tree.recv)
        else:
            self.pushExpression('.', tree.recv, self.rename(name))

    def acceptIndexExpr(self, tree):
        suffix = str(tree)
        key = 'a'+suffix[suffix.rfind('['):]
        if self.hasenv(key):
            self.pushExpression(key, tree.recv)
        else:
            self.pushExpression('a[]', tree.recv, tree.index)

    def acceptSliceExpr(self, tree):
        suffix = str(tree)
        key = 'a'+suffix[suffix.rfind('['):]
        if self.hasenv(key):
            self.pushExpression(key, tree.recv)
        else:
            start = Index(tree.start) if tree.has('start') else '先頭'
            end = Index(tree.end) if tree.has('end') else '末尾'
            if tree.has('step'):
                self.pushExpression('a[::]', tree.recv, start, end, tree.step)
            else:
                self.pushExpression('a[::]', tree.recv, start, end)

    def acceptUnary(self, tree):
        name = str(tree.name)
        self.pushExpression(name, tree.expr)

    def acceptInfix(self, tree):
        name = str(tree.name)
        self.pushExpression(name, tree.left, tree.right)

    def acceptMul(self, tree):
        if tree[0] == 'List':
            self.pushExpression('a*', tree[0], tree[1])
        else:
            self.pushExpression('*', tree[0], tree[1])

    def acceptAnd(self, tree):
        self.pushExpression('and', AndThen(tree.left), tree.right)

    def acceptOr(self, tree):
        self.pushExpression('or', AndThen(tree.left), tree.right)

    def acceptNot(self, tree):
        self.pushExpression('not', NaiPrefix(tree[0], 'ない'))

    def acceptListArgument(self, tree):
        self.pushExpression('*', tree[0])

    def acceptGroup(self, tree):
        self.visit(tree[0])

    def acceptTuple(self, tree):
        if len(tree) == 1:
            self.visit(tree[0])
        else:
            self.pushExpression('()', Camma(tree))

    def acceptSet(self, tree):
        self.push(f'({Camma(tree)})の集合')

    def acceptList(self, tree):
        if len(tree) == 1 and tree[0] == 'ForExpr':
            self.acceptForExpr(tree[0])
        elif len(tree) != 0:
            self.pushExpression('[]', Camma(tree))
        else:
            self.pushExpression('[]')

    def acceptData(self, tree):
        if len(tree) != 0:
            self.pushExpression('{}', Camma(tree))
        else:
            self.pushExpression('{}')

    def acceptKeyValue(self, tree):
        key = self.stringfy(tree.name)
        value = self.stringfy(tree.value)
        self.push(f'({key}, {value})')

    def acceptEmpty(self, tree):
        pass

    def acceptNull(self, tree):
        self.pushExpression('None')

    def acceptTrue(self, tree):
        self.pushExpression('True')

    def acceptFalse(self, tree):
        self.pushExpression('False')

    def acceptInt(self, tree):
        self.push(str(tree))

    def acceptFloat(self, tree):
        self.push(str(tree))

    def acceptDouble(self, tree):
        self.push(str(tree))

    def acceptQString(self, tree):
        key = str(tree)
        if key.startswith('"'):
            key = "'" + key[1:-1] + "'"
        if self.hasenv(key):
            key = self.getenv(key)[0]
        self.push(key)

    def acceptMultiString(self, tree):
        self.push(self.pycode.index_name(str(tree)))

    def acceptFormat(self, tree):
        ss = ['"']
        for t in tree:
            if t == 'StringPart':
                ss.append(str(t))
            else:
                ss.append('{}')
        ss.append('"')
        self.push(''.join(ss))

    def acceptForExpr(self, tree):
        vars = Camma(tree.each)
        if tree.has('cond'):
            self.pushExpression('for', tree.append, vars,
                                tree.list, NounPrefix(tree.cond))
        else:
            self.pushExpression('for', tree.append, vars, tree.list)


def make_corpus(filename):
    transpiler = Kotonoha()
    transpiler.load('python3:builtin:random')
    with open(sys.argv[1]) as f:

        for line in f.readlines():
            line = line.strip()
            tree = transpiler.parse(line)
            if tree.isSyntaxError():
                continue
            j = transpiler.compile(line)
            p = transpiler.pycode.compile(line)
            if j.startswith('#'):
                print(j)
                print(p)


if __name__ == '__main__':
    for filename in sys.argv[1:]:
        make_corpus(filename)
    print(Counter(UNK).most_common(100), file=sys.stderr)
