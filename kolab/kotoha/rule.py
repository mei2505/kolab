
"""
synonym 置き換える 置換する
synonym 用いる とする
synonym 取り除く 除去する
synonym 表示する 出力する
synonym 区切り 区切り記号 区切り文字列 セパレータ
"""

math = __package__  # module
file = "ファイル名"  # symbol
s = '文字列'  # symbol
s2 = '文字列'  # symbol


len(a)  # aの[長さ|大きさ|要素数|サイズ]
max(a, b)  # aとbの[最大値|大きい値|大きい方]
max(a)  # aの 最大値
math.pi  # 円周率
a % 2 == 0   # a(整数)が 偶数かどうか

print()  # 空行を 出力する
print(a)  # aを 出力する
print(a, b)  # aと bを [順に|] 出力する

end = ''  # 改行を しない
end = s  # sを 終端記号に 用いる
sep = ''  # [区切り]が ない
sep = s  # sを [区切り]に 用いる
file = f  # fを 出力先に 用いる

flush = True  # [バッファを|] フラッシュする
flush = False  # [バッファを|] フラッシュしない

file = 'ファイル名'  # symbol
enc = 'エンコーディング'  # symbol
prefix = '接頭辞'  # symbol
suffix = '接尾辞'  # symbol

open(file)  # fileを 開く -> ファイル
open(file, 'w')  # fileを 書き込みモードで 開く -> ファイル
encoding = enc  # encを 用いる

s.startswith(prefix)  # sが prefixで 始まるかどうか
s.replace(old, new)  # sのold(文字列)を new(文字列)で 置き換える -> 文字列
s.replace(s2, '')  # sから s2を [全て|] 取り除く -> 文字列

X = Y  # a(変数)をyと する

