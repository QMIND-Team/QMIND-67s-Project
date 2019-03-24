from selenium import webdriver
import glob
import os
import time
import pandas as pd
import re
from shutil import copy2


"""
    These functions are used to download multiple stats from prospect-stats.com and merge the stats into one 
    data frame.  Run the functions, get_stats_range(), get_stats_all_combos() or download_multiple() to test.
"""

def update(leagues=['OHL', 'AHL', 'QMJHL', 'USHL', 'WHL'], players=['skaters', 'teams', 'goalies', 'defense', 'forwards'],
           strength=[' '], already_downloaded=True):
    """Function to download 2018-19 stats from prospect stats website and update all files.

            Args:
                leagues (List of str): The leagues you want statistics from.
                start_season (str): The first season you want statistics from.
                end_season (str): The last year you want statistics pulled from. Default is '2018-19'.
                players str: Skaters (All players), forwards, defense, goalies or teams.
                strength (List of str): 5v5, 5v4, 5v3, 4v5, 4v4, 4v3, 3v5, 3v4, 3v3 or ' ' (All).
                min_years (int): The number of years a player has to play to be included.
                already_downloaded (boolean): If data is already downloaded.

            Returns:
                void
        """
    if not already_downloaded:
        download_multiple(leagues=leagues, players=players, strength=strength)

    for league in leagues:
        for player_type in players:
            if player_type == 'teams':
                sort = 'ROW'
            elif player_type == 'goalies':
                sort = 'Sv%'
            else:
                sort = 'P'
            for play_type in strength:
                if league == 'OHL':
                    start_year = '1997-98'
                elif league == 'AHL':
                    start_year = '2005-06'
                elif league == 'QMJHL':
                    start_year = '1998-99'
                elif league == 'USHL':
                    start_year = '2002-03'
                elif league == 'WHL':
                    start_year = '1996-97'
                seasons = get_seasons(start_season=start_year, end_season='2016-17')
                if play_type != ' ':
                    for season in seasons:
                        merge(csvs=[league + '_' + season + '_to_2017-18_' + player_type + '_' + play_type + '.csv',
                                    league + '_2018-19_' + player_type + '_' + play_type + '.csv'],
                              filename=league + '_' + season + '_to_2018-19_' + player_type + '_' + play_type + '.csv',
                              all_strings=False, sort=sort)
                else:
                    for season in seasons:
                        merge(csvs=[league + '_' + season + '_to_2017-18_' + player_type + '.csv',
                                    league + '_2018-19_' + player_type + '.csv'],
                              filename=league + '_' + season + '_to_2018-19_' + player_type + '.csv',
                              all_strings=False, sort=sort)

def get_stats(leagues=['OHL'], start_season='2017-18', end_season='2018-19', players='skaters', strength=[' '],
                      min_years=1, already_downloaded=True):
    """Function to download stats from prospect stats website for individual players stats by clicking csv button and
    then merge them together.

        Args:
            leagues (List of str): The leagues you want statistics from.
            start_season (str): The first season you want statistics from.
            end_season (str): The last year you want statistics pulled from. Default is '2018-19'.
            players str: Skaters (All players), forwards, defense, goalies or teams.
            strength (List of str): 5v5, 5v4, 5v3, 4v5, 4v4, 4v3, 3v5, 3v4, 3v3 or ' ' (All).
            min_years (int): The number of years a player has to play to be included.
            already_downloaded (boolean): If data is already downloaded.

        Returns:
            void
    """
    # creates a list of all the seasons wanted for scraping
    seasons = get_seasons(start_season=start_season, end_season=end_season)

    if not already_downloaded:
        csvs = download_multiple(leagues=leagues, seasons=seasons, players=[players], strength=strength)
    else:
        csvs = []
        for league in leagues:
            for season in seasons:
                for play_type in strength:
                    if play_type != ' ':
                        csvs.append(league + '_' + season + '_' + players + '_' + play_type + '.csv')
                    else:
                        csvs.append(league + '_' + season + '_' + players + '.csv')

    filename = get_filename(leagues=leagues, start_season=start_season, end_season=end_season, players=players,
                            strength=strength)


    if players == 'teams':
        sort = 'ROW'
    elif players == 'goalies':
        sort = 'Sv%'
    else:
        sort = 'P'

    merge(csvs=csvs, filename=filename, all_strings=False, min_years=min_years, one_league=len(leagues) > 1, sort=sort)
    return

def download_all_year_combos(leagues=['OHL'], start_season='2017-18', end_season='2018-19', players=['skaters'],
                   already_downloaded=True):
    """Function to download stats from prospect stats website for individual players stats by clicking csv button and
        then merge all possible combinations.

        Args:
            leagues (List of str): The leagues you want statistics from.
            start_season (str): The first season you want statistics from.
            end_season (str): The last year you want statistics pulled from. Default is '2018-19'.
            players (List of str): Skaters (All players), forwards, defense, goalies or teams.
            already_downloaded (boolean): If data is already downloaded.

        Returns:
            void
    """
    seasons = get_seasons(start_season=start_season, end_season=end_season)

    if not already_downloaded:
        download_multiple(leagues=leagues, seasons=seasons, players=players)
    for league in leagues:
        for play in players:
            if play == 'teams':
                sort = 'ROW'
            elif play == 'goalies':
                sort = 'Sv%'
            else:
                sort = 'P'
            csvs = []
            for season in seasons:
                csvs.append(league + '_' + season + '_' + play + '.csv')
            for start_year in seasons[:-1]:
                start_idx = seasons.index(start_year)
                filename = ''
                for end_year in seasons[start_idx + 1:]:
                    end_idx = seasons.index(end_year)
                    if end_idx > start_idx + 1:
                        last_merge = filename
                        filename = league + '_' + start_year + '_to_' + end_year + '_' + play + '.csv'
                        merge(csvs=[last_merge, csvs[end_idx]], filename=filename, sort=sort, one_league=True)
                    else:
                        filename = league + '_' + start_year + '_to_' + end_year + '_' + play + '.csv'
                        merge(csvs=csvs[start_idx:end_idx + 1], filename=filename, sort=sort, one_league=True)
    return

def get_cluster_data(years=['2015-16', '2016-17', '2017-18'], already_downloaded=True):
    if not already_downloaded:
        download_multiple(leagues=['OHL'], seasons=['2015-16', '2016-17', '2017-18'], players=['skaters'], strength=[' '])

    dirpath = os.getcwd()
    path = dirpath + "/data/"
    csvs = []
    for year in years:
        filename = 'OHL_' + year + '_skaters.csv'
        csvs.append(filename)
        copy2(path + filename, dirpath + "/cluster_data")

    for year in years:
        df = pd.read_csv(dirpath + "/cluster_data/" + 'OHL_' + year + '_skaters.csv')
        for col in df:
            if col == 'Name':
                break
            else:
                df = df.drop(columns=col)
        df = df.sort_values('P', ascending=False)
        df = df.reset_index(drop=True)
        drop_index = []
        for index, row in df.iterrows():
            if row['Age'] < 16 or row['Age'] >= 17:
                drop_index.append(index)
        offset = 0
        for index in drop_index:
            df = df.drop(df.index[index - offset])
            offset += 1
        df = df.sort_values('P', ascending=False)
        df = df.reset_index(drop=True)

        df.to_csv('cluster_data/' + 'OHL_' + year + '_skaters.csv')

    merge(csvs=csvs, filename='OHL_cluster16_' + years[0] + '_to_' + years[len(years) - 1] + '.csv',
          all_strings = False, min_years = 1, sort = 'P', one_league = True)
    return


def download_multiple(leagues=['OHL'], seasons=['2018-19'], players=['skaters'], strength=[' ']):
    """Function to download stats from prospect stats website for individual players stats by clicking csv button.

        Args:
            leagues (List of str): The leagues you want statistics from.
            seasons (List of str): The seasons you want statistics from.
            players (List of str): Skaters (All players), forwards, defense, goalies or teams.
            strength (List of str): 5v5, 5v4, 5v3, 4v5, 4v4, 4v3, 3v5, 3v4, 3v3 or ' ' (All).

        Returns:
            void
    """
    dirpath = os.getcwd()
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': 'data'}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path=dirpath + '/chromedriver')

    csvs = []
    print('Downloading: ')
    for league in leagues:
        for season in seasons:
            for player_type in players:
                for play_type in strength:
                    download_csv(driver, league, season, player_type, play_type, csvs)
    driver.quit()
    print("Done")
    return csvs

def download_csv(driver, league='OHL', season='2018-19', players='skaters', play_type='', csvs):
    """Function to download a particular season's stats from prospect stats website by clicking csv button.

        Args:
            driver (WebDriver.Chrome): The web-driver used to web scrape.
            league (str): The league you want statistics from.
            season (str): The year you want statistics from.
            players (str): All players, forwards, defense, goalies or teams.
            play_type (str): 5v5, 5v4, 5v3, 4v5, 4v4, 4v3, 3v5, 3v4, 3v3 or All.
            csvs (List of str): The list of file names.

        Returns:
            void
     """
    if play_type == ' ':
        print(league + '_' + season + '_' + players + '...')
    else:
        print(league + '_' + season + '_' + players + '_' + play_type + '...')

    url = "http://prospect-stats.com/" + league + '/' + season + '/' + players + '/' + play_type
    driver.get(url)
    elem = driver.find_element_by_css_selector(
        "#table_1_wrapper > div.dt-buttons > button.dt-button.buttons-csv.buttons-html5")
    elem.click()
    time.sleep(1)

    if play_type == ' ':
        new_name = league + '_' + season + '_' + players + '.csv'
    else:
        new_name = league + '_' + season + '_' + players + '_' + play_type + '.csv'
    rename_csv(new_name)
    edit_csv(new_name, players)
    csvs.append(new_name)
    return

def get_stats_scrape(leagues=['OHL'], start_season='2018-19', end_season='2018-19', players='skaters', strength=[' '],
                      top_ten=True, min_years=1, already_scraped=True):
    """Function to scrape prospect stats website for individual players stats.

        Args:
            leagues (List of str): The leagues you want statistics from.
            start_season (str): The first season you want statistics from.
            end_season (str): The last year you want statistics pulled from. Default is '2018-19'.
            players (List of str): Skaters (All players), forwards, defense, goalies or teams.
            strength (List of str): 5v5, 5v4, 5v3, 4v5, 4v4, 4v3, 3v5, 3v4, 3v3 or ' ' (All).
            top_ten (boolean): True if only want the top ten players.
            min_years (int): Minimum years a player must play.

        Returns:
            void
    """
    # creates a list of all the seasons wanted for scraping
    seasons = get_seasons(start_season=start_season, end_season=end_season)

    if not already_scraped:
        csvs = scrape_multiple(leagues=leagues, seasons=seasons, players=[players], strength=strength, top_ten=top_ten)
    else:
        csvs = []
        for league in leagues:
            for season in seasons:
                for play_type in strength:
                    name = league + '_' + season + '_' + players
                    if play_type != ' ':
                        name += '_' + play_type
                    if top_ten:
                        name += '_top-ten'
                    csvs.append(name + '.csv')

    filename = get_filename(leagues=leagues, start_season=start_season, end_season=end_season, players=players,
                            strength=strength)

    if players == 'teams':
        sort = 'ROW'
    elif players == 'goalies':
        sort = 'Sv%'
    else:
        sort = 'P'

    merge(csvs=csvs, filename=filename, all_strings=True, min_years=min_years, one_league=len(leagues) == 1, sort=sort)
    return

def scrape_multiple(leagues=['OHL'], seasons=['2018-19'], players=['skaters'], strength=[' '], top_ten=True):
    """Function to scrape stats from prospect stats website for individual players stats.

        Args:
            leagues (List of str): The leagues you want statistics from.
            seasons (List of str): The seasons you want statistics from.
            players (List of str): Skaters (All players), forwards, defense, goalies or teams.
            strength (List of str): 5v5, 5v4, 5v3, 4v5, 4v4, 4v3, 3v5, 3v4, 3v3 or ' ' (All).
            top_ten (boolean): If only scrape top ten players.

        Returns:
            void
    """
    dirpath = os.getcwd()
    driver = webdriver.Firefox(executable_path=dirpath + '/geckodriver')

    csvs = []
    df = {}
    print('Scraping: ')
    for league in leagues:
        for season in seasons:
            for player_type in players:
                for play_type in strength:
                    df_dict = {}
                    cols = []
                    name = league + '_' + season + '_' + player_type
                    if play_type != ' ':
                        name += '_' + play_type
                    if top_ten:
                        name += '_top-ten'
                    print(name + '...')
                    csvs.append(name + '.csv')
                    # load website
                    url = "http://prospect-stats.com/" + league + '/' + season + '/' + player_type + '/' + play_type
                    driver.get(url)

                    # get all the column headers (Name, G, A, P, etc.) and dictionary
                    col_elements = driver.find_elements_by_css_selector(
                        ".dataTables_scrollHeadInner > table:nth-child(1) > thead:nth-child(1) > tr th")
                    for col in col_elements:
                        col = col.get_attribute("aria-label")
                        if col != '#':
                            col = re.match('^.*(?=(:))', col).group()
                            cols.append(col)
                    df_dict['cols'] = cols
                    j = 0  # to count number of rows
                    # get all data within rows and add to dictionary
                    rows = driver.find_elements_by_css_selector("#table_1 > tbody:nth-child(2) tr")
                    for row in rows:
                        if top_ten:
                            if j >= 10:
                                break
                        row_elements = row.find_elements_by_css_selector('td')
                        row_df = []
                        for feature in row_elements:
                            row_df.append(feature.text)
                        df_dict[j] = row_df
                        j += 1

                    # remove column headers from data
                    columns = df_dict.pop('cols')
                    # create data frame
                    df[name] = pd.DataFrame.from_dict(df_dict, orient='index', columns=columns)
                    df[name].to_csv('data/' + name + '.csv')
                    edit_csv(name + '.csv', player_type)

    driver.quit()
    return csvs

def merge(csvs, filename, all_strings=False, min_years=1, sort='P', one_league=True):
    """Function to merge multiple data frames into a single one.

        Args:
            csvs (List): Contains the names of the csv files being merged.
            filename (str): The filename for the new file being created.
            all_strings (boolean): True if all values are strings.
            min_years (int): The number of years a player has to play to be included.
            sort (str): The column to sort the data by.

        Returns:
            new_df: (pandas.DataFrame) Contains the summed data of all the years requested from prospect_stats().
    """
    dict = csvs_to_dict(csvs)
    for df in dict:
        for col in dict[df]:
            if col == 'Name':
                break
            else:
                dict[df] = dict[df].drop(columns=col)
        if not one_league:
            columns = dict[df].columns.tolist()
            print(columns)
            league = re.match('^[^_]+', df).group(0)
            dict[df]['League'] = league
            columns = columns[0:2] + ['League'] + columns[2:]
            print(columns)
            dict[df] = dict[df][columns]
        dict[df] = dict[df].sort_values(sort, ascending=False)
        dict[df] = dict[df].reset_index(drop=True)
    common_cols = get_common_cols(dict)
    remove_uncommon_cols(dict, common_cols)

    new_df = pd.DataFrame()
    temp = {}
    seasons = []
    i = 0
    print('Merging: ')
    for season in dict:
        print(season + '...')
        dict[season] = dict[season].reset_index(drop=True)
        dict[season]['Appearances'] = 1
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
                        new_df = new_df.append(pd.DataFrame([player], columns=cols), ignore_index=True)
                else:
                    new_df_index = new_df[new_df['Name'] == row['Name']].index[0]
                    combine(new_df, new_df_index, row, all_strings=all_strings)
        if i == 0:
            new_df = pd.DataFrame.from_dict(temp, orient='index', columns=cols)
        i += 1
    index_to_drop = []
    for index, row in new_df.iterrows():
        if row['Appearances'] < min_years:
            index_to_drop += index
        else:
            for column in new_df:
                if type_from_str(row[column]) == 'float':
                    new_df.loc[index, column] /= row['Appearances']
                    new_df.loc[index, column] = round(new_df.loc[index, column], 3)
    for index in index_to_drop:
        new_df = new_df[index].drop
    new_df = new_df.drop(columns='Appearances')
    new_df = new_df.sort_values(sort, ascending=False)
    new_df = new_df.reset_index(drop=True)
    new_df.to_csv('cluster_data/' + filename)
    print("Created: " + filename)
    return

def combine(df, idx, row, all_strings=False):
    """Function to combine the stats of two seasons for a player.

        Args:
            df (pandas.DataFrame): The data frame that the row is being added to.
            idx (int): Index of the data frame being added to.
            row (pandas.DataFrame): The data for 1 player's stats being added to df.
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
        else:
            df_matches = re.findall('[^\/]+', df.loc[idx, column])
            row_matches = re.findall('[^\/]+', row[column])
            for match in row_matches:
                if df_matches.count(match) == 0:
                    if df.loc[idx, column] != ' ':
                        df.loc[idx, column] += '/' + match
    return

def sort_file(filename, sort, ascending=False):

    """Function to sort a downloaded csv file.

        Args:
            filename (str): The name the file to be sorted.
            sort (str): How the file should be sorted.
            ascending (boolean): If file should be sorted in ascending order.

        Returns:
            void
    """
    file = 'data/' + filename
    df = pd.read_csv(file)
    df = df.sort_values(sort, ascending=ascending)
    df.to_csv('data/' + filename)
    return

def rename_csv(new_name):
    """Function to rename downloaded csv file.

        Args:
            new_name (str): The name the file is going to be named.

        Returns:
            void
    """
    dirpath = os.getcwd()
    path = dirpath + "/data/"
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
        df = pd.read_csv('cluster_data/' + file)
        dict_df[re.match('^[^.]+', file).group(0)] = df
    return dict_df

def edit_csv(csv, players):
    """Function to edit .csv file after downloading.

        Args:
            csv (str): The file name.

        Returns:
            void
    """
    if players == 'teams':
        sort = 'ROW'
    elif players == 'goalies':
        sort = 'Sv%'
    else:
        sort = 'P'
    df = pd.read_csv('data/' + csv)
    for col in df:
        if col == 'Name':
            break
        else:
            df = df.drop(columns=col)
    for index, row in df.iterrows():
        for column in df:
            if type_from_str(row[column]) == 'float':
                df.loc[index, column] = round(df.loc[index, column], 3)
    df = df.sort_values(sort, ascending=False)
    df = df.reset_index(drop=True)
    df.to_csv('data/' + csv)
    return

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
    """Function to convert stat to int, float or string.

        Args:
            stat (str): The stat being converted.

        Returns:
            Casted stat.
     """
    if type_from_str(stat) == 'int':
        return int(stat)
    elif type_from_str(stat) == 'float':
        return float(stat)
    else:
        return str(stat)

def get_seasons(start_season, end_season):
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

def get_filename(leagues, start_season, end_season, players, strength):
    filename = ''
    for league in leagues:
        filename += league + '_'
    filename += start_season
    if start_season != end_season:
        filename += '_to_' + end_season
    filename += '_' + players
    if strength != [' ']:
        for play_type in strength:
            filename += '_' + play_type
    filename += '.csv'
    return filename

download_multiple(leagues=['OHL'], seasons=['2018-19'])
#get_cluster_data()
#download_all_year_combos(leagues=['WHL'], start_season='1996-97', players=['skaters', 'teams'], already_downloaded=True)
