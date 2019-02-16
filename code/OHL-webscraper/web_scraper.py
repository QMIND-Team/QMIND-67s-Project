from selenium import webdriver
import glob
import os
import time
import pandas as pd
import re

"""
    These functions are used to scrape or download multiple stats from prospect-stats.com and 
    merge the stats into one dataframe.  Run the function get_stats_csv() to use these functions.
"""

def merge_dict_frames(dict, played_all_years=False, sort='P', ascending=False, all_strings=False):
    """Function to merge multiple data frames into a single one.

        Args:
            dict (dictionary): Contains the data frames returned from the different seasons/strengths.
            played_all_years (boolean): True if only want players that have played in all the years.
            sort (str): The column header to sort the data by.
            ascending (boolean): True if want data to be sorted in ascending order.
            all_strings (boolean): True if all values are strings.

        Returns:
            new_df: (pandas.DataFrame) Contains the summed data of all the years requested from prospect_stats().
    """
    new_df = pd.DataFrame()
    temp = {}
    seasons = []
    i = 0
    common_cols = get_common_cols(dict)
    remove_uncommon_cols(dict, common_cols)
    for season in dict:
        dict[season] = dict[season].reset_index(drop=True)
        seasons.append(season)

        # get column names
        if i == 0:
            cols = []
            for column in dict[season]:
                cols.append(column)
        for index, row in dict[season].iterrows():
            player = []
            for stat in row:
                if all_strings:
                    stat = convert_to_type(stat)
                player.append(stat)
            if i == 0:
                temp[index] = player
            else:
                if new_df[new_df['Name'] == row['Name']].empty:
                    if not played_all_years:
                        new_df = new_df.append(pd.DataFrame([player], columns=cols), ignore_index=True)
                else:
                    new_df_index = new_df[new_df['Name'] == row['Name']].index[0]
                    if not played_all_years:
                        combine(new_df, new_df_index, row, i, len(dict), all_strings=all_strings)
                    else:
                        new_df = new_df[new_df_index].drop
        if i == 0:
            new_df = pd.DataFrame.from_dict(temp, orient='index', columns=cols)
        i += 1
    new_df = new_df.sort_values(sort, ascending=ascending)
    new_df = new_df.reset_index(drop=True)
    return new_df

def get_common_cols(dict_dfs):
    """Function to find the common columns of multiple data frames in a Dictionary.

            Args:
                dict_dfs (Dictionary): Dictionary of multiple data frames.

            Returns:
                col_all_dfs (Series): Contains all the common columns of the data frames.
    """
    cols = []
    col_all_dfs = []
    i = 0
    num_dfs = len(dict_dfs)
    for df in dict_dfs:
        for column in dict_dfs[df]:
            cols.append(column)
            if i == num_dfs - 1:
                if cols.count(column) == num_dfs:
                    col_all_dfs.append(column)
        i += 1
    return col_all_dfs

def remove_uncommon_cols(dict_dfs, common_cols):
    """Function to remove uncommon columns of multiple data frames in a Dictionary.

        Args:
            dict_dfs (Dictionary): Dictionary of multiple data frames.
            common_cols (Series): Contains all the common columns of the data frames.

        Returns:
            void
    """
    for df in dict_dfs:
        for column in dict_dfs[df]:
            if common_cols.count(column) == 0:
                dict_dfs[df] = dict_dfs[df].drop(columns=column)
    return

def combine(df, idx, row, i, length, all_strings=False):
    """Function to combine the stats of two seasons for a player.

        Args:
            df (pandas.DataFrame): The data frame that the row is being added to.
            idx (int): Index of the data frame being added to.
            row (pandas.DataFrame): The data for 1 player's stats being added to df.
            i (int): The iteration of data frames being merged.
            length (int) The number of data frames in the dictionary.
            all_strings (boolean): True if all values are strings.

        Returns:
            void
    """
    for column in df:
        if all_strings:
            row[column] = convert_to_type(row[column])
        if type_from_str(row[column]) == 'int':
            df.loc[idx, column] += row[column]
        elif type_from_str(row[column]) == 'float':
            df.loc[idx, column] += row[column]
            if i == length - 1:
                df.loc[idx, column] /= length
                df.loc[idx, column] = round(df.loc[idx, column], 3)
        else:
            if df.loc[idx, column] != row[column]:
                if df.loc[idx, column] != ' ':
                    df.loc[idx, column] += '/' + row[column]
    return

def type_from_str(stat):
    """Function to determine the type of a stat.

        Args:
            stat (str): The stat being checked.

        Returns:
            (str): Type of string.
    """
    if re.match('^[\d,\-]+$', str(stat)) is not None:
        return 'int'
    elif re.match('^[\d,.,\-]+$', str(stat)) is not None:
        return 'float'
    else:
        # if re.match('(?!^[\d,.,\-]+$)^.+$', string) is not None
        return 'str'

def convert_to_type(stat):
    if type_from_str(stat) == 'int':
        return int(stat)
    elif type_from_str(stat) == 'float':
        return float(stat)
    else:
        return str(stat)

def get_stats_scrape(start_season, end_season='2018-19', strength=[' '], top_ten=False, played_all_years=False,
                     sort='P', ascending=False):
    """Function to scrape prospect stats website for individual players stats.

        Args:
            start_season (str): The first season you want statistics pulled from.
            end_season (str): The last year you want statistics pulled from. Default is '2018-2019'.
            strength (Series): 5v5, 5v4, 5v3, 4v5, 4v4, 4v3, 3v5, 3v4, 3v3 or ' ' (All).
            top_ten (boolean): True if only want the top ten players.
            played_all_years (boolean): True if only want players that have played in all the years.
            sort (str): The column header to sort the data by.
            ascending (boolean): True if want data to be sorted in ascending order.

        Returns:
            void
    """
    driver = webdriver.Firefox(executable_path='/Users/ianho/QMIND/QMIND-67s-Project/code/OHL-webscraper/geckodriver')

    # creates a list of all the seasons wanted for scraping
    start_year = int(start_season[0:4])
    end_year = int(end_season[0:4])
    seasons = []
    for x in range(start_year, end_year + 1):
        next_year = (x + 1) % 100
        season = str(x) + '-' + str(next_year)
        seasons.append(season)
    filename = start_season
    if start_season != end_season:
        filename += '_to_' + end_season
        if strength != [' ']:
            for play in strength:
                filename += '_' + play
    filename += '.csv'

    df = {}
    print('Scraping data for season: ')
    for season in seasons:
        for play_type in strength:
            df_dict = {}
            cols = []

            # load website
            url = "http://prospect-stats.com/OHL/" + season + "/skaters/" + play_type
            driver.get(url)
            if type == ' ':
                print(season + '...')
            else:
                print(season + '_' + play_type + '...')
        
            # get all the column headers (Name, G, A, P, etc.) and dictionary
            col_elements = driver.find_elements_by_css_selector(
                ".dataTables_scrollHeadInner > table:nth-child(1) > thead:nth-child(1) > tr th")
            for col in col_elements:
                col = col.get_attribute("aria-label")
                if col != '#':
                    col = re.match('^.*(?=(:))', col).group()
                    cols.append(col)
            df_dict['cols'] = cols
            j = 0 # to count number of rows
            # get all data within rows and add to dictionary
            rows = driver.find_elements_by_css_selector("#table_1 > tbody:nth-child(2) tr")
            for row in rows:
                row_elements = row.find_elements_by_css_selector('td')
                row_df = []
                for feature in row_elements:
                    row_df.append(feature.text)
                df_dict[j] = row_df
                j += 1
                if top_ten:
                    if j > 10:
                        break
            # remove column headers from data
            columns = df_dict.pop('cols')
            # create data frame
            if play_type == ' ':
                df[season] = pd.DataFrame.from_dict(df_dict, orient='index', columns=columns)
            else:
                df[season + '_' + play_type] = pd.DataFrame.from_dict(df_dict, orient='index', columns=columns)
        
    driver.quit()
    data = merge_dict_frames(df, all_strings=True, played_all_years=played_all_years, sort=sort, ascending=ascending)
    data.to_csv('data/' + filename)
    print("Done")
    return

def get_stats_csv(start_season, end_season='2018-19', strength=[' '], played_all_years=False,
                     sort='P', ascending=False):
    """Function to scrape prospect stats website for individual players stats by clicking csv button.

        Args:
            start_season (str): The first season you want statistics pulled from.
            end_season (str): The last year you want statistics pulled from. Default is '2018-19'.
            strength (str): 5v5, 5v4, 5v3, 4v5, 4v4, 4v3, 3v5, 3v4, 3v3 or ' ' (All).

        Returns:
            void
    """
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': 'data'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path='/Users/ianho/QMIND/QMIND-67s-Project/code/OHL-webscraper/chromedriver')

    # creates a list of all the seasons wanted for scraping
    start_year = int(start_season[0:4])
    end_year = int(end_season[0:4])
    seasons = []
    for x in range(start_year, end_year + 1):
        next_year = (x + 1) % 100
        season = str(x) + '-' + str(next_year)
        seasons.append(season)

    filename = start_season
    if start_season != end_season:
        filename += '_to_' + end_season
        if strength != [' ']:
            for play_type in strength:
                filename += '_' + play_type
    filename += '.csv'

    csvs = []
    print('Getting data for season: ')
    for season in seasons:
        for play_type in strength:
            download_csv(driver, season, csvs, play_type)
    driver.quit()
    dict_dfs = csvs_to_dict(csvs)
    for df in dict_dfs:
        dict_dfs[df] = dict_dfs[df].drop(columns='#')
    data = merge_dict_frames(dict_dfs, all_strings=False, played_all_years=played_all_years, sort=sort,
                             ascending=ascending)
    data.to_csv('data/' + filename)
    print("Done")
    return

def download_csv(driver, season, csvs, play_type=' '):
    """Function to download a particular season's stats from prospect stats website by clicking csv button.

        Args:
            driver (WebDriver.Chrome): The web-driver used to web scrape.
            season (str): The year you want statistics pulled from.
            csvs (Series): The list of file names.
            play_type (str): 5v5, 5v4, 5v3, 4v5, 4v4, 4v3, 3v5, 3v4, 3v3 or ' ' (Default).

        Returns:
            void
     """
    if play_type == ' ':
        print(season + '...')
    else:
        print(season + '_' + play_type + '...')

    url = "http://prospect-stats.com/OHL/" + season + "/skaters/" + play_type
    driver.get(url)
    elem = driver.find_element_by_css_selector(
        "#table_1_wrapper > div.dt-buttons > button.dt-button.buttons-csv.buttons-html5")
    elem.click()
    time.sleep(1)

    if play_type != ' ':
        new_name = season + '_' + play_type + '.csv'
    else:
        new_name = season + '.csv'
    rename_csv(new_name)
    csvs.append(new_name)
    return

def rename_csv(new_name):
    """Function to rename downloaded csv file.

        Args:
            new_name (str): The name the file is going to be named.

        Returns:
            void
    """
    path = "/Users/ianho/QMIND/QMIND-67s-Project/code/OHL-webscraper/data/"
    list_of_files = glob.glob(path + '*.csv')
    latest_file = max(list_of_files, key=os.path.getctime)
    for filename in list_of_files:
        if filename == latest_file:
            os.rename(filename, os.path.join(path, new_name))
    return

def csvs_to_dict(csvs):
    """Function to convert multiple csvs into one dictionary of data frames.

        Args:
            csvs (Series): The list of file names.

        Returns:
            dict_df (Dictionary): Contains all the data frames.
    """

    dict_df = {}
    for file in csvs:
        df = pd.read_csv('data/' + file)
        dict_df[re.match('^[^.]+', file).group(0)] = df
    return dict_df

#get_stats_csv('2016-17', end_season='2018-19', strength=[' '])