import sys, os, re
import pandas as pd
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDateTime, Qt, QTimer, pyqtSlot, QModelIndex
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QToolBar, QInputDialog, QListWidget, QAbstractItemView,
                             QGraphicsPixmapItem)


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
            positions = ['C', 'RW', 'LW', 'D']
        elif self.forwards.isChecked():
            positions = ['C', 'RW', 'LW']
        else:
            positions = ['D']
        statOne = str(self.stat1.currentText())
        statTwo = str(self.stat2.currentText())
        statThree = str(self.stat3.currentText())
        statFour = str(self.stat4.currentText())
        stats = [statOne, statTwo, statThree, statFour]
        #cluster(stats, positions)
        #self.update_pics()


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

        bargraph = QPixmap('simplebarchart.jpg')
        smaller_image = bargraph.scaled(600, 600, Qt.KeepAspectRatio, Qt.FastTransformation)
        labelBarGraph = QLabel("Bar Graph")
        labelBarGraph.setPixmap(smaller_image)
        self.layoutBarGraph = QVBoxLayout()
        self.layoutBarGraph.addWidget(labelBarGraph)
        barGraphTab.setLayout(self.layoutBarGraph)

        clusters = QPixmap('Clusters.png')
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
        self.playerList.addItems(['Ian', 'Willem', 'Hayden', 'Andrew', 'Adam'])

    def update_playerList(self):
        self.playerList.blockSignals(True)
        cluster = str(self.clusterChoice1.currentText())
        self.playerList.clear()

        dirpath = os.getcwd()
        df = pd.read_csv(dirpath + '/data/OHL_cluster16_2015-16_to_2017-18.csv')
        players = []
        for index, row in df.iterrows():
            if str(row['Cluster']) == cluster:
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
