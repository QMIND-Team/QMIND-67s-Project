import pandas as pd

dataframe = pd.DataFrame([[1,2,3],[4,5,6],[7,8,9]])
print(dataframe)


def dftocsv(df):
    df.to_csv('csvdata.csv')

dftocsv(dataframe)