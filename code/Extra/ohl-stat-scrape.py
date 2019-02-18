#Function to scrape the ohl website for individual team's player stats.

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import pandas as pd


def ohl_player_stats_by_team(team_name, end_season, range_seasons = 3, playoffs = False, regular_season = True):
    """Function to scrape the OHL website for individual team player stats.

    Args:
        team_name (str): OHL team name (capitalize first letter).
        end_season (int): The latest year you want statistics pulled from.
        range_seasons (int): The number of prior seasons including the end_season.
        (incomplete) playoffs (bool): Indicate whether you want playoffs statistics.
        regular_season (bool): Indicate whether you want regular season statistics.

    Returns:
        dict: dict containing dataframes of each requested year.

    """

    #load ohl website
    driver = webdriver.Firefox(executable_path='/Users/Adam/PycharmProjects/clustering-webscraping/geckodriver')
    driver.get("http://ontariohockeyleague.com/stats/team_players/63/7")
    seasons = driver.find_elements_by_css_selector(".full-scores__dropdown--season-select > label > select > option")
    season_values = []
    years = []
    dataframes = {}
    #search through seasons for the desired corresponding values
    for season in seasons:
        if regular_season:
            if 'Regular Season' in season.text:
                year = re.search('(\d{4})\-', season.text).group(1)
                if (end_season - range_seasons) < int(year) <= end_season:
                    season_values.append(season.get_attribute('value'))
                    years.append(int(year))
                    if len(season_values) == range_seasons:
                        break

    teams = driver.find_elements_by_css_selector('.full-scores__dropdown > label > select > option')

    for team in teams:
        if team_name in team.text: #could add regex to improve this
            team_value = team.get_attribute('value')

    #Create dataframes
    df = {}
    i = 0
    for season in season_values:
        df_dict = {}
        cols = []
        driver.get("http://ontariohockeyleague.com/stats/team_players/" + str(season) + '/' + str(team_value))
        col_elements = driver.find_elements_by_css_selector('#normal-header > tr > th')
        for col in col_elements:
            cols.append(col.text)

        df_dict['cols'] = cols

        rows = driver.find_elements_by_css_selector('.stats-data-table > tbody > tr')
        j = 0
        for row in rows:
            row_elements = row.find_elements_by_css_selector('td')
            row_df = []
            for feature in row_elements:
                row_df.append(feature.text)

            df_dict[j] = row_df

            j += 1

        columns = df_dict.pop('cols')
        dataframes[years[i]] = pd.DataFrame.from_dict(df_dict, orient='index', columns=columns)
        i += 1

    driver.quit()

    return dataframes


frame = ohl_player_stats_by_team('Colts', 2017)

for key in frame:
    print(frame.get(key).head())
