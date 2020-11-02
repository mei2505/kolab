import sys
import pegtree as pg

METHODS = {

}

class Tokenizer(object):
    buffers: list
    parser: object
    def __init__(self, grammar='puppy2.tpeg'):
        self.buffers = []
        peg = pg.grammar(grammar)
        self.parser = pg.generate(peg)

    def push(self, s):
        self.buffers.append(s)

    def parse(self, source):
        tree = self.parser(source)
        self.buffers = []
        self.visit(tree)
        return self.buffers
    
    def visit(self, tree):
        tag = tree.getTag()
        if tag not in METHODS:
            METHODS[tag] = f'accept{tag}'
        method = METHODS[tag]
        if hasattr(self, method):
            method = getattr(self, method)
            return method(tree)
        else:
            print('@TODO', repr(tree))
            self.push(str(tree))

    def pushTrees(self, tree, start='(', sep=',', end=')'):
        if start != '':
            self.push(start)
        if len(tree) > 0:
            trees = tree.getSubNodes()
            for t in trees[:-1]:
                self.visit(t)
                self.push(sep)
            self.visit(trees[-1])
        if end != '':
            self.push(end)

    def acceptSource(self, tree):
        self.pushTrees(tree, '', '[SEP]', '')

    def acceptBlock(self, tree):
        self.pushTrees(tree, '[BGN]', '[SEP]', '[END]')

    def acceptNone(self, tree):
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

    # [#QString 'a']
    def acceptQString(self, tree):
        self.push(str(tree))

    # [#Name 'a']
    def acceptName(self, tree):
        self.push(str(tree))

    # [#Tuple 'a']
    def acceptTuple(self, tree):
        if len(tree) == 1:
            self.visit(tree[0])
        else:
            self.pushTrees(tree, '(', ',', ')')

    # [#List 'a']
    def acceptList(self, tree):
        if len(tree) == 0:
            self.push('[]')
        else:
            self.pushTrees(tree, '[', ',', ']')

    # [#Data 'a']
    def acceptData(self, tree):
        self.push(str(tree))

    # [#ApplyExpr 'a']
    def acceptApplyExpr(self, tree):
        name = str(tree.name)
        self.push(name)
        self.pushTrees(tree.params)

    # [#MethodExpr 'a']
    def acceptMethodExpr(self, tree):
        self.visit(tree.recv)
        self.push('.')
        name = str(tree.name)
        self.push(name)
        self.pushTrees(tree.params)

    # [#IndexExpr 'a']
    def acceptIndexExpr(self, tree):
        self.visit(tree.recv)
        self.push('[')
        self.visit(tree.index)
        self.push(']')

    # [#GetExpr 'o.a']
    def acceptGetExpr(self, tree):
        self.visit(tree.recv)
        self.push('.')
        self.push(str(tree.name))

    # [#Infix left: [#Int '1']name: [#Name '+']right: [#Int '1']]
    def acceptUnary(self, tree):
        name = str(tree.name)
        self.push(name)
        self.visit(tree.expr)

    # [#Infix left: [#Int '1']name: [#Name '+']right: [#Int '1']]
    def acceptInfix(self, tree):
        name = str(tree.name)
        self.visit(tree.left)
        self.push(name)
        self.visit(tree.right)

    def acceptMul(self, tree):
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

    def acceptIfExpr(self, tree):
        self.visit(tree.get('then'))
        self.push('if')
        self.visit(tree.cond)
        self.push('else')
        self.visit(tree.get('else'))

    def acceptExpression(self, tree):
        self.visit(tree[0])

    def acceptVarDecl(self, tree):
        self.visit(tree.name)
        self.push('=')
        self.visit(tree.expr)

    def acceptMultiAssignment(self, tree):
        self.pushTrees(tree.left, '', ',', '')
        self.push('=')
        if len(tree.right) == 1:
            self.visit(tree.right)
        else:
            self.pushTrees(tree.right, '', ',', '')

    # a += 1
    def acceptSelfAssignment(self, tree):
        name = str(tree.name)
        self.visit(tree.left)
        self.push(name)
        self.visit(tree.right)

    # a = 1
    def acceptAssignment(self, tree):
        self.visit(tree.left)
        self.push('=')
        self.visit(tree.right)

    # with f as x:
    def acceptWith(self, tree):
        self.push('with')
        self.visit(tree.expr)
        self.push('as')
        self.visit(tree.get('as'))
        if tree.has('body'):
            self.push(':')
            self.visit(tree.body)

    # if a > 0: pass
    def acceptPass(self, tree):
        self.push('pass')

    # if a > 0: pass
    def acceptEmpty(self, tree):
        pass
    
    # assert a > 0
    def acceptAssert(self, tree):
        self.push('assert')
        self.visit(tree.cond)
        if tree.has('expr'):
            self.push(':')
            self.visit(tree.get('expr'))

    # if a > 0: pass
    def acceptIf(self, tree):
        self.push('if')
        self.visit(tree.cond)
        self.push(':')
        self.visit(tree.get('then'))
        if tree.has('elif'):
            for t in tree.get('elif').getSubNodes():
                self.visit(t)
        if tree.has('else'):
            self.push('else')
            self.push(':')
            self.visit(tree.get('else'))

    def acceptElif(self, tree, ):
        self.push('elif')
        self.visit(tree.cond)
        self.push(':')
        self.visit(tree.get('then'))

    def acceptWhile(self, tree):
        self.push('while')
        self.visit(tree.cond)
        self.push(':')
        self.visit(tree.body)

    def acceptFor(self, tree):
        self.push('for')
        self.pushTrees(tree.each, '', ',', '')
        self.push('in')
        self.visit(tree.list)
        self.push(':')
        self.visit(tree.body)

    def acceptTry(self, tree):
        self.push('try')
        self.visit(tree.body)
        if tree.has('except'):
            for t in tree.get('except'):
                self.push('except')
                if t.has('cond'):
                    self.visit(t.cond)
                if t.has('as'):
                    self.push('as')
                    self.visit(t.get('as'))
                self.push(':')
                self.visit(t.body)
        if tree.has('finally'):
            self.push('finally')
            self.push(':')
            self.visit(tree.get('finally'))

    # raise NameError from a
    def acceptRaise(self, tree):
        self.push('raise')
        self.visit(tree.expr)
        if tree.has('from'):
            self.push('from')
            self.visit(tree.get('from'))

    def acceptListForExpr(self, tree):
        self.push('[')
        self.visit(tree.append)
        for t in tree:
            self.push('for')
            self.visit(t.each)
            self.push('in')
            self.visit(t.list)
            if t.has('cond'):
                self.push('if')
                self.visit(t.cond)
        self.push(']')

    # break
    def acceptBreak(self, tree):
        self.push('break')

    # continue
    def acceptContinue(self, tree):
        self.push('continue')

    # def f(a,b):
    def acceptFuncDecl(self, tree):
        self.push('def')
        name = str(tree.name)
        self.push(name)
        self.pushTrees(tree.params)
        self.push(':')
        self.visit(tree.body)

    def acceptParamDecl(self, tree):
        name = str(tree.name)
        self.push(name)
        if tree.has('type'):
            self.push(':')
            self.push(str(tree.type))
        if tree.has('value'):
            self.push('=')
            self.visit(tree.value)

    # return
    def acceptReturn(self, tree):
        self.push('return')
        if tree.has('expr'):
            self.visit(tree.expr)

    # class C: pass
    def acceptClassDecl(self, tree):
        self.push('class')
        self.push(str(tree.name))
        if tree.has('extends'):
            self.pushTrees(tree.extends)
        self.push(':')
        self.visit(tree.body)

    def acceptImportDecl(self, tree):
        self.push('import')
        name = str(tree.name)
        self.push(name)
        if tree.has('as'):
            self.push(str(tree.get('alias')))

    def acceptFromDecl(self, tree):
        self.push('from')
        self.push(str(tree.name))
        self.pushTrees(tree.names, '', ',', '')

    def acceptDocument(self, tree):
        pass

defaultPyTokenizer = None

def pytokens(s):
    global defaultPyTokenizer
    if defaultPyTokenizer == None:
        defaultPyTokenizer = Tokenizer()
    return defaultPyTokenizer.parse(s)

#tokenizer = Tokenizer()
#print(transpiler.compile('a, b = c\nx,y = y,x'))
#print(transpiler.compile('print("hello,world", end="")'))
#print(transpiler.compile('print(i, fibo(1))'))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            print(pytokens(f.read()))
