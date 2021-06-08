import collections as collections  # collections
import datetime as datetime
import subprocess as subprocess
import re as re
import sys as sys
import math as math
import os as os
import functools as functools
import itertools as itertools
import bisect as bisect
import copy as copy
import random as random
x, y, z, n, start, end = ''
s = '文字列'

random.random()  # [0.0〜1.0の|] 乱数 -> float
random.choice(list)  # listから ランダムに選んだ 要素 -> x
random.shuffle(list)  # listを ランダムに シャッフルする -> list
random.sample(list)  # list から サンプルを 選ぶ -> list
random.sample(list, n)  # listから n個、サンプルを 選ぶ -> list
random.randrange(x)  # 0から x[未満]までの 整数乱数
random.randrange(x, y)  # xから y[未満|]までの 整数乱数
random.randint(x, y)  # xから yまでの 整数乱数
random.seed()  # 乱数生成を 初期化する
random.seed(x)  # xを シードとして 乱数生成を 初期化する

copy.deepcopy(x)  # xを 深く コピーする -> x
copy.copy(x)  # xを コピーする-> x

bisect.bisect_left(x, y)  # 順序を 保ったまま yを xに挿入できる位置
# 順序を 保ったまま yを start から {3}までの 範囲で xに挿入できる位置
bisect.bisect_left(x, y, start, end)

bisect.bisect_right(x, y)  # 順序を 保ったまま yを xに挿入できる最後の 位置
bisect.bisect_right(x, y)  # 順序を 保ったまま yを zから {3}までの 範囲で xに挿入できる位置
bisect.bisect(x, y)  # 順序を 保ったまま yを xに挿入できる最後の 位置
bisect.bisect(x, y)  # 順序を 保ったまま yを zから {3}までの 範囲で xに挿入できる位置
bisect.insort_left(x, y)  # yを xにソート順で挿入する
bisect.insort_right(x, y)  # yを xにソート順で最後に挿入する
bisect.insort(x, y)  # yを xにソート順で最後に挿入する

itertools.repeat(x)  # xの 無限列 -> list
itertools.repeat(x, n)  # xの n回続く列 -> list
itertools.count()  # 無限の 整数列 -> list
itertools.count(x)  # xから 始まる 無限の 整数列 -> list
itertools.count(x, y)  # xから 始まり x間隔で続く 無限の 整数列 ->list
itertools.cycle(x)  # xを 無限に繰り返した列 -> list
itertools.product(x, y)  # xと yの 直積 ->list
itertools.permutations(x)  # xの 順列 -> list
itertools.permutations(x, n)  # xの うち n個までの 順列 -> list
itertools.combinations(x)  # xの コンビネーション -> list
itertools.combinations(x, n)  # xの x個までの コンビネーション -> list
itertools.combinations_with_replacement(x)  # xの 重複コンビネーション -> list
itertools.combinations_with_replacement(x, n)  # xの x個までの 重複コンビネーション -> list

functools.reduce(function, x)  # xを functionで 集約する -> list
functools.reduce(function, x, y)  # zを 初期値として 、xを functionで 集約する -> list

deq = '両端キュー'

collections.deque(x)  # xの 両端キュー
maxlen = x  # xを 最大長とする

deq.appendleft(x)  # deqの 先頭に xを 追加する
deq.extendleft(x)  # deqの 先頭を xで伸長する
deq.popleft()  # deqの 先頭から 取り除いく
deq.rotate()  # deqの 要素を 右に ひとつ回転する
deq.rotate(n)  # deqの 要素を 右に n回、回転する

counter = '辞書カウンタ'
collections.Counter(x)  # xの 辞書カウンタ
counter.most_common()  # counterの 出現頻度順の 列
counter.most_common(n)  # counterの 上位 n個の 出現頻度順の 列

os.sep  # ファイルパスの セパレータ記号
os.getcwd()  # 現在の 作業ディレクトリ
os.system(x)  # x(システムコマンド)を 実行する

os.path.basename(x)  # xの ベースファイル名
os.path.dirname(x)  # xの ディレクトリ名
os.path.abspath(x)  # xの 絶対ファイルパス
os.path.split(x)  # xの (ディレクトリ名,ファイル名)
os.path.join(x, y)  # xと yを 連結したファイルパス
os.path.splitext(x, y)  # xの (ファイル名,拡張子)
os.path.get_size(x)  # x(ファイル)の 大きさ

subprocess.call(x)  # x(システムコマンド)を 実行する

dt = '日時'

datetime.datetime(x, y, z)  # x年 y月 z日の 日時 -> dt
datetime.datetime  # x年 x月 x日 x時 x分の 日時 -> dt
datetime.datetime  # x年 x月 x日 x時 x分 x秒の 日時 -> dt
datetime.datetime.now()  # 現在の 日時 -> dt
dt.weekday()  # dtの 週
dt.date()  # dtの 日付
dt.strftime(x)  # dtを fmt(書式)で 整形する
datetime.datetime.strptime  # xを 書式 yを 用いて構文解析した日時
datetime.strptime  # xを 書式 yを 用いて構文解析した日時
# dt.encode() # dtを 文字コード xで復号化した文字列
# .decode # xを 文字コード yで符号化したバイト列
# .decode # xを 文字コード yで zポリシーに基づき符号化したバイト列


math.ceil(x)  # xの切り上げ整数値
math.comb(x)  # xと xの コンビネーション
math.copysign(x, y)  # yの 符号が 同じ x
math.fabs(x)  # xの 絶対値
math.factorial(x)  # xの 階乗
math.floor(x)  # xの 切り捨て整数値
math.frexp(x)  # xの (仮数,指数)
math.gcd(x)  # xと xの 最大公約数
math.isclose(x, y)  # xと yが 近いかどうか
math.isfinite(x)  # xが 有限かどうか
math.isinf(x)  # xが 無限大かどうか
math.isnan(x)  # xが NaNかどうか
math.lcm(x, y)  # xと xの 最小公倍数
math.modf(x)  # xの(小数部,整数部)
math.perm
math.prod
math.remainder(x, y)  # xを yで割った剰余
math.exp(x)  # eの x乗
math.expml(x)  # $e ^ x-1$
math.log(x)  # xの 自然対数
math.log(x, y)  # yを 底とする xの 対数
math.log1p
math.log2(x)  # 2を 底とする xの 対数
math.log10(x)  # xの 常用対数
math.sqrt(x)  # xの 平方根
math.cos(x)  # xの 余弦
math.dist(x)  # xと xの ユークリッド距離
math.hypot(x, y)  # xと yの ノルム
math.sin(x)  # xの 正弦
math.tan(x)  # xの 正接
math.degrees(x)  # xの 角度
math.radians(x)  # xの ラジアン
math.acosh(x)  # xの 逆双曲線余弦
math.asinh(x)  # xの 逆双曲線正弦
math.atanh(x)  # xの 逆双曲線正接
math.cosh(x)  # xの 双曲線余弦
math.sinh(x)  # xの 双曲線正弦
math.tanh(x)  # xの 双曲線正接
math.gamma(x)  # xの ガンマ関数
math.lgamma(x)  # xの ガンマ関数の 絶対値の 自然対数
math.pi  # 円周率
math.e  # ネイピア数
math.inf  # 無限大
math.nan  # NaN

re.search(x, y)  # x(正規表現)が yにマッチする 最初の位置 -> int
re.match(x, y)  # yに x(正規表現)が [マッチする|含まれる]かどうか -> bool
re.fullmatch(x, y)  # x(正規表現)を y全体を　[マッチする|含まれる]かどうか -> bool
re.split(x, y)  # x(正規表現)を用いて、yを 分割する -> list
re.sub(x, y, z)  # zが x(正規表現)にマッチした箇所を yに置き換えた文字列
re.subn(x, y, z)  # zが x(正規表現)にマッチした箇所を yに置き換えた文字列の 組
re.findall(x, y)  # yが x(正規表現)にマッチした文字列の 列
re.compile(x)  # xを 正規表現に コンパイルする
flag = 'オプションフラグ'


sys.exit()  # プログラムを 正常終了する
sys.exit(x)  # プログラムを x(終了ステータス)で 終了する
