# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 13:27:32 2018

@author: Florian Ulrich Jehn
"""
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import calinski_harabaz_score
from sklearn.cluster import AgglomerativeClustering
import numpy as np
import pca
import seaborn as sns
import matplotlib.pyplot as plt
import read_attributes_signatures
import os
import sys
import scipy



def create_cluster_labels(df: pd.DataFrame, num_groups, return_score=False):
    """
    Clusters a dataframe, adds the cluster labels to it and returns it
    """
    np.random.seed(0)

    agg_clust = AgglomerativeClustering(n_clusters=num_groups,
                                        linkage="ward")
    X = df.copy(deep=True)
    X = StandardScaler().fit_transform(X)
    agg_clust.fit(X)
    labels = pd.DataFrame(list(agg_clust.labels_))
    labels.index = df.index
    labels.columns = ["Cluster"]
    if return_score:
        return agg_clust.connectivity
    else:
        return labels


def biplot(pca_df_with_labels,pca_object):
    """
    Plots the clustered PCA
    """
    colors= ["#e6194B", "#f58231", "#fffac8", "#bfef45",  "#3cb44b", 
             "#42d4f4", "#4363d8", "#911eb4", "#a9a9a9", "#ffffff"]
    # Basic set up
    alpha = 0.6
    fig = plt.Figure()
    pca_df_with_labels["Cluster"] = pca_df_with_labels["Cluster"] + 1

    # Plotting
    plot = sns.lmplot(x="PC 1",
               y="PC 2",
               data=pca_df_with_labels,
               hue="Cluster",
               fit_reg=False,
               palette=colors,#"gist_earth",
               scatter_kws={"s": 30, "alpha":1, "edgecolor":"black", "linewidth":0.3, "zorder":2})
    ax = plt.gca()
    # Names of the factors
    factors = ['Mean annual discharge', 'Mean winter discharge', 'Mean half-flow date',
       'Q95 (high flow)', 'Runoff ratio', 'Mean summer discharge']
    # using scaling factors to make the arrows
    arrow_size, text_pos = 7.0, 8.0,
    # Add the arrows
    for i, v in enumerate(pca_object.components_.T):
        ax.arrow(0, 0, arrow_size*v[0], arrow_size*v[1], head_width=0.2, head_length=0.2, linewidth=1.5, color="grey", zorder=3)
        # Fix the overlapping text
        if factors[i] == "Mean annual discharge":
            ax.text(v[0]*text_pos, v[1]*text_pos + 0.2, factors[i], color='black', ha='center', va='center', fontsize=9, zorder=4)
        elif factors[i] == "Q95 (high flow)":
            ax.text(v[0]*text_pos, v[1]*text_pos -0.2, factors[i], color='black', ha='center', va='center', fontsize=9, zorder=4)
        else:
            ax.text(v[0]*text_pos, v[1]*text_pos, factors[i], color='black', ha='center', va='center', fontsize=9, zorder=4)

    # Make plot nicer by removing the borders
    ax.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Add correct descriptions
    ax.set_ylabel("PC 2", alpha=alpha)
    ax.set_xlabel("PC 1", alpha=alpha)
    ax.grid(color="grey", alpha=alpha, zorder=4)
    plt.setp(ax.get_yticklabels(), alpha=alpha)
    plt.setp(ax.get_xticklabels(), alpha=alpha)
    plt.ylim(-2.5, 7)
    ax.tick_params(axis=u'both', which=u'both',length=0)
    legend = plot._legend
    for text in legend.get_texts():
        text.set_color("grey")
    legend.set_title("Catchment\n   Cluster")
    legend.get_title().set_color("grey")

    # Save the plot
    fig.tight_layout()
    plt.savefig("clusters.png", dpi=200, bbox_inches="tight")


def save_clusters_with_loc(labels):
    # Set the cwd to the directory of the file
    file_loc = os.path.dirname(sys.argv[0])
    os.chdir(file_loc)
    # Read in the files
    os.chdir(os.pardir + os.sep + "data" +  os.sep + "camels_attributes_v2.0")
    # Topo
    topo = pd.read_table("camels_topo.txt", sep=";", index_col=0)
    labels_loc = pd.merge(topo[["gauge_lat", "gauge_lon"]], labels, left_index=True, right_index=True, how="inner")
    os.chdir(file_loc)
    labels_loc.to_csv("labels_loc.txt")
    
    
def elbow(min_clusters, max_clusters, df):
    """Creates an elbow plot for a dataframe to determine the number
    of clusters"""
    score_dict = {}
    for num_clusters in range(min_clusters, max_clusters+1):
        labels = create_cluster_labels(df, num_clusters)
        score_dict[num_clusters] = calinski_harabaz_score(df, labels)
    metrics = pd.DataFrame.from_dict(score_dict, orient="index")
    metrics.plot()
        
    
    

if __name__ == "__main__":
    variance = 0.8
    pca_df = pca.pca_signatures(variance)
    metrics = elbow(5, 20, pca_df)
    labels = create_cluster_labels(pca_df, 10)
#    save_clusters_with_loc(labels)
    pca_df_with_labels = pd.concat([pca_df, labels], axis=1)
#    print(pca_df_with_labels.describe())
#    pca_object = pca.pca_signatures(0.80, return_pca=True)
#    biplot(pca_df_with_labels, pca_object)
    