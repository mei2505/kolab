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
x = y  # yを x と呼ぶ
x % 2 == 0   # xが 偶数かどうか -> bool
x % 2 == 1   # xが 奇数かどうか -> bool
x % 2 != 0   # xが 奇数かどうか -> bool
x % 2 != 1   # xが 偶数かどうか -> bool
x % y == 0   # xが yの 倍数かどうか -> bool
x % y == 0   # xが yの 倍数でないかどうか -> bool
x == y     # xが yに 等しいかどうか -> bool
x != y     # xが yに 等しくないかどうか -> bool
x is y     # xが yと [同一|同じ]かどうか -> bool
x is not y     # xが yに [同一|同じ]でないかどうか -> bool
x in y     # xが y[内|の中|]に [含まれる|ある]かどうか] -> bool
x not in y     # xが y[内|の中|]に [含まれない|ない]かどうか -> bool
x ** y  # x の y 乗 -> int
x | y  # x と y の 論理和 -> int
x ^ y  # x と y の 排他的論理和 -> int
x & y  # x と y の 論理積 -> int
x << n  # x の n ビット 左シフト -> int
x >> n  # x の n ビット 右シフト -> int
~x  # xの ビット反転 -> int

x + y  # x + y
x - y  # x - y
x * y  # x × y
x / y  # x / y
x // y  # x / y
x + y + z  # x + y + z
str + x  # strと xを 連結する -> str
str + x + y  # strと x, yを 連結する -> str
str * n   # strを n個、連結する -> str

# 組み込み関数（計算）

abs(x)  # xの 絶対値 -> int
bool(x)  # xが 真かどうか -> bool
complex(x, y)  # x(実数部), y(虚数部)の 複素数 -> complex
divmod(x, y)  # xと yの (商,余り) -> tuple

float(x)  # xの 浮動小数点数

int(x)  # xを 変換した 整数値
int(x, n)  # xを n進数として 変換した 整数値
base = x  # xを 基数と する

ord(c)  # cの [文字コード|コードポイント]

min(x)  # 数列xの 最大値 -> int
max(x, y)  # xと yの[大きい値|大きな方|最大値] -> int
max(x, y, z)  # x, y, zの 最大値 -> int

min(x)  # 数列xの 最小値 -> int
min(x, y)  # xと yの[小さい値|小さな方|最小値] -> int
min(x, y, z)  # x, y, zの 最小値 -> int

pow(x, y)  # xの y乗 -> int
pow(x, y, z)  # xの y乗を zにより 剰余する -> int


round(x)  # xの [四捨五入する|丸める] -> int
round(x, n)  # xの少数部を n桁で [四捨五入する|丸める] -> int
math.trunc(x)  # xの 少数部を 切り捨てる -> int
math.floor(x)  # x以下の 最大の整数 -> int
math.ceil(x)  # x以上の 最小の整数 -> int

# 組み込み関数（文字列）

ascii(x)  # xの 印字可能な 文字列 -> str

bin(x)  # xの ２進数文字列 -> str
hex(x)  # xの 16進数文字列 -> str
oct(x)  # xの 8進数文字列 -> str

chr(codepoint)  # codepointの 文字 -> str
repr(object)  # objectの 印字可能な 文字列 -> str
str(x)  # x の文字列 -> str

# 組み込み関数（リスト）

x[y]  # x [ y ]

all(iterable)  # iterableの 全ての 要素が 真かどうか -> bool
any(iterable)  # iterableの いずれかの 要素が 真かどうか -> bool

enumerate(x)  # xの 順序数列 -> list
enumerate(x, y)  # xの yから始まる 順序数列 -> list
start = x  # startから始まる

iter(x)  # xの イテレータ -> iterable
len(x)  # xの [長さ|要素数|サイズ] -> int
len(str)  # strの 文字数 -> int

list(x)  # xからの リスト -> list

next(x)  # xの 次の値

range(x)  # 0から xまでの 数列 -> list
range(x, y)  # xから yまでの 数列 -> list
range(x, y, z)  # xから zごとによる yまでの 数列 -> list
step = x  # 間隔は xにする

reversed(x)  # xの 逆順 -> list

set(x)  # xの 集合 -> set


"""
synonym 部分列 スライス
"""

slice(x)  # 0から xまでの 部分列 -> list
slice(x, y)  # xから yまでの 部分列 -> list
slice(x, y, z)  # xから zごとによる yまでの 部分列 -> list

"""
synonym 整列する ソートする
"""

sorted(x)  # xを ソートする -> list
reverse = False  # 逆順にする
key = x  # xを キーとする

sum(x)  # x(数列)の [総和|合計|合計値] -> int
sum(x)/len(x)  # x(数列)の [平均|平均値] -> int
tuple(x)  # xの タプル -> list

zip(x, y)  # xと yの 各要素の ペア列 -> list
zip(x, y, z)  # x, y, zの 各要素の タプル列 -> list

# 組み込み関数（辞書）

dict, dict2 = '辞書'
key = '項目名|キー'

'''
synonym 項目 エントリ
synonym 更新する アップデートする
'''

dict(x)  # xの 辞書 -> dict

dict[key]  # dictの key[項目] -> x
list(dict)  # dictの キーの一覧 -> list
len(dict)  # dictの [項目]数 -> int
dict.clear()  # dictの 全ての[項目]を 消去する
dict.copy()  # dictの [浅い|]コピー -> dict

dict.get(key)  # dictの key[項目] -> x
dict.get(key, x)  # dictの key[項目]か、もし[存在し|]なければ x -> x
dict.items()  # 辞書の[項目]一覧 -> list
dict.keys()  # dictの [項目名]一覧 -> list
dict.pop(key)  # dictの key(項目)を 取り出す -> x
dict.popitem()  # dictから 最後に 追加した項目を 取り出す -> x

dict.setdefault(key, x)  # dict内に key(項目)が [存在し|]なければ、その項目を xに する -> x

dict.update()  # dictを 更新する
dict.update(x)  # dictを xで 更新する

dict.values()  # dictの 値一覧 -> list

dict | dict2  # dictと dict2を マージする -> dict
dict |= dict2  # dictに dict2 を加える -> dict


# 組み込み関数（バイト列、IO）

encoding = 'エンコーディング|文字コード'
errors = 'エラーポリシー'
codepoint = 'コードポイント|文字コード'

bytearray(x)  # xの バイト配列 -> bytes
bytes(x)  # xの バイト列 -> bytes
errors = errors  # errorsに したがう
encoding = 'utf-8'  # UTF8を 用いる
errors = 'strict'  # エラー処理は 厳密に する
errors = 'ignore'  # エラー処理は しない

prompt = 'プロンプト'
input()  # 入力された 文字列 -> str
input(s)  # s(プロンプト)に対し、入力される -> str

memoryview(x)  # xの メモリビュー

'''
synonym 開く オープンする
'''

open(filename)  # filenameを 開く -> file
open(filename, 'r')  # filenameを 読み込みモードで 開く -> file
open(filename, 'w')  # filenameを 書き込みモードで 開く -> file
open(filename, 'a')  # filenameを 追加書き込みモードで 開く -> file
mode = 'r'  # 読み込みモードを 用いる
mode = 'w'  # 書き込みモードを 用いる
mode = 'a'  # 追加モードを 用いる
mode = 'b'  # バイナリモードを 用いる
mode = 'モード'
newline = '改行コード'
buffering = -1  # バッファリングしない
buffering = x  # バッファリングは x サイズに する

print()  # 空行を 表示する
print(x)  # xを 表示する
print(x, y)  # xと yを [順に]表示する
print(x, y, z)  # x、y、zを [順に]表示する

sep = s  # sを [セパレータ]に 用いる
end = ''  # 改行が ない
end = s  # sを 改行の 代わりに 用いる
file = file  # fileを 出力先に 用いる
flush = False  # フラッシュを 行わない
flush = True  # フラッシュを 行う

# 組み込み関数（関数）

function = '関数'

callable(x)  # xが 関数かどうか -> bool

eval(s)  # s(式)を 評価する -> x
globals()  # グローバル変数の 一覧 -> list

filter(function, x)  # xの各要素を functionを [用いて|適用して] フィルタする -> list
map(function, x)  # xの 各要素に functionを 適用する -> list

# 組み込み関数（オブジェクト）

attrname = '属性|プロパティ'
classinfo, classinfo2 = 'クラス'

delattr(x, attrname)  # xの attrnameを 削除する
getattr(x, attrname)  # xの attrnameの 値 -> x
hasattr(x, attrname)  # x が attrnameを 持つかどうか -> bool
setattr(x, attrname, y)  # xの attrnameの 値を yに する

hash(x)  # xの ハッシュ値 -> int

isinstance(x, classinfo)  # xが classinfoの インスタンスかどうか -> bool
issubclass(classinfo, classinfo2)  # classinfoが classinfo2の サブクラスかどうか -> bool
id(x)  # xの [ユニークな|]識別値 -> int
type(x)  # xの 型 -> type

# int

_int, _float = ''


n.bit_length()  # nの 二進法で表すために 必要な ビット数 -> int
n.to_bytes(x)  # nを x長の バイト列に 変換する -> bytes
byteorder = "big"  # ビックエンディアンを 用いる
byteorder = "little"  # リトルエンディアンを 用いる
_int.from_bytes(bytes)  # バイト列bytesから 整数に 変換する -> int

x.is_integer()  # x(浮動小数点数)が 整数かどうか -> bool
x.hex()  # x(浮動小数点数)の 16 進文字列表現 -> str
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

str.capitalize()  # strを キャピタライズする -> str
str.casefold()  # strを ケースフォルドする -> str

str.center(x)  # strを 幅xで 中央寄せする -> str
str.ljust(x)  # strを 幅xで 右寄せする -> str
str.rjust(x)  # strを 幅xで 左寄せする -> str
fillchar = c  # c(文字)で 埋める

str.count(sub)  # str内の subの 出現回数

str.encode()  # strを エンコードする -> bytes
str.endswith(suffix)  # strが suffixで 終わるかどうか
str.startswith(prefix)  # strが prefixで 始まるかどうか

str.expandtabs()  # str内の タブを空白文字で 置き換える -> str
str.expandtabs(n)  # str内の タブをn文字の空白文字で 置き換える -> str
tabsize = x  # タブは、空白 x 文字分と する

"""
synonym 見つかる 出現する
"""

str.find(sub)  # str[内]で subが 最初に 見つかる 位置 -> int
str.find(sub, start)  # str[内]を startから 探したとき、 subが 最初に 見つかる 位置 -> int
str.find(sub, start, end)
# str[内]を startから endまで 探したとき、 subが 最初に 見つかる 位置 -> int


str.index(sub)  # str[内]で subが 最初に 見つかる 位置 -> int
str.index(sub, start)  # str[内]を startから 探したとき、 subが 最初に 見つかる 位置 -> int
str.index(sub, start, end)
# str[内]を startから endまで 探したとき、 subが 最初に 見つかる 位置 -> int

str.rfind(sub)  # str[内]で subが 最後に 見つかる 位置 -> int
str.rfind(sub, start)  # str[内]を startから 探したとき、 subが 最後に 見つかる 位置 -> int
str.rfind(sub, start, end)
# str[内]を startから endまで 探したとき、 subが 最後に 見つかる 位置 -> int

str.rindex(sub)  # str[内]で subが 最後に 見つかる 位置 -> int
str.rindex(sub, start)  # str[内]を startから 探したとき、 subが 最後に 見つかる 位置 -> int
str.rindex(sub, start, end)
# str[内]を startから endまで 探したとき、 subが 最後に 見つかる 位置 -> int

"""
synonym 整形する フォーマットする
"""

fmt = 'フォーマット|書式'
fmt.format(x)  # fmtを xで 整形する -> str
fmt.format(x, y)  # fmtに xと yを 整形する -> str
fmt.format(x, y, z)  # fmtに x, y, z を 整形する -> str

str.isalnum()  # strが 英数字かどうか -> bool
str.isalpha()  # strが [アルファベット|英字]かどうか -> bool
str.isascii()  # strが ASCII文字かどうか -> bool
str.isdecimal()  # strが 数字かどうか -> bool
str.isdigit()  # strが 数字かどうか -> bool
str.isidentifier()  # strが 識別子文字かどうか -> bool
str.islower()  # strが [英小文字]かどうか -> bool
str.isnumeric()  # strが 数字かどうか -> bool
str.isprintable()  # strが 印字可能かどうか -> bool
str.isspace()  # strが 空白かどうか -> bool
str.istitle()  # strが 文字列がタイトルケース文字列かどうか -> bool
str.isupper()  # strが [英大文字]かどうか -> bool

"""
synonym 結合する 連結する ジョインする
"""

str.join(x)  # xを strを 間に入れて 結合する -> str


str.lower()  # strの [英小文字] -> str
str.upper()  # strの [英大文字] -> str

'''
synonym 置き換える 置換する
synonym 取り除く 除去する 
synonym 区切る 分割する パーティションする
'''

chars = '文字集合'
str.lstrip()  # strの 先頭から 空白を 取り除く -> str
str.lstrip(chars)  # strの 先頭から charsを 取り除く -> str
str.rstrip()  # strの 末尾から 空白を 取り除く -> str
str.rstrip(chars)  # strの 末尾から charsを 取り除く -> str
str.strip()  # strの 先頭と 末尾から 空白を 取り除く -> str
str.strip(chars)  # strの 先頭と 末尾から charsを 取り除く -> str


str.partition(sep)  # strを sepで 区切る -> tuple
str.partition(sep)  # strを 末尾から sepで 区切る -> tuple

str.removeprefix(prefix)  # strの 先頭から prefixを 取り除く -> str
str.removesuffix(suffix)  # strの 末尾から suffixを 取り除く -> str

str.replace(sub, s2)  # str[内]の sub を 全て s2に 置き換える -> str
str.replace(sub, '')  # str[内]の sub を 全て 取り除く -> str

'''
synonym 分割する 分ける スプリットする 
'''

str.split(sep)  # strを sep で 分割する -> list
str.rsplit(sep)  # strを sep で 分割する -> list
maxsplit = '最大分割回数'

convtable = '変換表'
str.translate(convtable)  # strを convtableに基づいて 変換する -> str

str.zfill(x)  # strを 幅xになるように、'0'文字で 埋める -> str
