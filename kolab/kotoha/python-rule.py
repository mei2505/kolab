# 準備
math = __package__  # module

file = "ファイル名"  # symbol
s = '文字列'  # symbol
s2 = '文字列'  # symbol

x = '値'  # symbol
y = '値'  # symbol
z = '値'  # symbol
n = '整数'  # symbol

"""
synonym 置き換える 置換する
synonym 用いる 使う する 用いる
synonym 取り除く 除去する 
synonym 表示する 出力する プリントする
synonym セパレータ 区切り記号 区切り文字列 セパレータ
"""

# 演算子
x % 2 == 0   # xが 偶数かどうか
x % 2 == 1   # xが 奇数かどうか
x % 2 != 0   # xが 奇数かどうか
x % 2 != 1   # xが 偶数かどうか
x % y == 0   # xが yの 倍数かどうか
x % y == 0   # xが yの 倍数でないかどうか
x == y     # xが yに 等しいかどうか
x != y     # xが yに 等しくないかどうか
x in y     # xが y[内|の中|]に [含まれるかどうか|あるかどうか]
x not in y     # xが y[内|の中|]に [含まれないかどうか|ないかどうか]
x ** y  # x の y 乗
x | y  # x と y の 論理和
x ^ y  # x と y の 排他的論理和
x & y  # x と y の 論理積
x << n  # x の n ビット 左シフト
x >> n  # x の n ビット 右シフト
# ~x  # xの ビット反転

# 組み込み関数

iterable = '列'  # symbol

# 組み込み関数（計算）

abs(x)  # xの 絶対値
bool(x)  # xが 真かどうか
complex(x, y)  # xと yの 複素数
divmod(x, y)  # xと yの 商と余り

float(x)  # xの 浮動小数点数

int(x)  # xを 変換した 整数値
int(x, base)  # xを base進数として 変換した 整数値
base = x  # xを 基数と する

ord(c)  # cの [文字コード|コードポイント]

min(iterable)  # iterableの 最大値
max(x, y)  # xと yの[大きい値|大きな方|最大値]
max(x, y, z)  # xと y、zの 最大値

min(iterable)  # iterableの 最小値
min(x, y)  # xと yの[小さい値|小さな方|最小値]
min(x, y, z)  # xと y、zの 最小値

pow(base, exp, mod)  # baseの exp乗
pow(base, exp, mod)  # baseの exp乗 の 剰余

round(x)  # xの [四捨五入する|丸める] -> 整数
round(x, ndigits)  # xの少数部を ndigists 桁に 丸めた 値
math.trunc(x)  # xの 少数部を 切り捨てる -> 整数
math.floor(x)  # x以下の 最大の整数
math.ceil(x)  # x以上の 最小の整数

# 組み込み関数（文字列）

ascii(object)  # objectの 印字可能な 文字列

bin(x)  # xの ２進数文字列
hex(x)  # xの 16進数文字列
oct(x)  # xの 8進数文字列

chr(codepoint)  # codepointの 文字
repr(object)  # objectの 印字可能な 文字列
str(x)  # x の文字列

# 組み込み関数（リスト）

all(iterable)  # iterableの 全ての 要素が 真かどうか
any(iterable)  # iterableの いずれかの 要素が 真かどうか

dict(object)  # objectの 辞書

start = '開始'  # symbol

enumerate(iterable)  # iterableの 順序数列
enumerate(iterable, start)  # iterableの startから始まる 順序数列
start = x  # startから始まる

iter(object)  # objectからの 列
len(object)  # objectの [長さ|要素数|サイズ]
list(iterable)  # iterableからの リスト

next(x)  # xの 次の値

range(stop)  # 0から stopまでの 数列
range(start, stop)  # startから stopまでの 数列
range(start, stop, step)  # startから stepごとによる stopまでの 数列
step = x  # 間隔は xにする

reversed(iterable)  # iterableの 逆順

set(iterable)  # iterableの 集合

slice(stop)  # 0から stopまでの スライス
slice(start, stop)  # startから stopまでの スライス
slice(start, stop, step)  # startから stepごとによる stopまでの スライス

"""
synonym ソートする 整列する
"""

sorted(iterable)  # iterable を ソートする
reverse = False  # 逆順に
key = x  # xを キーとして

sum(iterable)  # iterableの[総和|合計|合計値]
sum(x)/len(x)  # xの[平均|平均値]
tuple(x)  # xの タプル

zip(x, y)  # xと yの 各要素の ペア列
zip(x, y, z)  # xと y、zの 各要素の タプル列


# 組み込み関数（バイト列、IO）

source = 'ソース'  # symbol
encoding = 'エンコーディング|文字コード'  # symbol
errors = 'エラーポリシー'  # symbol
codepoint = 'コードポイント|文字コード'  # symbol

bytearray(source)  # sourceの バイト配列
bytes(source)  # sourceの バイト列
errors = errors  # errorsに したがう
encoding = 'utf-8'  # UTF8を 用いる
errors = 'strict'  # エラー処理は 厳密に する
errors = 'ignore'  # エラー処理は しない

prompt = 'プロンプト'  # symbol
input()  # 入力された 文字列
input(prompt)  # promptに対し、入力された 文字列
prompt = s  # プロンプトとして sを 用いる

memoryview(object)  # objectの メモリビュー
# open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)

open(file)  # fileを 開く -> ファイル
open(file, 'r')  # fileを 読み込みモードで 開く -> ファイル
open(file, 'w')  # fileを 書き込みモードで 開く -> ファイル
open(file, 'a')  # fileを 追加書き込みモードで 開く -> ファイル
mode = 'r'  # 読み込みモードを 用いる
mode = 'w'  # 書き込みモードを 用いる
mode = 'a'  # 追加モードを 用いる
mode = 'モード'  # symbol
newline = '改行コード'  # symbol

print()  # 空行を 表示する
print(x)  # xを 表示する
print(x, y)  # xと yを [順に]表示する
print(x, y, z)  # x、y、zを [順に]表示する

sep = s  # sを [セパレータ]に 用いる
end = ''  # 改行が ない
end = s  # sを 改行の 代わりに 用いる
file = f  # fを 出力先に 用いる
flush = False  # フラッシュを 行わない
flush = True  # フラッシュを 行う

# 組み込み関数（関数）

function = '関数'  # symbol

callable(object)  # objectが 関数かどうか

eval(s)  # sを 評価する
globals()  # グローバル変数の リスト

filter(function, iterable)  # iterableを functionを [用いて|適用して] フィルタする -> 列
map(function, iterable)  # iterableの 各要素に functionを 適用する -> 列

# 組み込み関数（オブジェクト）

attrname = 'プロパティ名|属性名'  # symbol
classinfo = 'クラス'  # symbol
classinfo2 = 'クラス'  # symbol

delattr(object, attrname)  # objectの attrnameを 削除する
getattr(object, attrname)  # objectの attrnameの 値
hasattr(object, attrname)  # object が attrnameを 持つかどうか
setattr(object, attrname, x)  # objectの attrnameの 値を xに する

hash(object)  # objectの ハッシュ値

isinstance(object, classinfo)  # objectが classinfoの インスタンスかどうか
issubclass(classinfo, classinfo2)  # objectが classinfoの サブクラスかどうか
id(object)  # objectの [ユニークな|]識別値
type(object)  # objectの 型

# int

n.bit_length()  # nの 二進法で表すために 必要な ビット数
n.to_bytes(length)  # nを length長の バイト列に 変換する -> バイト列
byteorder = "big"  # ビックエンディアンを 用いる
byteorder = "little"  # リトルエンディアンを 用いる
int.from_bytes(bytes)  # バイト列bytesから 整数に 変換する -> 整数

x.is_integer()  # x(浮動小数点数)が 整数かどうか
x.hex()  # x(浮動小数点数)の 16 進文字列表現
float.fromhex(s)  # s(16進文字列表現)を構文解析する -> 浮動小数点数


# string
#
string = __package__  # module
sub = '部分文字列'  # symbol
suffix = '接尾辞'  # symbol
prefix = '接頭辞'  # symbol

string.ascii_letters  # アルファベット
string.ascii_lowercase  # 英小文字
string.ascii_uppercase  # 英大文字
string.digits  # 数字
string.hexdigits  # 16進数字
string.octdigits  # 16進数字
string.punctuation  # 記号
string.printable  # 印刷可能な ASCII文字
string.whitespace  # 空白文字

str.capitalize()  # strを キャピタライズする -> 文字列
str.casefold()  # strを ケースフォルドする -> 文字列

str.center(x)  # strを 幅xで 中央寄せする -> 文字列
str.ljust(x)  # strを 幅xで 右寄せする -> 文字列
str.rjust(x)  # strを 幅xで 左寄せする -> 文字列
fillchar = c  # c(文字)で 埋める

str.count(sub)  # str内の subの 出現回数

str.encode()  # strを エンコードする -> バイト列
str.endswith(suffix)  # strが suffixで 終わるかどうか
str.startswith(prefix)  # strが prefixで 始まるかどうか

str.expandtabs()  # str内の タブを空白文字で 置き換える -> 文字列
str.expandtabs(n)  # str内の タブをn文字の空白文字で 置き換える -> 文字列
tabsize = x  # タブは、空白 x 文字分と する

"""
synonym 見つかる 出現する
"""

str.find(sub)  # str[内]で subが 最初に 見つかる 位置
str.find(sub, start)  # str[内]を startから 探したとき、 subが 最初に 見つかる 位置
str.find(sub, start, end)  # str[内]を startから endまで 探したとき、 subが 最初に 見つかる 位置

str.index(sub)  # str[内]で subが 最初に 見つかる 位置
str.index(sub, start)  # str[内]を startから 探したとき、 subが 最初に 見つかる 位置
str.index(sub, start, end)  # str[内]を startから endまで 探したとき、 subが 最初に 見つかる 位置

str.rfind(sub)  # str[内]で subが 最後に 見つかる 位置
str.rfind(sub, start)  # str[内]を startから 探したとき、 subが 最後に 見つかる 位置
str.rfind(sub, start, end)  # str[内]を startから endまで 探したとき、 subが 最後に 見つかる 位置

str.rindex(sub)  # str[内]で subが 最後に 見つかる 位置
str.rindex(sub, start)  # str[内]を startから 探したとき、 subが 最後に 見つかる 位置
str.rindex(sub, start, end)  # str[内]を startから endまで 探したとき、 subが 最後に 見つかる 位置

"""
synonym 当てはめる 適用する
"""

fmt = 'フォーマット|書式'  # symbol
fmt.format(x)  # fmtに x を当てはめる -> 文字列
fmt.format(x, y)  # fmtに xと yを を当てはめる -> 文字列
fmt.format(x, y, z)  # fmtに x、y、z を を当てはめる -> 文字列

str.isalnum()  # strが 英数字かどうか
str.isalpha()  # strが [アルファベット|英字]かどうか
str.isascii()  # strが ASCII文字かどうか
str.isdecimal()  # strが 数字かどうか
str.isdigit()  # strが 数字かどうか
str.isidentifier()  # strが 識別子文字かどうか
str.islower()  # strが [英小文字]かどうか
str.isnumeric()  # strが 数字かどうか
str.isprintable()  # strが 印字可能かどうか
str.isspace()  # strが 空白かどうか
str.istitle()  # strが 文字列がタイトルケース文字列かどうか
str.isupper()  # strが [英大文字]かどうか

str.join(iterable)  # iterableを strを 間に入れて 連結する -> 文字列

str.lower()  # strの [英小文字]
str.upper()  # strの [英大文字]

chars = '文字集合'  # symbol
str.lstrip()  # strの 先頭から 空白を 取り除く -> 文字列
str.lstrip(chars)  # strの 先頭から charsを 取り除く -> 文字列
str.rstrip()  # strの 末尾から 空白を 取り除く -> 文字列
str.rstrip(chars)  # strの 末尾から charsを 取り除く -> 文字列
str.strip()  # strの 先頭と 末尾から 空白を 取り除く -> 文字列
str.strip(chars)  # strの 先頭と 末尾から charsを 取り除く -> 文字列

str.partition(sep)  # strを sepで 区切る -> 文字列の組
str.partition(sep)  # strを 末尾から sepで 区切る -> 文字列の組

str.removeprefix(prefix)  # strの 先頭から prefixを 取り除く -> 文字列
str.removesuffix(suffix)  # strの 末尾から suffixを 取り除く -> 文字列

str.replace(sub, s2)  # str[内]の sub を 全て s2に 置き換える
str.replace(sub, '')  # str[内]の sub を 全て 取り除く -> 文字列

str.split(sep)  # strを sep で 分割する -> 文字列リスト
str.rsplit(sep)  # strを sep で 分割する -> 文字列リスト
maxsplit = '最大分割回数'  # symbol

convtable = '変換表'  # symbol
str.translate(convtable)  # strを convtableに基づいて 変換する -> 文字列

str.zfill(x)  # strを 幅xになるように、'0'文字で埋める -> 文字列
