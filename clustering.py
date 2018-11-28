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

def create_cluster_labels(df: pd.DataFrame, num_groups):
    """
    Clusters a dataframe, adds the cluster labels to it and returns it
    """
    np.random.seed(0)

    agg_clust = AgglomerativeClustering(n_clusters=num_groups,
                                        linkage="ward")
    X = df
    X = StandardScaler().fit_transform(X)
    agg_clust.fit(X)
    labels = list(agg_clust.labels_)
    return labels


def plot_clustering(pca_df_with_labels):
    """
    Plots the results of the PCA, colored by
    :return:
    """
    # Basic set up
    alpha = 0.6
    fig = plt.Figure()

    # Plotting
    sns.lmplot(x="PC 1",
               y="PC 2",
               data=pca_df_with_labels,
               hue="Clustering",
               fit_reg=False,
               legend=False,
               #palette="inferno",
               scatter_kws={"s": 10})
    ax = plt.gca()


    # Make plot nicer by removing the borders
    ax.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Add correct descriptions
    ax.set_title("Cluster n = 10", alpha=alpha)
    ax.set_ylabel("PC 2", alpha=alpha)
    ax.set_xlabel("PC 1", alpha=alpha)
    ax.grid(color="grey", alpha=alpha)
    plt.setp(ax.get_yticklabels(), alpha=alpha)
    plt.setp(ax.get_xticklabels(), alpha=alpha)

    # Save the plot
    fig.tight_layout()
    plt.savefig("clusters.png",  bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    variance = 0.8
    pca_df = pca.pca_signatures(variance)
    labels = pd.DataFrame(create_cluster_labels(pca_df, 10))
    labels.index = pca_df.index
    pca_df_with_labels = pd.concat([pca_df, labels], axis=1)
    pca_df_with_labels.columns = ["PC 1", "PC 2", "Clustering"]
    print(pca_df_with_labels.describe())
    plot_clustering(pca_df_with_labels)
    