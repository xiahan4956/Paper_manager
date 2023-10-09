
import pandas as pd

import os
import sys
sys.path.append(os.getcwd())

import networkx as nx
import community as community_louvain


def get_keyword_network_indicator(co_occurrence_matrix):
    '''
    In order to know the importance of keyword,
    Build the graph and calculate the centrality of the graph
    '''
    
    # First,build network graph
    G = build_g(co_occurrence_matrix)

    # Then,use Louvain to find community.It is for finding same group of keyword
    community_partition = community_louvain.best_partition(G, resolution=1.0)
       
    # Next,use networkx to calculate the various centrality.
    # The most important is betweenness_centrality,which represent the brige of the network.
    degree_centrality = nx.degree_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)

    # Save the betweenness,keyword_frequency,community_partition to dataframe
    df_degree_centrality = pd.DataFrame.from_dict(degree_centrality, orient='index', columns=['degree_centrality'])
    df_closeness_centrality = pd.DataFrame.from_dict(closeness_centrality, orient='index', columns=['closeness_centrality'])
    df_betweenness_centrality = pd.DataFrame.from_dict(betweenness_centrality, orient='index', columns=['betweenness_centrality'])
    df_communities = pd.DataFrame.from_dict(community_partition, orient='index', columns=['community'])
    df_frequency = pd.DataFrame(co_occurrence_matrix.sum(axis = 1)).rename(columns={0: 'frequency'})
    df = pd.concat([df_degree_centrality, df_closeness_centrality, df_betweenness_centrality, df_communities, df_frequency], axis=1)

    # Finally,rank the centrality
    df["betweenness_centrality_rank"] = df["betweenness_centrality"].rank(ascending=False, pct=True,method='dense')
    df["betweenness_centrality_rank"] = df["betweenness_centrality_rank"].round(2)
    df["degree_centrality_rank"] = df["degree_centrality"].rank(ascending=False, pct=True,method='dense')
    df["degree_centrality_rank"] = df["degree_centrality_rank"].round(2)
    df["closeness_centrality_rank"] = df["closeness_centrality"].rank(ascending=False, pct=True,method='dense')
    df["closeness_centrality_rank"] = df["closeness_centrality_rank"].round(2)

    return df 


def build_g(co_occurrence_matrix):
    '''Build the network graph from co_occurrence_matrix'''
    
    G = nx.from_numpy_array(co_occurrence_matrix.values)
    labels = dict(enumerate(co_occurrence_matrix.columns))
    G = nx.relabel_nodes(G, labels)
    print("build_g done")
    
    return G





