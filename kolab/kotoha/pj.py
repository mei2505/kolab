# typefix

import builtins


EOS = 'E'  # 文の終わり
NOT = 'N'  # 否定形
AND = 'A'  # 接続(short)
THEN = 'T'  # 接続
PAST = 'P'  # 過去
RESULT = '結果'

#  書く 書かない　書き　書いた


def OR(a, b):
    return


lemma_rule = {
    'く': 'VK5',
    'す': 'VK5',
    'つ': 'VT5',
    'ぬ': 'VN5',
    'む': 'VM5',
    'る': 'VR5',
    'う': 'VW5',
    'ぐ': 'VG5',
    'ぶ': 'VB5',
    'い': 'A',
}

# VERB1c = [鋳診観視見経簸着看獲煮流歴恐得干居射寝割似出ゐ] CK_VERB1 !'し' //
# HVERB1c = [れみへひねにでてせきえうい] CK_VERB1


def lemmatype(lemma):
    if lemma.endswith('する'):
        return 'VS'  # 　さ変
    if lemma.endswith('ずる'):
        return 'VZ'  # ざ変 論ずる
    if lemma.endswith('る') and len(lemma) > 2 and lemma[-2] in 'きべえげりえれけせめびてじぎい':
        return 'V1'
    return lemma_rule.get(lemma[-1], 'N')


def suffix(s, typefix):
    return s if len(typefix) == 1 else s + typefix[1:]


def emitVS(lemma, typefix):
    c = typefix[0]
    if c == EOS:
        return suffix(lemma, typefix)
    if c == THEN:
        return suffix(lemma[:-2]+'して', typefix)
    if c == PAST:
        return suffix(lemma[:-2]+'した', typefix)
    if c == AND:
        return suffix(lemma[:-2]+'し', typefix)
    if c == NOT:
        return suffix(lemma[:-2]+'し', typefix)
    return lemma + typefix


def emitVZ(lemma, typefix):  # 論じる
    c = typefix[0]
    if c == EOS:
        return suffix(lemma, typefix)
    if c == THEN:
        return suffix(lemma[:-2]+'じて', typefix)
    if c == PAST:
        return suffix(lemma[:-2]+'じた', typefix)
    if c == AND:
        return suffix(lemma[:-2]+'じ', typefix)
    if c == NOT:
        return suffix(lemma[:-2]+'じ', typefix)
    return lemma + typefix


def emitV1(lemma, typefix):  # 高める
    c = typefix[0]
    if c == EOS:
        return suffix(lemma, typefix)
    if c == THEN:
        return suffix(lemma[:-1]+'て', typefix)
    if c == PAST:
        return suffix(lemma[:-1]+'た', typefix)
    if c == AND:
        return suffix(lemma[:-1], typefix)
    if c == NOT:
        return suffix(lemma[:-1], typefix)
    return lemma + typefix


def emitA(lemma, typefix):  # 赤い　長さ
    c = typefix[0]
    if c == EOS:
        return suffix(lemma, typefix)
    if c == THEN:
        return suffix(lemma[:-1]+'くて', typefix)
    if c == PAST:
        return lemma[:-1]+'さ'
    if c == AND:
        return suffix(lemma[:-1]+'く', typefix)
    if c == NOT:
        return suffix(lemma[:-1]+'く', typefix)
    return lemma + typefix


def emitN(lemma, typefix):  # 距離
    c = typefix[0]
    if c == PAST and c == AND:
        return lemma
    return emitVS(lemma+' を 確認する', typefix)


def emitVK5(lemma, typefix):  # 書く
    c = typefix[0]
    if c == EOS:
        return suffix(lemma, typefix)
    if c == THEN:
        return suffix(lemma[:-1]+'いて', typefix)
    if c == PAST:
        return suffix(lemma[:-1]+'いた', typefix)
    if c == AND:
        return suffix(lemma[:-1]+'き', typefix)
    if c == NOT:
        return suffix(lemma[:-1]+'か', typefix)
    return lemma + typefix


def emitVS5(lemma, typefix):  # 探す
    c = typefix[0]
    if c == EOS:
        return suffix(lemma, typefix)
    if c == THEN:
        return suffix(lemma[:-1]+'して', typefix)
    if c == PAST:
        return suffix(lemma[:-1]+'した', typefix)
    if c == AND:
        return suffix(lemma[:-1]+'し', typefix)
    if c == NOT:
        return suffix(lemma[:-1]+'さ', typefix)
    return lemma + typefix


def emitVT5(lemma, typefix):  # 勝つ
    c = typefix[0]
    if c == EOS:
        return suffix(lemma, typefix)
    if c == THEN:
        return suffix(lemma[:-1]+'って', typefix)
    if c == PAST:
        return suffix(lemma[:-1]+'った', typefix)
    if c == AND:
        return suffix(lemma[:-1]+'ち', typefix)
    if c == NOT:
        return suffix(lemma[:-1]+'た', typefix)
    return lemma + typefix


def emitVN5(lemma, typefix):  # 死ぬ
    c = typefix[0]
    if c == EOS:
        return suffix(lemma, typefix)
    if c == THEN:
        return suffix(lemma[:-1]+'んで', typefix)
    if c == PAST:
        return suffix(lemma[:-1]+'んだ', typefix)
    if c == AND:
        return suffix(lemma[:-1]+'ぬ', typefix)
    if c == NOT:
        return suffix(lemma[:-1]+'な', typefix)
    return lemma + typefix


def emitVM5(lemma, typefix):  # 読む
    c = typefix[0]
    if c == EOS:
        return suffix(lemma, typefix)
    if c == THEN:
        return suffix(lemma[:-1]+'んで', typefix)
    if c == PAST:
        return suffix(lemma[:-1]+'んだ', typefix)
    if c == AND:
        return suffix(lemma[:-1]+'み', typefix)
    if c == NOT:
        return suffix(lemma[:-1]+'ま', typefix)
    return lemma + typefix


def emitVR5(lemma, typefix):  # 切る
    c = typefix[0]
    if c == EOS:
        return suffix(lemma, typefix)
    if c == THEN:
        return suffix(lemma[:-1]+'って', typefix)
    if c == PAST:
        return suffix(lemma[:-1]+'った', typefix)
    if c == AND:
        return suffix(lemma[:-1]+'り', typefix)
    if c == NOT:
        return suffix(lemma[:-1]+'ら', typefix)
    return lemma + typefix


def emitVW5(lemma, typefix):  # 笑う
    c = typefix[0]
    if c == EOS:
        return suffix(lemma, typefix)
    if c == THEN:
        return suffix(lemma[:-1]+'って', typefix)
    if c == PAST:
        return suffix(lemma[:-1]+'った', typefix)
    if c == AND:
        return suffix(lemma[:-1]+'い', typefix)
    if c == NOT:
        return suffix(lemma[:-1]+'わ', typefix)
    return lemma + typefix


def emitVG5(lemma, typefix):  # 防ぐ
    c = typefix[0]
    if c == EOS:
        return suffix(lemma, typefix)
    if c == THEN:
        return suffix(lemma[:-1]+'いで', typefix)
    if c == PAST:
        return suffix(lemma[:-1]+'いだ', typefix)
    if c == AND:
        return suffix(lemma[:-1]+'ぎ', typefix)
    if c == NOT:
        return suffix(lemma[:-1]+'が', typefix)
    return lemma + typefix


def emitVB5(lemma, typefix):  # 遊ぶ
    c = typefix[0]
    if c == EOS:
        return suffix(lemma, typefix)
    if c == THEN:
        return suffix(lemma[:-1]+'んで', typefix)
    if c == PAST:
        return suffix(lemma[:-1]+'んだ', typefix)
    if c == AND:
        return suffix(lemma[:-1]+'び', typefix)
    if c == NOT:
        return suffix(lemma[:-1]+'ば', typefix)
    return lemma + typefix


class Lemma(object):
    lemma: str  # 標準形
    lemmatype: str

    def __init__(self, lemma, variant=None):
        self.lemma = lemma
        self.lemmatype = lemmatype(lemma)

    def __repr__(self):
        return self.lemma

    def emit(self, typefix):
        return globals()[f'emit{self.lemmatype}'](self.lemma, typefix)


LEMMA = {}
TAIL = None


def lemma(w):
    global TAIL
    if w not in LEMMA:
        LEMMA[w] = Lemma(w)
        TAIL = None
    return LEMMA[w]


SUFFIXES = ['が', 'を', 'に', 'で', 'の', 'から', 'まで', 'より', '、']
SUFFIX_CHARS = 'がをにでのらり、くはも'


def match_suffix(s: str):
    for suffix in SUFFIXES:
        if s.endswith(suffix):
            return True
    return False


def rfind_head(s):
    for i in range(len(s)-2, 0, -1):
        if s[i] in SUFFIX_CHARS:
            return i+1
    return -1


def match_predicate(s):
    global TAIL
    pos = s.rfind(' ')
    if pos > 0:
        w = s[pos+1:]
        if s[pos-1] in SUFFIX_CHARS:
            return s[:pos], lemma(w)
    if TAIL is None:
        TAIL = list(sorted(LEMMA.keys(), key=lambda x: len(x))[::-1])
    pos = rfind_head(s)
    if pos != -1:
        return s[:pos], Lemma(s[pos:])
    return s, None


def test(s):
    w = lemma(s)
    print(w.emit('Eもの'), w.emit('Pもの'), w.emit(
        'T、'), w.emit('Aもの'), w.emit('Nない'))


# test('書く')
# test('ない')

# print(match_predicate('改行が ない'))
# print(match_predicate('コメントを 書き込む'))
# print(match_predicate('xを終端記号に 用いる'))
# print(match_predicate('s(文字列)がx(接頭辞)で 始まるかどうか'))
# print(match_predicate('s(文字列)がx(接頭辞)で始まるかどうか'))
# print(match_predicate('s(文字列)がx(接頭辞)の長さ'))
