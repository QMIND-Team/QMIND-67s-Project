import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import selection_functions as fctns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def cluster(stat1, stat2, stat3, stat4):

    # prepare data
    data = pd.read_csv('OHL_cluster16_2015-16_to_2017-18.csv')
    data = fctns.divided_by_GP(['HD G', 'HD Sh', 'MD G', 'MD Sh', 'LD G', 'LD Sh'], data)
    df_over30gp_oldindex = data.loc[data['GP'] > 30]
    df_over30gp = df_over30gp_oldindex.reset_index(drop = True)
    cluster_data = fctns.select_stats([stat1,stat2,stat3,stat4], df_over30gp)
    name_team = df_over30gp.iloc[:, [0,2]]
    cluster_data_with_name = pd.concat([name_team, cluster_data], axis = 1)

    #normalize the features
    sc_X = StandardScaler()
    cluster_data = sc_X.fit_transform(cluster_data)

    #run k-means
    kmeans = KMeans(n_clusters = 4, init = 'k-means++', max_iter = 300, n_init=10, random_state = 0)
    y_kmeans = kmeans.fit_predict(cluster_data)
    y_kmeans = pd.DataFrame(y_kmeans)
    fullresults = pd.concat([cluster_data_with_name, y_kmeans], axis = 1)
    fullresults.columns = ['Name','Team', stat1, stat2, stat3, stat4, 'Cluster']
    fullresults.to_csv('df_withclusters.csv')

    return fullresults

clusters = cluster('Sh%', 'A1/GP', 'xG/GP', 'HD Sh')

def prep_data(stat1, stat2, stat3, stat4):
    data = pd.read_csv('OHL_cluster16_2015-16_to_2017-18.csv')
    data = fctns.divided_by_GP(['HD G', 'HD Sh', 'MD G', 'MD Sh', 'LD G', 'LD Sh'], data)
    df_over30gp_oldindex = data.loc[data['GP'] > 30]
    df_over30gp = df_over30gp_oldindex.reset_index(drop=True)
    cluster_data = fctns.select_stats([stat1, stat2, stat3, stat4], df_over30gp)

    # normalize the features
    sc_X = StandardScaler()
    cluster_data = sc_X.fit_transform(cluster_data)

    return cluster_data

def cluster_visulaization(stat1, stat2, stat3, stat4):
    cluster_data = prep_data(stat1, stat2, stat3, stat4)
    pca = PCA(n_components=2)
    cluster_data_2d = pca.fit_transform(cluster_data)
    cluster_data_2d = pd.DataFrame(cluster_data_2d)
    kmeans = KMeans(n_clusters=4, init='k-means++', max_iter=300, n_init=10, random_state=0)
    y_kmeans = kmeans.fit_predict(cluster_data)
    y_kmeans = pd.DataFrame(y_kmeans)
    cluster_data_2d = pd.concat([cluster_data_2d, y_kmeans], axis=1)
    cluster_data_2d.columns = ['PCA 1', 'PCA 2', 'Cluster']

    cluster0 = fctns.select_cluster(0, cluster_data_2d)
    cluster1 = fctns.select_cluster(1, cluster_data_2d)
    cluster2 = fctns.select_cluster(2, cluster_data_2d)
    cluster3 = fctns.select_cluster(3, cluster_data_2d)

    plt.scatter(cluster0.iloc[:, 0], cluster0.iloc[:, 1], s=10, c='red', label='Cluster 0')
    plt.scatter(cluster1.iloc[:, 0], cluster1.iloc[:, 1], s=10, c='green', label='Cluster 1')
    plt.scatter(cluster2.iloc[:, 0], cluster2.iloc[:, 1], s=10, c='blue', label='Cluster 2')
    plt.scatter(cluster3.iloc[:, 0], cluster3.iloc[:, 1], s=10, c='yellow', label='Cluster 3')
    plt.xlabel('PCA 1')
    plt.ylabel('PCA 2')
    plt.title('Clusters')
    plt.legend()
    plt.savefig('Cluster_Visualization.png')
    return

cluster_visulaization('Sh%', 'A1/GP', 'xG/GP', 'HD Sh')




def cluster_info(stat1, stat2, stat3, stat4):
    kmeans = KMeans(n_clusters = 4, init = 'k-means++', max_iter = 300, n_init=10, random_state = 0)
    cluster_data = prep_data(stat1,stat2,stat3,stat4)
    y_kmeans = kmeans.fit_predict(cluster_data)
    centroids = kmeans.cluster_centers_
    centroids = pd.DataFrame(centroids)
    centroids.columns = [stat1, stat2, stat3, stat4]
    average_values = pd.Series(centroids.mean())
    cluster_info = centroids.subtract(average_values, axis=1)
    return cluster_info

info = cluster_info('Sh%', 'A1/GP', 'xG/GP', 'HD Sh')
print(info)

