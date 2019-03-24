import sys
import os
import re
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import scipy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDateTime, Qt, QTimer, pyqtSlot, QModelIndex
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit, QDial,
                             QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                             QLineEdit, QProgressBar, QPushButton, QRadioButton,
                             QScrollBar, QSizePolicy, QSlider, QSpinBox, QStyleFactory,
                             QTableWidget, QTabWidget, QTextEdit, QVBoxLayout, QWidget,
                             QToolBar, QInputDialog, QListWidget, QAbstractItemView,
                             QGraphicsPixmapItem, QMessageBox)
import warnings
warnings.filterwarnings("ignore")


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

def clean_nan(data):
    for index, row in data.iterrows():
        for stat in row:
            if type_from_str(stat) == 'float':
                if math.isnan(convert_to_type(stat)):
                    data.drop(data.index[0], inplace=True)
    data = data.reset_index(drop=True)
    return data

def get_seasons(start_season, end_season):
    """
    Returns a list of all the seasons in a range.
    :param start_season: The first season.
    :param end_season: The last season.
    :return: A list of all the seasons in a range.
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


def select_age(df, age):
    """
    Returns only the data containing players within a certain age range.
    :param df: The data frame containing the data.
    :param age: The age of players wanted.
    :return: The new data frame with only players in a certain age range.
    """
    if age != 0:
        df = df.loc[df['Age'] >= int(age)]
        return df.loc[df['Age'] < int(age) + 1]
    else:
        return df

def select_position(df, positions):
    """
    Returns only the data containing players that play a certain position.
    :param df: The data frame containing the data.
    :param positions: The position wanted.
    :return: The new data frame with only players that play that position.
    """
    if positions == 'Defense':
        return df.loc[df['Pos'] == 'D']
    elif positions == 'Forwards':
        return df.loc[df['Pos'] != 'D']
    else:
        return df

def select_stats(stats, dataset):
    """
    Returns a new data set containing only the wanted stats.
    :param stats: The column names for the wanted stats.
    :param dataset: The original data set.
    :return: The new data set containing only the wanted stats.
    """
    df = dataset.loc[:, stats]
    return df

def divided_by_GP(stats, dataset):
    """
    Returns data set with added columns containing stats/GP.
    :param stats: Stats used to create per game stats.
    :param dataset: Original data set.
    :return: The new data set with new stat columns.
    """
    GP_vector = dataset.loc[:, 'GP']
    dataset.loc[:,stats] = dataset.loc[:, stats].div(GP_vector, axis = 0)
    return dataset

def select_team(team, dataset):
    """
    Returns data set with players only from one team.
    :param team: Name of team.
    :param dataset: Original data set.
    :return: New data set only with players from particular team.
    """
    dataset['temp'] = 0
    length = len(team) + 1
    temp1 = team + '/'
    temp2 = '/' + team
    temp3 = '/' + team + '/'
    N = dataset.shape[0]
    for i in range(0, N):
        dataset_team = dataset.loc[i, 'Team']
        dataset_team1 = dataset_team[0:length]
        dataset_team2 = dataset_team[-length:]
        if temp1 == dataset_team1 or temp2 == dataset_team2:
            dataset.loc[i, 'temp'] = 1
        if dataset.loc[i, 'Team'] == team:
            dataset.loc[i, 'temp'] = 1
        if temp3 in dataset.loc[i, 'Team']:
            dataset.loc[i, 'temp'] = 1
    new_df = dataset[dataset['temp'] == 1]
    new_df = new_df.iloc[:, :-1]
    return new_df

def select_cluster(cluster, dataset):
    """
    Returns new dataset with players from particular cluster.
    :param cluster: Cluster number wanted.
    :param dataset: Original data set.
    :return: New data set with only players from wanted cluster.
    """
    new_df = dataset[dataset['Cluster'] == cluster]
    return new_df

def sort_by_cluster(dataset):
    """
    Sorts players by cluster.
    :param dataset: Unsorted dataset.
    :return: Sorted dataset.
    """
    new_df = dataset.sort_values('Cluster')
    return new_df

def cluster_counter(value, dataset):
    """
    Counts number of players in each cluster.
    :param value: Cluster number.
    :param dataset: Original dataset.
    :return: Number of players in cluster.
    """
    N = dataset.shape[0]
    count = 0
    for i in range (0, N):
        if (dataset.loc[i, 'Cluster'] == value):
            count = count + 1
    return count

def add_team2df(team_name, dataset, new_dataset):
    """
    Adds a team's cluster vector to the new data set which includes information about all teams
    :param team_name: Name of team.
    :param dataset: Original data set.
    :param new_dataset: New data set to get cluster column added.
    :return: New dataset.
    """
    dataset = dataset.reset_index(drop=True)
    team_cluster = []
    for i in range(0, 4):
        count = cluster_counter(i, dataset)
        team_cluster.append(count)
    team_cluster = pd.DataFrame([team_cluster])
    team_cluster = pd.concat([team_name, team_cluster], axis=1)
    new_dataset = new_dataset.append([team_cluster])
    return new_dataset

def find_percentages(dataset):
    """
    Finds percentage of elements in one row of a columns.
    :param dataset: Original data set.
    :return: New data set.
    """
    N = dataset.shape[0]
    new_df = dataset.copy(deep=True)
    for i in range(0, N):
        sum = new_df.iloc[i, 1:].sum()
        new_df.iloc[i, 1:] = 100*new_df.iloc[i, 1:].div(sum)
    return new_df

def cluster(data, stat1, stat2, stat3, stat4):
    """
    Runs k-means clustering algorithm on data to cluster players.
    :param data: Dataset.
    :param stat1: First stat used to cluster.
    :param stat2: Second stat used to cluster.
    :param stat3: Third stat used to cluster.
    :param stat4: Fourth stat used to cluster.
    :return: Results of algorithm with cluster number column added to each player.
    """
    # prepare data
    cols = data.columns.tolist()
    if cols.count('HD G') > 0:
        data = divided_by_GP(['HD G', 'HD Sh', 'MD G', 'MD Sh', 'LD G', 'LD Sh'], data)
    data = data.reset_index(drop=True)
    cluster_data = select_stats([stat1, stat2, stat3, stat4], data)
    name_team = data.loc[:, ['Name', 'Team']]
    cluster_data_with_name = pd.concat([name_team, cluster_data], axis=1)

    #normalize the features
    sc_X = StandardScaler()
    cluster_data = sc_X.fit_transform(cluster_data)

    #run k-means
    kmeans = KMeans(n_clusters=4, init='k-means++', max_iter=300, n_init=10, random_state=0)
    y_kmeans = kmeans.fit_predict(cluster_data)
    y_kmeans = pd.DataFrame(y_kmeans)
    fullresults = pd.concat([cluster_data_with_name, y_kmeans], axis=1)
    fullresults.columns = ['Name', 'Team', stat1, stat2, stat3, stat4, 'Cluster']
    fullresults.to_csv('df_withclusters.csv')

    return fullresults

def prep_data(data, stat1, stat2, stat3, stat4):
    """
    Prepares the data to be used by adding per game stats to data.
    :param data: Original dataset.
    :param stat1: First stat used.
    :param stat2: Second stat used.
    :param stat3: Third stat used.
    :param stat4: Fourth stat used.
    :return: New dataset.
    """
    cols = data.columns.tolist()
    if cols.count('HD G') > 0:
        data = divided_by_GP(['HD G', 'HD Sh', 'MD G', 'MD Sh', 'LD G', 'LD Sh'], data)
    data = data.reset_index(drop=True)
    cluster_data = select_stats([stat1, stat2, stat3, stat4], data)

    # normalize the features
    sc_X = StandardScaler()
    cluster_data = sc_X.fit_transform(cluster_data)

    return cluster_data

def cluster_visualization(data, stat1, stat2, stat3, stat4):
    """
    Creates .png file visualizing the clusters.
    :param data: Data set.
    :param stat1: First stat used to cluster.
    :param stat2: Second stat used to cluster.
    :param stat3: Third stat used to cluster.
    :param stat4: Fourth stat used to cluster.
    :return: void
    """
    cluster_data = prep_data(data, stat1, stat2, stat3, stat4)
    pca = PCA(n_components=2)
    cluster_data_2d = pca.fit_transform(cluster_data)
    cluster_data_2d = pd.DataFrame(cluster_data_2d)
    kmeans = KMeans(n_clusters=4, init='k-means++', max_iter=300, n_init=10, random_state=0)
    y_kmeans = kmeans.fit_predict(cluster_data)
    y_kmeans = pd.DataFrame(y_kmeans)
    cluster_data_2d = pd.concat([cluster_data_2d, y_kmeans], axis=1)
    cluster_data_2d.columns = ['PCA 1', 'PCA 2', 'Cluster']

    cluster0 = select_cluster(0, cluster_data_2d)
    cluster1 = select_cluster(1, cluster_data_2d)
    cluster2 = select_cluster(2, cluster_data_2d)
    cluster3 = select_cluster(3, cluster_data_2d)

    plt.scatter(cluster0.iloc[:, 0], cluster0.iloc[:, 1], s=10, c='red', label='Cluster 0')
    plt.scatter(cluster1.iloc[:, 0], cluster1.iloc[:, 1], s=10, c='green', label='Cluster 1')
    plt.scatter(cluster2.iloc[:, 0], cluster2.iloc[:, 1], s=10, c='blue', label='Cluster 2')
    plt.scatter(cluster3.iloc[:, 0], cluster3.iloc[:, 1], s=10, c='black', label='Cluster 3')
    plt.xlabel('PCA 1')
    plt.ylabel('PCA 2')
    plt.title('Clusters')
    plt.legend()
    file = 'images/Cluster_Visualization.png'
    if os.path.isfile(file):
        os.remove(file)
    plt.savefig(file)
    plt.cla()
    return

def cluster_info(data, stat1, stat2, stat3, stat4):
    """
    Returns normalized average stats for each cluster.
    :param data: Data for clusters.
    :param stat1: First stat used to cluster.
    :param stat2: Second stat used to cluster.
    :param stat3: Third stat used to cluster.
    :param stat4: Fourth stat used to cluster.
    :return: New normalized cluster averages for each stat.
    """
    kmeans = KMeans(n_clusters=4, init='k-means++', max_iter=300, n_init=10, random_state=0)
    cluster_data = prep_data(data, stat1, stat2, stat3, stat4)
    y_kmeans = kmeans.fit_predict(cluster_data)
    centroids = kmeans.cluster_centers_
    centroids = pd.DataFrame(centroids)
    centroids.columns = [stat1, stat2, stat3, stat4]
    average_values = pd.Series(centroids.mean())
    cluster_info = centroids.subtract(average_values, axis=1)
    return cluster_info

def bar_graph(stat1, stat2, stat3, stat4, stats):
    """
    Creates a bargraph showing the data returned from cluster_info() and saves it as a .png.
    :param stat1: First stat used to cluster.
    :param stat2: Second stat used to cluster.
    :param stat3: Third stat used to cluster.
    :param stat4: Fourth stat used to cluster.
    :param stats: data from cluster_info().
    :return: void
    """
    datac0 = stats.loc[:, stat1]
    datac1 = stats.loc[:, stat2]
    datac2 = stats.loc[:, stat3]
    datac3 = stats.loc[:, stat4]
    # create plot
    plt.subplots()
    index = np.arange(4)

    bar_width = 0.2
    opacity = 0.8

    plt.bar(index, datac0, bar_width,
            alpha=opacity,
            color='blue',
            label='Cluster 0')

    plt.bar(index + bar_width, datac1, bar_width,
            alpha=opacity,
            color='green',
            label='Cluster 1')

    plt.bar(index + 2 * bar_width, datac2, bar_width,
            alpha=opacity,
            color='red',
            label='Cluster 2')

    plt.bar(index + 3 * bar_width, datac3, bar_width,
            alpha=opacity,
            color='black',
            label='Cluster 3')


    plt.xlabel('Clusters')
    plt.ylabel('Mean')
    plt.title('Statistic Means for each Cluster')
    plt.xticks(index + bar_width, (stat1, stat2, stat3, stat4))
    plt.legend()
    plt.tight_layout()
    file = 'images/bargraph.png'
    if os.path.isfile(file):
        os.remove(file)
    plt.savefig(file)
    plt.cla()

def cluster_points_relationship(teamdata, fullresults, stat1, stat2, stat3, stat4):
    all_teams_clusters = pd.DataFrame([])
    ohl_dict = {"Ottawa 67's": 'OTT', 'Windsor Spitfires': 'WSR', 'Sudbury Wolves': 'SBY',
                'Sault Ste. Marie Greyhounds': 'SSM', 'Sarnia Sting': 'SAR', 'Saginaw Spirit': 'SAG',
                'Peterborough Petes': 'PBO', 'Owen Sound Attack': 'OS', 'Oshawa Generals': 'OSH',
                'North Bay Battalion': 'NB', 'Niagara IceDogs': 'NIAG', 'Mississauga Steelheads': 'MISS',
                'London Knights': 'LDN', 'Kitchener Rangers': 'KIT', 'Kingston Frontenacs': 'KGN',
                'Hamilton Bulldogs': 'HAM', 'Guelph Storm': 'GUE', 'Flint Firebirds': 'FLNT', 'Erie Otters': 'ER',
                'Barrie Colts': 'BAR'}

    for key in ohl_dict:
        all_teams_clusters = add_team2df(pd.DataFrame([key]), select_team(ohl_dict[key], fullresults), all_teams_clusters)

    all_teams_clusters.columns = ['Team', 'Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 3']
    all_teams_clusters = all_teams_clusters.reset_index(drop=True)
    percent_each_cluster = find_percentages(all_teams_clusters)
    percent_each_cluster = percent_each_cluster.reset_index(drop=True)
    points = []
    for index, row in percent_each_cluster.iterrows():
        pts = teamdata[teamdata['Name'] == row['Team']]['ROW']
        points.append(int(pts))
    points = pd.Series(points)
    percent_each_cluster['Points'] = points.values
    df_with_wins = percent_each_cluster
    df_with_wins.columns = ['Team', 'Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 3', 'Points']
    OHL_results = df_with_wins.iloc[0:20, :]
    OHL_results = OHL_results.sort_values('Points')
    c0x = OHL_results.loc[:, "Cluster 0"]
    c0y = OHL_results.loc[:, "Points"]
    c1x = OHL_results.loc[:, "Cluster 1"]
    c1y = OHL_results.loc[:, "Points"]
    c2x = OHL_results.loc[:, "Cluster 2"]
    c2y = OHL_results.loc[:, "Points"]
    c3x = OHL_results.loc[:, "Cluster 3"]
    c3y = OHL_results.loc[:, "Points"]
    x = [c0x, c1x, c2x, c3x]
    y = [c0y, c1y, c2y, c3y]
    results = []
    for cluster in range(0, 4):
        slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x[cluster], y[cluster])
        slope = round(slope, 3)
        r_square = round(r_value * r_value, 3)
        results.append([slope, r_square])

        sb.regplot(x=x[cluster], y=y[cluster], ci=None, label="Slope = " + str(slope) + ", R-Squared = " +
                                                              str(r_square))
        plt.xlabel('Percentage of Players in Cluster ' + str(cluster))
        plt.ylabel('Team Points')
        plt.title('Cluster ' + str(cluster) + ' - Points Relationship')
        plt.legend()
        plt.tight_layout()
        file = 'images/Cluster_' + str(cluster) + '.png'
        if os.path.isfile(file):
            os.remove(file)
        plt.savefig(file)
        plt.cla()

    return results

class Window(QDialog):
    """
    This class creates the PyQt5 Window and all the widgets to create the GUI.
    """

    def __init__(self):
        super().__init__()

        self.createLeftGroupBox()
        self.createRightWidget()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.leftGroupBox, 0, 0, 1, 1)
        mainLayout.addWidget(self.rightWidget, 0, 1, 1, 2)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Player Cluster")
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        QApplication.setPalette(QApplication.style().standardPalette())

    def createLeftGroupBox(self):
        self.leftGroupBox = QGroupBox("Input Statistics")

        leagueLabel = QLabel('League: ')
        self.league = QComboBox()
        self.allLeagues = QCheckBox("All Leagues")
        hboxLeague = QHBoxLayout()
        hboxLeague.addStretch()
        hboxLeague.addWidget(leagueLabel)
        hboxLeague.addWidget(self.league)
        #hboxLeague.addWidget(self.allLeagues)
        hboxLeague.addStretch()

        self.allLeagues.setCheckable(True)

        startLabel = QLabel('Years: ')
        self.start = QComboBox()
        endLabel = QLabel('to')
        self.end = QComboBox()
        hboxYear = QHBoxLayout()
        hboxYear.addStretch()
        hboxYear.addWidget(startLabel)
        hboxYear.addWidget(self.start)
        hboxYear.addWidget(endLabel)
        hboxYear.addWidget(self.end)
        hboxYear.addStretch()

        ageLabel = QLabel('Age: ')
        self.age = QComboBox()
        self.allAges = QCheckBox("All Ages")
        hboxAge = QHBoxLayout()
        hboxAge.addStretch()
        hboxAge.addWidget(ageLabel)
        hboxAge.addWidget(self.age)
        hboxAge.addWidget(self.allAges)
        hboxAge.addStretch()

        self.allAges.setCheckable(True)
        self.allAges.setChecked(True)

        self.allPlayers = QRadioButton("All Players")
        self.forwards = QRadioButton("Forwards")
        self.defense = QRadioButton("Defense")
        hboxPosition = QHBoxLayout()
        hboxPosition.addStretch()
        hboxPosition.addWidget(self.allPlayers)
        hboxPosition.addWidget(self.forwards)
        hboxPosition.addWidget(self.defense)
        hboxPosition.addStretch()

        self.allPlayers.setCheckable(True)
        self.allPlayers.setChecked(True)
        self.forwards.setCheckable(True)
        self.defense.setCheckable(True)

        stat1Label = QLabel('Stat 1: ')
        self.stat1 = QComboBox()
        hboxStat1 = QHBoxLayout()
        hboxStat1.addStretch()
        hboxStat1.addWidget(stat1Label)
        hboxStat1.addWidget(self.stat1)
        hboxStat1.addStretch()

        stat2Label = QLabel('Stat 2: ')
        self.stat2 = QComboBox()
        hboxStat2 = QHBoxLayout()
        hboxStat2.addStretch()
        hboxStat2.addWidget(stat2Label)
        hboxStat2.addWidget(self.stat2)
        hboxStat2.addStretch()

        stat3Label = QLabel('Stat 3: ')
        self.stat3 = QComboBox()
        hboxStat3 = QHBoxLayout()
        hboxStat3.addStretch()
        hboxStat3.addWidget(stat3Label)
        hboxStat3.addWidget(self.stat3)
        hboxStat3.addStretch()

        stat4Label = QLabel('Stat 4: ')
        self.stat4 = QComboBox()
        hboxStat4 = QHBoxLayout()
        hboxStat4.addStretch()
        hboxStat4.addWidget(stat4Label)
        hboxStat4.addWidget(self.stat4)
        hboxStat4.addStretch()

        self.enterButton = QPushButton("Run Algorithm")
        hboxEnter = QHBoxLayout()
        hboxEnter.addStretch()
        hboxEnter.addWidget(self.enterButton)
        hboxEnter.addStretch()

        self.runAll = QPushButton("Run All")
        hboxRunAll = QHBoxLayout()
        hboxRunAll.addStretch()
        hboxRunAll.addWidget(self.runAll)
        hboxRunAll.addStretch()

        self.initialize_input()
        self.league.currentTextChanged.connect(self.league_change)
        self.allLeagues.toggled.connect(self.league.setDisabled)
        self.start.currentTextChanged.connect(self.start_year_change)
        self.end.currentTextChanged.connect(self.end_year_change)
        self.allAges.toggled.connect(self.age.setDisabled)
        self.stat1.currentTextChanged.connect(self.update_stats)
        self.stat2.currentTextChanged.connect(self.update_stats)
        self.stat3.currentTextChanged.connect(self.update_stats)
        self.stat4.currentTextChanged.connect(self.update_stats)
        self.enterButton.clicked.connect(self.run_alg)
        self.runAll.clicked.connect(self.run_all_cluster)

        layout = QVBoxLayout()
        layout.addLayout(hboxLeague)
        layout.addLayout(hboxYear)
        layout.addLayout(hboxAge)
        layout.addLayout(hboxPosition)
        layout.addLayout(hboxStat1)
        layout.addLayout(hboxStat2)
        layout.addLayout(hboxStat3)
        layout.addLayout(hboxStat4)
        layout.addLayout(hboxEnter)
        #layout.addLayout(hboxRunAll)
        self.leftGroupBox.setLayout(layout)

    def initialize_input(self):
        leagues = ['OHL']
        #leagues = ['OHL', 'AHL', 'QMJHL', 'USHL', 'WHL']
        self.league.addItems(leagues)

        # update start years based on league
        self.update_start_years()

        # update end years based on start years
        self.update_end_year()

        # update ages based on league and years
        self.update_age()
        self.age.setDisabled(True)

        if self.allLeagues.isChecked():
            league = 'OHL_AHL_QMJHL_USHL_WHL'
        else:
            league = str(self.league.currentText())
        start_year = str(self.start.currentText())
        end_year = str(self.end.currentText())
        if start_year == end_year:
            file = 'data/' + league + '_' + start_year + '_skaters.csv'
        else:
            file = 'data/' + league + '_' + start_year + '_to_' + end_year + '_skaters.csv'
        try:
            data = pd.read_csv(file)
            data = clean_nan(data)
            stats = data.columns.tolist()
            del stats[0:6]

            stat1 = stats[0]
            stat2 = stats[1]
            stat3 = stats[2]
            stat4 = stats[3]

            stats.remove(stat1)
            stats.remove(stat2)
            stats.remove(stat3)
            stats.remove(stat4)

            self.stat1.addItem(stat1)
            self.stat2.addItem(stat2)
            self.stat3.addItem(stat3)
            self.stat4.addItem(stat4)

            self.stat1.addItems(stats)
            self.stat2.addItems(stats)
            self.stat3.addItems(stats)
            self.stat4.addItems(stats)
        except FileNotFoundError:
            QMessageBox.about(self, 'Error', "The data is not available")


    def league_change(self):
        # update start years based on league
        self.update_start_years()

        # update end years based on start years
        self.update_end_year()

        # update age based on league and years
        self.update_age()

        # update stats based on league, start and end years, and team
        self.update_stats()

    def start_year_change(self):
        # update end years based on start year
        self.update_end_year()

        # update age based on league and years
        self.update_age()

        # update stats based on league, start and end years, and team
        self.update_stats()

    def end_year_change(self):
        # update age based on league and years
        self.update_age()

        # update stats based on league, start and end years, and team
        self.update_stats()

    def update_start_years(self):
        # update start years based on league
        league = str(self.league.currentText())
        years = {'OHL': ['2018-19', '2017-18', '2016-17', '2015-16', '2014-15', '2013-14', '2012-13', '2011-12',
                         '2010-11', '2009-10', '2008-09', '2007-08', '2006-07', '2005-06', '2004-05', '2003-04',
                         '2002-03', '2001-02', '2000-01', '1999-00', '1998-99', '1997-98'],
                 'AHL': ['2018-19', '2017-18', '2016-17', '2015-16', '2014-15', '2013-14', '2012-13', '2011-12',
                         '2010-11', '2009-10', '2008-09', '2007-08', '2006-07', '2005-06'],
                 'QMJHL': ['2018-19', '2017-18', '2016-17', '2015-16', '2014-15', '2013-14', '2012-13', '2011-12',
                           '2010-11', '2009-10', '2008-09', '2007-08', '2006-07', '2005-06', '2004-05', '2003-04',
                           '2002-03', '2001-02', '2000-01', '1999-00', '1998-99'],
                 'USHL': ['2018-19', '2017-18', '2016-17', '2015-16', '2014-15', '2013-14', '2012-13', '2011-12',
                          '2010-11', '2009-10', '2008-09', '2007-08', '2006-07', '2005-06', '2004-05', '2003-04',
                          '2002-03'],
                 'WHL': ['2018-19', '2017-18', '2016-17', '2015-16', '2014-15', '2013-14', '2012-13', '2011-12',
                         '2010-11', '2009-10', '2008-09', '2007-08', '2006-07', '2005-06', '2004-05', '2003-04',
                         '2002-03', '2001-02', '2000-01', '1999-00', '1998-99', '1997-98', '1996-97']}
        self.start.blockSignals(True)
        self.start.clear()
        self.start.addItems(years[league])
        self.start.blockSignals(False)

    def update_end_year(self):
        # update end years based on start years
        end = str(self.end.currentText())
        start = str(self.start.currentText())
        self.end.blockSignals(True)
        self.end.clear()
        start_year = int(start[0:4])
        years = []
        for year in range(start_year, 2019):
            years.append(str(year) + '-' + str(year + 1)[2:4])
        years = list(reversed(years))
        self.end.addItems(years)
        self.end.setCurrentText(end)
        self.end.blockSignals(False)

    def update_age(self):
        if self.allLeagues.isChecked():
            league = 'OHL_AHL_QMJHL_USHL_WHL'
        else:
            league = str(self.league.currentText())
        start_year = str(self.start.currentText())
        end_year = str(self.end.currentText())
        if start_year == end_year:
            file = 'data/' + league + '_' + start_year + '_skaters.csv'
        else:
            file = 'data/' + league + '_' + start_year + '_to_' + end_year + '_skaters.csv'
        try:
            data = pd.read_csv(file)
            data = data.loc[data['GP'] > 30]
            if self.allPlayers.isChecked():
                positions = 'All'
            elif self.forwards.isChecked():
                positions = 'Forwards'
            else:
                positions = 'Defense'
            data = select_position(data, positions)
            data = clean_nan(data)
            ages = []
            for index, row in data.iterrows():
                if ages.count(int(row['Age'])) == 0:
                    ages.append(int(row['Age']))
            ages.sort()
            ages = [str(age) for age in ages]
            self.age.blockSignals(True)
            self.age.clear()
            self.age.addItems(ages)
            self.age.blockSignals(False)
        except FileNotFoundError:
            QMessageBox.about(self, 'Error', "The data is not available")

    def update_stats(self):
        stat1 = str(self.stat1.currentText())
        stat2 = str(self.stat2.currentText())
        stat3 = str(self.stat3.currentText())
        stat4 = str(self.stat4.currentText())
        if self.allLeagues.isChecked():
            league = 'OHL_AHL_QMJHL_USHL_WHL'
        else:
            league = str(self.league.currentText())
        start_year = str(self.start.currentText())
        end_year = str(self.end.currentText())
        if start_year == end_year:
            file = 'data/' + league + '_' + start_year + '_skaters.csv'
        else:
            file = 'data/' + league + '_' + start_year + '_to_' + end_year + '_skaters.csv'
        try:
            data = pd.read_csv(file)
            stats = data.columns.tolist()
            del stats[0:6]
            if stats.count(stat1) > 0:
                stats.remove(stat1)
            if stats.count(stat2) > 0:
                stats.remove(stat2)
            if stats.count(stat3) > 0:
                stats.remove(stat3)
            if stats.count(stat4) > 0:
                stats.remove(stat4)

            self.stat1.blockSignals(True)
            self.stat2.blockSignals(True)
            self.stat3.blockSignals(True)
            self.stat4.blockSignals(True)

            self.stat1.clear()
            self.stat2.clear()
            self.stat3.clear()
            self.stat4.clear()

            self.stat1.addItem(stat1)
            self.stat2.addItem(stat2)
            self.stat3.addItem(stat3)
            self.stat4.addItem(stat4)

            self.stat1.addItems(stats)
            self.stat2.addItems(stats)
            self.stat3.addItems(stats)
            self.stat4.addItems(stats)

            self.stat1.blockSignals(False)
            self.stat2.blockSignals(False)
            self.stat3.blockSignals(False)
            self.stat4.blockSignals(False)
        except FileNotFoundError:
            QMessageBox.about(self, 'Error', "The data is not available")

    def run_alg(self):
        if self.allLeagues.isChecked():
            league = 'OHL_AHL_QMJHL_USHL_WHL'
        else:
            league = str(self.league.currentText())
        start_year = str(self.start.currentText())
        end_year = str(self.end.currentText())
        if start_year == end_year:
            file = 'data/' + league + '_' + start_year + '_skaters.csv'
            teamfile = 'data/' + league + '_' + start_year + '_teams.csv'
        else:
            file = 'data/' + league + '_' + start_year + '_to_' + end_year + '_skaters.csv'
            teamfile = 'data/' + league + '_' + start_year + '_to_' + end_year + '_teams.csv'
        try:
            data = pd.read_csv(file)
            teamdata = pd.read_csv(teamfile)
            if self.allAges.isChecked():
                age = 0
            else:
                age = str(self.age.currentText())
            if self.allPlayers.isChecked():
                positions = 'All'
            elif self.forwards.isChecked():
                positions = 'Forwards'
            else:
                positions = 'Defense'
            data = data.loc[data['GP'] > 30]
            data = select_age(data, age)
            data = select_position(data, positions)
            data = clean_nan(data)
            if data.shape[0] < 4:
                QMessageBox.about(self, 'Error', "There are not enough players in this group to cluster.")
                return
            stat1 = str(self.stat1.currentText())
            stat2 = str(self.stat2.currentText())
            stat3 = str(self.stat3.currentText())
            stat4 = str(self.stat4.currentText())
            results = cluster(data, stat1, stat2, stat3, stat4)
            stats = cluster_info(data, stat1, stat2, stat3, stat4)
            bar_graph(stat1, stat2, stat3, stat4, stats)
            cluster_visualization(data, stat1, stat2, stat3, stat4)
            slope_rsq = cluster_points_relationship(teamdata, results, stat1, stat2, stat3, stat4)
            self.update_playerList()
            self.update_pics()
        except FileNotFoundError:
            QMessageBox.about(self, 'Error', "The data is not available")

    def run_all_cluster(self):
        if self.allLeagues.isChecked():
            league = 'OHL_AHL_QMJHL_USHL_WHL'
        else:
            league = str(self.league.currentText())
        start_year = str(self.start.currentText())
        end_year = str(self.end.currentText())
        if start_year == end_year:
            file = 'data/' + league + '_' + start_year + '_skaters.csv'
            teamfile = 'data/' + league + '_' + start_year + '_teams.csv'
        else:
            file = 'data/' + league + '_' + start_year + '_to_' + end_year + '_skaters.csv'
            teamfile = 'data/' + league + '_' + start_year + '_to_' + end_year + '_teams.csv'
        try:
            data = pd.read_csv(file)
            teamdata = pd.read_csv(teamfile)
            if self.allAges.isChecked():
                age = 0
            else:
                age = str(self.age.currentText())
            if self.allPlayers.isChecked():
                positions = 'All'
            elif self.forwards.isChecked():
                positions = 'Forwards'
            else:
                positions = 'Defense'
            data = data.loc[data['GP'] > 30]
            data = select_age(data, age)
            data = select_position(data, positions)
            data = clean_nan(data)
            if data.shape[0] < 4:
                QMessageBox.about(self, 'Error', "There are not enough players in this group to cluster.")
                return
            stats = data.columns.tolist()
            del stats[0:6]
            self.stat1.blockSignals(True)
            self.stat2.blockSignals(True)
            self.stat3.blockSignals(True)
            self.stat4.blockSignals(True)
            self.stat1.clear()
            self.stat2.clear()
            self.stat3.clear()
            self.stat4.clear()
            self.stat1.addItems(stats)
            self.stat2.addItems(stats)
            self.stat3.addItems(stats)
            self.stat4.addItems(stats)
            i = 0
            dict = {}
            regression = []
            for stat1 in stats:
                self.stat1.setCurrentText(stat1)
                for stat2 in stats[stats.index(stat1) + 1:]:
                    if stat2 != stat1:
                        self.stat2.setCurrentText(stat2)
                        for stat3 in stats[stats.index(stat2) + 1:]:
                            if stat3 != stat1 and stat3 != stat2:
                                self.stat3.setCurrentText(stat3)
                                for stat4 in stats[stats.index(stat3) + 1:]:
                                    if stat4 != stat1 and stat4 != stat2 and stat4 != stat3:
                                        self.stat4.setCurrentText(stat4)
                                        results = cluster(data, stat1, stat2, stat3, stat4)
                                        slope_rqs = cluster_points_relationship(teamdata, results, stat1, stat2, stat3, stat4)
                                        for c in range(0, 4):
                                            try:
                                                regression.append([stat1, stat2, stat3, stat4, c, slope_rqs[i][0], slope_rqs[i][1]])
                                            except IndexError:
                                                print(slope_rqs, "Index error")
                        dict[stat1 + stat2] = pd.DataFrame(regression,
                                                            columns=["Stat 1", "Stat 2", "Stat 3", "Stat 4",
                                                                    "Cluster", "Slope", "R-Squared"])
                        dict[stat1 + stat2] = dict[stat1 + stat2].sort_values(by=['R-Squared', 'Slope'], ascending=[False, False])
                        dict[stat1 + stat2].to_csv("results/" + stat1 + '_' + stat2 + ".csv")
                        i += 1
            self.stat1.blockSignals(False)
            self.stat2.blockSignals(False)
            self.stat3.blockSignals(False)
            self.stat4.blockSignals(False)
        except FileNotFoundError:
            QMessageBox.about(self, 'Error', "The data is not available")


    def update_pics(self):
        bargraph = QPixmap('images/bargraph.png')
        smaller = bargraph.scaled(800, 800, Qt.KeepAspectRatio, Qt.FastTransformation)
        labelBarGraph = QLabel("Bar Graph")
        labelBarGraph.setPixmap(smaller)
        for i in range(self.layoutBarGraph.count()):
            if type(self.layoutBarGraph.itemAt(i)) != QHBoxLayout:
                self.layoutBarGraph.itemAt(i).widget().close()
        self.layoutBarGraph.addWidget(labelBarGraph)

        seeClusters = QPixmap('images/Cluster_Visualization.png')
        smaller_pic = seeClusters.scaled(800, 800, Qt.KeepAspectRatio, Qt.FastTransformation)
        labelSeeClusters = QLabel("Cluster Visualization")
        labelSeeClusters.setPixmap(smaller_pic)
        for i in range(self.layoutSeeCluster.count()):
            if type(self.layoutSeeCluster.itemAt(i)) != QHBoxLayout:
                self.layoutSeeCluster.itemAt(i).widget().close()
        self.layoutSeeCluster.addWidget(labelSeeClusters)

        cluster = str(self.clusterChoice2.currentText())
        clusterVSWin = QPixmap('images/Cluster_' + cluster + '.png')
        smaller_image = clusterVSWin.scaled(800, 800, Qt.KeepAspectRatio, Qt.FastTransformation)
        labelClusterVSWin = QLabel("Cluster vs Wins")
        labelClusterVSWin.setPixmap(smaller_image)
        for i in range(self.layoutClusterVSWin.count()):
            if type(self.layoutClusterVSWin.itemAt(i)) != QHBoxLayout:
                self.layoutClusterVSWin.itemAt(i).widget().close()
        self.layoutClusterVSWin.addWidget(labelClusterVSWin)

    def createRightWidget(self):

        self.rightWidget = QTabWidget()
        playerListTab = QWidget()
        barGraphTab = QWidget()
        seeClusterTab = QWidget()
        clusterWinTab = QWidget()
        self.rightWidget.addTab(playerListTab, "Player List")
        self.rightWidget.addTab(barGraphTab, "Cluster Statistics")
        self.rightWidget.addTab(seeClusterTab, "Visualization")
        self.rightWidget.addTab(clusterWinTab, "Percentage of Players in Cluster vs Wins")

        hboxClusterChoice1 = QHBoxLayout()
        hboxClusterChoice1.addStretch()
        clusterLabel1 = QLabel("Cluster: ")
        self.clusterChoice1 = QComboBox()
        hboxClusterChoice1.addWidget(clusterLabel1)
        hboxClusterChoice1.addWidget(self.clusterChoice1)
        hboxClusterChoice1.addStretch()

        hboxPlayerList = QHBoxLayout()
        hboxPlayerList.addStretch()
        self.playerList = QListWidget()
        hboxPlayerList.addWidget(self.playerList)
        hboxPlayerList.addStretch()

        layoutPlayerList = QVBoxLayout()
        layoutPlayerList.addLayout(hboxClusterChoice1)
        layoutPlayerList.addLayout(hboxPlayerList)
        playerListTab.setLayout(layoutPlayerList)

        bargraph = QPixmap('images/bargraph.png')
        smaller_image = bargraph.scaled(800, 800, Qt.KeepAspectRatio, Qt.FastTransformation)
        labelBarGraph = QLabel("Bar Graph")
        labelBarGraph.setPixmap(smaller_image)
        self.layoutBarGraph = QVBoxLayout()
        self.layoutBarGraph.addWidget(labelBarGraph)
        barGraphTab.setLayout(self.layoutBarGraph)

        clusters = QPixmap('images/Cluster_Visualization.png')
        smaller_image = clusters.scaled(800, 800, Qt.KeepAspectRatio, Qt.FastTransformation)
        labelSeeClusters = QLabel("Clusters")
        labelSeeClusters.setPixmap(smaller_image)
        self.layoutSeeCluster = QVBoxLayout()
        self.layoutSeeCluster.addWidget(labelSeeClusters)
        seeClusterTab.setLayout(self.layoutSeeCluster)

        hboxClusterChoice2 = QHBoxLayout()
        hboxClusterChoice2.addStretch()
        clusterLabel2 = QLabel("Cluster: ")
        self.clusterChoice2 = QComboBox()
        hboxClusterChoice2.addWidget(clusterLabel2)
        hboxClusterChoice2.addWidget(self.clusterChoice2)
        hboxClusterChoice2.addStretch()

        clusterVSWin = QPixmap('images/Cluster_0.png')
        smaller_image = clusterVSWin.scaled(800, 800, Qt.KeepAspectRatio, Qt.FastTransformation)
        labelClusterVSWin = QLabel("Cluster vs Wins")
        labelClusterVSWin.setPixmap(smaller_image)
        self.layoutClusterVSWin = QVBoxLayout()
        self.layoutClusterVSWin.addLayout(hboxClusterChoice2)
        self.layoutClusterVSWin.addWidget(labelClusterVSWin)
        clusterWinTab.setLayout(self.layoutClusterVSWin)

        self.clusterChoice2.currentTextChanged.connect(self.update_clusterVSwin)
        self.initialize_clusters()
        self.clusterChoice1.currentTextChanged.connect(self.update_playerList)
        self.playerList.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def initialize_clusters(self):

        self.clusterChoice1.addItems(['0', '1', '2', '3'])
        self.clusterChoice2.addItems(['0', '1', '2', '3'])

    def update_playerList(self):
        self.playerList.blockSignals(True)
        cluster = str(self.clusterChoice1.currentText())
        self.playerList.clear()

        df = pd.read_csv('df_withclusters.csv')
        players = []
        for index, row in df.iterrows():
            if str(row['Cluster']) == str(cluster):
                players.append(row['Team'] + ' - ' + row['Name'])

        self.playerList.addItems(players)
        self.playerList.blockSignals(False)

    def update_clusterVSwin(self):
        cluster = str(self.clusterChoice2.currentText())
        pic = 'images/Cluster_' + cluster + '.png'
        pixmap = QPixmap(pic)
        smaller_rink = pixmap.scaled(800, 800, Qt.KeepAspectRatio, Qt.FastTransformation)
        labelClusterVSWin = QLabel("Cluster Vs Wins")
        labelClusterVSWin.setPixmap(smaller_rink)
        for i in range(self.layoutClusterVSWin.count()):
            if type(self.layoutClusterVSWin.itemAt(i)) != QHBoxLayout:
                self.layoutClusterVSWin.itemAt(i).widget().close()
        self.layoutClusterVSWin.addWidget(labelClusterVSWin)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gallery = Window()
    gallery.show()
    sys.exit(app.exec_())
