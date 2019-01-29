import pandas as pd

def rr_zone(shot):
    MIDDLE_LINE = 50
    TOP_OF_CIRCLE = 40
    # zone 1 is left side while looking at net
    # zone 2 is right side while looking at net
    # zone 3 is above top of circle
    if shot['Y-Coordinate'] < TOP_OF_CIRCLE:
        if shot['X-Coordinate'] < MIDDLE_LINE:
            return 1
        else:
            return 2
    else:
        return 3

def royal_road(df):
    # add new column for crossing royal road
    df['Royal Road'] = 0

    # 1 if rebound crossed, 0 if it did not cross
    for index in range(0, df.shape[0]-1):
        if rr_zone(df.loc[(index + 1)]) != rr_zone(df.loc[(index)]):
            if df.loc[(index + 1), ('Rebound Type')] >= 1:
                df.loc[(index + 1), ('Royal Road')] = 1
    return df

def rebound_type(df):
    # add new column for rebound type
    df['Rebound Type'] = 0

    # 0 if not rebound, 1, 2, 3 if one-second, two-second, three-second rebounds
    for index in range(0, df.shape[0]-1):
        if df.loc[(index + 1), ('Time')] - df.loc[(index), ('Time')] <= 1:
            df.loc[(index + 1), ('Rebound Type')] = 1
        elif df.loc[(index + 1), ('Time')] - df.loc[(index), ('Time')] <= 2:
            df.loc[(index + 1), ('Rebound Type')] = 2
        elif df.loc[(index + 1), ('Time')] - df.loc[(index), ('Time')] <= 3:
            df.loc[(index + 1), ('Rebound Type')] = 3
    return df

df = pd.DataFrame({'Time': [5, 8, 10, 11], 'X-Coordinate': [45, 32, 56, 50], 'Y-Coordinate': [30, 20, 25, 45]})
print(df)
df = rebound_type(df)
print(df)
df = royal_road(df)
print(df)
