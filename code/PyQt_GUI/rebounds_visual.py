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

        leagueLabel = QLabel('League: ')
        self.league = QComboBox()
        hboxLeague = QHBoxLayout()
        hboxLeague.addStretch()
        hboxLeague.addWidget(leagueLabel)
        hboxLeague.addWidget(self.league)
        hboxLeague.addStretch()

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

        teamLabel = QLabel('Team: ')
        self.team = QComboBox()
        self.allPlayers = QCheckBox("All players")
        hboxTeam = QHBoxLayout()
        hboxTeam.addStretch()
        hboxTeam.addWidget(teamLabel)
        hboxTeam.addWidget(self.team)
        hboxTeam.addWidget(self.allPlayers)
        hboxTeam.addStretch()

        self.playerList = QComboBox()
        hboxPlayers = QHBoxLayout()
        hboxPlayers.addStretch()
        hboxPlayers.addWidget(self.playerList)
        hboxPlayers.addStretch()

        self.stat_menu = QComboBox()
        self.initialize_values()
        self.allPlayers.toggled.connect(self.playerList.setDisabled)
        #self.playerList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.start.currentTextChanged.connect(self.start_year_change)
        self.end.currentTextChanged.connect(self.end_year_change)
        self.league.currentTextChanged.connect(self.league_change)
        self.team.currentTextChanged.connect(self.team_change)
        self.playerList.currentTextChanged.connect(self.player_change)

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
        layout.addLayout(hboxLeague)
        layout.addLayout(hboxYear)
        layout.addLayout(hboxTeam)
        layout.addLayout(hboxPlayers)
        layout.addLayout(hboxShots)
        self.leftGroupBox.setLayout(layout)

    def initialize_values(self):
        leagues = ['OHL', 'AHL', 'QMJHL', 'USHL', 'WHL']
        self.league.addItems(leagues)

        # update start years based on league
        self.update_start_years()

        # update end years based on start years
        self.update_end_year()

        # update teams based on league, start and end years
        self.update_teams()

        # update players based on league, start and end years, and team
        self.update_players()

        # update stat categories based on league and start and end years
        self.update_categories()

        # update stat based on league, start and end years, player and stat category
        self.update_stat()

    def league_change(self):
        # update start years based on league
        self.update_start_years()

        # update end years based on start years
        self.update_end_year()

        # update teams based on league, start and end years
        self.update_teams()

        # update players based on league, start and end years, and team
        self.update_players()

        # update stat categories based on league, and start and end years
        self.update_categories()

        # update stat based on league, start and end years, player and stat category
        self.update_stat()

    def start_year_change(self):
        # update end years based on start year
        self.update_end_year()

        # update players based on league, start and end years, and team
        self.update_players()

        # update stat categories based on league, and start and end years
        self.update_categories()

        # update stat based on league, start and end years, player and stat category
        self.update_stat()

    def end_year_change(self):
        # update players based on league, start and end years, and team
        self.update_players()

        # update stat categories based on league, and start and end years
        self.update_categories()

        # update stat based on league, start and end years, player and stat category
        self.update_stat()

    def team_change(self):
        # update players based on league, start and end years, and team
        self.update_players()

        # update stat categories based on league, and start and end years
        self.update_categories()

        # update stat based on league, start and end years, player and stat category
        self.update_stat()

    def player_change(self):
        # update stat categories based on league, and start and end years
        self.update_categories()

        # update stat based on league, start and end years, player and stat category
        self.update_stat()

    def category_change(self):
        # update stat based on league, start and end years, player and stat category
        self.update_stat()

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

    def update_teams(self):
        # update teams based on league, start and end years
        league = str(self.league.currentText())
        start = str(self.start.currentText())
        end = str(self.end.currentText())
        if start == end:
            teams_file = league + '_' + start + '_teams.csv'
        else:
            teams_file = league + '_' + start + '_to_' + end + '_teams.csv'

        dirpath = os.getcwd()
        teams_df = pd.read_csv(dirpath + '/../OHL-webscraper/data/' + teams_file)
        teams = []
        for index, row in teams_df.iterrows():
            teams.append(row['Name'])
        teams.sort()
        self.team.blockSignals(True)
        self.team.clear()
        if league == 'OHL':
            top = "Ottawa 67's"
            self.team.addItem(top)
            teams.remove(top)
        self.team.addItems(teams)
        self.team.blockSignals(False)

    def update_players(self):
        # update players based on league, start and end years, and team
        ohl_dict = {"Ottawa 67's": 'OTT', 'Windsor Spitfires': 'WSR', 'Sudbury Wolves': 'SBY',
                    'Sault Ste. Marie Greyhounds': 'SSM', 'Sarnia Sting': 'SAR', 'Saginaw Spirit': 'SAG',
                    'Peterborough Petes': 'PBO', 'Owen Sound Attack': 'OS', 'Oshawa Generals': 'OSH',
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
        self.playerList.blockSignals(True)
        self.playerList.clear()
        start = str(self.start.currentText())
        end = str(self.end.currentText())
        league = str(self.league.currentText())
        team = str(self.team.currentText())
        if start == end:
            players_file = league + '_' + start + '_skaters.csv'
        else:
            players_file = league + '_' + start + '_to_' + end + '_skaters.csv'
        dirpath = os.getcwd()
        df = pd.read_csv(dirpath + '/../OHL-webscraper/data/' + players_file)
        if league == 'OHL':
            team_short = ohl_dict[team]
        if league == 'AHL':
            team_short = ahl_dict[team]
        players = []
        positions = []
        for index, row in df.iterrows():
            on_teams = re.match('^[^/]+', row['Team']).group()
            if on_teams.count(team_short) > 0:
                players.append(row['Name'])
                positions.append(row['Pos'])
        for index in range(0, len(players)):
            players[index] = positions[index] + ' - ' + players[index]
        self.playerList.addItems(players)
        """
        matching_items = self.playerList.findItems(players[0], Qt.MatchExactly)
        for item in matching_items:
            self.playerList.setCurrentItem(item)
        """
        self.playerList.blockSignals(False)

    def update_categories(self):
        # update stat categories based on league, and start and end years
        start = str(self.start.currentText())
        end = str(self.end.currentText())
        league = str(self.league.currentText())

        if start == end:
            players_file = league + '_' + start + '_skaters.csv'
        else:
            players_file = league + '_' + start + '_to_' + end + '_skaters.csv'
        dirpath = os.getcwd()
        df = pd.read_csv(dirpath + '/../OHL-webscraper/data/' + players_file)
        cols = []
        for column in df:
            cols.append(column)
        cols.remove('Name')
        cols.remove('Pos')
        cols.remove('Team')
        cols.pop(0)
        self.stat_menu.blockSignals(True)
        self.stat_menu.clear()
        self.stat_menu.addItems(cols)
        self.stat_menu.blockSignals(False)

    def update_stat(self):
        # update stat based on league, start and end years, player and stat category
        start = str(self.start.currentText())
        end = str(self.end.currentText())
        league = str(self.league.currentText())
        if start == end:
            players_file = league + '_' + start + '_skaters.csv'
        else:
            players_file = league + '_' + start + '_to_' + end + '_skaters.csv'
        dirpath = os.getcwd()
        df = pd.read_csv(dirpath + '/../OHL-webscraper/data/' + players_file)

        player = str(self.playerList.currentText())
        player_name = re.search('(?<= - ).*$', player).group()
        cat = str(self.stat_menu.currentText())
        for index, rows in df.iterrows():
            if df.loc[index, 'Name'] == player_name:
                print(df.loc[index, cat])

    def createRightWidget(self):

        self.rightWidget = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()
        self.rightWidget.addTab(tab1, "Plot")
        self.rightWidget.addTab(tab2, "Heat Map")

        hboxStats = QHBoxLayout()
        hboxStats.addStretch()
        label = QLabel("Stats")
        hboxStats.addWidget(label)
        hboxStats.addWidget(self.stat_menu)
        hboxStats.addStretch()

        self.stat_menu.currentTextChanged.connect(self.category_change)


        layout = QVBoxLayout()
        layout.addLayout(hboxStats)
        tab1.setLayout(layout)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    gallery = Window()
    gallery.show()
    sys.exit(app.exec_())
