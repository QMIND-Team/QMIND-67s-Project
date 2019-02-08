import pandas as pd
import math
import matplotlib.pyplot as plt

def rr_zone(shot):
    '''this function is used for determining if the shot crossed the royal road by return what zone it is in'''
    MIDDLE_LINE = 50
    TOP_OF_CIRCLE = 24.2
    # zone 1 is left side while looking at net
    # zone 2 is right side while looking at net
    # zone 3 is above top of circle
    if shot['y'] < TOP_OF_CIRCLE:
        if shot['x'] < MIDDLE_LINE:
            return 1
        else:
            return 2
    else:
        return 3

def royal_road(df):
    '''this function adds a new column to whether or not the rebound crossed the royal road'''
    # add new column for crossing royal road
    df['royal_road'] = 0

    # 1 if rebound crossed, 0 if it did not cross
    for index in range(0, df.shape[0]-1):
        if rr_zone(df.loc[(index + 1)]) != rr_zone(df.loc[(index)]):
            if df.loc[(index + 1), ('reb')] == 1:
                df.loc[(index + 1), ('royal_road')] = 1
    return df

def rebound_type(df):
    '''this function returns the dataframe with 4 new columns:
    'reb' is for whether or not the shot was off a rebound
    'reb1' is for whether or not the rebound was 1 second after the prev shot
    'reb2' is for whether or not the rebound was 2 second after the prev shot
    'reb3' is for whether or not the rebound was 3 second after the prev shot
    '''
    # add new columns for rebound type
    df['reb'] = 0
    df['reb1'] = 0
    df['reb2'] = 0
    df['reb3'] = 0

    # 0 if not rebound, 1, 2, 3 if one-second, two-second, three-second rebounds
    for index in range(0, df.shape[0]-1):
        if df.loc[(index + 1), ('time')] - df.loc[(index), ('time')] <= 3:
            df.loc[(index + 1), ('reb')] = 1
            if df.loc[(index + 1), ('time')] - df.loc[(index), ('time')] <= 2:
                if df.loc[(index + 1), ('time')] - df.loc[(index), ('time')] <= 1:
                    df.loc[(index + 1), ('reb1')] = 1
                else:
                    df.loc[(index + 1), ('reb2')] = 1
            else:
                df.loc[(index + 1), ('reb3')] = 1
    return df

def polar_coords(df, ):
    '''this function adds the polar coordinates of the shot with respect to the net
    0 degrees is in the centre of the ice'''
    NET_X = 50
    NET_Y = 6.7 # goal line
    df['dist'] = 0
    df['deg'] = 0 # ex 10 = 10 degress right of centre line, -45 = 45 degrees left of centre line, >90 is behind net
    df['side'] = 'R' # side when facing net
    for index in range(0, df.shape[0]):
        df.loc[(index), ('dist')] = math.sqrt((df.loc[(index), ('x')] - NET_X) ** 2 + (df.loc[(index), ('y')] - NET_Y) ** 2)
        if df.loc[(index), ('y')] > NET_Y:
            df.loc[(index), ('deg')] = abs(math.degrees(math.atan((df.loc[(index), ('x')] - NET_X) / (df.loc[(index), ('y')] - NET_Y))))
        elif df.loc[(index), ('y')] == NET_Y:
            df.loc[(index), ('deg')] = 90
        else:
            df.loc[(index), ('deg')] = 180 - abs(math.degrees(math.atan((df.loc[(index), ('x')] - NET_X) / (df.loc[(index), ('y')] - NET_Y))))
        if df.loc[(index), ('x')] > NET_X:
            df.loc[(index), ('deg')] *= -1
            df.loc[(index), ('side')] = 'L'
    return df


df = pd.DataFrame({'time': [5, 8, 10, 11, 15, 18, 20], 'x': [50, 25, 75, 0, 100, 0, 100], 'y': [30, 31.7, 31.7, 6.7, 6.7, 5, 5]})
plt.plot(df['x'], df['y'])
print(df)
print("\n\n")
df = polar_coords(df)
print(df)
print("\n\n")
df = rebound_type(df)
print(df)
print("\n\n")
df = royal_road(df)
print(df)

