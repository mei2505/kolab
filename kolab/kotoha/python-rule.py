# 準備
import string as string
math = __package__  # module

object = ''
x, y, z, n = ''
num, n, n2 = ''  # 数値
str, _str, s, s2, s3, str2 = '文字列'
c, c2 = '文字'
list, list2 = 'リスト'
tuple, tuple2 = 'タプル'
iterable, iterable2 = '列|イテレータ'  # symbol
file = "ファイル"
filename = "ファイル名"

"""
synonym 用いる 使う する 用いる
synonym 表示する 出力する プリントする
synonym セパレータ 区切り記号 区切り文字列 セパレータ
"""

# 演算子
x = y  # yをxと呼ぶ
x % 2 == 0   # xが偶数かどうか
x % 2 == 1   # xが奇数かどうか
x % 2 != 0   # xが奇数かどうか
x % 2 != 1   # xが偶数かどうか
x % y == 0   # xがyの倍数かどうか
x % y == 0   # xがyの倍数でないかどうか
x == y     # xがyに 等しいかどうか
x != y     # xがyに 等しくないかどうか
x is y     # xがyと [同一|同じ]かどうか
x is not y     # xがyに [同一|同じ]でないかどうか
x in y     # xがy[内|の中|]に [含まれる|ある]かどうか] -> bool
x not in y     # xがy[内|の中|]に [含まれない|ない]かどうか
x ** y  # xのy 乗 -> int
x | y  # xと yの論理和 -> int
x ^ y  # xと yの排他的論理和 -> int
x & y  # xと yの論理積 -> int
x << n  # xのnビット、左シフト -> int
x >> n  # xのnビット、右シフト -> int
~x  # xのビット反転 -> int

x + y  # x + y
x - y  # x - y
x * y  # x × y
x / y  # x / y
x // y  # x / y
x + y + z  # x + y + z
str + x  # strと xを連結する -> str
str + x + y  # strと x, yを連結する -> str
str * n   # strをn個、連結する -> str

# 組み込み関数（計算）

abs(x)  # xの絶対値 -> int
bool(x)  # xが真かどうか
complex(x, y)  # x(実数部), y(虚数部)の複素数 -> complex
divmod(x, y)  # xと yの(商,余り) -> tuple

float(x)  # xの浮動小数点数

int(x)  # xを変換した 整数値
int(x, n)  # xをn進数として 変換した 整数値
base = x  # xを基数と する

ord(c)  # cの[文字コード|コードポイント]

min(x)  # 数列xの最大値 -> int
max(x, y)  # xと yの[大きい値|大きな方|最大値] -> int
max(x, y, z)  # x, y, zの最大値 -> int

min(x)  # 数列xの最小値 -> int
min(x, y)  # xと yの[小さい値|小さな方|最小値] -> int
min(x, y, z)  # x, y, zの最小値 -> int

pow(x, y)  # xのy乗 -> int
pow(x, y, z)  # xのy乗をzにより 剰余する -> int


round(x)  # xの[四捨五入する|丸める] -> int
round(x, n)  # xの少数部をn桁で [四捨五入する|丸める] -> int
math.trunc(x)  # xの少数部を切り捨てる -> int
math.floor(x)  # x以下の最大の整数 -> int
math.ceil(x)  # x以上の最小の整数 -> int

# 組み込み関数（文字列）

ascii(x)  # xの印字可能な 文字列 -> str

bin(x)  # xの２進数文字列 -> str
hex(x)  # xの16進数文字列 -> str
oct(x)  # xの8進数文字列 -> str

chr(codepoint)  # codepointの文字 -> str
repr(object)  # objectの印字可能な 文字列 -> str
str(x)  # xの文字列 -> str

# 組み込み関数（リスト）

x[y]  # x [ y ]

all(iterable)  # iterableの全ての要素が真かどうか
any(iterable)  # iterableのいずれかの要素が真かどうか

enumerate(x)  # xの順序数列 -> list
enumerate(x, y)  # xのyから始まる 順序数列 -> list
start = x  # startから始まる

iter(x)  # xのイテレータ -> iterable
len(x)  # xの[長さ|要素数|サイズ] -> int
len(str)  # strの文字数 -> int

list(x)  # xからのリスト -> list

next(x)  # xの次の値

range(x)  # 0から xまでの数列 -> list
range(x, y)  # xから yまでの数列 -> list
range(x, y, z)  # xから zごとによる yまでの数列 -> list
step = x  # 間隔は xにする

reversed(x)  # xの逆順 -> list

set(x)  # xの集合 -> set


"""
synonym 部分列 スライス
"""

slice(x)  # 0から xまでの部分列 -> list
slice(x, y)  # xから yまでの部分列 -> list
slice(x, y, z)  # xから zごとによる yまでの部分列 -> list

"""
synonym 整列する ソートする
"""

sorted(x)  # xをソートする -> list
reverse = False  # 逆順にする
key = x  # xをキーとする

sum(x)  # x(数列)の[総和|合計|合計値] -> int
sum(x)/len(x)  # x(数列)の[平均|平均値] -> int
tuple(x)  # xのタプル -> list

zip(x, y)  # xと yの各要素のペア列 -> list
zip(x, y, z)  # x, y, zの各要素のタプル列 -> list

# 組み込み関数（辞書）

dict, dict2 = '辞書'
key = '項目名|キー'

'''
synonym 項目 エントリ
synonym 更新する アップデートする
'''

dict(x)  # xの辞書 -> dict

dict[key]  # dictのkey[項目] -> x
list(dict)  # dictのキーの一覧 -> list
len(dict)  # dictの[項目]数 -> int
dict.clear()  # dictの全ての[項目]を消去する
dict.copy()  # dictの[浅い|]コピー -> dict

dict.get(key)  # dictのkey[項目] -> x
dict.get(key, x)  # dictのkey[項目]か、もし[存在し|]なければ x -> x
dict.items()  # 辞書の[項目]一覧 -> list
dict.keys()  # dictの[項目名]一覧 -> list
dict.pop(key)  # dictのkey(項目)を取り出す -> x
dict.popitem()  # dictから 最後に 追加した項目を取り出す -> x

dict.setdefault(key, x)  # dict内に key(項目)が[存在し|]なければ、その項目をxに する -> x

dict.update()  # dictを更新する
dict.update(x)  # dictをxで 更新する

dict.values()  # dictの値一覧 -> list

dict | dict2  # dictと dict2をマージする -> dict
dict |= dict2  # dictに dict2 を加える -> dict


# 組み込み関数（バイト列、IO）

encoding = 'エンコーディング|文字コード'
errors = 'エラーポリシー'
codepoint = 'コードポイント|文字コード'

bytearray(x)  # xのバイト配列 -> bytes
bytes(x)  # xのバイト列 -> bytes
errors = errors  # errorsに したがう
encoding = 'utf-8'  # UTF8を用いる
errors = 'strict'  # エラー処理は 厳密に する
errors = 'ignore'  # エラー処理は しない

prompt = 'プロンプト'
input()  # 入力された 文字列 -> str
input(s)  # s(プロンプト)に対し、入力される -> str

memoryview(x)  # xのメモリビュー

'''
synonym 開く オープンする
'''

open(filename)  # filenameを開く -> file
open(filename, 'r')  # filenameを読み込みモードで 開く -> file
open(filename, 'w')  # filenameを書き込みモードで 開く -> file
open(filename, 'a')  # filenameを追加書き込みモードで 開く -> file
mode = 'r'  # 読み込みモードを用いる
mode = 'w'  # 書き込みモードを用いる
mode = 'a'  # 追加モードを用いる
mode = 'b'  # バイナリモードを用いる
mode = 'モード'
newline = '改行コード'
buffering = -1  # バッファリングしない
buffering = x  # バッファリングは x サイズに する

print()  # 空行を表示する
print(x)  # xを表示する
print(x, y)  # xと yを[順に]表示する
print(x, y, z)  # x、y、zを[順に]表示する

sep = s  # sを[セパレータ]に 用いる
end = ''  # 改行がない
end = s  # sを改行の代わりに 用いる
file = file  # fileを出力先に 用いる
flush = False  # フラッシュを行わない
flush = True  # フラッシュを行う

# 組み込み関数（関数）

function = '関数'

callable(x)  # xが関数かどうか

eval(s)  # s(式)を評価する -> x
globals()  # グローバル変数の一覧 -> list

filter(function, x)  # xの各要素をfunctionを[用いて|適用して] フィルタする -> list
map(function, x)  # xの各要素に functionを適用する -> list

# 組み込み関数（オブジェクト）

attrname = '属性|プロパティ'
classinfo, classinfo2 = 'クラス'

delattr(x, attrname)  # xのattrnameを削除する
getattr(x, attrname)  # xのattrnameの値 -> x
hasattr(x, attrname)  # x がattrnameを持つかどうか
setattr(x, attrname, y)  # xのattrnameの値をyに する

hash(x)  # xのハッシュ値 -> int

isinstance(x, classinfo)  # xがclassinfoのインスタンスかどうか
issubclass(classinfo, classinfo2)  # classinfoがclassinfo2のサブクラスかどうか
id(x)  # xの[ユニークな|]識別値 -> int
type(x)  # xの型 -> type

# int

_int, _float = ''

n.bit_length()  # nの二進法で表すために 必要な ビット数 -> int
n.to_bytes(x)  # nをx長のバイト列に 変換する -> bytes
byteorder = "big"  # ビックエンディアンを用いる
byteorder = "little"  # リトルエンディアンを用いる
_int.from_bytes(bytes)  # バイト列bytesから 整数に 変換する -> int

x.is_integer()  # x(浮動小数点数)が整数かどうか
x.hex()  # x(浮動小数点数)の16 進文字列表現 -> str
_float.fromhex(s)  # s(16進文字列表現)を構文解析する -> float


# string
#
sub = '部分文字列'
suffix = '接尾辞'
prefix = '接頭辞'

string.ascii_letters  # アルファベット
string.ascii_lowercase  # 英小文字
string.ascii_uppercase  # 英大文字
string.digits  # 数字
string.hexdigits  # 16進数字
string.octdigits  # 16進数字
string.punctuation  # 記号
string.printable  # 印刷可能な ASCII文字
string.whitespace  # 空白文字

str.capitalize()  # strをキャピタライズする -> str
str.casefold()  # strをケースフォルドする -> str

str.center(x)  # strを幅xで 中央寄せする -> str
str.ljust(x)  # strを幅xで 右寄せする -> str
str.rjust(x)  # strを幅xで 左寄せする -> str
fillchar = c  # c(文字)で 埋める

str.count(sub)  # str内のsubの出現回数

str.encode()  # strをエンコードする -> bytes
str.endswith(suffix)  # strがsuffixで 終わるかどうか
str.startswith(prefix)  # strがprefixで 始まるかどうか

str.expandtabs()  # str内のタブを空白文字で 置き換える -> str
str.expandtabs(n)  # str内のタブをn文字の空白文字で 置き換える -> str
tabsize = x  # タブは、空白 x 文字分と する

"""
synonym 見つかる 出現する
"""

str.find(sub)  # str[内]で subが最初に 見つかる 位置 -> int
str.find(sub, start)  # str[内]をstartから 探したとき、 subが最初に 見つかる 位置 -> int
str.find(sub, start, end)
# str[内]をstartから endまで 探したとき、 subが最初に 見つかる 位置 -> int


str.index(sub)  # str[内]で subが最初に 見つかる 位置 -> int
str.index(sub, start)  # str[内]をstartから 探したとき、 subが最初に 見つかる 位置 -> int
str.index(sub, start, end)
# str[内]をstartから endまで 探したとき、 subが最初に 見つかる 位置 -> int

str.rfind(sub)  # str[内]で subが最後に 見つかる 位置 -> int
str.rfind(sub, start)  # str[内]をstartから 探したとき、 subが最後に 見つかる 位置 -> int
str.rfind(sub, start, end)
# str[内]をstartから endまで 探したとき、 subが最後に 見つかる 位置 -> int

str.rindex(sub)  # str[内]で subが最後に 見つかる 位置 -> int
str.rindex(sub, start)  # str[内]をstartから 探したとき、 subが最後に 見つかる 位置 -> int
str.rindex(sub, start, end)
# str[内]をstartから endまで 探したとき、 subが最後に 見つかる 位置 -> int

"""
synonym 整形する フォーマットする
"""

fmt = 'フォーマット|書式'
fmt.format(x)  # fmtをxで 整形する -> str
fmt.format(x, y)  # fmtに xと yを整形する -> str
fmt.format(x, y, z)  # fmtに x, y, z を整形する -> str

str.isalnum()  # strが英数字かどうか
str.isalpha()  # strが[アルファベット|英字]かどうか
str.isascii()  # strがASCII文字かどうか
str.isdecimal()  # strが数字かどうか
str.isdigit()  # strが数字かどうか
str.isidentifier()  # strが識別子文字かどうか
str.islower()  # strが[英小文字]かどうか
str.isnumeric()  # strが数字かどうか
str.isprintable()  # strが印字可能かどうか
str.isspace()  # strが空白かどうか
str.istitle()  # strが文字列がタイトルケース文字列かどうか
str.isupper()  # strが[英大文字]かどうか

"""
synonym 結合する 連結する ジョインする
"""

str.join(x)  # xをstrを間に入れて 結合する -> str


str.lower()  # strの[英小文字] -> str
str.upper()  # strの[英大文字] -> str

'''
synonym 置き換える 置換する
synonym 取り除く 除去する 
synonym 区切る 分割する パーティションする
'''

chars = '文字集合'
str.lstrip()  # strの先頭から 空白を取り除く -> str
str.lstrip(chars)  # strの先頭から charsを取り除く -> str
str.rstrip()  # strの末尾から 空白を取り除く -> str
str.rstrip(chars)  # strの末尾から charsを取り除く -> str
str.strip()  # strの先頭と 末尾から 空白を取り除く -> str
str.strip(chars)  # strの先頭と 末尾から charsを取り除く -> str


str.partition(sep)  # strをsepで 区切る -> tuple
str.partition(sep)  # strを末尾から sepで 区切る -> tuple

str.removeprefix(prefix)  # strの先頭から prefixを取り除く -> str
str.removesuffix(suffix)  # strの末尾から suffixを取り除く -> str

str.replace(sub, s2)  # str[内]のsub を全て s2に 置き換える -> str
str.replace(sub, '')  # str[内]のsub を全て 取り除く -> str

'''
synonym 分割する 分ける スプリットする 
'''

str.split(sep)  # strをsep で 分割する -> list
str.rsplit(sep)  # strをsep で 分割する -> list
maxsplit = '最大分割回数'

convtable = '変換表'
str.translate(convtable)  # strをconvtableに基づいて 変換する -> str

str.zfill(x)  # strを幅xになるように、'0'文字で 埋める -> str
