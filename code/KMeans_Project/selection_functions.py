import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
dataset = pd.read_csv('2018-19_OHL_Skaters.csv')

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







