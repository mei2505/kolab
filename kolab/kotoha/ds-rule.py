"""
synonym 置き換える 置換する
synonym 用いる 使う する
synonym 取り除く 除去する
synonym 表示する 出力する
synonym セパレータ 区切り記号 区切り文字列
synonym 作成する 生成する
synonym インデックス インデックス名 行の名前 行名 index
synonym カラム カラム名 列の名前 列名 column

"""

pd.read_csv(file) # file(CSVファイル)から [データを|] 読む -> データフレーム
# pd.read_excel("foo.xlsx", "Sheet1", index_col=None, na_values=["NA"]) # xxxx
pd.Series(array) # array(一次元配列)から　[Siries型|シリーズ型]を　作成する -> シリーズ
pd.DataFrame(array) # array(配列)から　[Dataframe型|データフレーム型]を　作成する -> データフレーム

df = 'データフレーム'  # symbol
col = '列'  # symbol

df.head() # dfの [上|初めの|先頭の|先頭|最初の] 5行
df.tail() # dfの [下|後ろの|末尾の|末尾|最後の] 5行
df.head(x) # dfの [上|初めの|先頭の|先頭|最初の] x行
df.tail(x) # dfの [下|後ろの|末尾の|末尾|最後の] x行
df.drop_duplicates() # dfから 重複した行を 削除する -> データフレーム
df.describe() # dfの [要約統計量|統計情報]
df.set_index(col) # dfの colを インデックスとする -> データフレーム
df.sort_index() # dfの インデックスで [並び替える|ソートする] -> データフレーム
df.sort_values(col) # dfの colを参照して [並び替える|ソートする] -> データフレーム
df.isnull().sum() # dfに含まれる欠損値の個数を 列ごとに [算出する|カウントする] -> データフレーム
# df.to_numpy()
# df.copy()
# df.mean()
# df.to_csv(file)
# df.to_excel(file, sheet_name="Sheet1")

df.dtypes # dfの データ型
df.shape # dfの [行数と列数|行数および列数|形状]
df.index # dfの インデックス
df.columns # dfの カラム
df.T # dfの [転置行列|トランスポーズ|行と列の入れ替え]
df.transpose() # dfの [転置行列|トランスポーズ|行と列の入れ替え]

index = index_name # index_name(一次元配列)を インデックスとして
columns = columns_name # columns_name(一次元配列)を カラムとして
by = col # colで
ascending = True # 昇順に
ascending = False # 降順に
inplace = True # 新たに
inplace = False # 置き換えずに
# axis = 0
# axis = 1

