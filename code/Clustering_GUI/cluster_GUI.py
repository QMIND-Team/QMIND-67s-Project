import sys, os, re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDateTime, Qt, QTimer, pyqtSlot, QModelIndex
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QToolBar, QInputDialog, QListWidget, QAbstractItemView,
                             QGraphicsPixmapItem)

## determine which stats you would like to cluster with
## insert column names in an array and the dataset you would like to select from

def select_stats(stats, dataset):
    df = dataset.loc[:, stats]
    return df

## editing the dataset to include all per/game stats
## input the dataset and the stats you want to divide by games

def divided_by_GP(stats, dataset):
    GP_vector = dataset.loc[:, 'GP']
    dataset.loc[:,stats] = dataset.loc[:, stats].div(GP_vector, axis = 0)
    return dataset

## this function is to select all the players from one team
## input the team you would like to select as a string and the dataset

def select_team(team, dataset):
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

## this function is to select all the players of a certain cluster
## input the dataset and the cluster you would like to select

def select_cluster(cluster, dataset):
    new_df = dataset[dataset['Cluster'] == cluster]
    return new_df

## this function is meant to sort players by their cluster
## just input the dataset

def sort_by_cluster(dataset):
    new_df = dataset.sort_values('Cluster')
    return new_df

## this function counts the number of times a particular value shows up in the cluster column
## input the dataset and the particular value you wish to count

def cluster_counter(value, dataset):
    N = dataset.shape[0]
    count = 0
    for i in range (0, N):
        if (dataset.loc[i, 'Cluster'] == value):
            count = count + 1
    return count

## this functions adds a team's cluster vector to the new dataset which includes information about all teams
## input the team name as a string in a datafrane, dthe dataset, and the new dataset

def add_team2df(team_name, dataset, new_dataset):
    dataset = dataset.reset_index(drop=True)
    team_cluster = []
    for i in range(0, 4):
        count = cluster_counter(i, dataset)
        team_cluster.append(count)
    team_cluster = pd.DataFrame([team_cluster])
    team_cluster = pd.concat([team_name, team_cluster], axis = 1)
    new_dataset = new_dataset.append([team_cluster])
    return new_dataset

## this function finds the percentage of elements in one row of a column
## input the dataset

def find_percentages(dataset):
    N = dataset.shape[0]
    new_df = dataset.copy(deep=True)
    for i in range (0,N):
        sum = new_df.iloc[i, 1:].sum()
        new_df.iloc[i, 1:] = 100*new_df.iloc[i, 1:].div(sum)
    return new_df

def cluster(stat1, stat2, stat3, stat4, positions):
    defense = False
    forwards = False
    if positions == 'Defense':
        defense = True
    elif positions == 'Forwards':
        forwards = True
    # prepare data
    data = pd.read_csv('data/OHL_cluster16_2015-16_to_2017-18.csv')
    data = divided_by_GP(['HD G', 'HD Sh', 'MD G', 'MD Sh', 'LD G', 'LD Sh'], data)
    df_over30gp_oldindex = data.loc[data['GP'] > 30]
    if defense:
        df_positions = df_over30gp_oldindex.loc[df_over30gp_oldindex['Pos'] == 'D']
    elif forwards:
        df_positions = df_over30gp_oldindex.loc[df_over30gp_oldindex['Pos'] != 'D']
    else:
        df_positions = df_over30gp_oldindex
    df_over30gp = df_positions.reset_index(drop=True)
    cluster_data = select_stats([stat1, stat2, stat3, stat4], df_over30gp)
    name_team = df_over30gp.loc[:, ['Name', 'Team']]
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
    fullresults.to_csv('data/df_withclusters.csv')

    return fullresults

def prep_data(stat1, stat2, stat3, stat4, positions):
    data = pd.read_csv('data/OHL_cluster16_2015-16_to_2017-18.csv')
    defense = False
    forwards = False
    if positions == 'Defense':
        defense = True
    elif positions == 'Forwards':
        forwards = True
    if defense:
        data = data.loc[data['Pos'] == 'D']
    elif forwards:
        data = data.loc[data['Pos'] != 'D']
    else:
        data = data
    data = divided_by_GP(['HD G', 'HD Sh', 'MD G', 'MD Sh', 'LD G', 'LD Sh'], data)
    df_over30gp_oldindex = data.loc[data['GP'] > 30]
    df_over30gp = df_over30gp_oldindex.reset_index(drop=True)
    cluster_data = select_stats([stat1, stat2, stat3, stat4], df_over30gp)

    # normalize the features
    sc_X = StandardScaler()
    cluster_data = sc_X.fit_transform(cluster_data)

    return cluster_data

def cluster_visualization(stat1, stat2, stat3, stat4, positions):
    cluster_data = prep_data(stat1, stat2, stat3, stat4, positions)
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
    plt.scatter(cluster3.iloc[:, 0], cluster3.iloc[:, 1], s=10, c='yellow', label='Cluster 3')
    plt.xlabel('PCA 1')
    plt.ylabel('PCA 2')
    plt.title('Clusters')
    plt.legend()
    file = 'Cluster_Visualization.png'
    if os.path.isfile(file):
        os.remove(file)  # Opt.: os.system("rm "+strFile)
    plt.savefig(file)
    plt.cla()
    return

def cluster_info(stat1, stat2, stat3, stat4, positions):
    kmeans = KMeans(n_clusters = 4, init = 'k-means++', max_iter = 300, n_init=10, random_state = 0)
    cluster_data = prep_data(stat1,stat2,stat3,stat4, positions)
    y_kmeans = kmeans.fit_predict(cluster_data)
    centroids = kmeans.cluster_centers_
    centroids = pd.DataFrame(centroids)
    centroids.columns = [stat1, stat2, stat3, stat4]
    average_values = pd.Series(centroids.mean())
    cluster_info = centroids.subtract(average_values, axis=1)
    return cluster_info

def bar_graph(datac1, datac2, datac3, datac4):
    # create plot
    fig, ax = plt.subplots()
    index = np.arange(4)

    bar_width = 0.2
    opacity = 0.8

    cluster1 = plt.bar(index, datac1, bar_width,
                    alpha=opacity,
                    color='b',
                    label='Cluster 1')

    cluster2 = plt.bar(index + bar_width, datac2, bar_width,
                    alpha=opacity,
                    color='g',
                    label='Cluster 2')

    cluster3 = plt.bar(index + 2 * bar_width, datac3, bar_width,
                    alpha=opacity,
                    color='r',
                    label='Cluster 3')

    cluster4 = plt.bar(index + 3 * bar_width, datac4, bar_width,
                    alpha=opacity,
                    color='y',
                    label='Cluster 4')


    plt.xlabel('Clusters')
    plt.ylabel('Mean')
    plt.title('Statistic Means for each Cluster')
    plt.xticks(index + bar_width, ('P', 'G', 'A', 'Sh'))
    plt.legend()
    plt.tight_layout()
    file = 'bargraph.png'
    if os.path.isfile(file):
        os.remove(file)
    plt.savefig(file)
    plt.cla()

class Window(QDialog):

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

        self.initialize_input()
        self.stat1.currentTextChanged.connect(self.update_stats)
        self.stat2.currentTextChanged.connect(self.update_stats)
        self.stat3.currentTextChanged.connect(self.update_stats)
        self.stat4.currentTextChanged.connect(self.update_stats)
        self.enterButton.clicked.connect(self.run_alg)

        # connect forwards/defense

        layout = QVBoxLayout()
        layout.addLayout(hboxPosition)
        layout.addLayout(hboxStat1)
        layout.addLayout(hboxStat2)
        layout.addLayout(hboxStat3)
        layout.addLayout(hboxStat4)
        layout.addLayout(hboxEnter)
        self.leftGroupBox.setLayout(layout)

    def initialize_input(self):
        dirpath = os.getcwd()
        df = pd.read_csv(dirpath + '/data/OHL_cluster16_2015-16_to_2017-18.csv')
        stats = df.columns.tolist()
        del stats[0:6]

        statOne = stats[0]
        statTwo = stats[1]
        statThree = stats[2]
        statFour = stats[3]

        stats.remove(statOne)
        stats.remove(statTwo)
        stats.remove(statThree)
        stats.remove(statFour)

        self.stat1.addItem(statOne)
        self.stat2.addItem(statTwo)
        self.stat3.addItem(statThree)
        self.stat4.addItem(statFour)

        self.stat1.addItems(stats)
        self.stat2.addItems(stats)
        self.stat3.addItems(stats)
        self.stat4.addItems(stats)

    def update_stats(self):

        self.stat1.blockSignals(True)
        self.stat2.blockSignals(True)
        self.stat3.blockSignals(True)
        self.stat4.blockSignals(True)
        statOne = str(self.stat1.currentText())
        statTwo = str(self.stat2.currentText())
        statThree = str(self.stat3.currentText())
        statFour = str(self.stat4.currentText())

        self.stat1.clear()
        self.stat2.clear()
        self.stat3.clear()
        self.stat4.clear()

        dirpath = os.getcwd()
        df = pd.read_csv(dirpath + '/data/OHL_cluster16_2015-16_to_2017-18.csv')
        stats = df.columns.tolist()
        del stats[0:6]
        stats.remove(statOne)
        stats.remove(statTwo)
        stats.remove(statThree)
        stats.remove(statFour)

        self.stat1.addItem(statOne)
        self.stat2.addItem(statTwo)
        self.stat3.addItem(statThree)
        self.stat4.addItem(statFour)

        self.stat1.addItems(stats)
        self.stat2.addItems(stats)
        self.stat3.addItems(stats)
        self.stat4.addItems(stats)

        self.stat1.blockSignals(False)
        self.stat2.blockSignals(False)
        self.stat3.blockSignals(False)
        self.stat4.blockSignals(False)

    def run_alg(self):
        if self.allPlayers.isChecked():
            positions = 'All'
        elif self.forwards.isChecked():
            positions = 'Forwards'
        else:
            positions = 'Defense'
        statOne = str(self.stat1.currentText())
        statTwo = str(self.stat2.currentText())
        statThree = str(self.stat3.currentText())
        statFour = str(self.stat4.currentText())
        df = cluster(statOne, statTwo, statThree, statFour, positions)
        stats = cluster_info(statOne, statTwo, statThree, statFour, positions)
        c1stats = stats.loc[:, statOne]
        c2stats = stats.loc[:, statTwo]
        c3stats = stats.loc[:, statThree]
        c4stats = stats.loc[:, statFour]
        bar_graph(c1stats, c2stats, c3stats, c4stats)
        cluster_visualization(statOne, statTwo, statThree, statFour, positions)
        self.update_playerList()
        self.update_pics()


    def update_pics(self):
        bargraph = QPixmap('bargraph.png')
        smaller = bargraph.scaled(600, 600, Qt.KeepAspectRatio, Qt.FastTransformation)
        labelBarGraph = QLabel("Bar Graph")
        labelBarGraph.setPixmap(smaller)
        for i in range(self.layoutBarGraph.count()):
            if type(self.layoutBarGraph.itemAt(i)) != QHBoxLayout:
                self.layoutBarGraph.itemAt(i).widget().close()
        self.layoutBarGraph.addWidget(labelBarGraph)

        seeClusters = QPixmap('Cluster_Visualization.png')
        smaller_pic = seeClusters.scaled(600, 600, Qt.KeepAspectRatio, Qt.FastTransformation)
        labelSeeClusters = QLabel("Cluster Visualization")
        labelSeeClusters.setPixmap(smaller_pic)
        for i in range(self.layoutSeeCluster.count()):
            if type(self.layoutSeeCluster.itemAt(i)) != QHBoxLayout:
                self.layoutSeeCluster.itemAt(i).widget().close()
        self.layoutSeeCluster.addWidget(labelSeeClusters)


    def createRightWidget(self):

        self.rightWidget = QTabWidget()
        playerListTab = QWidget()
        barGraphTab = QWidget()
        seeClusterTab = QWidget()
        clusterWinTab = QWidget()
        self.rightWidget.addTab(playerListTab, "Cluster Player List")
        self.rightWidget.addTab(barGraphTab, "Cluster Statistics")
        self.rightWidget.addTab(seeClusterTab, "Cluster Visualization")
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

        self.initialize_playerList()
        self.clusterChoice1.currentTextChanged.connect(self.update_playerList)

        bargraph = QPixmap('bargraph.png')
        smaller_image = bargraph.scaled(600, 600, Qt.KeepAspectRatio, Qt.FastTransformation)
        labelBarGraph = QLabel("Bar Graph")
        labelBarGraph.setPixmap(smaller_image)
        self.layoutBarGraph = QVBoxLayout()
        self.layoutBarGraph.addWidget(labelBarGraph)
        barGraphTab.setLayout(self.layoutBarGraph)

        clusters = QPixmap('Cluster_Visualization.png')
        smaller_image = clusters.scaled(600, 600, Qt.KeepAspectRatio, Qt.FastTransformation)
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

        clusterVSWin = QPixmap('Cluster_0.png')
        smaller_image = clusterVSWin.scaled(600, 600, Qt.KeepAspectRatio, Qt.FastTransformation)
        labelClusterVSWin = QLabel("Cluster vs Wins")
        labelClusterVSWin.setPixmap(smaller_image)
        self.layoutClusterVSWin = QVBoxLayout()
        self.layoutClusterVSWin.addLayout(hboxClusterChoice2)
        self.layoutClusterVSWin.addWidget(labelClusterVSWin)
        clusterWinTab.setLayout(self.layoutClusterVSWin)

        self.initialize_clusterVSwin()
        self.clusterChoice2.currentTextChanged.connect(self.update_clusterVSwin)

    def initialize_playerList(self):

        self.clusterChoice1.addItems(['0', '1', '2', '3'])

    def update_playerList(self):
        self.playerList.blockSignals(True)
        cluster = str(self.clusterChoice1.currentText())
        self.playerList.clear()

        dirpath = os.getcwd()
        df = pd.read_csv(dirpath + '/data/df_withclusters.csv')
        players = []
        for index, row in df.iterrows():
            if str(row['Cluster']) == str(cluster):
                players.append(row['Team'] + ' - ' + row['Name'])

        self.playerList.addItems(players)
        self.playerList.blockSignals(False)

    def initialize_clusterVSwin(self):
        self.clusterChoice2.addItems(['0', '1', '2', '3'])

    def update_clusterVSwin(self):
        cluster = str(self.clusterChoice2.currentText())
        pic = 'Cluster_' + cluster + '.png'
        pixmap = QPixmap(pic)
        smaller_rink = pixmap.scaled(600, 600, Qt.KeepAspectRatio, Qt.FastTransformation)
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
