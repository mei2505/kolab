import csv
import pathlib

# Read DIC

DIC = {}
base = pathlib.Path(__file__).parent.resolve()


def load_dic_from_file(filename):
    with open(f'{base / filename}') as f:
        d = []
        for w in f.readlines():
            w = w.strip()
            if len(w) == 0 or w.startswith('#'):
                continue
            d.append(w)
        return d


def load_dic():
    global DIC
    DIC['SA5'] = set(load_dic_from_file('SA5.txt'))
    DIC['TA5'] = load_dic_from_file('TA5.txt')
    DIC['RA5'] = load_dic_from_file('VR5.txt')
    DIC['BA5'] = load_dic_from_file('BA5.txt')
    DIC['V1'] = load_dic_from_file('V1.txt')


load_dic()


def isHira(c):
    return 12354 <= ord(c) <= 12435


def isVerbSA5(stem):
    if isHira(stem[-1]):
        return True
    return stem in DIC['SA5']


def isVerbDIC(stem, dic):
    for w in DIC[dic]:
        if stem.endswith(w):
            return True
    return False


def isVerbTA5(stem):
    return isVerbDIC(stem, 'TA5')


def isVerbBA5(stem):
    return isVerbDIC(stem, 'BA5')


def isVerbRA5(stem):
    return isVerbDIC(stem, 'RA5')


def isVerbV1(stem):
    return isVerbDIC(stem, 'V1')


def isFormalVerb(w):
    if w.endswith('する') or w.endswith('ずる'):
        return True
    tail = w[-1]
    if tail in 'くすつぬむうぐぶただい':
        return True
    if tail == 'る':
        return isVerbRA5(w[:-1]) or isVerbV1(w[:-1])
    return False


def splitVerbalNoun(w, noun=''):
    if w.endswith('かどうか'):
        return w[:-4], 'かどうか'
    if isFormalVerb(w):
        return w, noun
    for index in range(len(w)-1, 0, -1):
        c = w[index]
        if c in 'くすつぬむうぐぶただいる':
            verb = w[:index+1]
            if isFormalVerb(verb):
                return verb, w[index+1:]
    return '', w


print(splitVerbalNoun('赤くない仕組み'))
print(splitVerbalNoun('学習しました仕組み'))
print(splitVerbalNoun('AからBを引いた値'))


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

# POS 語尾から判定する


POS = {
    # サ変
    'する': 'VS',  # 行動する => 行動し
    'した': 'VS@past',  # 先に、サ行５段をチェック
    'しない': 'VS@not',
    'しなかった': 'VS@past@not',
    'じる': 'VZ',
    'じた': 'VZ@past',
    'じない': 'VZ@not',
    'じなかった': 'VZ@past@not',
    # 形容詞
    'い': 'A',
    'くない': 'A@not',
    'かった': 'A@past',
    'くなかった': 'A@past@not',
    # グループ2
    'る': 'V1',  # 先に、ラ行５段をチェック
    'ない': 'V1@not',
    'た': 'V1@past',
    'なかった': 'V1@past@not',
    # 5段活用
    'く': 'VK5',  # 書く
    'いた': 'VK5@past',  # 書いた => 書く
    'かない': 'VK5@not',
    'かなかった': 'VK5@past@not',
    'す': 'VS5',  # 探す
    'さない': 'VS5@not',
    'さなかった': 'VS5@past@not',
    'つ': 'VT5',  # 勝つ
    'たない': 'VT5@not',
    'たなかった': 'VT5@past@not',
    'ぬ': 'VN5',  # な行 死ぬのみ
    '死んだ': 'VN5@past',
    'しんだ': 'VN5@past',
    'なない': 'VN5@not',
    'ななかった': 'VN5@past@not',
    'む': 'VM5',  # ま行
    'まない': 'VM5@not',  # ま行
    'まなかった': 'VM5@past@not',
    # 'る': 'VR5', # ら行 切る、先に１段動詞
    'らない': 'VR5@not',
    'らなかった': 'VR5@past@not',
    'う': 'VW5',  # わ行
    'わない': 'VW5@not',  # わ行
    'わなかった': 'VW5@past@not',  # わ行
    'ぐ': 'VG5',  # が行
    'がない': 'VG5@not',  # が行
    'いだ': 'VG5@past',  # 書いた => 書く
    'がなかった': 'VG5@past@not',  # が行
    'ぶ': 'VB5',
    'ばない': 'VB5@not',
    'ばなかった': 'VB5@past@not',
    # 'った': 'って', #
    # 'んだ': 'んで', #
    # 'た': 'て', #できなかった
    # 'で': 'だ', #できなかった
    # 特殊
    'である': 'VR5',
    'でない': 'VR5@not',
    'てみる': 'V1',
    'てみた': 'V1@past',
    'てみない': 'V1@not',
    'てみなかった': 'V1@past@not',
}

POSTAIL = sorted(POS.keys(), key=lambda x: len(x), reverse=True)


def pos(w):
    if w.endswith('る'):
        if isVerbRA5(w[:-1]):
            return 'VR5'
    if w.endswith('した'):
        if isVerbSA5(w[:-2]):
            return 'VS5@past'
        return 'VS@past'
    if w.endswith('った') and not w.endswith('なかった'):
        if isVerbRA5(w[:-2]):
            return 'VR5@past'
        if isVerbTA5(w[:-2]):
            return 'VT5@past'
        return 'VW5@past'
    if w.endswith('んだ'):
        if isVerbBA5(w[:-2]):
            return 'VB5@past'
        return 'VM5@past'
    for tail in POSTAIL:
        if w.endswith(tail):
            return POS[tail]
    return 'N'  # Noun


NOT = {
    # サ変
    'する': 'しない',  # 行動する => 行動し
    'した': 'しなかった',  # 先に、サ行５段をチェック
    'しない': 'する',
    'しなかった': 'した',
    'じる': 'じない',
    'じた': 'じなかった',
    'じない': 'じる',
    'じなかった': 'じた',
    # 形容詞
    'い': 'くない',
    'くない': 'い',
    'かった': 'くなかった',
    'くなかった': 'かった',
    # グループ2
    'る': 'ない',  # 先に、ラ行５段をチェック
    'ない': 'る',
    'た': 'なかった',
    'なかった': 'た',
    # 5段活用
    'く': 'かない',  # 書く
    'かない': 'く',
    'いた': 'かなかった',
    'かなかった': 'いた',
    'す': 'さない',  # 探す
    'さない': 'す',
    'さなかった': 'した',
    'つ': 'たない',  # 勝つ
    'たない': 'つ',
    'たなかった': 'った',
    'ぬ': 'なない',  # な行 死ぬのみ
    '死んだ': '死ななかった',
    'しんだ': 'しななかった',
    'なない': 'ぬ',
    'ななかった': 'んだ',
    'む': 'まない',  # ま行
    'まない': 'む',  # ま行
    'んだ': 'まなかった',  # 先にバ行をチェック
    'まなかった': 'んだ',
    # 'る': 'VR5', # ら行 切る、先に１段動詞
    'らない': 'る',
    'らなかった': 'った',
    'う': 'わない',  # わ行
    'わない': 'う',
    'った': 'わなかった',  # ラ行とた行は先にチェック
    'わなかった': 'った',
    'ぐ': 'がない',  # が行
    'がない': 'ぐ',
    'いだ': 'がなかった',  # 書いた => 書く
    'がなかった': 'いだ',
    'ぶ': 'ばない',
    'ばない': 'ぶ',
    'ばなかった': 'んだ',
    # 'った': 'って', #
    # 'んだ': 'んで', #
    # 'た': 'て', #できなかった
    # 'で': 'だ', #できなかった
    # 特殊
    'である': 'でない',
    'でない': 'である',
    'てみる': 'てみない',
    'てみた': 'てみなかった',
    'てみない': 'てみる',
    'てみなかった': 'てみた',
}

NOTTAIL = sorted(NOT.keys(), key=lambda x: len(x), reverse=True)


def toNOT(w, suffix_noun='かどうか'):
    if w.endswith(suffix_noun):
        return toNOT(w[:-len(suffix_noun)], suffix_noun) + suffix_noun
    if w.endswith('る'):
        if w.endswith('である'):
            return w[:-3] + 'でない'
        if isVerbRA5(w[:-1]):
            return w[:-1] + 'らない'
    if w.endswith('した'):
        if isVerbSA5(w[:-2]):
            return w[:-2] + 'さなかった'
    if w.endswith('った') and not w.endswith('なかった'):
        if w.endswith('であった'):
            return w[:-4] + 'でなかった'
        if isVerbRA5(w[:-2]):
            return w[:-2] + 'らなかった'
        if isVerbTA5(w[:-2]):
            return w[:-2] + 'たなかった'
    if w.endswith('んだ'):
        if isVerbBA5(w[:-2]):
            return w[:-2] + 'ばなかった'
        # return w[:-2] + 'まなかった'
    for tail in NOTTAIL:
        if w.endswith(tail):
            return w[:-len(tail)] + NOT[tail]
    return w + 'でない'


PAST = {
    # サ変
    'する': 'した',  # 行動する => 行動し
    'じる': 'じた',  # 行動しない => 行動する
    # 形容詞
    'い': 'かった',  # 等しかった => 等しい
    # 'かった': 'く', # 等しくなかった => 等しくなく
    # 5段活用
    'く': 'いた',  # 書く => 書く
    'す': 'した',  # 探さない => 探す
    'つ': 'った',  # 勝たない => 勝つ
    'ぬ': 'んだ',  # な行
    'む': 'んだ',  # ま行
    'る': 'った',  # ら行 切る
    'う': 'った',  # わ行
    'ぐ': 'いだ',  # が行
    'ぶ': 'んだ',
}

PASTTAIL = sorted(PAST.keys(), key=lambda x: len(x), reverse=True)


def toPAST(w: str, suffix_noun='かどうか'):
    if w.endswith(suffix_noun):
        return toPAST(w[:-len(suffix_noun)], suffix_noun) + suffix_noun
    if w.endswith('る'):
        if isVerbV1(w[:-1]):
            return w[:-1] + 'た'
    for tail in PASTTAIL:
        if w.endswith(tail):
            return w[:-len(tail)] + PAST[tail]
    return w


PRESENT = {
    # サ変
    'した': 'する',  # 先に、サ行５段をチェック
    'しなかった': 'しない',
    'じた': 'じる',
    'じなかった': 'じない',
    # 形容詞
    'かった': 'い',
    'くなかった': 'くない',
    # グループ2
    'た': 'る',
    'なかった': 'ない',
    # 5段活用
    'いた': 'く',
    '死んだ': '死ぬ',
    'しんだ': 'しぬ',
    # 'る': 'VR5', # ら行 切る、先に１段動詞
    'ぐ': 'がない',  # が行
}

PRESENTTAIL = sorted(PRESENT.keys(), key=lambda x: len(x), reverse=True)


def toPRESENT(w: str, suffix_noun='かどうか'):
    if w.endswith(suffix_noun):
        return toPRESENT(w[:-len(suffix_noun)], suffix_noun) + suffix_noun
    if w.endswith('した'):
        if isVerbSA5(w[:-2]):
            return w[:-2] + 'す'
        return w[:-2] + 'する'
    if w.endswith('った') and not w.endswith('なかった'):
        if isVerbRA5(w[:-2]):
            return w[:-2] + 'る'
        if isVerbTA5(w[:-2]):
            return w[:-2] + 'つ'
        return w[:-2] + 'う'
    if w.endswith('んだ'):
        if isVerbBA5(w[:-2]):
            return w[:-2] + 'ぶ'
        return w[:-2] + 'む'
    for tail in PRESENTTAIL:
        if w.endswith(tail):
            return w[:-len(tail)] + PRESENT[tail]
    return w


THEN = {
    # サ変
    'する': 'し',  # 行動する => 行動し
    'した': 'し',  # 行動した => 行動し
    'じる': 'じ',  # 行動しない => 行動する
    'じた': 'じ',  # 行動しなかった => 行動した
    # 形容詞
    'い': 'く',  # 等しくない => 等しい
    'かった': 'く',  # 等しくなかった => 等しくなく
    # 5段活用
    'く': 'き',  # 書く => 書く
    'す': 'し',  # 探さない => 探す
    'つ': 'ち',  # 勝たない => 勝つ
    'ぬ': 'に',  # な行
    'む': 'み',  # ま行
    # 'る': 'り', # ら行 切る
    'う': 'い',  # わ行
    'ぐ': 'ぎ',  # が行
    'ぶ': 'び',
    'いた': 'いて',  # 書いた => 書く
    'った': 'って',
    'んだ': 'んで',
    # グループ2
    # 'る': '', #できない
    'た': 'て',  # できなかった
    'で': 'だ',  # できなかった
}

THENTAIL = sorted(THEN.keys(), key=lambda x: len(x), reverse=True)


def toTHEN(s: str):
    if s.endswith('かどうか'):
        s = s[:-4]
    for tail in THENTAIL:
        if s.endswith(tail):
            return s[:-len(tail)] + THEN[tail]
    if s.endswith('る'):
        stem = s[:-1]
        if isVerbRA5(stem):
            return stem + 'り'
        return stem
    return s


def appendNoun(s, noun='とき'):  # +とき
    if s.endswith('かどうか'):
        return appendNoun(s[:-4], noun)
    if s[-1] in 'くすつぬむうぐぶただいる':
        return s + noun
    return s + 'の' + noun


def test_not(w):
    print(w, pos(w), toNOT(w), toNOT(toNOT(w)), toPAST(w), toNOT(toPAST(w)))


test_not('探した')
test_not('見つかる')
test_not('見つかった')
test_not('発見された')
test_not('書いた')
test_not('探した')
test_not('買った')
test_not('死んだ')
test_not('切った')
test_not('読んだ')
test_not('防いだ')
test_not('笑った')
test_not('高めた')
test_not('猫である')
test_not('書く')
test_not('探す')
test_not('買う')
test_not('死ぬ')
test_not('切る')
test_not('読む')
test_not('防ぐ')
test_not('笑う')
test_not('高める')
test_not('猫であるかどうか')
