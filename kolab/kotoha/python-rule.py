# 準備
import string
import math

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

_用いる = '使う|する|用いる'
_プリントする = '表示する|出力する|プリントする'
_セパレータ = '区切り記号|区切り文字列|セパレータ'


# 演算子

x = y  # yをxと呼ぶ
x % 2 == 0   # xが偶数かどうか
x % 2 == 1   # xが奇数かどうか
x % 2 != 0   # xが奇数かどうか
x % 2 != 1   # xが偶数かどうか
x % y == 0   # xがyの倍数かどうか
x % y == 0   # xがyの倍数でないかどうか
x == y     # xがyに等しいかどうか
x != y     # xがyに等しくないかどうか

_同一 = '同じ|同一'
x is y     # xがyと同一かどうか
x is not y     # xがyと同一でないかどうか

_含まれる = '含まれる|ある'
_含まれない = '含まれない|ない'
_内 = '内|の中|中'

x in y     # xがy内に含まれるかどうか -> bool
x not in y     # xがy内に含まれないかどうか -> bool

x ** y  # xのy乗 -> int
x | y  # xとyの論理和 -> int
x ^ y  # xとyの排他的論理和 -> int
x & y  # xとyの論理積 -> int
x << n  # xのnビット、左シフト -> int
x >> n  # xのnビット、右シフト -> int
~x  # xのビット反転 -> int

x + y  # x + y
x - y  # x `-` y
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

int(x)  # xを整数に変換する -> int(値)
int(x, n)  # xをn進数として整数に変換する -> int(値)
base = x  # xを基数とする

_コードポイント = '文字コード|コードポイント'

ord(c)  # cのコードポイント

_大きな方 = '大きな値|大きな方|最大値'
_小さな方 = '小さな値|小さな方|最小値'

min(x)  # 数列xの最大値 -> int
max(x, y)  # xと yの大きな方 -> int
max(x, y, z)  # x, y, zの最大値 -> int

min(x)  # 数列xの最小値 -> int
min(x, y)  # xとyの小さな方 -> int
min(x, y, z)  # x, y, zの最小値 -> int

pow(x, y)  # xのy乗 -> int
pow(x, y, z)  # xのy乗をzにより 剰余する -> int

_丸める = '四捨五入する|丸める'
round(x)  # xの丸める -> int
round(x, n)  # xの少数部をn桁[まで|]で丸める -> int
math.trunc(x)  # xの少数部を切り捨てる -> int
math.floor(x)  # x以下の最大の整数 -> int
math.ceil(x)  # x以上の最小の整数 -> int

# 組み込み関数（文字列）

ascii(x)  # xの印字可能な文字列 -> str

bin(x)  # xの２進数文字列 -> str
hex(x)  # xの16進数文字列 -> str
oct(x)  # xの8進数文字列 -> str

chr(c)  # c(コードポイント)の文字 -> str
repr(object)  # objectの印字可能な文字列 -> str
str(x)  # xの文字列 -> str

# 組み込み関数（リスト）

x[y]  # x [ y ]

all(iterable)  # iterableの全ての要素が真かどうか -> bool
any(iterable)  # iterableのいずれかの要素が真かどうか -> bool

enumerate(x)  # xの順序数列 -> list
enumerate(x, y)  # xのyから始まる 順序数列 -> list
start = x  # startから始まる

_長さ = '長さ|要素数|サイズ|長さ'

iter(x)  # xのイテレータ -> iterable
len(x)  # xの長さ -> int
len(str)  # strの文字数 -> int

list(x)  # xからのリスト -> list

next(x)  # xの次の値

range(x)  # 0からxまでの数列 -> list
range(x, y)  # xからyまでの数列 -> list
range(x, y, z)  # xからzごとによる yまでの数列 -> list
step = x  # 間隔は xにする

reversed(x)  # xの逆順 -> list

set(x)  # xの集合 -> set


_スライス = '部分列|スライス'

slice(x)  # 0からxまでのスライス -> list
slice(x, y)  # xからyまでのスライス -> list
slice(x, y, z)  # xからzごとによる yまでのスライス -> list

_ソートする = 'ソートする|整列する|ソートする'

sorted(x)  # xをソートする -> list
reverse = False  # 逆順にする
key = x  # xをキーとする

_合計 = '合計値|総和|合計'
_平均 = '平均値|平均'

sum(x)  # x(数列)の合計 -> int
sum(x)/len(x)  # x(数列)の平均 -> int
tuple(x)  # xのタプル -> list

zip(x, y)  # xと yの各要素のペア列 -> list
zip(x, y, z)  # x, y, zの各要素のタプル列 -> list

# 組み込み関数（辞書）

dict, dict2 = '辞書'
key = '項目名|キー'

_エントリ = '項目|エントリ'
_アップデートする = '更新する|アップデートする'

dict(x)  # xの辞書 -> dict

dict[key]  # dictのkey(エントリ) -> x
list(dict)  # dictのキー一覧 -> list
len(dict)  # dictの_エントリ数 -> int
dict.clear()  # dictの全てのエントリを消去する
dict.copy()  # dictの[浅い|]コピー -> dict

dict.get(key)  # dictのkey(エントリ) -> x
dict.get(key, x)  # dictのkey(エントリ)か、もし[存在し|]なければ x -> x
dict.items()  # 辞書のエントリ一覧 -> list
dict.keys()  # dictのエントリ一覧 -> list
dict.pop(key)  # dictのkey(エントリ)を取り出す -> x
dict.popitem()  # dictから最後に追加したエントリを取り出す -> x

dict.setdefault(key, x)  # dict内にkey(エントリ)が[存在し|]なければ、そのエントリをxにする -> x

dict.update()  # dictをアップデートする
dict.update(x)  # dictをxでアップデートする

dict.values()  # dictの値一覧 -> list

dict | dict2  # dictと dict2をマージする -> dict
dict |= dict2  # dictにdict2 を加える -> dict


# 組み込み関数（バイト列、IO）

encoding = 'エンコーディング|文字コード'
errors = 'エラーポリシー'
codepoint = 'コードポイント|文字コード'

bytearray(x)  # xのバイト配列 -> bytes
bytes(x)  # xのバイト列 -> bytes
errors = errors  # errorsにしたがう
encoding = 'utf-8'  # UTF8を用いる
errors = 'strict'  # エラー処理は厳密にする
errors = 'ignore'  # エラー処理はしない

prompt = 'プロンプト'
input()  # 入力された 文字列 -> str
input(s)  # s(プロンプト)に対し、入力される -> str

memoryview(x)  # xのメモリビュー

_オープンする = '開く|オープンする'

open(filename)  # filenameをオープンする -> file
open(filename, 'r')  # filenameを読み込みモードでオープンする -> file
open(filename, 'w')  # filenameを書き込みモードでオープンする -> file
open(filename, 'a')  # filenameを追加書き込みモードでオープンする -> file
mode = 'r'  # 読み込みモードを用いる
mode = 'w'  # 書き込みモードを用いる
mode = 'a'  # 追加モードを用いる
mode = 'b'  # バイナリモードを用いる
mode = 'モード'
newline = '改行コード'
buffering = -1  # バッファリングしない
buffering = x  # バッファリングは x サイズにする

print()  # 空行を表示する
print(x)  # xを表示する
print(x, y)  # xと yを[順に]表示する
print(x, y, z)  # x、y、zを[順に]表示する

sep = s  # sをセパレータに用いる
end = ''  # 改行がない
end = s  # sを改行の代わりに用いる
file = file  # fileを出力先に用いる
flush = False  # フラッシュを行わない
flush = True  # フラッシュを行う

# 組み込み関数（関数）

function = '関数'

callable(x)  # xが関数かどうか

eval(s)  # s(式)を評価する -> x
globals()  # グローバル変数の一覧 -> list

_適用して = '用いて|適用して'
filter(function, x)  # xの各要素をfunctionを適用して、フィルタする -> list
map(function, x)  # xの各要素にfunctionを適用する -> list

# 組み込み関数（オブジェクト）

attrname = '属性|プロパティ'
class1, class2 = 'クラス'

delattr(x, attrname)  # xのattrnameを削除する
getattr(x, attrname)  # xのattrnameの値 -> x
hasattr(x, attrname)  # x がattrnameを持つかどうか -> bool
setattr(x, attrname, y)  # xのattrnameの値をyにする

hash(x)  # xのハッシュ値 -> int

isinstance(x, class1)  # xがclass1のインスタンスかどうか -> bool
issubclass(class1, class2)  # class1がclass2のサブクラスかどうか -> bool
id(x)  # xのユニークな識別値 -> int
type(x)  # xの型 -> type

# int

n, _int, _float = ''

n.bit_length()  # nの二進法で表すために必要なビット数 -> int
n.to_bytes(x)  # nをx長のバイト列に変換する -> bytes
byteorder = "big"  # ビックエンディアンを用いる
byteorder = "little"  # リトルエンディアンを用いる
_int.from_bytes(bytes)  # バイト列bytesから整数に変換する -> int

x.is_integer()  # x(浮動小数点数)が整数かどうか
x.hex()  # x(浮動小数点数)の16 進文字列表現 -> str
_float.fromhex(s)  # s(16進文字列表現)を構文解析する -> float


# string
#
sub = '部分文字列'
suffix = '接尾辞'
prefix = '接頭辞'

string.ascii_letters  # アルファベット -> str
string.ascii_lowercase  # 英小文字 -> str
string.ascii_uppercase  # 英大文字 -> str
string.digits  # 数字 -> str
string.hexdigits  # 16進数字 -> str
string.octdigits  # 16進数字 -> str
string.punctuation  # 記号 -> str
string.printable  # 印刷可能なASCII文字 -> str
string.whitespace  # 空白文字 -> str

str.capitalize()  # strをキャピタライズする -> str
str.casefold()  # strをケースフォルドする -> str

str.center(x)  # strを幅xで中央寄せする -> str
str.ljust(x)  # strを幅xで右寄せする -> str
str.rjust(x)  # strを幅xで左寄せする -> str
fillchar = c  # c(文字)で埋める

str.count(sub)  # str内のsubの出現回数

str.encode()  # strをエンコードする -> bytes
str.endswith(suffix)  # strがsuffixで終わるかどうか
str.startswith(prefix)  # strがprefixで始まるかどうか

str.expandtabs()  # str内のタブを空白文字で置き換える -> str
str.expandtabs(n)  # str内のタブをn文字の空白文字で置き換える -> str
tabsize = x  # タブは、空白 x 文字分と する

_見つかる = '見つかる|出現する'
_内 = '内|の中|中'

str.find(sub)  # str内でsubが見つかる -> int
str.find(sub)  # str内でsubが見つかる -> int
str.find(sub)  # str内でsubが最初に見つかる -> int(位置)
str.find(sub, start)  # str内をstartから探したとき、 subが最初に見つかる -> int(位置)
str.find(sub, start, end)
# str内をstartからendまで探したとき、 subが最初に見つかる -> int(位置)

str.find(sub) >= 0  # str内でsubが見つかるかどうか -> bool
str.find(sub) == -1  # str内でsubが見つからないかどうか -> bool

str.index(sub)  # str内でsubが最初に見つかる -> int(位置(位置)
str.index(sub, start)  # str内をstartから探したとき、 subが最初に見つかる -> int(位置)
str.index(sub, start, end)
# str内をstartからendまで探したとき、 subが最初に見つかる -> int(位置)

str.rfind(sub)  # str内でsubが最後に見つかる -> int(位置)
str.rfind(sub, start)  # str内をstartから探したとき、 subが最後に見つかる -> int(位置)
str.rfind(sub, start, end)
# str内をstartからendまで探したとき、 subが最後に見つかる -> int(位置)

str.rindex(sub)  # str内でsubが最後に見つかる -> int(位置)
str.rindex(sub, start)  # str内をstartから探したとき、 subが最後に見つかる -> int(位置)
str.rindex(sub, start, end)
# str内をstartからendまで探したとき、 subが最後に見つかる -> int(位置)

_フォーマットする = '整形する|フォーマットする'
fmt = 'フォーマット|書式'
fmt.format(x)  # fmtをxでフォーマットする -> str
fmt.format(x, y)  # fmtにxと yをフォーマットする -> str
fmt.format(x, y, z)  # fmtにx, y, z をフォーマットする -> str

_アルファベット = "アルファベット|英字"

str.isalnum()  # strが英数字かどうか
str.isalpha()  # strがアルファベットかどうか
str.isascii()  # strがASCII文字かどうか
str.isdecimal()  # strが数字かどうか
str.isdigit()  # strが数字かどうか
str.isidentifier()  # strが識別子文字かどうか
str.islower()  # strが英小文字かどうか
str.isnumeric()  # strが数字かどうか
str.isprintable()  # strが印字可能かどうか
str.isspace()  # strが空白かどうか
str.istitle()  # strがタイトルケース文字列かどうか
str.isupper()  # strが英大文字かどうか

_ジョインする = '結合する|連結する|ジョインする'

str.join(x)  # xをstrを間に入れてジョインする -> str

str.lower()  # strの英小文字 -> str
str.upper()  # strの英大文字 -> str

_リプレースする = '置き換える|置換する|リプレースする'
_取り除く = '取り除く|除去する'
_パーティションする = '区切る|分割する|パーティションする'

chars = '文字集合'
str.lstrip()  # strの先頭から空白を取り除く -> str
str.lstrip(chars)  # strの先頭からcharsを取り除く -> str
str.rstrip()  # strの末尾から空白を取り除く -> str
str.rstrip(chars)  # strの末尾からcharsを取り除く -> str
str.strip()  # strの先頭と 末尾から空白を取り除く -> str
str.strip(chars)  # strの先頭と 末尾からcharsを取り除く -> str


str.partition(sep)  # strをsepでパーティションする -> tuple
str.partition(sep)  # strを末尾からsepでパーティションする -> tuple

str.removeprefix(prefix)  # strの先頭からprefixを取り除く -> str
str.removesuffix(suffix)  # strの末尾からsuffixを取り除く -> str

str.replace(sub, s2)  # str内のsub を全て s2に置き換える -> str
str.replace(sub, '')  # str内のsub を全て 取り除く -> str

_スプリットする = '分割する|分ける|スプリットする'

str.split(sep)  # strをsepでスプリットする -> list
str.rsplit(sep)  # strをsepでスプリットする -> list
maxsplit = '最大分割回数'

convtable = '変換表'
str.translate(convtable)  # strをconvtableに基づいて 変換する -> str

str.zfill(x)  # strを幅xになるように、'0'文字で埋める -> str
