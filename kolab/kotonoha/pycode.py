import sys
import pegtree as pg
from pegtree import ParseTree
from kolab.kotonoha.visitor import TransCompiler

RESERVED = {
    'math', 'numpy', 'np', 'pandas', 'pd',
    'datetime', 'urllib', 'random', 'io', 'itertools', 'functools',
    'os', 'sys', 'subprocess', 'time', 're', 'requests',
    'int', 'str', 'float'
}


class VocabMap(object):
    voc: dict

    def __init__(self, env, token_format='{}'):
        self.token = token_format
        self.env = env
        self.voc = {}

    def init(self):
        self.voc = {}

    def new_name(self, old_name=None):
        s = self.token.format(chr(ord('A')+(len(self.voc) % 27)))
        if old_name is not None:
            self.voc[old_name] = s
        # s = old_name
        return s

    def isIndexedName(self, name):
        if name.endswith('Error'):
            return False
        return name not in RESERVED

    def rename(self, name, rename=True):
        if name.startswith('"'):
            name = "'" + name[1:-1] + "'"
        if name in self.env:
            d = self.env[name]
            if 0 in d:
                return d[0] if rename else name
        if name not in self.voc:
            if self.isIndexedName(name):
                return self.new_name(name)
            return name
        else:
            return self.voc[name]

    def index_name(self, name):
        return self.rename(name, False)


class PythonCode(TransCompiler):
    vocmap: VocabMap

    def __init__(self, grammar='../pegtree/puppy2.tpeg'):
        TransCompiler.__init__(self)
        peg = pg.grammar(grammar)
        self.parser = pg.generate(peg)
        self.vocmap = None
        self.isTrimString = False

    def load(self, modules, experimental=False):
        pass

    def compile(self, source):
        tree = self.parser(source)
        self.indent = 0
        return self.stringfy(tree, ' ')

    def set_vocmap(self, vocmap):
        self.vocmap = vocmap

    def acceptSeq(self, tree, sep=','):
        for i, e in enumerate(tree.getSubNodes()):
            if i > 0:
                self.push(sep)
            self.visit(e)

    def acceptSource(self, tree):
        trees = tree.getSubNodes()
        for t in trees:
            self.pushBOS()
            self.visit(t)

    def acceptBlock(self, tree):
        self.indent += 1
        self.acceptSource(tree)
        self.indent -= 1

    def acceptDocument(self, tree):
        pass

    def accepterr(self, tree):
        pass
        #print('E', str(tree), file=sys.stderr)

    def acceptClassDecl(self, tree):
        self.push('class')
        self.visit(tree.name)
        if tree.has('extends'):
            self.push('(')
            self.acceptSeq(tree.extends)
            self.push(')')
        self.push(':')
        self.visit(tree.body)

    def acceptVarTypeDecl(self, tree):
        self.visit(tree.name)
        self.push(':')
        self.push(str(tree.type))

    # Statement

    def acceptPass(self, tree):
        self.push('pass')

    def acceptAssert(self, tree):
        self.push('assert')
        self.visit(tree.cond)

    def acceptIf(self, tree):
        self.push('if')
        self.visit(tree.cond)
        self.push(':')
        self.visit(tree.get('then'))
        if tree.has('elif'):
            for t in tree.get('elif').getSubNodes():
                self.visit(t)
        if tree.has('else'):
            self.visit(tree.get('else'))

    def acceptElif(self, tree):
        self.pushBOS()
        self.push('elif')
        self.visit(tree.cond)
        self.push(':')
        self.visit(tree.get('then'))

    def acceptElse(self, tree):
        self.pushBOS()
        self.push('else')
        self.push(':')
        self.visit(tree[0])

    def acceptWhile(self, tree):
        self.push('while')
        self.visit(tree.cond)
        self.push(':')
        self.visit(tree.body)

    def acceptTry(self, tree):
        self.push('try')
        self.push(':')
        self.visit(tree.body)
        if tree.has('except'):
            for e in tree.get('except'):
                self.visit(e)
        if tree.has('else'):
            self.visit(tree.get('else'))
        if tree.has('finally'):
            self.visit(tree.get('finally'))

    def acceptExcept(self, tree):
        self.pushBOS()
        self.push('except')
        if tree.has('cond'):
            self.push(str(tree.cond))
            if tree.has('as'):
                self.push('as')
                self.visit(tree.get('as'))
        self.push(':')
        self.visit(tree.body)

    def acceptFinally(self, tree):
        self.pushBOS()
        self.push('finally')
        self.push(':')
        self.visit(tree[0])

    def acceptWith(self, tree):
        self.pushBOS()
        self.push('with')
        self.visit(tree.expr)
        self.push('as')
        self.visit(tree.name)
        self.push(':')
        self.visit(tree.body)

    # break

    def acceptBreak(self, tree):
        self.push('break')

    # continue
    def acceptContinue(self, tree):
        self.push('continue')

    def acceptFor(self, tree):
        self.push('for')
        self.acceptSeq(tree.each)
        self.push('in')
        self.visit(tree.list)
        self.push(':')
        self.visit(tree.body)

    def acceptImportDecl(self, tree):
        self.push('import')
        name = str(tree.name)
        self.push(name)
        if tree.has('as'):
            self.push('as')
            self.push(str(tree.get('as')))

    def acceptFromDecl(self, tree):
        self.push('from')
        self.push(str(tree.name).replace('.', ' . '))
        self.push('import')
        self.acceptSeq(tree.names)
        if tree.has('as'):
            self.push('as')
            self.push(str(tree.get('as')))

    def acceptVarDecl(self, tree):
        self.visit(tree.name)
        self.push('=')
        self.visit(tree.expr)

    def acceptAssignment(self, tree):
        self.visit(tree.left)
        self.push('=')
        self.visit(tree.right)

    # a,b = c [#MultiAssignment left: [# [#Name 'a'][#Name 'b']]right: [#Name 'c']]
    def acceptMultiAssignment(self, tree):
        self.acceptSeq(tree.left)
        self.push('=')
        if len(tree.right) == 0:
            self.visit(tree.right)
        else:
            self.acceptSeq(tree.right)

    # a += 1
    def acceptSelfAssignment(self, tree):
        self.visit(tree.left)
        self.push(tree.name)
        self.visit(tree.right)

    def acceptDelete(self, tree):
        self.push('del')
        self.visit(tree.expr)

    def acceptExpression(self, tree):
        self.visit(tree[0])

    # def f(a,b):
    def acceptFuncDecl(self, tree):
        self.push('def')
        self.push(str(tree.name))
        self.push('(')
        self.acceptSeq(tree.params)
        self.push(')')
        self.push(':')
        self.visit(tree.body)

    def acceptParamDecl(self, param):
        self.visit(param.name)
        if param.has('type'):
            self.push(':')
            self.push(str(param.type))
        if param.has('value'):
            self.push('=')
            self.push(str(param.value))

    def acceptFuncExpr(self, tree):
        self.push('lambda')
        self.acceptSeq(tree.params)
        self.push(':')
        self.visit(tree.body)

    # return

    def acceptReturn(self, tree):
        self.push('return')
        if tree.has('expr'):
            self.visit(tree.expr)

    def acceptYield(self, tree):
        self.push('yield')
        if tree.has('expr'):
            self.visit(tree.expr)

    def acceptRaise(self, tree):
        self.push('raise')
        self.visit(tree.expr)

    # Expression
    def acceptName(self, tree):
        name = str(tree)
        if self.vocmap is not None:
            name = self.vocmap.index_name(name)
        self.push(name)

    def acceptGlobal(self, tree):
        self.push('global')
        self.acceptSeq(tree[0])

    def acceptNonLocal(self, tree):
        self.push('nonlocal')
        self.acceptSeq(tree[0])

    # [#ApplyExpr 'a']

    def acceptApplyExpr(self, tree):
        name = str(tree.name)
        self.push(name)
        self.push('(')
        self.acceptSeq(tree.params)
        self.push(')')

    def acceptMethodExpr(self, tree):
        self.visit(tree.recv)
        self.push('.')
        self.push(str(tree.name))
        self.push('(')
        self.acceptSeq(tree.params)
        self.push(')')

    def acceptOption(self, tree):
        for i, t in enumerate(tree):
            if i > 0:
                self.push(',')
            self.push(str(t.name))
            self.push('=')
            self.visit(t.value)

    #  o.name
    def acceptGetExpr(self, tree):
        self.visit(tree.recv)
        self.push('.')
        name = str(tree.name)
        self.push(name)

    def acceptIndexExpr(self, tree):
        self.visit(tree.recv)
        self.push('[')
        self.visit(tree.index)
        self.push(']')

    def acceptSliceExpr(self, tree):
        self.visit(tree.recv)
        self.push('[')
        if tree.has('start'):
            self.visit(tree.start)
        self.push(':')
        if tree.has('end'):
            self.visit(tree.end)
        if tree.has('step'):
            self.push(':')
            self.visit(tree.step)
        self.push(']')

    def acceptUnary(self, tree):
        name = str(tree.name)
        self.push(name)
        self.visit(tree.expr)

    def acceptInfix(self, tree):
        self.visit(tree.left)
        name = str(tree.name)
        self.push(name)
        self.visit(tree.right)

    def acceptMul(self, tree: ParseTree):
        self.visit(tree[0])
        self.push('*')
        self.visit(tree[1])

    def acceptAnd(self, tree):
        self.visit(tree.left)
        self.push('and')
        self.visit(tree.right)

    def acceptOr(self, tree):
        self.visit(tree.left)
        self.push('or')
        self.visit(tree.right)

    def acceptNot(self, tree):
        self.push('not')
        self.visit(tree[0])

    def acceptListArgument(self, tree):
        self.push('*')
        self.visit(tree[0])

    def acceptGroup(self, tree):
        self.push('(')
        self.visit(tree[0])
        self.push(')')

    def acceptTuple(self, tree):
        self.push('(')
        for i, e in enumerate(tree.getSubNodes()):
            if i > 0:
                self.push(',')
            self.visit(e)
        self.push(')')

    def acceptSet(self, tree):
        self.push('{')
        self.acceptSeq(tree, ',')
        self.push('}')

    def acceptList(self, tree):
        if len(tree) == 1 and tree[0] == 'ForExpr':
            self.visit(tree[0])
        else:
            self.push('[')
            self.acceptSeq(tree, ',')
            self.push(']')

    def acceptData(self, tree):
        self.push('{')
        self.acceptSeq(tree, ',')
        self.push('}')

    def acceptKeyValue(self, tree):
        self.push(str(tree.name))
        self.push(':')
        self.visit(tree.value)

    def acceptEmpty(self, tree):
        pass

    def acceptNull(self, tree):
        self.push('None')

    def acceptTrue(self, tree):
        self.push('True')

    def acceptFalse(self, tree):
        self.push('False')

    def acceptInt(self, tree):
        self.push(str(tree))

    def acceptFloat(self, tree):
        self.push(str(tree))

    def acceptDouble(self, tree):
        self.push(str(tree))

    def acceptQString(self, tree):
        s = str(tree)
        if self.vocmap is not None:
            s = self.vocmap.index_name(s)
        if self.isTrimString and ' ' in s:
            quote = s[0]
            s = s.split(' ')[0] + quote
        self.push(s)

    def acceptMultiString(self, tree):
        s = str(tree)
        if self.vocmap is not None:
            s = self.vocmap.index_name(s)
        if self.isTrimString and ' ' in s:
            quote = s[0]
            s = s.split(' ')[0] + quote
        self.push(s)

    def acceptFormat(self, tree):
        self.push(str(tree))

    def acceptIfExpr(self, tree):
        self.visit(tree.then)
        self.push('if')
        self.visit(tree.cond)
        self.push('else')
        self.visit(tree.get('else'))

    def acceptForExpr(self, tree):
        self.push('[')
        self.visit(tree.append)
        self.push('for')
        self.acceptSeq(tree.each)
        self.push('in')
        self.visit(tree.list)
        if tree.has('cond'):
            self.push('if')
            self.visit(tree.cond)
        self.push(']')

    def acceptListForExpr(self, tree):
        self.push('[')
        self.visit(tree.append)
        for e in tree.getSubNodes():
            self.acceptForExprIter(e)
        self.push(']')

    def acceptForExprIter(self, tree):
        self.push('for')
        self.acceptSeq(tree.each)
        self.push('in')
        self.visit(tree.list)
        if tree.has('cond'):
            self.push('if')
            self.visit(tree.cond)


def main(argv):
    from tqdm import tqdm
    transpiler = PythonCode()
    transpiler.isTrimString = True
    for filename in tqdm(argv):
        try:
            with open(filename) as f:
                ss = []
                for line in f.readlines():
                    if line[0].isspace():
                        ss.append(line)
                    else:
                        s = ''.join(ss)
                        if len(s) > 0:
                            compiled = transpiler.compile(s)
                            print(compiled)
                        ss = [line]
                s = ''.join(ss)
                if len(s) > 0:
                    compiled = transpiler.compile(s)
                    print(compiled)
        except UnicodeDecodeError:
            pass
        except AttributeError:
            print('Parser Error @' + filename, file=sys.stderr)
            pass


def allfiles(path, filelist):
    import os
    files = os.listdir(path)
    for file in files:
        npath = os.path.join(path, file)
        if os.path.isdir(npath):
            allfiles(npath, filelist)
        if os.path.isfile(npath) and npath.endswith('.py'):
            if 'test' not in npath:  # and os.path.getsize(npath) < 32_000:
                filelist.append(npath)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        filelist = []
        allfiles('/usr/local/lib/python3.9/site-packages', filelist)
        print(f'filesize {len(filelist)}', file=sys.stderr)
        main(filelist)
