import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import selection_functions as fctns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

OHL = pd.read_csv('2018-19_OHL_Skaters.csv')
QMJHL = pd.read_csv('2018-19_QMJHL_Skaters.csv')

# shaping the datasets correctly and joining them together
QMJHL_1 = QMJHL.iloc[:, 0:21]
QMJHL_2 = QMJHL.iloc[:, 38:]
QMJHL = pd.concat([QMJHL_1, QMJHL_2], axis = 1)
fulldataset = OHL.append(QMJHL)
fulldataset = fulldataset.iloc[:,1:]

# now, want to edit the data set for our purposes
fulldataset = fctns.divided_by_GP(['HD G', 'HD Sh', 'MD G', 'MD Sh', 'LD G', 'LD Sh'], fulldataset)
df_over30gp_oldindex = fulldataset.loc[fulldataset['GP'] > 30]
df_over30gp = df_over30gp_oldindex.reset_index(drop = True)
cluster_data = fctns.select_stats(['Sh%','A1/GP','xG/GP','HD Sh'], df_over30gp)
name_team = df_over30gp.iloc[:, [0,2]]
cluster_data_with_name = pd.concat([name_team, cluster_data], axis = 1)

#normalize the features
sc_X = StandardScaler()
cluster_data = sc_X.fit_transform(cluster_data)


# now going to apply "elbow method" to determine ideal number of clusters
'''
    wcss = []
    for i in range (1,11):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', max_iter = 300, n_init = 10)
    kmeans.fit(cluster_data)
    wcss.append(kmeans.inertia_)
    plt.plot(range(1,11),wcss)
    plt.title('Number of clusters')
    plt.ylabel('WCSS')
    #plt.show()
    '''

# this shows that 3-4 clusters is ideal, I will proceed with 4 clusters
# fitting the data with KMeans
kmeans = KMeans(n_clusters = 4, init = 'k-means++', max_iter = 300, n_init=10, random_state = 0)
y_kmeans = kmeans.fit_predict(cluster_data)
y_kmeans = pd.DataFrame(y_kmeans)
fullresults = pd.concat([cluster_data_with_name, y_kmeans], axis = 1)
fullresults.columns = ['Name','Team','Sh%', 'A1/GP', 'xG/GP', 'HD Sh', 'Cluster']


# at this point we have clustered every player's data
# we now want to determine what percentage of players are in each cluster on each team
all_teams_clusters = pd.DataFrame([])

ott = fctns.select_team('OTT', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Ottawa']), ott, all_teams_clusters)

niag = fctns.select_team('NIAG', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Niagra']), niag, all_teams_clusters)

nb = fctns.select_team('NB', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['North Bay']), nb, all_teams_clusters)

kgn = fctns.select_team('KGN', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Kingston']), kgn, all_teams_clusters)

ldn = fctns.select_team('LDN', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['London']), ldn, all_teams_clusters)

os = fctns.select_team('OS', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Owen Sound']), os, all_teams_clusters)

ssm = fctns.select_team('SSM', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Sault Saint Marie']), ssm, all_teams_clusters)

ham = fctns.select_team('HAM', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Hamilton']), ham, all_teams_clusters)

osh = fctns.select_team('OSH', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Oshawa']), osh, all_teams_clusters)

sar = fctns.select_team('SAR', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Sarnia']), sar, all_teams_clusters)

gue = fctns.select_team('GUE', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Guelph']), gue, all_teams_clusters)

er = fctns.select_team('ER', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Erie']), er, all_teams_clusters)

miss = fctns.select_team('MISS', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Missisauga']), miss, all_teams_clusters)

bar = fctns.select_team('BAR', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Barrie']), bar, all_teams_clusters)

sag = fctns.select_team('SAG', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Saginaw']), sag, all_teams_clusters)

kit = fctns.select_team('KIT', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Kitchener']), kit, all_teams_clusters)

flnt = fctns.select_team('FLNT', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Flint']), flnt, all_teams_clusters)

pbo = fctns.select_team('PBO', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Peterborough']), pbo, all_teams_clusters)

sby = fctns.select_team('SBY', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Sudbury']), sby, all_teams_clusters)

wsr = fctns.select_team('WSR', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Windsor']), wsr, all_teams_clusters)

bac = fctns.select_team('BAC', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Baie-Comeau']), niag, all_teams_clusters)

rim = fctns.select_team('RIM', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Rimouski']), rim, all_teams_clusters)

dru = fctns.select_team('DRU', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Drummondville']), dru, all_teams_clusters)

rou = fctns.select_team('ROU', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Rouyn-Noranda']), rou, all_teams_clusters)

mon = fctns.select_team('MON', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Moncton']), mon, all_teams_clusters)

hal = fctns.select_team('HAL', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Halifax']), hal, all_teams_clusters)

bat = fctns.select_team('BAT', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Acadie-Bathurst']), bat, all_teams_clusters)

cha = fctns.select_team('CHA', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Charlottetown']), cha, all_teams_clusters)

blb = fctns.select_team('BLB', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Blainville-Boisbriand']), blb, all_teams_clusters)

cap = fctns.select_team('CAP', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Cape Breton']), cap, all_teams_clusters)

she = fctns.select_team('SHE', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Sherbrooke']), she, all_teams_clusters)

vic = fctns.select_team('VIC', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Victoriaville']), vic, all_teams_clusters)

chi = fctns.select_team('CHI', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Chicoutimi']), chi, all_teams_clusters)

sha = fctns.select_team('SHA', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Shawinigan']), sha, all_teams_clusters)

vdo = fctns.select_team('VDO', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(["Val-d'Or"]), vdo, all_teams_clusters)

gat = fctns.select_team('GAT', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Gatineau']), gat, all_teams_clusters)

que = fctns.select_team('QUE', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Quebec']), que, all_teams_clusters)

snb = fctns.select_team('SNB', fullresults)
all_teams_clusters = fctns.add_team2df(pd.DataFrame(['Saint John']), snb, all_teams_clusters)

all_teams_clusters.columns = ['Team', 'Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 3']
all_teams_clusters = all_teams_clusters.reset_index(drop = True)
#print(all_teams_clusters)

#now we reproduce the all_teams_clusters but with percentages in each
percent_each_cluster = fctns.find_percentages(all_teams_clusters)

#now we will add a column with the team's points and split data into OHL and QMJHL
points = pd.DataFrame([89,73,54,26,83,59,79,57,75,53,68,49,61,50,76,56,26,53,71,52, 83, 77, 88, 95, 69,85,17 ,67,40, 71, 66, 50, 65, 32, 43, 45, 55, 28])
df_with_wins = pd.concat([percent_each_cluster, points], axis=1)
df_with_wins.columns = ['Team', 'Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 3', 'Points']
OHL_results = df_with_wins.iloc[0:20, :]
QMJHL_results = df_with_wins.iloc[20:, :]
all_team_results = df_with_wins.sort_values('Points')
OHL_results = OHL_results.sort_values('Points')
QMJHL_results = QMJHL_results.sort_values('Points')

#now, I am looking to gain more information about each cluster
centroids = kmeans.cluster_centers_
centroids = pd.DataFrame(centroids)
centroids.columns = ['Sh %', 'A1/GP', 'xG/GP', 'HD Sh']
average_values = pd.Series(centroids.mean())
cluster_info = centroids.subtract(average_values, axis = 1)

#now going to produce a list of players in each cluster
OHL_playerresults = fullresults.iloc[0:372,:]
QMJHL_playerresults = fullresults.iloc[372:,:]


OHL_cluster0players = fctns.select_cluster(0, OHL_playerresults)
#QMJHL_cluster0players = fctns.select_cluster('Cluster 0', QMJHL_playerresults)
OHL_cluster1players = fctns.select_cluster(1, OHL_playerresults)
#QMJHL_cluster1players = fctns.select_cluster('Cluster 1', QMJHL_playerresults)
OHL_cluster2players = fctns.select_cluster(2, OHL_playerresults)
#QMJHL_cluster2players = fctns.select_cluster('Cluster 2', QMJHL_playerresults)
OHL_cluster3players = fctns.select_cluster(3, OHL_playerresults)
#QMJHL_cluster3players = fctns.select_cluster('Cluster 3', QMJHL_playerresults)

OHL_cluster0players = OHL_cluster0players.iloc[:,0]
OHL_cluster1players = OHL_cluster1players.iloc[:,0]
OHL_cluster2players = OHL_cluster2players.iloc[:,0]
OHL_cluster3players = OHL_cluster3players.iloc[:,0]
'''
    cluster_info.to_csv('Cluster_Info.csv')
    all_team_results.to_csv('Team Results.csv')
    OHL_cluster0players.to_csv('Cluster_0_players.csv')
    OHL_cluster1players.to_csv('Cluster_1_players.csv')
    OHL_cluster2players.to_csv('Cluster_2_players.csv')
    OHL_cluster3players.to_csv('Cluster_3_players.csv')
    '''
'''
    #now we will visualize the data
    X_0 = OHL_results.loc[:, 'Cluster 0']
    X_1 = OHL_results.loc[:, 'Cluster 1']
    X_2 = OHL_results.loc[:, 'Cluster 2']
    X_3 = OHL_results.loc[:, 'Cluster 3']
    Y = OHL_results.loc[:, 'Points']
    plt.plot(X_0,Y, 'bo')
    plt.title('Cluster 0 - Points Relationship')
    plt.ylabel('Team Points')
    plt.xlabel('Percentage of Players in Cluster 0')
    plt.axis([0,40,15,95])
    z = np.polyfit(X_0, Y, 1)
    p = np.poly1d(z)
    plt.plot(X_0,p(X_0),"r--")
    plt.show()
    '''

#this section is now focused on visualizing the data in 2D

pca = PCA(n_components=2)
cluster_data_2d = pca.fit_transform(cluster_data)
explained_variance = pca.explained_variance_ratio_
cluster_data_2d = pd.DataFrame(cluster_data_2d)
cluster_data_2d = pd.concat([cluster_data_2d, y_kmeans], axis = 1)
cluster_data_2d.columns = ['PCA 1', 'PCA 2', 'Cluster']

cluster0 = fctns.select_cluster(0, cluster_data_2d)
cluster1 = fctns.select_cluster(1, cluster_data_2d)
cluster2 = fctns.select_cluster(2, cluster_data_2d)
cluster3 = fctns.select_cluster(3, cluster_data_2d)


plt.scatter(cluster0.iloc[:, 0], cluster0.iloc[:,1], s = 10, c = 'red', label = 'Cluster 0')
plt.scatter(cluster1.iloc[:, 0], cluster1.iloc[:,1], s = 10, c = 'green', label = 'Cluster 1')
plt.scatter(cluster2.iloc[:, 0], cluster2.iloc[:,1], s = 10, c = 'blue', label = 'Cluster 2')
plt.scatter(cluster3.iloc[:, 0], cluster3.iloc[:,1], s = 10, c = 'yellow', label = 'Cluster 3')
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')
plt.title('Clusters')
plt.legend()
plt.show()
