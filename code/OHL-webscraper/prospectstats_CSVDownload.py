"""
prospect-stats_CSVDownload.py

Downloads .csv files from prospect-stats.com and saves files with new name.

Created by Ian Ho on 2019-02-17.
Copyright © 2019 Ian Ho. All rights reserved.
"""

from selenium import webdriver
import os
import glob
import re
import time
import pandas as pd

def downloadCSV(driver, league='OHL', season='2018-19', player_type='skaters', play_type=''):
    """
    Downloads stats by clicking csv button.
    :param driver: The web-driver used to web scrape.
    :param league: 'OHL', 'AHL', 'QMJHL', 'USHL', or 'WHL'
    :param season: '2018-19', '2017-18', '2016-17', ... (earliest year depends on league)
    :param player_type: 'skaters', 'teams', 'goalies', 'forwards', or defense'
    :param play_type: ' ', '5v5', '5v4', '5v3', '4v5', '4v4', '4v3', '3v5', '3v4', or '3v3'
    :return: Name of downloaded file.
    """
    print(getFileName(league, season, season, player_type, play_type) + '...')
    url = "http://prospect-stats.com/" + league + '/' + season + '/' + player_type + '/' + play_type
    driver.get(url)
    elem = driver.find_element_by_css_selector("#table_1_wrapper > div.dt-buttons > button.dt-button.buttons-csv.buttons-html5")
    elem.click()
    time.sleep(1)

    new_name = getFileName(league, season, season, player_type, play_type)
    renameLatestDownload(new_name)
    cleanCSV(new_name, player_type)
    return new_name

def downloadSingleCSV(league='OHL', season='2018-19', player_type='skaters', play_type=' '):
    """
    Download a particular league's stats for one season, player type and play type.
    :param league: 'OHL', 'AHL', 'QMJHL', 'USHL', or 'WHL'
    :param season: '2018-19', '2017-18', '2016-17', ... (earliest year depends on league)
    :param player_type: 'skaters', 'teams', 'goalies', 'forwards', or defense'
    :param play_type: ' ', '5v5', '5v4', '5v3', '4v5', '4v4', '4v3', '3v5', '3v4', or '3v3'
    :return: Name of downloaded file in list.
    """
    driver = getWebDriver()
    print('Getting data for: ')
    new_name = downloadCSV(driver, league, season, player_type, play_type)
    driver.quit()
    print("Done")
    return [new_name]

def downloadMultipleCSV(leagues=['OHL'], start_year='2015-16', end_year='2018-19', player_types=['skaters'], play_types=[' ']):
    """
    Downloads every combination of league, player type and play type for consecutive years.
    :param league: 'OHL', 'AHL', 'QMJHL', 'USHL', or 'WHL'
    :param start_year: The first year to be downloaded.
    :param end_year: The last year to be downloaded.
    :param player_type: 'skaters', 'teams', 'goalies', 'forwards', or defense'
    :param play_type: ' ', '5v5', '5v4', '5v3', '4v5', '4v4', '4v3', '3v5', '3v4', or '3v3':param leagues:
    :return: List of all files downloaded.
    """
    file_names = []
    seasons = getSeasons(start_year, end_year)
    driver = getWebDriver()
    print('Getting data for: ')
    for league in leagues:
        for season in seasons:
            for player_type in player_types:
                for play_type in play_types:
                    name = downloadCSV(driver, league, season, player_type, play_type)
                    file_names.append(name)
    driver.quit()
    print("Done")
    return file_names

def renameLatestDownload(new_name):
    """
    Renames downloaded .csv file to more descriptive name.
    :param new_name: New name.
    :return: void
    """
    dirpath = os.getcwd()
    path = dirpath + "/data/"
    list_of_files = glob.glob(path + '*.csv')
    latest_file = max(list_of_files, key=os.path.getctime)
    for filename in list_of_files:
        if filename == latest_file:
            os.rename(filename, os.path.join(path, new_name))
    return

def getWebDriver():
    """
    Returns the ChromeDriver element used to get data.
    :return: ChromeDriver element used to get data.
    """
    dirpath = os.getcwd()
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': 'data'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=dirpath + '/chromedriver')
    return driver

def getFileName(league='OHL', start_year='2018-19', end_year='2018-19', player_type='skaters', play_types=[' ']):
    """
    Returns name of file for particular combination of league, season, player type, and play type.
    :param league: 'OHL', 'AHL', 'QMJHL', 'USHL', or 'WHL'
    :param season: '2018-19', '2017-18', '2016-17', ... (earliest year depends on league)
    :param player_type: 'skaters', 'teams', 'goalies', 'forwards', or defense'
    :param play_types: ' ', '5v5', '5v4', '5v3', '4v5', '4v4', '4v3', '3v5', '3v4', or '3v3'
    :return: name of file for particular combination of league, season, player type, and play type.
    """
    if end_year == start_year:
        name = league + '_' + start_year + '_' + player_type
    else:
        name = league + '_' + start_year + '_to_' + end_year + '_' + player_type
    for play_type in play_types:
        if play_type != ' ':
            name += '_' + play_type
    return name + '.csv'

def getSeasons(start_season, end_season):
    """
    Returns list of all seasons from start season to end season included.
    :param start_season: First season in list.
    :param end_season: Last season in list.
    :return: list of all seasons from start season to end season included.
    """
    start_year = int(start_season[0:4])
    end_year = int(end_season[0:4])
    seasons = []
    for x in range(start_year, end_year + 1):
        next_year = str((x + 1) % 100)
        if len(next_year) == 1:
            next_year = '0' + next_year
        season = str(x) + '-' + str(next_year)
        seasons.append(season)
    return seasons

def cleanData(df, player_type):
    """
    Cleans dataframe (checks for None values and rounds floats) and sorts it appropriately.
    :param df: Dataframe.
    :param player_type: Type of player in data.
    :return: void
    """
    for col in df:
        if col == 'Name':
            break
        else:
            df = df.drop(columns=col)
    offset = 0
    for index, row in df.iterrows():
        for column in df:
            if len(row) != df.shape[1] or not isLegal(df, row[column], column, index):
                df = df.drop(df.index[index - offset])
                offset += 1
    sort = getSortType(player_type)
    df = df.sort_values(sort, ascending=False)
    df = df.reset_index(drop=True)
    return df

def cleanCSV(file_name, player_type):
    """
    Cleans up csv (checks for None values and rounds floats) and sorts it appropriately.
    :param file_name: Name of file to clean.
    :param player_type: Type of player in data.
    :return: void
    """
    df = pd.read_csv('data/' + file_name)
    df = cleanData(df, player_type)
    df.to_csv('data/' + file_name)
    return

def typeFromString(stat):
    """
    Returns type of value if converted from a String.
    :param stat: Statistic being checked.
    :return: type as String.
    """
    if re.match('^[\d,\-]+$', str(stat)) is not None:
        return 'int'
    elif re.match('^[\d,.,\-]+$', str(stat)) is not None:
        return 'float'
    # if re.match('(?!^[\d,.,\-]+$)^.+$', string) is not None
    return 'str'

def castToType(stat, column):
    """
    Converts statistic to correct type.
    :param stat: Statistic being converted.
    :param column: Column statistic is under.
    :return: Converted stat.
    """
    if typeOfColumn(column) == 'int':
        return int(stat)
    elif typeOfColumn(column) == 'float':
        return float(stat)
    return str(stat)

def typeOfColumn(col):
    """
    Returns the general type that each value in a column should have.
    :param col: The column.
    :return: 'int', 'float' or 'str.
    """
    int_list = ['GP', 'G', 'A1', 'A2', 'P1', 'P', 'Sh', 'HD G', 'HD Sh', 'MD G', 'MD Sh', 'LD G', 'LD Sh', 'FOW', 'FOT',
                'ROW', 'GF', 'GA', 'GD', 'SF', 'SA', 'SD', 'HD GF', 'HD GA', 'HD GD', 'HD SF', 'HD SA', 'HD SD',
                'MD GF', 'MD GA', 'MD GD', 'MD SF', 'MD SA', 'MD SD', 'LD GF', 'LD GA', 'LD GD', 'LD SF', 'LD SA',
                'LD SD', 'Appearances']
    float_list = ['Age', 'Sh%', 'G/GP', 'A1/GP', 'A2/GP', 'P1/GP', 'P/GP', 'Sh/GP', 'xG', 'xG/GP', 'HD Sh%', 'MD Sh%',
                  'LD Sh%', 'FOW%', 'GF%', 'SF%', 'Sv%', 'PDO', 'xGF%', 'xGF', 'xGA', 'xGD', 'xSh%', 'xSv%', 'xPDO',
                  'GFAX', 'GFAX/30', 'GSAX', 'GSAX/30', 'HD GF%', 'HD SF%', 'HD Sh%', 'HD Sv%', 'MD GF%', 'MD SF%',
                  'MD Sh%', 'MD Sv%', 'LD GF%', 'LD SF%', 'LD Sh%', 'LD Sv%']
    if col in int_list:
        return 'int'
    elif col in float_list:
        return 'float'
    return 'str'

def isLegal(df, stat, column, index):
    """
    Checks if the stat has a legal value for the column it is in.
    :param df: Dataframe.
    :param stat: Stat being checked.
    :param column: Column containing stat.
    :param index: Index of stat used for getting location.
    :return: True if legal value, False is not legal value.
    """
    df.loc[index, column] = castToType(stat)
    if typeOfColumn(column) == 'str':
        if typeFromString(stat) != 'str':
            df.loc[index, column] = str(stat)
        elif re.match('[\w,\d]+', stat) is None:
            return False

    elif typeOfColumn(column) == 'float':
        if typeFromString(stat) == 'str':
            return False
        elif typeFromString(stat) == 'int':
            df.loc[index, column] = float(stat)
        df.loc[index, column] = round(df.loc[index, column], 3)

    elif typeOfColumn(column) == 'int':
        if typeFromString(stat) == 'str':
            return False
        elif typeFromString(stat) == 'float':
            df.loc[index, column] = int(round(stat))

    if column == 'Age':
        if stat < 10 or stat > 60:
            return False
    return True

def getSortType(player_type):
    """
    Returns the column to sort by based on which type of player the stats are about.
    :param player_type: 'skaters', 'goalies', 'teams', 'forwards', or 'defense'
    :return: column name
    """
    if player_type == 'teams':
        return 'ROW'
    elif player_type == 'goalies':
        return 'Sv%'
    return 'P'
