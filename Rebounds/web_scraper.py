from selenium import webdriver
import pandas as pd
import re

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
                if j>10:
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

dataframe = prospect_stats('2017-2018')
print(dataframe)
