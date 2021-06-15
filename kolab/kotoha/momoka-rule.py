
"""
synonym 置き換える 置換する
synonym 用いる とする
synonym 取り除く 除去する
synonym 表示する 出力する
synonym 区切り 区切り記号 区切り文字列 セパレータ
"""

pd = __package__ # module

file = 'ファイル名' # symbol

pd.read_csv(file)  # read data frame from file(CSV file) -> data frame

df = '表データ|データフレーム'  # symbol
col = '列|属性|カラム' #symbol
col2 = '列|属性|カラム' #symbol
row = '行|インデックス' #symbol

df[col]  # dfの col -> 表データ
df[[col, col2]]  # dfから colと col2のみ 選ぶ -> 表データ
df.columns  # dfの カラム名リスト

df.drop([col], axis=1) # df から colを 取り除く -> 表データ
df.drop([row], axis=0) # df から rowを 取り除く -> 表データ
df.drop([row]) # df から rowを 取り除く -> 表データ

inplace = True # 操作は インプレイスで行う
