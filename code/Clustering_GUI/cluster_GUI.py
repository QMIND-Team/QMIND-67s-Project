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

def typeFromString(stat):
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

def castToType(stat):
    """Function to convert stat to int, float or string.

        Args:
            stat (str): The stat being converted.

        Returns:
            Casted stat.
     """
    if typeFromString(stat) == 'int':
        return int(stat)
    elif typeFromString(stat) == 'float':
        return float(stat)
    else:
        return str(stat)

def getSeasons(start_season, end_season):
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

def normalize(data, stat1, stat2, stat3, stat4):
    std1 = data.loc[:, stat1].std()
    std2 = data.loc[:, stat2].std()
    std3 = data.loc[:, stat3].std()
    std4 = data.loc[:, stat4].std()
    avg1 = data.loc[:, stat1].mean()
    avg2 = data.loc[:, stat2].mean()
    avg3 = data.loc[:, stat3].mean()
    avg4 = data.loc[:, stat4].mean()
    data.loc[:, stat1] = (data.loc[:, stat1] - avg1) / std1
    data.loc[:, stat2] = (data.loc[:, stat2] - avg2) / std2
    data.loc[:, stat3] = (data.loc[:, stat3] - avg3) / std3
    data.loc[:, stat4] = (data.loc[:, stat4] - avg4) / std4
    return data

def divideByGP(stats, dataset):
    """
    Returns data set with added columns containing stats/GP.
    :param stats: Stats used to create per game stats.
    :param dataset: Original data set.
    :return: The new data set with new stat columns.
    """
    GP_vector = dataset.loc[:, 'GP']
    dataset.loc[:,stats] = dataset.loc[:, stats].div(GP_vector, axis = 0)
    return dataset

def cluster(player_data, team_data, stats):
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
    player_data = player_data.loc[:, ['Name', 'Team'] + stats]
    cluster_data = player_data.loc[:, stats]
    sc_X = StandardScaler()
    cluster_data = sc_X.fit_transform(cluster_data)
    cluster_data = pd.DataFrame(cluster_data, columns=stats)
    kmeans = KMeans(n_clusters=4, init='k-means++', max_iter=300, n_init=10, random_state=0)
    predictions = kmeans.fit_predict(cluster_data)
    player_data['Cluster'] = predictions

    centroids = kmeans.cluster_centers_
    centroids = pd.DataFrame(centroids, columns=stats)
    centroidBarGraph(stats, centroids)

    player_data['Distance from Centroid'] = 0
    for index, row in player_data.iterrows():
        for stat in stats:
            player_data.loc[index, 'Distance from Centroid'] += pow(cluster_data.loc[index, stat] - centroids.loc[row['Cluster'], stat], 2)
        player_data.loc[index, 'Distance from Centroid'] = math.sqrt(player_data.loc[index, 'Distance from Centroid'])
    player_data.to_csv("df_withclusters.csv")

    cluster0 = player_data.loc[player_data['Cluster'] == 0]
    cluster0 = cluster0.drop(columns='Cluster')
    cluster0 = cluster0.sort_values('Distance from Centroid', ascending=True)
    cluster0 = cluster0.reset_index(drop=True)
    cluster0.to_csv("Cluster0.csv")
    cluster1 = player_data.loc[player_data['Cluster'] == 1]
    cluster1 = cluster1.drop(columns='Cluster')
    cluster1 = cluster1.sort_values('Distance from Centroid', ascending=True)
    cluster1 = cluster1.reset_index(drop=True)
    cluster1.to_csv("Cluster1.csv")
    cluster2 = player_data.loc[player_data['Cluster'] == 2]
    cluster2 = cluster2.drop(columns='Cluster')
    cluster2 = cluster2.sort_values('Distance from Centroid', ascending=True)
    cluster2 = cluster2.reset_index(drop=True)
    cluster2.to_csv("Cluster2.csv")
    cluster3 = player_data.loc[player_data['Cluster'] == 3]
    cluster3 = cluster3.drop(columns='Cluster')
    cluster3 = cluster3.sort_values('Distance from Centroid', ascending=True)
    cluster3 = cluster3.reset_index(drop=True)
    cluster3.to_csv("Cluster3.csv")

    visualizeCluster(cluster_data, predictions)
    clusterVSwins(team_data, player_data)



    return cluster0, cluster1, cluster2, cluster3

def visualizeCluster(cluster_data, predictions):
    """
    Creates .png file visualizing the clusters.
    :param data: Data set.
    :param stat1: First stat used to cluster.
    :param stat2: Second stat used to cluster.
    :param stat3: Third stat used to cluster.
    :param stat4: Fourth stat used to cluster.
    :return: void
    """
    pca = PCA(n_components=2)
    cluster_data_2d = pca.fit_transform(cluster_data)
    cluster_data_2d = pd.DataFrame(cluster_data_2d)
    cluster_data_2d['Cluster'] = predictions
    cluster_data_2d.columns = ['PCA 1', 'PCA 2', 'Cluster']

    cluster0 = cluster_data_2d.loc[cluster_data_2d['Cluster'] == 0]
    cluster1 = cluster_data_2d.loc[cluster_data_2d['Cluster'] == 1]
    cluster2 = cluster_data_2d.loc[cluster_data_2d['Cluster'] == 2]
    cluster3 = cluster_data_2d.loc[cluster_data_2d['Cluster'] == 3]

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

def centroidBarGraph(stats, centroid_data):
    """
    Creates a bargraph showing the data returned from cluster_info() and saves it as a .png.
    :param stat1: First stat used to cluster.
    :param stat2: Second stat used to cluster.
    :param stat3: Third stat used to cluster.
    :param stat4: Fourth stat used to cluster.
    :param stats: data from cluster_info().
    :return: void
    """
    # create plot
    plt.subplots()
    index = np.arange(4)

    bar_width = 0.2
    opacity = 0.8

    plt.bar(index, centroid_data.iloc[:, 0], bar_width,
            alpha=opacity,
            color='blue',
            label='Cluster 0')

    plt.bar(index + bar_width, centroid_data.iloc[:, 1], bar_width,
            alpha=opacity,
            color='green',
            label='Cluster 1')

    plt.bar(index + 2 * bar_width, centroid_data.iloc[:, 2], bar_width,
            alpha=opacity,
            color='red',
            label='Cluster 2')

    plt.bar(index + 3 * bar_width, centroid_data.iloc[:, 3], bar_width,
            alpha=opacity,
            color='black',
            label='Cluster 3')

    plt.xlabel('Clusters')
    plt.ylabel('Mean')
    plt.title('Statistic Means for each Cluster')
    plt.xticks(index + bar_width, stats)
    plt.legend()
    plt.tight_layout()
    file = 'images/bargraph.png'
    if os.path.isfile(file):
        os.remove(file)
    plt.savefig(file)
    plt.cla()
    return

def clusterVSwins(team_data, player_data):

    ohl_dict = {"Ottawa 67's": 'OTT', 'Windsor Spitfires': 'WSR', 'Sudbury Wolves': 'SBY',
                'Sault Ste. Marie Greyhounds': 'SSM', 'Sarnia Sting': 'SAR', 'Saginaw Spirit': 'SAG',
                'Peterborough Petes': 'PBO', 'Owen Sound Attack': 'OS', 'Oshawa Generals': 'OSH',
                'North Bay Battalion': 'NB', 'Niagara IceDogs': 'NIAG', 'Mississauga Steelheads': 'MISS',
                'London Knights': 'LDN', 'Kitchener Rangers': 'KIT', 'Kingston Frontenacs': 'KGN',
                'Hamilton Bulldogs': 'HAM', 'Guelph Storm': 'GUE', 'Flint Firebirds': 'FLNT', 'Erie Otters': 'ER',
                'Barrie Colts': 'BAR'}

    team_cluster_count = pd.DataFrame([], columns=['Team', 'Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 3'])
    for key in ohl_dict:
        players_on_team = player_data.loc[player_data['Team'] == ohl_dict[key]]
        players_on_team = players_on_team.reset_index(drop=True)
        cluster_count = [0, 0, 0, 0]
        for index, row in players_on_team.iterrows():
            cluster_count[row['Cluster']] += 1
        if players_on_team.shape[0] == 0:
            return
        cluster_count = [x / players_on_team.shape[0] * 100 for x in cluster_count]
        team_cluster_count = team_cluster_count.append({'Team': key,
                                                        'Cluster 0': cluster_count[0],
                                                        'Cluster 1': cluster_count[1],
                                                        'Cluster 2': cluster_count[2],
                                                        'Cluster 3': cluster_count[3]}, ignore_index=True)

    team_cluster_count = team_cluster_count.reset_index(drop=True)
    points = []
    for index, row in team_cluster_count.iterrows():
        pts = team_data[team_data['Name'] == row['Team']]['ROW']
        points.append(int(pts))
    team_cluster_count['Points'] = points
    team_cluster_count.columns = ['Team', 'Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 3', 'Points']
    team_cluster_count = team_cluster_count.sort_values('Points')
    c0x = team_cluster_count.loc[:, "Cluster 0"]
    c1x = team_cluster_count.loc[:, "Cluster 1"]
    c2x = team_cluster_count.loc[:, "Cluster 2"]
    c3x = team_cluster_count.loc[:, "Cluster 3"]
    y = team_cluster_count.loc[:, "Points"]
    x = [c0x, c1x, c2x, c3x]
    results = []
    for cluster in range(0, 4):
        slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x[cluster], y)
        slope = round(slope, 3)
        r_square = round(r_value * r_value, 3)
        results.append([slope, r_square])

        sb.regplot(x=x[cluster], y=y, ci=None, label="Slope = " + str(slope) + ", R-Squared = " + str(r_square))
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

        self.initializeInput()
        self.league.currentTextChanged.connect(self.leagueChange)
        self.allLeagues.toggled.connect(self.league.setDisabled)
        self.start.currentTextChanged.connect(self.startYearChange)
        self.end.currentTextChanged.connect(self.endYearChange)
        self.allAges.toggled.connect(self.age.setDisabled)
        self.stat1.currentTextChanged.connect(self.updateStats)
        self.stat2.currentTextChanged.connect(self.updateStats)
        self.stat3.currentTextChanged.connect(self.updateStats)
        self.stat4.currentTextChanged.connect(self.updateStats)
        self.enterButton.clicked.connect(self.runAlgorithm)
        self.runAll.clicked.connect(self.runAllCluster)

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
        return

    def initializeInput(self):
        leagues = ['OHL']
        #leagues = ['OHL', 'AHL', 'QMJHL', 'USHL', 'WHL']
        self.league.addItems(leagues)

        # update start years based on league
        self.updateStartYears()

        # update end years based on start years
        self.updateEndYear()

        # update ages based on league and years
        self.updateAge()
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
        return

    def leagueChange(self):
        # update start years based on league
        self.updateStartYears()

        # update end years based on start years
        self.updateEndYear()

        # update age based on league and years
        self.updateAge()

        # update stats based on league, start and end years, and team
        self.updateStats()
        return

    def startYearChange(self):
        # update end years based on start year
        self.updateEndYear()

        # update age based on league and years
        self.updateAge()

        # update stats based on league, start and end years, and team
        self.updateStats()
        return

    def endYearChange(self):
        # update age based on league and years
        self.updateAge()

        # update stats based on league, start and end years, and team
        self.updateStats()
        return

    def updateStartYears(self):
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
        return

    def updateEndYear(self):
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
        return

    def updateAge(self):
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
            player_data = pd.read_csv(file)

            if self.forwards.isChecked():
                player_data = player_data.loc[player_data['Pos'].isin(['C', 'RW', 'LW'])]
            elif self.defense.isChecked():
                player_data = player_data.loc[player_data['Pos'] == 'D']

            player_data = player_data.loc[player_data['GP'] > 30]
            ages = []
            for index, row in player_data.iterrows():
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
        return

    def updateStats(self):
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
        return

    def runAlgorithm(self):
        if self.allLeagues.isChecked():
            league = 'OHL_AHL_QMJHL_USHL_WHL'
        else:
            league = str(self.league.currentText())
        start_year = str(self.start.currentText())
        end_year = str(self.end.currentText())

        if start_year == end_year:
            player_filename = 'data/' + league + '_' + start_year + '_skaters.csv'
            team_filename = 'data/' + league + '_' + start_year + '_teams.csv'
        else:
            player_filename = 'data/' + league + '_' + start_year + '_to_' + end_year + '_skaters.csv'
            team_filename = 'data/' + league + '_' + start_year + '_to_' + end_year + '_teams.csv'
        try:
            player_data = pd.read_csv(player_filename)
            team_data = pd.read_csv(team_filename)

            if not self.allAges.isChecked():
                age = str(self.age.currentText())
                player_data = player_data.loc[round(player_data['Age']) == int(age)]

            if self.forwards.isChecked():
                player_data = player_data.loc[player_data['Pos'].isin(['C', 'RW', 'LW'])]
            elif self.defense.isChecked():
                player_data = player_data.loc[player_data['Pos'] == 'D']

            player_data = player_data.loc[player_data['GP'] > 30]

            if player_data.shape[0] < 10:
                QMessageBox.about(self, 'Error', "There are not enough players in this group to cluster.")
                return

            player_data = player_data.reset_index(drop=True)

            stats = [str(self.stat1.currentText())]
            stats.append(str(self.stat2.currentText()))
            stats.append(str(self.stat3.currentText()))
            stats.append(str(self.stat4.currentText()))

            if 'HD G' in player_data.columns.tolist():
                player_data = divideByGP(['HD G', 'HD Sh', 'MD G', 'MD Sh', 'LD G', 'LD Sh'], player_data)

            cluster(player_data, team_data, stats)

            self.updatePlayerList()
            self.updatePics()
        except FileNotFoundError:
            QMessageBox.about(self, 'Error', "The data is not available")
        return

    def runAllCluster(self):
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
            player_data = pd.read_csv(file)
            team_data = pd.read_csv(teamfile)
            if not self.allAges.isChecked():
                age = str(self.age.currentText())
                player_data = player_data.loc[round(player_data['Age']) == int(age)]

            if self.forwards.isChecked():
                player_data = player_data.loc[player_data['Pos'] in ['C', 'RW', 'LW']]
            elif self.defense.isChecked():
                player_data = player_data.loc[player_data['Pos'] == 'D']

            player_data = player_data.loc[player_data['GP'] > 30]

            if player_data.shape[0] < 4:
                QMessageBox.about(self, 'Error', "There are not enough players in this group to cluster.")
                return
            stats = player_data.columns.tolist()
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
                                        results = cluster(player_data, stats)
                                        slope_rqs = clusterVSwins(team_data, results, stats)
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
        return


    def updatePics(self):
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
        return

    def createRightWidget(self):

        self.rightWidget = QTabWidget()
        playerListTab = QWidget()
        playerSearchTab = QWidget()
        barGraphTab = QWidget()
        seeClusterTab = QWidget()
        clusterWinTab = QWidget()
        self.rightWidget.addTab(playerListTab, "Player List")
        self.rightWidget.addTab(barGraphTab, "Cluster Statistics")
        self.rightWidget.addTab(seeClusterTab, "Visualization")
        self.rightWidget.addTab(clusterWinTab, "Percentage of Players in Cluster vs Wins")

        # first tab, left side
        vboxClusterList = QVBoxLayout()

        hboxClusterChoice1 = QHBoxLayout()
        hboxClusterChoice1.addStretch()
        clusterLabel1 = QLabel("Cluster: ")
        self.clusterChoice1 = QComboBox()
        hboxClusterChoice1.addWidget(clusterLabel1)
        hboxClusterChoice1.addWidget(self.clusterChoice1)
        hboxClusterChoice1.addStretch()
        vboxClusterList.addLayout(hboxClusterChoice1)

        hboxClusterListExplain1 = QHBoxLayout()
        hboxClusterListExplain1.addStretch()
        clusterExplain1 = QLabel("All players in cluster")
        hboxClusterListExplain1.addWidget(clusterExplain1)
        hboxClusterListExplain1.addStretch()
        vboxClusterList.addLayout(hboxClusterListExplain1)

        hboxClusterListExplain2 = QHBoxLayout()
        hboxClusterListExplain2.addStretch()
        clusterExplain2 = QLabel("(sorted by ascending distance from Centroid)")
        hboxClusterListExplain2.addWidget(clusterExplain2)
        hboxClusterListExplain2.addStretch()
        vboxClusterList.addLayout(hboxClusterListExplain2)

        hboxClusterList = QHBoxLayout()
        hboxClusterList.addStretch()
        self.clusterList = QListWidget()
        hboxClusterList.addWidget(self.clusterList)
        hboxClusterList.addStretch()
        vboxClusterList.addLayout(hboxClusterList)

        # first tab, right side
        vboxNearestList = QVBoxLayout()

        hboxPlayerSearch = QHBoxLayout()
        hboxPlayerSearch.addStretch()
        self.playerSearchEntry = QLineEdit()
        self.playerSearchEnter = QPushButton("Enter")
        hboxPlayerSearch.addWidget(self.playerSearchEntry)
        hboxPlayerSearch.addWidget(self.playerSearchEnter)
        hboxPlayerSearch.addStretch()
        vboxNearestList.addLayout(hboxPlayerSearch)

        hboxNearestListExplain1 = QHBoxLayout()
        hboxNearestListExplain1.addStretch()
        nearestExplain1 = QLabel("Closest 5 players to chosen player")
        hboxNearestListExplain1.addWidget(nearestExplain1)
        hboxNearestListExplain1.addStretch()
        vboxNearestList.addLayout(hboxNearestListExplain1)

        hboxNearestListExplain2 = QHBoxLayout()
        hboxNearestListExplain2.addStretch()
        nearestExplain2 = QLabel("(sorted by ascending distance from player):")
        hboxNearestListExplain2.addWidget(nearestExplain2)
        hboxNearestListExplain2.addStretch()
        vboxNearestList.addLayout(hboxNearestListExplain2)

        hboxNearestList = QHBoxLayout()
        hboxNearestList.addStretch()
        self.nearestList = QListWidget()
        hboxNearestList.addWidget(self.nearestList)
        hboxNearestList.addStretch()
        vboxNearestList.addLayout(hboxNearestList)

        layoutPlayerLists = QHBoxLayout()
        layoutPlayerLists.addLayout(vboxClusterList)
        layoutPlayerLists.addLayout(vboxNearestList)
        playerListTab.setLayout(layoutPlayerLists)

        # second tab
        bargraph = QPixmap('images/bargraph.png')
        smaller_image = bargraph.scaled(800, 800, Qt.KeepAspectRatio, Qt.FastTransformation)
        labelBarGraph = QLabel("Bar Graph")
        labelBarGraph.setPixmap(smaller_image)
        self.layoutBarGraph = QVBoxLayout()
        self.layoutBarGraph.addWidget(labelBarGraph)
        barGraphTab.setLayout(self.layoutBarGraph)

        # third tab
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

        # fourth tab
        clusterVSWin = QPixmap('images/Cluster_0.png')
        smaller_image = clusterVSWin.scaled(800, 800, Qt.KeepAspectRatio, Qt.FastTransformation)
        labelClusterVSWin = QLabel("Cluster vs Wins")
        labelClusterVSWin.setPixmap(smaller_image)
        self.layoutClusterVSWin = QVBoxLayout()
        self.layoutClusterVSWin.addLayout(hboxClusterChoice2)
        self.layoutClusterVSWin.addWidget(labelClusterVSWin)
        clusterWinTab.setLayout(self.layoutClusterVSWin)

        self.clusterChoice2.currentTextChanged.connect(self.updateClusterVSwin)
        self.initializeClusters()
        self.clusterChoice1.currentTextChanged.connect(self.updatePlayerList)
        self.playerSearchEnter.clicked.connect(self.updateNearestList)
        self.clusterList.setSelectionMode(QAbstractItemView.ExtendedSelection)


    def initializeClusters(self):
        self.clusterChoice1.addItems(['0', '1', '2', '3'])
        self.clusterChoice2.addItems(['0', '1', '2', '3'])
        return

    def updatePlayerList(self):
        self.clusterList.blockSignals(True)
        cluster = str(self.clusterChoice1.currentText())
        self.clusterList.clear()

        df = pd.read_csv('Cluster' + cluster + '.csv')
        teams = df['Team'].tolist()
        players = df['Name'].tolist()
        list_items = []
        for i in range(0, len(teams)):
            list_items.append(teams[i] + ' - ' + players[i])

        self.clusterList.addItems(list_items)
        self.clusterList.blockSignals(False)
        return

    def updateNearestList(self):
        self.nearestList.blockSignals(True)
        player = str(self.playerSearchEntry.text())
        self.nearestList.clear()

        df = pd.read_csv('df_withclusters.csv')
        stats = df.columns.tolist()
        remove_stats = []
        for stat in stats:
            if stat in ['Name', 'Team', 'Cluster', 'Distance from Centroid', 'Unnamed: 0']:
                remove_stats.append(stat)
        for stat in remove_stats:
            stats.remove(stat)
        player_index = df.loc[df['Name'] == player].index
        if player_index.empty:
            QMessageBox.about(self, 'Error', "The player is not in the dataset.")
            return
        else:
            player_index = player_index[0]
        cluster = df.loc[player_index, 'Cluster']
        self.nearestList.addItem('Cluster: ' + str(cluster))
        df['Distance'] = 0
        for index, row in df.iterrows():
            for stat in stats:
                df.loc[index, 'Distance'] += pow(df.loc[index, stat] - df.loc[player_index, stat], 2)
            df.loc[index, 'Distance'] = math.sqrt(df.loc[index, 'Distance'])
        df = df.sort_values('Distance', ascending=True)
        df = df.reset_index(drop=True)
        nearest_teams = df.loc[1:6, 'Team'].tolist()
        nearest_names = df.loc[1:6, 'Name'].tolist()
        nearest = []
        for i in range(1, 6):
            nearest.append(nearest_teams[i] + ' - ' + nearest_names[i])
        self.nearestList.addItems(nearest[0:5])
        self.nearestList.blockSignals(True)
        return

    def updateClusterVSwin(self):
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
        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gallery = Window()
    gallery.show()
    sys.exit(app.exec_())
