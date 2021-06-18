'''
# 例
x,y,z = ''
list, list2 = 'リスト'

# カタカナ英語を挿入する
_アペンドする = '追加する|アペンドする'
_エクステンドする = '追加する|エクステンドする'

# 動詞で終わらせる
list.append(x) # listにxをアペンドする
list.extend(list2) # listの最後尾にlist2をエクステンドする

list.myfind(x) # listからx(要素)を探す -> int(位置)

'''

import pandas as pd
import numpy as np

df, df2, df3 = '表データ|データフレーム'
s ,s2 = '配列データ|シリーズ'
X,x,Y,y,Z,z = ''

_リネイムする = '名前を変更する|リネイムする'
_セットする = '設定する|セットする'
_リセットする = '振り直す|リセットする'
_トランスポーズする = '転置する|トランスポーズする'
_コンバージョンする = '変換する|コンバージョンする'
_リファレンス  = '参照する|リファレンスする'
_エクストラクションとする = '抽出する|エクストラクションする'
_ゲットする = '取得する|ゲットする'
_コピーする = '複製する|コピーする'

df.rename(columns={'X': 'x'}) # dfの[列名|カラム]Xを[列名|カラム]xにリネイムする
df.rename(index={'Y': 'y'}) # dfの[行名|インデックス]Xを[行名|インデックス]xにリネイムする
df = df.reset_index(drop=True) # dfの行名を[0始まりの連番|0から始まる番号|0始まり|連番]にリセットする
df = df.set_index('x') # dfの行xを[行名|インデックス]にセットする
df = df.T # dfをトランスポーズする
df.values.tolist() # dfの[値|バリュー]をリストにコンバージョンする -> list

s.ix['x'] # sのxの値をリファレンスする -> int(値)
s.ix[x] # sのx番目の値をリファレンスする -> int(値)
df.ix['x', 'y'] # dfの[行名|インデックス]xと[列名|カラム]yの値をリファレンスする -> int(値)
df.ix[x, y] # dfのx行目のy列目の値をリファレンスする -> int(値)
df.at["x","y"] # dfの[行名|インデックス]xと[列名|カラム]yの値をエクストラクションする -> int(値)
df.iat(x,y) # dfのx行目のy列目の値をエクストラクションする -> int(値)

np.sqrt(df) # dfの全ての値を平方根にコンバージョンする -> DataFrame
np.abs(df) # dfの全ての値を絶対値にコンバージョンする -> DataFrame

df.max() # dfの各列の最大値をゲットする -> Series
np.amax(df) # dfの各列の最大値をゲットする -> Series
df.max(axis=1) # dfの各行の最大値をゲットする -> Series
np.amax(df, axis=1) # dfの各行の最大値をゲットする -> Series
df.mean() # dfの各列の平均値をゲットする -> Series
np.mean(df) # dfの各列の平均値をゲットする -> Series
df.mean(axis=1) # dfの各行の平均値をゲットする -> Series
np.mean(df, axis=1) # dfの各行の平均値をゲットする -> Series
df.min() # dfの各列の最小値をゲットする -> Series
np.amix(df) # dfの各列の最小値をゲットする -> Series
df.min(axis=1) # dfの各行の最小値をゲットする -> Series
np.amin(df, axis=1) # dfの各行の最小値をゲットする -> Series

df.describe() # dfの各列の要約統計量をゲットする -> DataFrame
df.count() # dfの[要素|データ|値]の数をカウントする -> Series
df.nunique() # dfの[一意|ユニーク]な[要素|データ|値]の数をカウントする -> Series
df.std() # dfの各列の最頻値をゲットする -> Series
df.median() # dfの各列の中央値をゲットする -> Series

df.copy() # dfをコピーする -> DataFrame

df.to_dict() # dfを辞書にコンバージョンする -> dict


