from selenium import webdriver
import pandas as pd
import numpy
import re

def merge_frames(dict, played_all_years=False, sort='Name', ascending=False):
    """Function to merge multiple dataframes into a single one.

        Args:
            dict (dictionary): Contains the dataframes returned from the different seasons/strengths.

        Returns:
            new_df: Dataframe containing the summed data of all the years requested from prospect_stats().

    """
    new_df = pd.DataFrame()
    temp = {}
    seasons = []
    not_all_years = {}
    nay_df = pd.DataFrame() # df for not_all_years
    nay_index = 0
    i = 0
    offset = 0
    """
    Add separate functionalities for Pos, #, Inactive, Rookie, Team.
    e.x. functionality of taking strings from Team column and adding into dataframe as team1/team2/team3.
    """
    for season in dict:
        dict[season] = dict[season].sort_values('Name')
        dict[season] = dict[season].reset_index(drop=True)
        seasons.append(season)
        if i == 0:
            cols = []
            for column in dict[season]:
                cols.append(column)
        for index, row in dict[season].iterrows():
            player = []
            just_added = 0
            for stat in row:
                stat = get_type_from_str(stat)(stat)
                player.append(stat)
            if i == 0:
                temp[index] = player
            else:
                # if player played in one season and not another, names wont line up
                while new_df.loc[index + offset, 'Name'] != row['Name']:
                    if new_df[new_df['Name'] == row['Name']].empty:
                        # new player in dict[season]
                        if played_all_years:
                            if nay_index == 0:
                                not_all_years[nay_index] = player
                                nay_df = pd.DataFrame.from_dict(not_all_years, orient='index', columns=cols)
                            else:
                                nay_df.append(player)
                            nay_df = nay_df.reset_index(drop=True)
                            nay_index += 1
                            dict[season] = dict[season].loc[index].drop
                        else:
                            new_df = new_df.append(pd.DataFrame([player], columns=cols))
                            new_df = new_df.sort_values('Name')
                            new_df = new_df.reset_index(drop=True)
                            just_added = row['Name']
                            break
                    else:
                        #new player in new_df
                        if played_all_years:
                            new_player = []
                            for stat in new_df.loc[index + offset]:
                                new_player.append(stat)
                            if nay_index == 0:
                                not_all_years[nay_index] = new_player
                                nay_df = pd.DataFrame.from_dict(not_all_years, orient='index', columns=cols)
                            else:
                                nay_df.append(new_player)
                            nay_df = nay_df.reset_index(drop=True)
                            nay_index += 1
                            new_df = new_df.loc[index + offset].drop
                        else:
                            offset += 1
                if just_added != row['Name']:
                    combine(new_df, index + offset, row, i, len(dict))
        if i == 0:
            new_df = pd.DataFrame.from_dict(temp, orient='index', columns=cols)
        i += 1
    new_df = new_df.sort_values(sort, ascending=ascending)
    new_df = new_df.reset_index(drop=True)
    return new_df

def combine(df, idx, row, i, length):
    """Function to combine the stats of two seasons or two players.

            Args:
                df (dataframe): The dataframe the row is being added to.
                idx (int): Index of dataframe being added to.
                row (dataframe): The dataframe for 1 player's stats being added to df.
                i (int): The iteration of dataframes being merged.
                length (int) The number of dataframes in the dictionary.

            Returns:
                void

        """
    for column in df:
        type = get_type_from_str(row[column])
        if type == int:
            df.loc[idx, column] += int(row[column])
        elif type == float:
            df.loc[idx, column] += float(row[column])
            if i == length - 1:
                df.loc[idx, column] /= length
        elif type == str:
            if df.loc[idx, column] != row[column]:
                if df.loc[idx, column] != ' ':
                    df.loc[idx, column] += '|' + row[column]
    return

def get_type_from_str(thing):
        if re.match('^\d+$', thing) != None:
            return int
        if re.match('^[\d,.]+$', thing) != None:
            return float
        if re.match('(?!^[\d,.]+$)^.+$', thing) != None:
            return str

def prospect_stats(start_season, end_season='2018-19', strength=[' '], top_ten=0):
    """Function to scrape prospect stats website for individual players stats.

        Args:
            start_season (str): The first season you want statistics pulled from.
            end_season (str): The last year you want statistics pulled from. Default is '2018-2019'.
            strength (str): 5v5, 5v4, 5v3, 4v5, 4v4, 4v3, 3v5, 3v4, 3v3 or All (Default).

        Returns:
            dataframe: dict containing dataframes of each requested year.

    """
    driver = webdriver.Firefox(executable_path='C:/Users/Willem Atack/Documents/Coding/QMIND/67s/code/OHL-webscraper/geckodriver')

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
                if top_ten:
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

dataframe = prospect_stats('2017-2018', top_ten=1)
data = merge_frames(dataframe, sort='P')
print(data)
