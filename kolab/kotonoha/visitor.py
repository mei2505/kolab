#import pegtree as pg
from pegtree import ParseTree

from logging import getLogger
logger = getLogger(__name__)


class Visitor(object):
    def __init__(self, methods=None):
        self.methods = methods if methods is not None else {}

    def visit(self, tree: ParseTree):
        tag = tree.getTag()
        methods = self.methods
        if tag not in methods:
            methods[tag] = f'accept{tag}'
        method = methods[tag]
        if hasattr(self, method):
            method = getattr(self, method)
            return method(tree)
        else:
            logger.warning(
                f'@TODO undefined {method} method for {repr(tree)}')
            self.push(str(tree))

    def TODO(self, msg, tree):
        logger.warning(f'@TODO {msg} for {repr(tree)}')


PARENT = '..'


class TransCompiler(Visitor):
    buffers: list
    env: dict
    indent: int
    level: int

    def __init__(self, methods=None):
        Visitor.__init__(self, methods)
        self.buffers = []
        self.env = {}
        self.indent = 0

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

    def pushEOS(self, eos=''):
        self.push(eos)

    def pushenv(self):
        self.env = {PARENT: self.env}

    def popenv(self):
        if PARENT in self.env:
            self.env = self.env[PARENT]

    def getenv(self, key, default_value={}):
        env = self.env
        while env is not None:
            if key in env:
                return env[key]
            env = env.get(PARENT, None)
        # if isinstance(key, str) and '.' in key:
        #     key = key[key.find('.')+1:]
        #     return self.getenv(key, default_value)
        return default_value

    def hasenv(self, key):
        return self.getenv(key, None) is not None

    def setenv(self, key, value):
        self.env[key] = value

    def stringfy(self, tree, sep=''):
        stacked = self.buffers
        self.buffers = []
        self.visit(tree)
        s = sep.join(self.buffers)
        self.buffers = stacked
        return s
