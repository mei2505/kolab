import sys
import csv, pathlib
import pegtree as pg
#from pjcorpus import get_corpus

METHODS = {

}

PARENT = '..'
InsertionPoint = '@'

class Visitor(object):
    buffers: list
    env: dict
    level:int
    indent: int

    def push(self, *ss):
        for s in ss:
            s = str(s)
            if s != '':
                self.buffers.append(s)

    def pushBOS(self, bos=''):
        if len(self.buffers) > 0:
            self.buffers.append('\n')
        if self.indent > 0:
            self.buffers.append("  " * self.indent)
        self.push(bos)

    def getenv(self, key, default_value={}):
        env = self.env
        while env is not None:
            if key in env:
                return env[key]
            env = env.get(PARENT, None)  
        return default_value
    
    def hasenv(self, key):
        return self.getenv(self, key) is not None

    def setenv(self, key, value):
        self.env[key] = value
    
    def stringfy(self, tree, trf=None):
        if self.level < 5 and not isinstance(tree, str):
            stored_buffer = self.buffers
            stored_level = self.level
            self.buffers = []
            self.level += 1
            self.visit(tree)
            s = ''.join(self.buffers)
            self.buffers = stored_buffer
            self.level = stored_level
            if trf is not None:
                s = trf(s)
            if self.level > 1:
                s = chunk(s)
            return s
        else:
            return str(tree)

    def groupfy(self, tree, max=2):
        xs = [self.stringfy(t) for t in tree]
        if len(xs) <= max:
            return 'と'.join(xs)
        return '、'.join(xs)

    def pushStatement(self, key, tree=None, tree2=None):
        self.pushBOS('')
        d = self.getenv(key)
        if tree is None:
            self.push(d['code'])
        elif tree2 is None:
            e = str(tree)
            self.push(d['code'].format(e))
        else:
            e = str(tree)
            e2 = str(tree2)
            self.push(d['code'].format(e, e2))

    def pushSentence(self, key, *tree):
        self.pushBOS('# ')
        self.level = 0
        params = [t if isinstance(t, str) else self.stringfy(t) for t in tree]
        defined = self.getenv(key)
        #print('@', key, len(tree), defined)
        self.push(defined[len(tree)].format(*params))

    def pushParallelCorpus(self, tree):
        if tree.has('doc'):
            name = None
            if tree.has('name'):
                name = str(tree.name)
            for t in tree.doc.getSubNodes():
                if t == 'KeyValue':
                    key = name
                    if t.has('key'):
                        key = str(t.key)
                    if key != None:
                        self.setenv(key, {0: str(t.value)})
                else:
                    self.pushBOS('## ' + str(t))

    def pushApplication(self, name, params, defined, ext=''):
        #print('@', p)
        for i in range(len(params)):
            if not isinstance(params[i], str):
                params[i] = self.stringfy(params[i])
        if len(params) in defined:
            template = defined[len(params)].replace(InsertionPoint, ext)
            self.push(template.format(*params))
        elif 1 in defined:
            template = defined[1].replace(InsertionPoint, ext)
            self.push(template.format(self.groupfy(params)))
        else:
            params = ','.join(params)
            self.push(f'{name}({params})') 

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
            self.push(repr(tree))

# 文字列操作

def chunk(s):
    nested = 0
    found = False
    for i in range(len(s)):
        if s.startswith("{{", i):
            nested += 1
        elif s.startswith("}}", i):
            nested -= 1
        elif nested == 0 and s[i] in "にをがで":
            found = True
            break
        else:
            pass
    if found:
        return '{{' + s + '}}'
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

def not_nai(s): # ないは自分でつける
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

def read_corpus(module, env={}):
    with open(f'{base}/python-corpus/{module}.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2 and row[1] != '':
                check_pair(row[0], row[1], env)

PARAMS = ('{}', '{0}', '{1}', '{2}', '{3}')

def check_pair(key, value, env):
    if 'A' in value:
        value = value.replace('A', '{0}')
        value = value.replace('B', '{1}')
        value = value.replace('C', '{2}')
        value = value.replace('C', '{3}')

    localkey = sum(value.count(x) for x in PARAMS)
    if ':' in key:
        key, localkey = key.split(':')
    if key not in env:
        env[key] = {}
    entry = env[key]
    if localkey in entry:
        print('@duplicated', key, localkey, entry[localkey], value)
    entry[localkey] = value
    #print(value, and_then(value), and_noun(value)+'とき', not_nai(value))

PYTHON = {}
read_corpus('python3', PYTHON)
read_corpus('builtin', PYTHON)
read_corpus('random', PYTHON)

py = 'py'
ja = 'ja'

class Kotonoha(Visitor):
    parser: object
    def __init__(self, grammar='../pegtree/puppy2.tpeg'):
        peg = pg.grammar(grammar)
        self.parser = pg.generate(peg)
        self.rootEnv = PYTHON

    def compile(self, source):
        tree = self.parser(source)
        self.buffers = []
        self.env = { PARENT: self.rootEnv }
        self.indent = 0
        self.level=0
        self.visit(tree)
        return ''.join(self.buffers)

    # Source

    def acceptSource(self, tree):
        trees = tree.getSubNodes()
        for t in trees[:-1]:
            self.visit(t)
        self.visit(trees[-1])
    
    def acceptBlock(self, tree):
        self.indent += 1
        self.acceptSource(tree)
        self.indent -= 1

    ## Statement

    def acceptPass(self, tree):
        self.pushSentence('pass')
        self.pushStatement('pass')

    # if a > 0: pass
    def acceptAssert(self, tree):
        self.pushSentence('assert', self.stringfy(tree.cond, trf=not_nai))
        self.pushStatement('assert', tree.cond)

    # if a > 0: pass
    def acceptIf(self, tree):
        self.pushSentence('if', self.stringfy(tree.cond, trf=and_noun))
        self.pushStatement('if', tree.cond)
        self.visit(tree.get('then'))
        if tree.has('elif'):
            for t in tree.get('elif').getSubNodes():
                self.visit(t)
        if tree.has('else'):
            self.pushSentence('else')
            self.pushStatement('else')
            self.visit(tree.get('else'))

    def acceptElif(self, tree, ):
        self.pushSentence('elif', self.stringfy(tree.cond, trf=and_noun))
        self.pushStatement('elif', tree.cond)
        self.visit(tree.get('then'))

    def acceptWhile(self, tree):
        self.pushSentence('while', self.stringfy(tree.cond, trf=and_noun))
        self.pushStatement('while', tree.cond)
        self.visit(tree.body)

    # break
    def acceptBreak(self, tree):
        self.pushSentence('break')
        self.pushStatement('break')

    # continue
    def acceptContinue(self, tree):
        self.pushSentence('continue')
        self.pushStatement('continue')

    def acceptFor(self, tree):
        self.pushSentence('for', self.groupfy(tree.each), tree.list)
        self.pushStatement('for', tree.each, tree.list)
        self.visit(tree.body)

    def acceptImportDecl(self, tree):
        name = str(tree.name)
        self.pushSentence('import', name)
        self.pushStatement('import', name)

    def acceptVarDecl(self, tree):
        #name = str(tree.get('name', 'left'))
        self.pushParallelCorpus(tree)
        name = str(tree.get('name'))
        self.pushSentence('=', name, tree.expr)
        self.pushStatement('=', name, tree.expr)

    def acceptAssignment(self, tree):
        #name = str(tree.get('name', 'left'))
        name = str(tree.get('left'))
        self.pushSentence('=A', name, tree.right)
        self.pushStatement('=A', name, tree.right)

    # a,b = c [#MultiAssignment left: [# [#Name 'a'][#Name 'b']]right: [#Name 'c']]
    def acceptMultiAssignment(self, tree):
        if len(tree.left) == 2 and len(tree.right) == 2:
            A = str(tree.left[0])
            B = str(tree.left[1])
            AA = str(tree.right[0])
            BB = str(tree.right[1])
            if A == BB and B == AA:
                self.pushSentence('=SWAP', tree.left[0], tree.left[1])
                self.pushStatement('=SWAP', tree.left[0], tree.left[1])
                return
        #print('@', repr(tree.right), len(tree.right))
        if tree.right == 'Tuple':
            self.pushSentence('=', self.groupfy(tree.left), self.groupfy(tree.right))
            self.pushStatement('=', tree.left, tree.right)
        else:
            self.pushSentence('=D', self.groupfy(tree.left), tree.right)
            self.pushStatement('=D', tree.left, tree.right)
        
    # a += 1
    def acceptSelfAssignment(self, tree):
        name = str(tree.name)
        p = [self.stringfy(tree.left), self.stringfy(tree.right)]
        self.pushApplication(name, p, self.getenv(name))

    def acceptExpression(self, tree):
        self.pushParallelCorpus(tree)
        self.pushSentence('', tree[0])
        self.pushStatement('', tree[0])

    # def f(a,b):
    def acceptFuncDecl(self, tree):
        name = str(tree.name)
        self.pushSentence('def', name, tree.params)
        self.pushStatement('def', name, tree.params)
        stacked_env = self.env
        self.env = {PARENT: self.env}
        self.visit(tree.body)
        self.env = stacked_env

    # return
    def acceptReturn(self, tree):
        self.pushParallelCorpus(tree)        
        if tree.has('expr'):
            self.pushSentence('return', tree.expr)
            self.pushStatement('return', tree.expr)
        else:
            self.pushSentence('return')
            self.pushStatement('return', '')


    # Expression 
    def acceptName(self, tree):
        name = str(tree)
        defined = self.getenv(name)
        if 0 in defined:
            self.push(defined[0])
        else:
            self.push(str(tree))


    # [#ApplyExpr 'a']
    def acceptApplyExpr(self, tree):
        name = str(tree.name)
        defined = self.getenv(name)
        params, extra = self.makeParamList(tree.params, defined)
        self.pushApplication(name, params, defined, extra)

    def makeParamList(self, params, fd):
        p = []
        p2=[]
        for tree in params.getSubNodes():
            #print(repr(tree), f'{tree[0].name}' if len(tree) > 0 else '@')
            if tree.getTag() == 'Data' and len(tree) > 0 and f'{tree[0].name}=' in fd:
                for t in tree.getSubNodes():
                    key = str(t.name)+'='
                    keyval = key+str(t.value).replace("'", '"')
                    if keyval in fd:
                        p2.append(fd[keyval])
                    elif key in fd:
                        p2.append(fd[key].format(self.stringfy(t.value)))
            else:
                p.append(self.stringfy(tree))
        return p, ''.join(p2)
    
    def acceptMethodExpr(self, tree):
        #print('@recv', recv)
        name = str(tree.name)
        defined = self.getenv(f'{str(tree.recv)}.{name}')
        if len(defined) > 0:
            params, extra = self.makeParamList(tree.params, defined)
            self.pushApplication(name, params, defined, extra)
        else:
            recv = self.stringfy(tree.recv)
            defined = self.getenv(f'.{name}')
            if len(defined) > 0:
                params, extra = self.makeParamList(tree.params, defined)
                params = [recv] + params
                self.pushApplication(name, params, defined, extra)
            else:
                self.push(str(tree))

    # [#IndexExpr 'a']
    def acceptIndexExpr(self, tree):
        recv = self.stringfy(tree.recv)
        index = self.stringfy(tree.index)
        if index == '0':
            self.push(f'{recv}の先頭')
        elif index == '-1':
            self.push(f'{recv}の末尾')
        else:
            self.push(f'{recv}[{index}]')

    #  o.name
    def acceptGetExpr(self, tree):
        recv = self.stringfy(tree.recv)
        name = self.stringfy(tree.name)
        defined = self.getenv(f'.{name}')
        if len(defined) > 0:
            self.push(f'{recv}の{defined.get(0, name)}')
            return
        defined = self.getenv(name)
        if len(defined) > 0:
            self.push(f'{recv}の{defined.get(0, name)}')
        else:
            self.push(f'{recv}.{name}')

    def acceptUnary(self, tree):
        name = str(tree.name)
        p = [self.stringfy(tree.expr)]
        self.pushApplication(name, p, self.getenv(name))

    def acceptInfix(self, tree):
        name = str(tree.name)
        p = [self.stringfy(tree.left), self.stringfy(tree.right)]
        self.pushApplication(name, p, self.getenv(name))

    def acceptAnd(self, tree):
        p = [self.stringfy(tree.left, trf=and_then), self.stringfy(tree.right)]
        self.push(f'{p[0]}、かつ{p[1]}')

    def acceptOr(self, tree):
        p = [self.stringfy(tree.left, trf=and_then), self.stringfy(tree.right)]
        self.push(f'{p[0]}、または{p[1]}')

    def acceptNot(self, tree):
        self.push(self.stringfy(tree.expr, trf=not_nai) + 'ない')

    def acceptListArgument(self, tree):
        self.pushApplication('*', [tree[0]], self.getenv('*'))

    def acceptGroup(self, tree):
        self.visit(tree[0])

    def acceptTuple(self, tree):
        self.push(f'({self.groupfy(tree)})の組')

    def acceptSet(self, tree):
        self.push(f'({self.groupfy(tree)})の集合')

    def symbol(self, key, param = 0):
        entry = self.getenv(key)
        if param == 0 or param == None:
            return entry[0]
        else:
            return entry[1].format(param)

    def acceptList(self, tree):
        if len(tree) == 1 and tree[0] == 'ForExpr':
            self.push(self.stringfy(tree[0]))
        else:
            self.push(self.symbol('[]', None if len(tree) == 0 else self.groupfy(tree)))

    def acceptData(self, tree):
        self.push(self.symbol('{}', None if len(tree) == 0 else self.groupfy(tree)))

    def acceptKeyValue(self, tree):
        key = self.stringfy(tree.name)
        value = self.stringfy(tree.value)
        self.push(f'({key}, {value})')

    def acceptNull(self, tree):
        self.push(self.symbol('None'))

    def acceptTrue(self, tree):
        self.push(self.symbol('True'))

    def acceptFalse(self, tree):
        self.push(self.symbol('False'))

    def acceptInt(self, tree):
        self.push(str(tree))

    def acceptFloat(self, tree):
        self.push(str(tree))

    def acceptDouble(self, tree):
        self.push(str(tree))

    def acceptQString(self, tree):
        self.push(str(tree))

    def acceptIfExpr(self, tree):
        defined = self.getenv('if')
        cond = self.stringfy(tree.cond, trf=and_noun)
        self.pushApplication('if', [cond, tree.then, tree.get('else')], defined)

    def acceptForExpr(self, tree):
        defined = self.getenv('for')
        vars = self.groupfy(tree.each)
        if tree.has('cond'):
            self.pushApplication('for', [tree.append, vars, tree.list, self.stringfy(tree.cond, trf=and_noun)], defined)
        else:
            self.pushApplication('for', [tree.append, vars, tree.list], defined)


'''
puppy_peg = pg.grammar('puppy2.tpeg')
puppy_parser = pg.generate(puppy_peg)


def isMultiLine(tree):
    return '\n' in str(tree)


'''

if __name__ == '__main__':
    transpiler = Kotonoha()
    print(transpiler.compile("if defined:"))
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            print(transpiler.compile(f.read()))
