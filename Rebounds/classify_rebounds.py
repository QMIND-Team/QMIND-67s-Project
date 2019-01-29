import pandas as pd

def classifyRebounds(df):
    # add new column for rebound type
    df['Rebound Type'] = 0

    for index in range(0, df.shape[0]-1):
        # 0 if not rebound, 1, 2, 3 if one-second, two-second, three-second rebounds
        if df.loc[(index + 1), ('Time')] - df.loc[(index), ('Time')] <= 1:
            df.loc[(index + 1), ('Rebound Type')] = 1
        elif df.loc[(index + 1), ('Time')] - df.loc[(index), ('Time')] <= 2:
            df.loc[(index + 1), ('Rebound Type')] = 2
        elif df.loc[(index + 1), ('Time')] - df.loc[(index), ('Time')] <= 3:
            df.loc[(index + 1), ('Rebound Type')] = 3
    return df

df = pd.DataFrame({'Time': [1, 5, 10, 26, 46, 47, 50, 51, 51]})
print(df)
df = classifyRebounds(df)
print(df)
print(df.loc[df['Rebound Type'] == 1])
