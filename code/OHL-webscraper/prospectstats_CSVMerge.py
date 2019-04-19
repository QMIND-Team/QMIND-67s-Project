"""
prospect-stats_CSVMerge.py

Merges .csv files containing player stats from prospect-stats.com downloaded using prospect_stats_csv_merge.py and
saves files with new name.

Created by Ian Ho on 2019-02-17.
Copyright © 2019 Ian Ho. All rights reserved.
"""

import os
import pandas as pd
import re
import prospectstats_CSVDownload as psCSVdl

def merge(csv1, csv2, new_name, all_years=False, sort='P',):
    """
    Combines the stats of multiple files into one with combined stats for all players and saves to new name.
    :param csv1: Name of first file.
    :param csv2: Name of second file.
    :param new_name: Name of new file created.
    :param all_years: If only players that played in all years should be included.
    :param sort: Column to sort by.
    :return: Updated dataframe.
    """
    df1 = pd.read_csv('data/' + csv1)
    df2 = pd.read_csv('data/' + csv2)

    for column in df1:
        if column != 'Name':
            df1 = df1.drop(columns=column)
        else:
            break
    for column in df2:
        if column != 'Name':
            df2 = df2.drop(columns=column)
        else:
            break

    print('Merging: ' + csv1 + ' and ' + csv2 + '...')
    df1['Appearances'] = 1
    df2['Appearances'] = 1
    common_cols = removeUncommonCols(df1, df2)

    for index, row in df2.iterrows():
        if df1[df1['Name'] == row['Name']].empty:
            player = row.tolist()
            if not all_years:
                df1 = df1.append(pd.DataFrame([player], columns=common_cols), ignore_index=True)
        else:
            df1_index = df1[df1['Name'] == row['Name']].index[0]
            combine(df1, df1_index, row)
    offset = 0
    if all_years:
        for index, row in df1.iterrows():
            if row['Appearances'] < 2:
                df1 = df1.drop(df1.index[index - offset])
                offset += 1
    df1 = df1.sort_values(sort, ascending=False)
    df1 = df1.reset_index(drop=True)
    for index, row in df1.iterrows():
        for column in df1:
            if psCSVdl.typeOfColumn(column) == 'float':
                df1.loc[index, column] /= row['Appearances']
                df1.loc[index, column] = round(df1.loc[index, column], 3)
    df1 = df1.drop(columns='Appearances')
    df1.to_csv('data/' + new_name)
    return new_name

def mergeSeasonRange(league='OHL', start_year='2015-16', end_year='2018-19', player_type='skaters', play_types=[''], all_years=False):
    """
    Merges the stats of multiple files together into one and saves under new name.
    :param league: League.
    :param start_year: First year being merged.
    :param end_year: Last year being merged.
    :param player_type: 'skaters', 'teams', 'goalies', 'forwards', or 'defense'.
    :param play_types: '', '5v5', '5v4', '5v3', '4v5', '4v4', '4v3', '3v5', '3v4', or '3v3'
    :param all_years: If only players that played in all years should be included.
    :return: name of new file created.
    """
    seasons = psCSVdl.getSeasons(start_year, end_year)
    sort = psCSVdl.getSortType(player_type)
    new_name = psCSVdl.getFileName(league, start_year, end_year, player_type, play_types)
    csv_names = []
    for season in seasons:
        for play_type in play_types:
            csv_names.append(psCSVdl.getFileName(league, season, season, player_type, play_type))
    for file_name in csv_names[1:]:
        merge(csv_names[0], file_name, new_name, all_years, sort)
    print('Created: ' + new_name)
    return new_name

def mergeAllSeasonCombinations(league='OHL', start_season='2017-18', end_season='2018-19', player_type='skaters', play_types=[''], all_years=False):
    """
    Merges the stats of multiple files together for separate files for every combination of consecutive years.
    :param league: League.
    :param start_season: First year being merged.
    :param end_season: Last year being merged.
    :param player_type: 'skaters', 'teams', 'goalies', 'forwards', or 'defense'.
    :param play_types: '', '5v5', '5v4', '5v3', '4v5', '4v4', '4v3', '3v5', '3v4', or '3v3'
    :param all_years: If only players that played in all years should be included.
    :return: list of all file names created
    """
    seasons = psCSVdl.getSeasons(start_season, end_season)
    file_names = []
    for start_year in seasons[:-1]:
        start_idx = seasons.index(start_year)
        for end_year in seasons[start_idx + 1:]:
            end_idx = seasons.index(end_year)
            if end_idx - start_idx == 1:
                file_names.append(mergeSeasonRange(league, start_year, end_year, player_type, play_types, all_years))
            else:
                csv = psCSVdl.getFileName(league, end_year, end_year, player_type, play_types)
                print(csv)
                new_name = psCSVdl.getFileName(league, start_year, end_year, player_type, play_types)
                merge(file_names[-1], csv, new_name, all_years, psCSVdl.getSortType(player_type))
                print('Created: ' + new_name)
                file_names.append(new_name)
    return file_names

def getCommonCols(df1, df2):
    """
    Returns which columns are common between two dataframes.
    :param df1: First dataframe.
    :param df2: Second dataframe.
    :return: list of common columns.
    """
    cols1 = []
    common_cols = []
    for column in df1:
        cols1.append(column)
    for column in df2:
        if cols1.count(column) > 0:
            common_cols.append(column)
    return common_cols

def removeUncommonCols(df1, df2):
    """
    Removes columns from two dataframes that are not common between the two.
    :param df1: First dataframe.
    :param df2: Second dataframe.
    :return: void
    """
    common_cols = getCommonCols(df1, df2)
    for column in df1:
        if common_cols.count(column) == 0:
            df1 = df1.drop(columns=column)
    for column in df2:
        if common_cols.count(column) == 0:
            df2 = df2.drop(columns=column)
    return common_cols

def combine(df, idx, row):
    """
    Combines row with the correct row in the merged dataframe.
    :param df: Dataframe.
    :param idx: Index to be combined in dataframe.
    :param row: Row being combined with dataframe.
    :return: void
    """
    for column in df:
        row[column] = psCSVdl.castToType(row[column], column)
        if psCSVdl.typeOfColumn(column) == 'str':
            new_strings = re.findall('[^\/]+', row[column])
            for string in new_strings:
                original_strings = re.findall('[^\/]+', df.loc[idx, column])
                if original_strings.count(string) == 0:
                    if df.loc[idx, column] == '':
                        df.loc[idx, column] = string
                    else:
                        df.loc[idx, column] += '/' + string
        else:
            df.loc[idx, column] += row[column]
    return

def renameCSV(old_name, new_name):
    """
    Renames a csv file.
    :param old_name: Old file name.
    :param new_name: New file name.
    :return: void
    """
    dirpath = os.getcwd()
    path = dirpath + "/data/"
    os.rename(old_name, os.path.join(path, new_name))
    return

def copyCSV(original, new_name):
    """
    Creates a copy of the csv to a new file name.
    :param original: original file name.
    :param new_name: new file name.
    :return: void
    """
    df = pd.read_csv('data/' + original)
    df.to_csv('data/' + new_name)
    return
