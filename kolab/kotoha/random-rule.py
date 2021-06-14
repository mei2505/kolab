import collections   # collections
import datetime
import subprocess
import re
import sys
import math
import os
import functools
import itertools
import bisect
import copy
import random
x, y, z, n, i, j = ''
s = '文字列'

_サンプリングする = 'サンプルを選ぶ|サンプリングする'
_乱数シード = '乱数生成列|乱数シード'

random.random()  # 乱数 -> float
random.choice(list)  # listからランダムに選ぶ -> x(要素)
random.shuffle(list)  # listをランダムに シャッフルする -> list
random.sample(list)  # list からサンプリングする -> list
random.sample(list, n)  # listからn個、サンプリングする -> list
random.randrange(x)  # 0からx[未満]までの整数乱数 -> int
random.randrange(x, y)  # xからy[未満|]までの整数乱数 -> int
random.randint(x, y)  # xからyまでの整数乱数 -> int
random.seed()  # 乱数シードを初期化する
random.seed(x)  # 乱数シードをxで初期化する

copy.deepcopy(x)  # xを深くコピーする -> x
copy.copy(x)  # xをコピーする-> x

bisect.bisect_left(x, y)  # xの順序を保ったまま、yを左から挿入できる位置
bisect.bisect_left(x, y, i, j)  # xの順序を保ったまま、iからjまでの範囲でyを左から挿入できる位置
bisect.bisect_right(x, y)  # xの順序を保ったまま、yを右から挿入できる位置
bisect.bisect_right(x, y, i, j)  # xの順序を保ったまま、iからjまでの範囲でyを右から挿入できる位置
bisect.bisect(x, y)  # xの順序を保ったまま、yを挿入できる位置
bisect.bisect(x, y, i, j)  # xの順序を保ったまま、iからjまでの範囲でyを挿入できる位置
bisect.insort_left(x, y)  # xにyをソート順で左から挿入する
bisect.insort_right(x, y)  # 　xにyをソート順で右から挿入する
bisect.insort(x, y)  # xにyをソート順で挿入する

itertools.repeat(x)  # xの無限列 -> list
itertools.repeat(x, n)  # xをn回繰り返した列 -> list
itertools.count()  # 0から始まる 無限の整数列 -> list
itertools.count(x)  # xから始まる 無限の整数列 -> list
itertools.count(x, y)  # xから始まり x間隔で続く 無限の整数列 ->list
itertools.cycle(x)  # xを無限に繰り返した列 -> list
itertools.product(x, y)  # xとyの直積 ->list
itertools.permutations(x)  # xの順列 -> list
itertools.permutations(x, n)  # xのうち n個までの順列 -> list
itertools.combinations(x)  # xのコンビネーション -> list
itertools.combinations(x, n)  # xのx個までのコンビネーション -> list
itertools.combinations_with_replacement(x)  # xの重複コンビネーション -> list
itertools.combinations_with_replacement(x, n)  # xのx個までの重複コンビネーション -> list

_リデュースする = '削減する|集約計算する|リデュースする'
functools.reduce(function, x)  # xをfunctionでリデュースする -> list
functools.reduce(function, x, y)  # zを初期値として 、xをfunctionでリデュースする -> list

deq = '両端キュー'

collections.deque(x)  # xの両端キュー
maxlen = x  # xを最大長とする

deq.appendleft(x)  # deqの先頭にxを追加する
deq.extendleft(x)  # deqの先頭をxで伸長する
deq.popleft()  # deqの先頭から取り除く
deq.rotate()  # deqの要素を右に ひとつ回転する
deq.rotate(n)  # deqの要素を右に n回、回転する

counter = '辞書カウンタ'
collections.Counter(x)  # xの辞書カウンタ -> counter
counter.most_common()  # counterの出現頻度[が高い|]順の列
counter.most_common(n)  # counterの上位 n位までの出現頻度順[が高い|]の列

os.sep  # ファイルパスのセパレータ
os.getcwd()  # 現在の作業ディレクトリ
os.system(x)  # x(システムコマンド)を実行する

os.path.basename(x)  # xのベースファイル名
os.path.dirname(x)  # xのディレクトリ名
os.path.abspath(x)  # xの絶対ファイルパス
os.path.split(x)  # xの(ディレクトリ名,ファイル名)
os.path.join(x, y)  # xとyを連結したファイルパス
os.path.splitext(x, y)  # xの(ファイル名,拡張子)
os.path.get_size(x)  # x(ファイル)の大きさ

subprocess.call(x)  # x(システムコマンド)を実行する

dt = '日時'

datetime.datetime(x, y, z)  # x年 y月 z日の日時 -> dt
datetime.datetime  # x年 x月 x日 x時 x分の日時 -> dt
datetime.datetime  # x年 x月 x日 x時 x分 x秒の日時 -> dt
datetime.datetime.now()  # 現在の日時 -> dt
dt.weekday()  # dtの週
dt.date()  # dtの日付
dt.strftime(x)  # dtをfmt(書式)で整形する
datetime.datetime.strptime  # xを書式 yを用いて構文解析した日時
datetime.strptime  # xを書式 yを用いて構文解析した日時
# dt.encode() # dtを文字コード xで復号化した文字列
# .decode # xを文字コード yで符号化したバイト列
# .decode # xを文字コード yでzポリシーに基づき符号化したバイト列


math.ceil(x)  # xの切り上げ整数値
math.comb(x)  # xとxのコンビネーション
math.copysign(x, y)  # yの符号が同じ x
math.fabs(x)  # xの絶対値
math.factorial(x)  # xの階乗
math.floor(x)  # xの切り捨て整数値
math.frexp(x)  # xの(仮数,指数)
math.gcd(x, y)  # xとyの最大公約数
math.isclose(x, y)  # xとyが近いかどうか
math.isfinite(x)  # xが有限かどうか
math.isinf(x)  # xが無限大かどうか
math.isnan(x)  # xがNaNかどうか
math.lcm(x, y)  # xとyの最小公倍数
math.modf(x)  # xの(小数部,整数部)
math.perm
math.prod
math.remainder(x, y)  # xをyで割った剰余
math.exp(x)  # eのx乗
math.expml(x)  # $e ^ x-1$
math.log(x)  # xの自然対数
math.log(x, y)  # yを底とする xの対数
math.log1p
math.log2(x)  # 2を底とする xの対数
math.log10(x)  # xの常用対数
math.sqrt(x)  # xの平方根
math.cos(x)  # xの余弦
math.dist(x)  # xとxのユークリッド距離
math.hypot(x, y)  # xとyのノルム
math.sin(x)  # xの正弦
math.tan(x)  # xの正接
math.degrees(x)  # xの角度
math.radians(x)  # xのラジアン
math.acosh(x)  # xの逆双曲線余弦
math.asinh(x)  # xの逆双曲線正弦
math.atanh(x)  # xの逆双曲線正接
math.cosh(x)  # xの双曲線余弦
math.sinh(x)  # xの双曲線正弦
math.tanh(x)  # xの双曲線正接
math.gamma(x)  # xのガンマ関数
math.lgamma(x)  # xのガンマ関数の絶対値の自然対数
math.pi  # 円周率
math.e  # ネイピア数
math.inf  # 無限大
math.nan  # NaN

_マッチする = 'マッチする|含まれる|マッチする'

re.search(x, y)  # x(正規表現)がyにマッチする 最初の位置 -> int
re.match(x, y)  # yに x(正規表現)がマッチするかどうか -> bool
re.fullmatch(x, y)  # x(正規表現)をy全体をマッチするかどうか -> bool
re.split(x, y)  # x(正規表現)を用いて、yをスプリットする -> list
re.sub(x, y, z)  # x(正規表現)にマッチしたyの部分をzに置き換える -> str
re.subn(x, y, z)  # x(正規表現)にマッチしたyの部分をzに置き換える -> list
re.findall(x, y)  # x(正規表現)にマッチしたz内の文字列リスト -> list
re.compile(x)  # xを正規表現に コンパイルする
flag = 'オプションフラグ'


sys.exit()  # プログラムを正常終了する
sys.exit(x)  # プログラムをx(終了ステータス)で終了する
