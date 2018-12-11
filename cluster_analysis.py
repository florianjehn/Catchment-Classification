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
import seaborn as sns


def plot_all_regressions(combined_df, color_dict):
    """
    Plots the weighted coefficient of determination
    """
    alpha = 0.6
    fig, axes = plt.subplots(nrows=5, ncols=2, sharex=True)
    for i, (label, cluster) in enumerate(combined_df.groupby("Cluster")):
        ax = axes[i // 2, i % 2]
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
        # plot it
        r2_df_weighted.sort_values().plot(kind="barh", ax=ax, color="#4C72B0")
        # make it nicer
        ax.set_title("Cluster {} (n = {})".format(label + 1, cluster.shape[0]), alpha=alpha)
        ax.grid(False)
        ax.set_facecolor("white")
        ax.xaxis.grid(color="lightgrey")
        ax.set_xlabel("Weigthed Coefficient of Determination", alpha=alpha)
        plt.setp(ax.get_yticklabels(), alpha=alpha)
        plt.setp(ax.get_xticklabels(), alpha=alpha)

        # Color the ylabels
        for tick_label in ax.axes.get_yticklabels():
            tick_text = tick_label.get_text()
            tick_label.set_color(color_dict[tick_text])
        
        
    fig.set_size_inches(8.3, 11.7)
    fig.tight_layout()
    plt.savefig("all_regressions.png", dpi=200, bbox_inches="tight")
        

def plot_all_attributes(combined_df):
    """
    Plots the 5 catchment attributes with the lowest range"
    """   
    alpha = 0.6
    fig, axes = plt.subplots(nrows=14, ncols=1, sharex=True)
    attributes = list(combined_df.columns[2:-1])
    attributes.remove("Dominant geological class")
    for i, att in enumerate(attributes):

        ax = axes[i-1]
        # Get the five attributes with the lowest range
        sns.boxplot(combined_df[att], groupby=combined_df["Cluster"],
                        palette="terrain", 
                        linewidth=1, saturation=0.5, ax=ax, whis="range")
        ax.set_xlabel("")
        ax.set_xticklabels([str(i) for i in range(1,11)])

        ax.set_ylabel(ax.get_ylabel(), rotation=0, labelpad=70)
    
    axes[13].set_xlabel("Cluster")
                 
    fig.set_size_inches(8.3, 11.7)
    fig.tight_layout()
    plt.savefig("cluster_atts.png", dpi=200, bbox_inches="tight")
    
    
def plot_all_signatures_boxplot(sig_plot_df, color_dict):
    """
    Plots the signatures seperated by the clusters
    """
    fig, axes = plt.subplots(nrows=6, ncols=1, sharex=True)
    signatures = list(sig_plot_df.columns[:-1])
    for i, sig in enumerate(signatures):

        ax = axes[i-1]
        # Get the five attributes with the lowest range
        sns.boxplot(sig_plot_df[sig], groupby=sig_plot_df["Cluster"],
                        palette="terrain", 
                        linewidth=1, saturation=0.5, ax=ax, whis="range")
        ax.set_xlabel("")
        ax.set_xticklabels([str(i) for i in range(1,11)])
        ax.set_ylabel(ax.get_ylabel(), rotation=0, labelpad=70)
    
    axes[5].set_xlabel("Cluster")
                 
    fig.set_size_inches(8.3, 11.7)
    fig.tight_layout()
    plt.savefig("cluster_sigs.png", dpi=200, bbox_inches="tight")
    

def plot_all_signatures_swarm(sig_plot_df, color_dict):
    """
    Plots the signatures seperated by the clusters
    """
    fig, axes = plt.subplots(nrows=6, ncols=1, sharex=True)
    signatures = list(sig_plot_df.columns[:-1])
    for i, sig in enumerate(signatures):

        ax = axes[i-1]
        # Get the five attributes with the lowest range
        sns.swarmplot(y=sig_plot_df[sig], x=sig_plot_df["Cluster"],
                        palette="gnuplot", size=1.5,
                        ax=ax)
        ax.set_xlabel("")
        ax.yaxis.grid(color="grey")
        ax.set_facecolor("white")
        ax.set_xticklabels([str(i) for i in range(1,11)])
        ax.set_ylabel(ax.get_ylabel(), rotation=0, labelpad=70)
    
    axes[5].set_xlabel("Cluster")
                 
    fig.set_size_inches(8.3, 11.7)
    fig.tight_layout()
    plt.savefig("cluster_sigs.png", dpi=200, bbox_inches="tight")
    
         
def calc_coefficient_of_variation(df, num):
    """
    Finds the num columns with the lowest range in a df
    """
    cv = pd.DataFrame()
    cv["Attributes"] = df.columns[2:]
    cv = cv.set_index("Attributes")
    cv["CV"] = None
    for col in df.columns:
        if df[col].dtype != float:
            continue
        std = df[col].std()
        mean = abs(df[col].mean())
        cv_col = std / mean if mean > 0 else 0
        cv.loc[col,: "CV"] = cv_col 
        
    return cv.dropna().sort_values(by="CV", ascending=False)

if __name__ == "__main__":
    # Dictionary for the broad categories
    color_dict = {"Area": "#D64139", "Mean elevation": "#D64139", "Mean slope": "#D64139",
                  "Fraction of precipitation\nfalling as snow": "royalblue", "Aridity": "royalblue", "Frequency of high\nprecipitation events": "royalblue",
                  "Depth to bedrock": "#D6BD39", "Sand fraction": "#D6BD39", "Clay fraction": "#D6BD39",
                  "Forest fraction": "forestgreen", "LAI maximum": "forestgreen", "Green vegetation\nfraction maximum": "forestgreen",
                  "Dominant geological class": "grey", "Subsurface porosity": "grey", "Subsurface permeability": "grey"}
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
  #  plot_all_regressions(combined_df, color_dict)
#    plot_all_attributes(combined_df)
    sig_plot_df = pd.concat([sig_df, combined_df["Cluster"]], axis=1)
#    plot_all_signatures(sig_plot_df, color_dict) 
    plot_all_signatures_swarm(sig_plot_df, color_dict)
