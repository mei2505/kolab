df.drop(index=['001', '002'])
df.drop(columns=['birth', 'year'])
df.loc[['001', '002'], ['birth', 'year']]
df.loc[:, 'Birth']
df.loc['005', :]
df.loc['003']
df.age
df.at['002', 'uid']
df.iloc[[3, 4], [1, 7]]
df.iloc[2]
df.iat[2, 5]
df[['uid', 'point']]
# df['uid']