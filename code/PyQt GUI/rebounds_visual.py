import sys, os
import pandas as pd
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDateTime, Qt, QTimer, pyqtSlot
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QToolBar, QInputDialog, QListWidget, QAbstractItemView, QGraphicsPixmapItem)

class Window(QDialog):

    def __init__(self):
        super().__init__()

        self.createLeftGroupBox()
        self.createRightWidget()
        self.createProgressBar()


        mainLayout = QGridLayout()



        mainLayout.addWidget(self.leftGroupBox, 0, 0, 1, 1)
        mainLayout.addWidget(self.rightWidget, 0, 1, 1, 2)
        mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Rebound Visualization")
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        QApplication.setPalette(QApplication.style().standardPalette())

    def createLeftGroupBox(self):
        self.leftGroupBox = QGroupBox("Select")

        reboundLabel = QLabel("Types of Rebounds")
        hboxRebLabel = QHBoxLayout()
        hboxRebLabel.addStretch()
        hboxRebLabel.addWidget(reboundLabel)
        hboxRebLabel.addStretch()

        self.oneSecondRebounds = QCheckBox("1 Second")
        self.twoSecondRebounds = QCheckBox("2 Second")
        self.threeSecondRebounds = QCheckBox("3 Second")
        hboxRebType = QHBoxLayout()
        hboxRebType.addStretch()
        hboxRebType.addWidget(self.oneSecondRebounds)
        hboxRebType.addWidget(self.twoSecondRebounds)
        hboxRebType.addWidget(self.threeSecondRebounds)
        hboxRebType.addStretch()

        self.oneSecondRebounds.setCheckable(True)
        self.oneSecondRebounds.setChecked(True)
        self.twoSecondRebounds.setCheckable(True)
        self.twoSecondRebounds.setChecked(True)
        self.threeSecondRebounds.setCheckable(True)
        self.threeSecondRebounds.setChecked(True)

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

        leagueLabel = QLabel('League: ')
        self.league = QComboBox()
        hboxLeague = QHBoxLayout()
        hboxLeague.addStretch()
        hboxLeague.addWidget(leagueLabel)
        hboxLeague.addWidget(self.league)
        hboxLeague.addStretch()

        teamLabel = QLabel('Team: ')
        self.team = QComboBox()
        self.allPlayers = QCheckBox("All players")
        hboxTeam = QHBoxLayout()
        hboxTeam.addStretch()
        hboxTeam.addWidget(teamLabel)
        hboxTeam.addWidget(self.team)
        hboxTeam.addWidget(self.allPlayers)
        hboxTeam.addStretch()

        self.playerList = QListWidget()
        hboxPlayers = QHBoxLayout()
        hboxPlayers.addStretch()
        hboxPlayers.addWidget(self.playerList)
        hboxPlayers.addStretch()

        self.initialize_values()
        self.allPlayers.toggled.connect(self.playerList.setDisabled)
        self.playerList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.start.currentTextChanged.connect(self.start_change)
        self.league.currentTextChanged.connect(self.league_change)
        self.team.currentTextChanged.connect(self.team_change)

        shots = QRadioButton('Shots')
        goals = QRadioButton('Goals')
        royalroad = QCheckBox("Royal Road")
        hboxShots = QHBoxLayout()
        hboxShots.addStretch()
        hboxShots.addWidget(shots)
        hboxShots.addWidget(goals)
        hboxShots.addWidget(royalroad)
        hboxShots.addStretch()

        shots.setCheckable(True)
        shots.setChecked(True)
        goals.setCheckable(True)
        royalroad.setCheckable(True)

        layout = QVBoxLayout()
        layout.addLayout(hboxRebLabel)
        layout.addLayout(hboxRebType)
        layout.addLayout(hboxYear)
        layout.addLayout(hboxLeague)
        layout.addLayout(hboxTeam)
        layout.addLayout(hboxPlayers)
        layout.addLayout(hboxShots)
        self.leftGroupBox.setLayout(layout)

    def initialize_values(self):
        years = ['2018-19', '2017-18', '2016-17', '2015-16', '2014-15', '2013-14', '2012-13', '2011-12', '2010-11',
                 '2009-10', '2008-09', '2007-08', '2006-07', '2005-06', '2004-05', '2003-04', '2002-03', '2001-02',
                 '2000-01', '1999-00', '1998-99', '1997-98']
        leagues = ['OHL', 'AHL', 'QMJHL', 'USHL', 'WHL']
        ohl = ["Ottawa 67's", 'Windsor Spitfires', 'Sudbury Wolves', 'Sault Ste. Marie Greyhounds', 'Sarnia Sting', 'Saginaw Spirit',
               'Peterborough Petes', 'Owen Sound Attack',  'Oshawa Generals', 'North Bay Battalion',
               'Niagara IceDogs', 'Mississauga Steelheads', 'London Knights', 'Kitchener Rangers',
               'Kingston Frontenacs', 'Hamilton Bulldogs', 'Guelph Storm', 'Flint Firebirds', 'Erie Otters',
               'Barrie Colts']
        ottawa = ['Tye Felhaber', 'Austen Keating', 'Sasha Chmelevski', 'Marco Rossi', 'Noel Hoefenmayer',
                  'Kody Clark', 'Sam Bitten', 'Mitchell Hoelscher', 'Jack Quinn', 'Graeme Clarke', 'Kevin Bahl',
                  'Merrick Rippon', 'Quinn Yule', 'Hudson Wilson', 'Nikita Okhotyuk', 'Lucas Peric',
                  'Cameron Tolnai', 'Alec Belanger', 'Matthew Maggio', 'Yanic Crete', 'Jesse Dick',
                  'William Sirman', 'Felix - Antoine Tourigny']
        self.start.addItems(years)
        self.end.addItems(years)
        self.league.addItems(leagues)
        self.team.addItems(ohl)
        self.playerList.addItems(ottawa)

    def start_change(self):
        self.end_restrict()
        self.league_change()
        self.team_change()

    def end_restrict(self):
        start = str(self.start.currentText())
        self.end.blockSignals(True)
        self.end.clear()
        start_year = int(start[0:4])
        years = []
        for year in range(start_year, 2019):
            years.append(str(year) + '-' + str(year + 1)[2:4])
        years = list(reversed(years))
        self.end.addItems(years)
        self.end.blockSignals(False)

    def league_change(self):
        self.team.blockSignals(True)
        self.team.clear()
        self.team.blockSignals(False)
        start = str(self.start.currentText())
        end = str(self.end.currentText())
        league = str(self.league.currentText())
        dirpath = os.getcwd()

        if start == end:
            teams_file = league + '_' + start + '_teams.csv'
        else:
            teams_file = league + '_' + start + '_to_' + end + '_teams.csv'
        teams_df = pd.read_csv(dirpath + '/../KMeans_Project/OHL-webscraper/data/' + teams_file)
        teams = []
        for index, row in teams_df.iterrows():
            teams.append(row['Name'])
        self.team.addItems(teams)


    def team_change(self):
        ohl_dict = {"Ottawa 67's": 'OTT', 'Windsor Spitfires': 'WSR', 'Sudbury Wolves': 'SBY',
                    'Sault Ste. Marie Greyhounds': 'SSM', 'Sarnia Sting': 'SAR', 'Saginaw Spirit': 'SAG',
                    'Peterborough Petes': 'PBO', 'Owen Sound Attack': 'OS',  'Oshawa Generals': 'OSH',
                    'North Bay Battalion': 'NB', 'Niagara IceDogs': 'NIAG', 'Mississauga Steelheads': 'MISS',
                    'London Knights': 'LDN', 'Kitchener Rangers': 'KIT', 'Kingston Frontenacs': 'KGN',
                    'Hamilton Bulldogs': 'HAM', 'Guelph Storm': 'GUE', 'Flint Firebirds': 'FLNT', 'Erie Otters': 'ER',
                    'Barrie Colts': 'BAR'}
        ahl_dict = {'Bakersfield Condors': 'BAK', 'Belleville Senators': 'BEL', 'Binghamton Devils': 'BNG',
                    'Bridgeport Sound Tigers': 'BRI', 'Charlotte Checkers': 'CHA', 'Chicago Wolves': 'CHI',
                    'Cleveland Monsters': 'CLE', 'Colorado Eagles': 'COL', 'Grand Rapids Griffins': 'GR',
                    'Hartford Wolf Pack': 'HFD', 'Hershey Bears': 'HER', 'Iowa Wild': 'IA', 'Laval Rocket': 'LAV',
                    'Lehigh Valley Phantoms': 'LV', 'Manitoba Moose': 'MB', 'Milwaukee Admirals': 'MIL',
                    'Ontario Reign': 'ONT', 'Providence Bruins': 'PRO', 'Rochester Americans': 'ROC',
                    'Rockford IceHogs': 'RFD', 'San Antonio Rampage': 'SA', 'San Diego Gulls': 'SD',
                    'San Jose Barracuda': 'SJ', 'Springfield Thunderbirds': 'SPR', 'Stockton Heat': 'STK',
                    'Syracuse Crunch': 'SYR', 'Texas Stars': 'TEX', 'Toronto Marlies': 'TOR',
                    'Tucson Roadrunners': 'TUC', 'Utica Comets': 'UTI', 'Wilkes-Barre/Scranton Penguins': 'WBS'}
        self.playerList.clear()
        start = str(self.start.currentText())
        end = str(self.end.currentText())
        league = str(self.league.currentText())
        team = str(self.team.currentText())
        if league == 'OHL':
            team_short = ohl_dict[team]
        if league == 'AHL':
            team_short = ahl_dict[team]
        dirpath = os.getcwd()

        if start == end:
            players_file = league + '_' + start + '_skaters.csv'
        else:
            players_file = league + '_' + start + '_to_' + end + '_skaters.csv'

        df = pd.read_csv(dirpath + '/../KMeans_Project/OHL-webscraper/data/' + players_file)
        players = []
        for index, row in df.iterrows():
            if row['Team'] == team_short:
                players.append(row['Name'])
        self.playerList.addItems(players)

    def createRightWidget(self):
        self.rightWidget = QTabWidget()

        tab1 = QWidget()
        hbox = QHBoxLayout()
        rinkplot = QPixmap('Plot-122.png')
        smaller_rink = rinkplot.scaled(600, 600, Qt.KeepAspectRatio, Qt.FastTransformation)
        label = QLabel("Rink Plot")
        label.setPixmap(smaller_rink)
        hbox.addWidget(label)
        tab1.setLayout(hbox)
        tab2 = QWidget()

        self.rightWidget.addTab(tab1, "Plot")
        self.rightWidget.addTab(tab2, "Heat Map")

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) / 100)

class QComboBox(QComboBox):
    def combobox_changed(self):
        print('ya')
        print(str(self.currentText()))
        return str(self.currentText())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    gallery = Window()
    gallery.show()
    sys.exit(app.exec_())
