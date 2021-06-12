# suffix

import builtins

_A = 1
_I = 1 << 1
_U = 1 << 2
_E = 1 << 3
_O = 1 << 4
_N = 1 << 10
THEN = 1 << 5
PAST = 1 << 6
CASE = 1 << 9
NOT = 1 << 7
CMD = 1 << 8

# POS タイプ
VS = 'VS'  # サ変　
VZ = 'VZ'  # サ変
V1 = 'V1'  # 上一段、下一段
VK5 = 'VK5'  # カ行五段活用
VS5 = 'VS5'  # サ行五段活用
VT5 = 'VT5'  # タ行五段活用
VN5 = 'VN5'  # ナ行五段活用
VM5 = 'VM5'  # マ行五段活用
VR5 = 'VR5'  # ラ行五段活用
VW5 = 'VW5'  # ワ行五段活用
VG5 = 'VG5'  # ガ行五段活用
VB5 = 'VB5'  # バ行五段活用
ADJ = 'ADJ'  # 形容詞


def emitVS(lemma, c):
    if c & THEN == THEN:
        return lemma[:-2] + 'して'
    if c & PAST == PAST:
        return lemma[:-2] + 'した'
    if c & _N == _N:
        return lemma[:-2]
    if c & _I == _I:
        return lemma[:-2] + 'し'
    if c & _A == _A:
        return lemma[:-2] + 'し'  # ない
    if c & _E == _E:
        return lemma[:-2] + 'すれ'  # ば
    if c & _O == _O:
        return lemma[:-2] + 'しよ'  # う
    if c & CMD == CMD:
        return lemma[:-2] + 'せよ'  #
    return lemma


def emitVZ(lemma, c):  # 論じる
    if c & THEN == THEN:
        return lemma[:-2]+'じて'
    if c & PAST == PAST:
        return lemma[:-2]+'じた'
    if c & _N == _N:
        return lemma[:-2]
    if c & _I == _I:
        return lemma[:-2]+'じ'
    if c & _A == _A:
        return lemma[:-2]+'じ'  # ない
    if c & _E == _E:
        return lemma[:-2]+'ずれ'  # ば
    if c & _O == _O:
        return lemma[:-2]+'じよ'  # う
    if c & CMD == CMD:
        return lemma[:-2]+'ぜよ'  #
    return lemma


def emitV1(lemma, c):  # 高める
    if c & THEN == THEN:
        return lemma[:-1]+'て'
    if c & PAST == PAST:
        return lemma[:-1]+'た'
    if c & _I == _I or c & _N == _N:
        return lemma[:-1]
    if c & _A == _A:
        return lemma[:-1]  # ない
    if c & _E == _E:
        return lemma[:-1]+'れ'  # ば
    if c & _O == _O:
        return lemma[:-1]+'よ'  # う
    if c & CMD == CMD:
        return lemma[:-1]+'よ'  #
    return lemma


def emitADJ(lemma, c):  # ない 赤い
    if c & THEN == THEN:
        return lemma[:-1]+'くて'
    if c & PAST == PAST:
        return lemma[:-1]+'かった'
    if c & _N == _N:
        return lemma[:-1] + 'さ'
    if c & _I == _I:
        return lemma[:-1] + 'く'
    if c & _A == _A:
        return lemma[:-1] + 'く'  # ない
    if c & _E == _E:
        return lemma[:-1] + 'けれ'  # ば
    # if c & _O == _O:
    #     return lemma[:-1]+'よ'  # う
    # if c & CMD == CMD:
    #     return lemma[:-1]+'よ'  #
    return lemma


def emitN(lemma, c):  # 距離
    return lemma
    # c = suffix[0]
    # if c & PAST == PAST and c & _I == _I:
    #     return lemma
    # return emitVS(lemma+' を 確認する', suffix)


def emitVK5(lemma, c):  # 書く
    if c & THEN == THEN:
        return lemma[:-1]+'いて'
    if c & PAST == PAST:
        return lemma[:-1]+'いた'
    if c & _I == _I or c & _N == _N:
        return lemma[:-1] + 'き'
    if c & _A == _A:
        return lemma[:-1] + 'か'  # ない
    if c & _E == _E:
        return lemma[:-1]+'け'  # ば
    if c & _O == _O:
        return lemma[:-1]+'こ'  # う
    if c & CMD == CMD:
        return lemma[:-1]+'け'  #
    return lemma


def emitVS5(lemma, c):  # 探す
    if c & THEN == THEN:
        return lemma[:-1]+'して'
    if c & PAST == PAST:
        return lemma[:-1]+'した'
    if c & _I == _I or c & _N == _N:
        return lemma[:-1] + 'し'
    if c & _A == _A:
        return lemma[:-1] + 'さ'  # ない
    if c & _E == _E:
        return lemma[:-1]+'せ'  # ば
    if c & _O == _O:
        return lemma[:-1]+'そ'  # う
    if c & CMD == CMD:
        return lemma[:-1]+'せ'  #
    return lemma


def emitVT5(lemma, c):  # 勝つ
    if c & THEN == THEN:
        return lemma[:-1]+'って'
    if c & PAST == PAST:
        return lemma[:-1]+'った'
    if c & _I == _I or c & _N == _N:
        return lemma[:-1] + 'ち'
    if c & _A == _A:
        return lemma[:-1] + 'た'  # ない
    if c & _E == _E:
        return lemma[:-1]+'て'  # ば
    if c & _O == _O:
        return lemma[:-1]+'と'  # う
    if c & CMD == CMD:
        return lemma[:-1]+'て'  #
    return lemma


def emitVN5(lemma, c):  # 死ぬ
    if c & THEN == THEN:
        return lemma[:-1]+'んで'
    if c & PAST == PAST:
        return lemma[:-1]+'んだ'
    if c & _I == _I or c & _N == _N:
        return lemma[:-1] + 'に'
    if c & _A == _A:
        return lemma[:-1] + 'な'  # ない
    if c & _E == _E:
        return lemma[:-1]+'ね'  # ば
    if c & _O == _O:
        return lemma[:-1]+'の'  # う
    if c & CMD == CMD:
        return lemma[:-1]+'ね'  #
    return lemma


def emitVM5(lemma, c):  # 読む
    if c & THEN == THEN:
        return lemma[:-1]+'んで'
    if c & PAST == PAST:
        return lemma[:-1]+'んだ'
    if c & _I == _I or c & _N == _N:
        return lemma[:-1] + 'み'
    if c & _A == _A:
        return lemma[:-1] + 'ま'  # ない
    if c & _E == _E:
        return lemma[:-1]+'め'  # ば
    if c & _O == _O:
        return lemma[:-1]+'も'  # う
    if c & CMD == CMD:
        return lemma[:-1]+'め'  #
    return lemma


def emitVR5(lemma, c):  # 切る
    if c & THEN == THEN:
        return lemma[:-1]+'って'
    if c & PAST == PAST:
        return lemma[:-1]+'った'
    if c & _I == _I or c & _N == _N:
        return lemma[:-1] + 'り'
    if c & _A == _A:
        return lemma[:-1] + 'ら'  # ない
    if c & _E == _E:
        return lemma[:-1]+'れ'  # ば
    if c & _O == _O:
        return lemma[:-1]+'ろ'  # う
    if c & CMD == CMD:
        return lemma[:-1]+'れ'  #
    return lemma


def emitVW5(lemma, c):  # 笑う
    if c & THEN == THEN:
        return lemma[:-1]+'って'
    if c & PAST == PAST:
        return lemma[:-1]+'った'
    if c & _I == _I or c & _N == _N:
        return lemma[:-1] + 'い'
    if c & _A == _A:
        return lemma[:-1] + 'わ'  # ない
    if c & _E == _E:
        return lemma[:-1]+'え'  # ば
    if c & _O == _O:
        return lemma[:-1]+'お'  # う
    if c & CMD == CMD:
        return lemma[:-1]+'え'  #
    return lemma


def emitVG5(lemma, c):  # 防ぐ
    if c & THEN == THEN:
        return lemma[:-1]+'いで'
    if c & PAST == PAST:
        return lemma[:-1]+'いだ'
    if c & _I == _I or c & _N == _N:
        return lemma[:-1] + 'ぎ'
    if c & _A == _A:
        return lemma[:-1] + 'が'  # ない
    if c & _E == _E:
        return lemma[:-1]+'げ'  # ば
    if c & _O == _O:
        return lemma[:-1]+'ご'  # う
    if c & CMD == CMD:
        return lemma[:-1]+'げ'  #
    return lemma


def emitVB5(lemma, c):  # 遊ぶ
    if c & THEN == THEN:
        return lemma[:-1]+'んで'
    if c & PAST == PAST:
        return lemma[:-1]+'んだ'
    if c & _I == _I or c & _N == _N:
        return lemma[:-1] + 'び'
    if c & _A == _A:
        return lemma[:-1] + 'ば'  # ない
    if c & _E == _E:
        return lemma[:-1]+'べ'  # ば
    if c & _O == _O:
        return lemma[:-1]+'ぼ'  # う
    if c & CMD == CMD:
        return lemma[:-1]+'べ'  #
    return lemma


verb_lemma_suffix = {
    'く': VK5,
    'す': VS5,
    'つ': VT5,
    'ぬ': VN5,
    'む': VM5,
    'る': VR5,
    'う': VW5,
    'ぐ': VG5,
    'ぶ': VB5,
    'い': ADJ,
}

# VERB1c = [鋳診観視見経簸着看獲煮流歴恐得干居射寝割似出ゐ] CK_VERB1 !'し' //
# HVERB1c = [れみへひねにでてせきえうい] CK_VERB1


def guess_verb_pos(verb):
    if verb.endswith('する'):
        return VS  # 　さ変
    if verb.endswith('ずる'):
        return VZ  # ざ変 論ずる
    if verb.endswith('る') and len(verb) > 2 and verb[-2] in 'きべえげりえれけせめびてじぎい':
        return 'V1'
    return verb_lemma_suffix.get(verb[-1], 'N')

####


class Word(object):
    def emit(self, c=_U):
        return ''

    def isNoun(self):
        return False

    def __str__(self):
        return self.emit()


class Noun(Word):
    w: str

    def __init__(self, w):
        self.w = w

    def isNoun(self):
        return True

    def __repr__(self):
        return str(self.w)

    def emit(self, c=_U):
        if isinstance(self.w, Word):
            return self.w.emit(_N)
        return str(self.w)


class Neg(object):  # 否定あり
    pass


class Verb(Word, Neg):
    w: str  # 標準形
    pos: str

    def __init__(self, lemma, pos=None):
        self.w = lemma
        self.pos = guess_verb_pos(lemma) if pos is None else pos

    def __repr__(self):
        return self.w

    def emit(self, c=_U):
        return globals()[f'emit{self.pos}'](self.w, c)


class Suffix(Word):
    inner: Word
    suffix: str

    def __init__(self, inner, suffix=''):
        self.inner = inner
        self.suffix = suffix

    def updateInner(self, inner):
        return Suffix(inner, self.suffix)

    def emit(self, c=_U):
        return self.inner.emit(_U) + self.suffix


class Past(Suffix):
    inner: Word

    def __init__(self, inner):
        Suffix.__init__(self, inner, '')

    def updateInner(self, inner):
        return Past(inner)

    def emit(self, c=_U):
        return self.inner.emit(PAST)


class Can(Suffix, Neg):
    inner: Word

    def __init__(self, inner):
        Suffix.__init__(self, inner, '')

    def updateInner(self, inner):
        return Can(inner)

    def emit(self, c=_U):
        if isinstance(self.inner, Verb):
            if self.inner.pos == VS:  # 検索できる 検索できない
                return emitV1(self.inner.emit(_N)+'できる', c)
            if self.inner.pos == V1:  # 高められる 高められない
                return emitV1(self.inner.emit(_N)+'られる', c)
        return emitV1(self.inner.emit(_E)+'る', c)


class Passive(Suffix, Neg):
    inner: Word

    def __init__(self, inner):
        Suffix.__init__(self, inner, '')

    def updateInner(self, inner):
        return Passive(inner)

    def emit(self, c=_U):
        if isinstance(self.inner, Verb):
            if self.inner.pos == VS:  # 検索される 検索されない
                return emitV1(self.inner.emit(_N)+'される', c)
            if self.inner.pos == V1:  # 高められる 高められない
                return emitV1(self.inner.emit(_N)+'られる', c)
        return emitV1(self.inner.emit(_A)+'れる', c)


class Not(Suffix):
    inner: Word

    def __init__(self, inner):
        Suffix.__init__(self, inner, '')

    def updateInner(self, inner):
        return Not(inner)

    def emit(self, c=_U):
        return self.inner.emit(_A) + Verb('ない', ADJ).emit(c)


COMMA = '、'


class Then(Suffix):
    inner: Word
    c: int

    def __init__(self, inner, c=_I, suffix=COMMA):
        Suffix.__init__(self, inner, suffix)
        #self.inner = inner
        #self.suffix = suffix
        self.c = c

    def updateInner(self, inner):
        return Then(inner, self.c)

    def emit(self, c=_U):
        return self.inner.emit(self.c) + self.suffix


class IfCase(Suffix):
    inner: str

    def __init__(self, inner, suffix=COMMA):
        Suffix.__init__(self, inner, suffix)

    def updateInner(self, inner):
        return IfCase(inner, self.suffix)

    def __repr__(self):
        return f'{self.w}#case'

    def emit(self, c=_U):
        if self.suffix == COMMA:
            return self.inner.emit(_E) + 'ば' + COMMA
        return self.inner.emit(_U) + self.suffix


def noun_(w):
    if isinstance(w, Word) and w.isNoun():
        return w
    return Noun(w)


def can_(w):
    if isinstance(w, Verb):
        return Can(w)
    return w


def passive_(w):
    if isinstance(w, Verb):
        return Passive(w)
    return w


def past_(w):
    if isinstance(w, Verb) or isinstance(w, Not):
        return Past(w)
    return w


def not_(w):
    if isinstance(w, Neg):
        return Not(w)
    if isinstance(w, Suffix):
        if isinstance(w, Not):
            return w.inner
        else:
            return w.updateInner(not_(w.inner))
    return w


def and_(w):
    return Then(w)


def then_(w):
    return Then(w, c=THEN)


def case_(w):
    return IfCase(w)


class _Polite(object):
    inner: Verb

    def __init__(self, inner):
        self.inner = inner

    def emit(self, c=_U):
        prefix = self.inner.emit(AND, '')
        if c & THEN == THEN:
            return prefix + 'まして'
        if c & PAST == PAST:
            return prefix + 'ました'
        if c == NOT:
            return prefix + 'ません'
        return prefix + 'ます'


# 遊ぶ #polite #not #past
# 遊ぶ
# print(_Then(_Not(Verb('遊ぶ')), Noun('人')).emit(_U))


def pj_suffix(verb, ss):
    suffix = f'{ss[0]}_'
    if suffix in globals():
        verb = globals()[suffix](verb)
    if len(ss) > 1:
        return pj_suffix(verb, ss[1:])
    return verb


def pj(s):
    if '#' in s:
        ss = s.split('#')
        return pj_suffix(pj(ss[0]), ss[1:])
    pos = guess_verb_pos(s)
    if pos == 'N':
        return Noun(s)
    return Verb(s, pos)


print(pj('等しい#not#case'))
print(pj('等しい#then'))
print(pj('等しい#and'))
print(pj('書く#past'))
print(pj('書く#past#not'))
print(pj('書く#not#past#case'))

print(pj('書く#can'), pj('書く#can#not'))
print(pj('高める#can'), pj('高める#can#not'))
print(pj('検索する#can'), pj('検索する#can#not'))

print(pj('書く#passive#past'), pj('書く#passive#not#past'))
print(pj('高める#passive'), pj('高める#passive#not'))
print(pj('検索する#passive'), pj('検索する#passive#not'))
