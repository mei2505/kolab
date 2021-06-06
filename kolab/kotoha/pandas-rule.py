"""
synonym 置き換える 置換する
synonym 用いる 使う する
synonym 取り除く 除去する
synonym 表示する 出力する
synonym 区切り記号 区切り文字列  cpat = self.visit(tree[0])
synonym 作成する 生成する
synonym 選択する 選ぶ 抽出する
synonym 保存する 書き込む
synonym 読む 読み込む
synonym 要素 データ
synonym インデックス インデックス名 行の名前 行名 index
synonym カラム カラム名 列の名前 列名 column
"""

import pandas as pd

df, df2, df3 = '表データ|データフレーム'
col, col2, col3 = '列|属性|カラム'
row, row2, row3 = '行|インデックス'
col_idx = '列番号'  # symbol
col2_idx = '列番号'  # symbol
row_idx = '行番号'  # symbol
row2_idx = '行番号'  # symbol
file = 'ファイル名'  # symbol
array = '配列'  # symbol
exp = '条件式'  # symbol
val_before = '値|バリュー'  # symbol
val_after = '値|バリュー'  # symbol
val_before2 = '値|バリュー'  # symbol
val_after2 = '値|バリュー'  # symbol

pd.read_csv(file)  # fileから [表データを|csvファイルを] 読む -> df
pd.read_excel(file)  # fileから [表データを|excelファイルを] 読む -> df
pd.Series(array)  # arrayから　シリーズ型を　作成する -> シリーズ
pd.DataFrame(array)  # arrayから　データフレーム型を　作成する -> df
pd.options.display.precision  # 小数点以下の桁数
pd.options.display.max_rows  # 最大表示行数
pd.options.display.max_columns  # 最大表示列数
pd.concat([df, df2])  # dfと df2を [連結する|コンカットする]
pd.merge(df, df2)  # dfと df2を [結合する|マージする] -> df

df.head()  # dfの [上|初めの|先頭の|先頭|最初の] 5行 -> df
df.tail()  # dfの [下|後ろの|末尾の|末尾|最後の] 5行 -> df
df.head(x)  # dfの [上|初めの|先頭の|先頭|最初の] x行 -> df
df.tail(x)  # dfの [下|後ろの|末尾の|末尾|最後の] x行 -> df
# df.drop(val)  # dfの valを 削除する -> データフレーム
# df.drop(index=[row, row2])  # dfの rowと row2を 削除する -> データフレーム
# df.drop(columns=[col, col2])  # dfの colと col2を 削除する -> データフレーム
df.drop(index=row)  # dfの rowを 削除する -> データフレーム
df.drop(columns=col)  # dfの colを 削除する -> データフレーム
df.drop_duplicates()  # dfから 重複した行を 削除する -> データフレーム
df.duplicated()  # dfの 重複した行を 確認する
df.describe()  # dfの [要約統計量|統計情報]
df.set_index(col)  # dfの colを インデックスとする -> データフレーム
df.sort_index()  # dfの インデックスで [並び替える|ソートする] -> データフレーム
df.sort_values(col)  # dfの colを参照して [並び替える|ソートする] -> データフレーム
df.isnull().sum()  # dfに含まれる欠損値の個数を 列ごとに [算出する|カウントする] -> データフレーム
df.to_numpy()  # dfの numpy配列
df.groupby(col)  # df内の colの要素を [集約する|グループ化する] -> データフレーム
df.copy()  # dfを コピーする -> データフレーム
df.mean()  # dfの 平均を 算出する
df.merge(df2)  # dfと df2を [結合する|マージする] -> データフレーム
df.to_csv(file)  # fileとして [表データを|csvファイルを] 保存する
df.to_excel(file)  # fileとして [表データを|excelファイルを] 保存する

df.dtypes  # dfの データ型
df.shape  # dfの [行数と列数|行数および列数|形状]
df.size  # dfの [全要素数|サイズ]
df.index  # dfの インデックス
df.values  # dfの [値|バリュー]
df.columns  # dfの カラム
df.T  # dfの [転置行列|行と列の入れ替え|トランスポーズ]
df.transpose()  # dfの [転置行列|行と列の入れ替え|トランスポーズ]
df.query(exp)  # dfから expに当てはまるものを 選択する -> データフレーム
df.astype(d_type)  # dfのデータ型を d_typeとする -> データフレーム
# df.replace({val_before: val_after, val_before2: val_after2})  # df内のval_beforeと val_before2をそれぞれ val_afterと val_after2に 置き換える -> データフレーム
# df.replace([val_before, val_before2], [val_after, val_after2])  # df内のval_beforeと val_before2をそれぞれ val_afterと val_after2に 置き換える -> データフレーム
# df.replace(val_before, val_after)  # df内のval_beforeを val_afterに 置き換える -> データフレーム

# df.loc[[row, row2], [col, col2]]  # dfから rowと row2の colと col2を 選択する -> データフレーム
# df.loc[:, col]  # dfから colを 選択する -> データフレーム
# df.loc[row, :]  # dfから rowを 選択する -> データフレーム
df.loc[row]  # dfから rowを 選択する -> データフレーム
df.col  # dfから colを 選択する -> データフレーム
# df.at[row, col]  # dfから rowの colを 選択する -> データフレーム
# df.iloc[[row_idx, row2_idx], [col_idx, col2_idx]]  # dfからrow_idxと row2_idxの col_idxと col_idx2の要素を 選択する -> データフレーム
df.iloc[row_idx]  # dfから row_idxの要素を 選択する -> データフレーム
# df.iat[row_idx, col_idx]  # dfから row_idxの col_idxの要素を 選択する -> データフレーム
df[[col, col2]]  # dfから colと col2のみ 選択する -> データフレーム
df[col]  # dfから colを 選択する -> データフレーム

index = index_name  # index_name(一次元配列)を インデックスとして
columns = columns_name  # columns_name(一次元配列)を カラムとして
by = col  # colで
ascending = True  # 昇順で
ascending = False  # 降順で
inplace = True  # 新たに
inplace = False  # 置き換えずに
dtype = d_type  # d_typeを データ型として
axis = 0  # 行方向で
axis = 1  # 列方向で
header = row_idx  # ヘッダーを row_idxして
index_col = col_idx  # インデックスを col_idxとして
na_values = symbol  # 欠損値を symbolとして
encoding = encode  # エンコーディングを encode として
sheet_name = sheet  # シート名sheetのデータを
join = 'outer'  # 外部結合で
join = 'inner'  # 内部結合で
on = col  # キーを colとして
how = 'inner'  # 内部結合で
how = 'left'  # 左結合で
how = 'right'  # 右結合で
how = 'outer'  # 外部結合で
