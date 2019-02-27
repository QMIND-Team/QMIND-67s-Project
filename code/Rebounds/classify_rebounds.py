import pandas as pd
import math
import matplotlib.pyplot as plt

def rr_zone(shot):
    """This function determines where the shot is on the ice relative to the royal road line.

        Args:
            shot (row in dataframe): The shot you want to evaluate.

        Returns:
            1, 2, or 3 depending on which zone it is in.

    Zone 1: Left side while looking at net, below the top of the circle.
    Zone 2: Right side while looking at net, below the top of the circle.
    Zone 3: Above the top of the circle.

    """
    MIDDLE_LINE = 50
    TOP_OF_CIRCLE = 24.2

    if shot['y'] < TOP_OF_CIRCLE:
        if shot['x'] < MIDDLE_LINE:
            return 1
        else:
            return 2
    else:
        return 3

def royal_road(df):
    """This function adds a column in the data frame depicting whether or not the rebound crossed the royal road.

        Args:
            df (data frame): The set of shots you want to evaluate.

        Returns:
            df (data frame): The updated data set with a 1 or 0 if the rebound crossed the royal road or not.

    """
    # add new column for crossing royal road
    df['royal_road'] = 0

    # 1 if rebound crossed, 0 if it did not cross
    for index in range(0, df.shape[0]-1):
        if rr_zone(df.loc[(index + 1)]) != rr_zone(df.loc[(index)]):
            if df.loc[(index + 1), ('reb')] == 1:
                df.loc[(index + 1), ('royal_road')] = 1
    return df

def rebound_type(df):
    """This function adds 4 new columns in the data frame depicting what kind of rebound each shot is.

        Args:
            df (data frame): The set of shots you want to evaluate.

        Returns:
            df (data frame): The updated data set with a 1 or 0 in each of the four columns.

    The four columns are 'reb', 'reb1', 'reb2', 'reb3'.
    'reb': whether or not the shot was off a rebound.
    'reb1': whether or not the rebound was 1 second after the prev shot.
    'reb2': whether or not the rebound was 2 second after the prev shot.
    'reb3': whether or not the rebound was 3 second after the prev shot.

    """
    # add new columns for rebound type
    df['reb'] = 0
    df['reb1'] = 0
    df['reb2'] = 0
    df['reb3'] = 0

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
    """This function adds columns for the polar coordinates of the shot with respect to the net.

        Args:
            df (data frame): The set of shots you want to evaluate

        Returns:
            df (data frame): The updated data set with the distance, angle and which side of the net the shot was taken
            from.

    e.x. 'deg' = 10 means the shot was taken 10 degrees right of the centre line.
         'deg' = -45 means the shot was taken 45 degrees left of the centre line.
         'deg' = 95 means the shot was taken 95 degrees right of the centre line (behind the net).

    """
    # 0 degrees is in the centre of the ice
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

"""
This is an example dataset used to test each function

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

"""
