from selenium import webdriver
import pandas as pd
import numpy
import re

def merge_frames(dict):
    """Function to merge multiple dataframes into a single one.

        Args:
            dict (dictionary): Contains the dataframes returned from the different seasons/strengths.

        Returns:
            new_df: Dataframe containing the summed data of all the years requested from prospect_stats().

    """
    new_df = pd.DataFrame()
    temp = {}
    #sort_by_name()
    seasons = []
    i = 0
    for season in dict:
        seasons.append(season)
        cols = []
        for column in dict[season]:
            if i == 0:
                cols.append(column)
        for index, row in dict[season].iterrows():
            player = []
            for stat in row:
                player.append(stat)
            if i == 0:
                temp[index] = player
            else:
                for column in dict[season]:
                    if isinstance(new_df.loc[(index), (column)], numpy.int64):
                        new_df.loc[(index), (column)] += row[column]
                    elif isinstance(new_df.loc[(index), (column)], numpy.double):
                        new_df.loc[(index), (column)] += row[column]
                        if i == len(dict)-1:
                            new_df.loc[(index), (column)] /= i + 1
        if i == 0:
            new_df = pd.DataFrame.from_dict(temp, orient='index', columns=cols)
        i += 1

    return new_df

def sort_by_name(df):
    """





    """

    return


def prospect_stats(start_season, end_season = '2018-19', strength=[' ']):
    """Function to scrape prospect stats website for individual players stats.

        Args:
            start_season (int): The first season you want statistics pulled from.
            end_season (int): The last year you want statistics pulled from. Default is '2018-2019'.
            strength (string): 5v5, 5v4, 5v3, 4v5, 4v4, 4v3, 3v5, 3v4, 3v3 or All (Default).

        Returns:
            dataframe: dict containing dataframes of each requested year.

        """
    driver = webdriver.Firefox(executable_path='/Users/ianho/QMIND/QMIND-67s-Project/Rebounds/geckodriver')

    # creates a list of all the seasons wanted for scraping
    start_year = int(start_season[0:4])
    end_year = int(end_season[0:4])
    seasons = []
    for x in range(start_year, end_year + 1):
        next_year = (x + 1) % 100
        season = str(x) + '-' + str(next_year)
        seasons.append(season)


    dataframe = {}
    for season in seasons:
        for type in strength:
            df_dict = {}
            cols = []

            # load website
            url = "http://prospect-stats.com/OHL/" + season + "/skaters/" + type
            driver.get(url)
            if type == ' ':
                print('Scraping data for season: ' + season + '...')
            else:
                print('Scraping data for season: ' + season + '_' + type + '...')
        
            # get all the column headers (Name, G, A, P, etc.) and dictionary
            col_elements = driver.find_elements_by_css_selector(
                ".dataTables_scrollHeadInner > table:nth-child(1) > thead:nth-child(1) > tr th")
            for col in col_elements:
                col = col.get_attribute("aria-label")
                if (col != '#'):
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
                if j > 10:
                    break
            # remove column headers from data
            columns = df_dict.pop('cols')
            # create dataframe
            if type == ' ':
                dataframe[season] = pd.DataFrame.from_dict(df_dict, orient='index', columns=columns)
            else:
                dataframe[season + '_' + type] = pd.DataFrame.from_dict(df_dict, orient='index', columns=columns)
        
    driver.quit()

    return dataframe

dataframe = prospect_stats('2017-2018', strength=['5v5', '3v3'])
print(dataframe)
"""
d1 = pd.DataFrame({'Pos': ['C', 'RW', 'LW', 'D'], '#': ['1', '2', '3', '4'], 'Inactive': [' ', ' ', ' ', ' '], 'Rookie': [' ', ' ', ' ', '*'], 'Name': ['Ian', 'Willem', 'Andrew', 'Hayden'], 'Team': ['OTT', 'OTT', 'OTT', 'OTT'], 'GP': [50.0, 51.0, 52.0, 53.0], 'G': [25, 57, 36, 84], 'A': [99, 68, 54, 25]})
d2 = pd.DataFrame({'Pos': ['C', 'RW', 'LW', 'D'], '#': ['1', '2', '3', '4'], 'Inactive': [' ', ' ', ' ', ' '], 'Rookie': [' ', ' ', ' ', '*'], 'Name': ['Ian', 'Willem', 'Andrew', 'Hayden'], 'Team': ['OTT', 'OTT', 'OTT', 'OTT'], 'GP': [73.0, 46.0, 50.0, 46.0], 'G': [25, 43, 87, 55], 'A': [35, 46, 25, 46]})
data = {'2017-18': d1, '2018-19': d2}
dfs = []
"""
data = merge_frames(dataframe)
print(data)
