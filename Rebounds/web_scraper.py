from selenium import webdriver
import pandas as pd
import re

def prospect_stats(start_season, end_season = '2018-19'):

    driver = webdriver.Firefox(executable_path='/Users/ianho/QMIND/QMIND-67s-Project/Rebounds/geckodriver')

    # creates a list of all the seasons wanted for scraping
    start_year = int(start_season[0] + start_season[1] + start_season[2] + start_season[3])
    end_year = int(end_season[0] + end_season[1] + end_season[2] + end_season[3])
    seasons = []
    for x in range(start_year, end_year + 1):
        year_plus_one = (x + 1) % 100
        season = str(x) + '-' + str(year_plus_one)
        seasons.append(season)

    df = {}
    dataframes = {}
    i = 0 # to count number of seasons
    for season in seasons:
        df_dict = {}
        cols = []

        # load website
        url = "http://prospect-stats.com/OHL/" + season + "/skaters/"# + strength
        driver.get(url)
        
        # get all the column headers (Name, G, A, P, etc.) and dictionary
        col_elements = driver.find_elements_by_css_selector(
            ".dataTables_scrollHeadInner > table:nth-child(1) > thead:nth-child(1) > tr th")
        for col in col_elements:
            col = col.get_attribute("aria-label")
            if (col != '#'):
                col = re.match('^.*(?=(:))', col).group()
                cols.append(col)
        df_dict['cols'] = cols
        print(df_dict)
        
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
        
        # remove column headers from data
        columns = df_dict.pop('cols')
        # create dataframe
        dataframes[seasons[i]] = pd.DataFrame.from_dict(df_dict, orient = 'index', columns = columns)
        i+=1
        
    driver.quit()

    return dataframes

dataframe = prospect_stats('2018-2019')
print(dataframe)