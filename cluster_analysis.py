# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 14:52:40 2018

@author: Florian Ulrich Jehn
"""

import pca
import clustering
import linear_regression
import read_attributes_signatures
import pandas as pd
import matplotlib.pyplot as plt

def plot_all_regressions(combined_df):
    """
    Plots the weighted coefficient of determination
    """
    r2_df_weighted.sort_values().plot(kind="barh", color="#4C72B0", ax=ax)
    plt.savefig("r2_scores_ " + describer + ".png")
    plt.close()
    for label, cluster in combined_df.groupby("Cluster"):
        print("Cluster num " + str(label))
        # Seperate to get the right format for the other functions
        pca_df_cluster = cluster[["PC 1", "PC 2"]]
        attributes = cluster.columns[2:-1]
        att_df_cluster = cluster[attributes]
        # Encode the attributes
        att_df_cluster = linear_regression.cat_to_num(att_df_cluster)
        # Calculate the linear regressions
        r2_df = linear_regression.calc_all_linear_regressions(pca_df_cluster, att_df_cluster)
        r2_df_weighted = linear_regression.weight_regression_by_var(r2_df, [0.74567053, 0.18828154])
        # only select the 5 most important characteristics
        r2_df_weighted = r2_df_weighted.sort_values(ascending=False).head(5)
        
        ax = axes[]

        plt.xlim(0,1)

        
        
        
        linear_regression.plot_regressions(r2_df_weighted, "cluster_" + str(label) + "_num_" + str(att_df_cluster.shape[0]), ax=ax)


if __name__ == "__main__":
    # Calculate the PCA
    variance = 0.8
    pca_df = pca.pca_signatures(variance)
    # Get the catchment attributes
    meta_df = read_attributes_signatures.read_meta()
    att_df, sig_df = read_attributes_signatures.seperate_attributes_signatures(meta_df)
    # Create the clusters
    labels = clustering.create_cluster_labels(pca_df, 10)
    combined_df = pd.concat([pca_df, att_df, labels], axis=1)
    # Create the figures for the clusters
    
    