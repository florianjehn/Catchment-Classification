# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 14:52:40 2018

@author: Florian Ulrich Jehn
"""

import pca
import clustering
import read_attributes_signatures
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import regression
import matplotlib.patches as mpatches


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
        att_df_cluster = regression.cat_to_num(att_df_cluster)
        # Calculate the linear regressions
        r2_df = regression.calc_all_linear_regressions(pca_df_cluster, att_df_cluster)
        r2_df_weighted = regression.weight_regression_by_var(r2_df, [0.74567053, 0.18828154])
        # only select the 5 most important characteristics
        r2_df_weighted = r2_df_weighted.sort_values(ascending=False).head(5)
        # plot it
        r2_df_weighted.sort_values().plot(kind="barh", ax=ax, color="#4C72B0",zorder=3)
        # make it nicer
        ax.set_title("Cluster {} (n = {})".format(label + 1, cluster.shape[0]), alpha=alpha)
        ax.grid(False)
        ax.set_facecolor("white")
        ax.xaxis.grid(color="lightgrey",zorder=0)
        ax.set_xlabel("Weigthed Coefficient of Determination", alpha=alpha)
        plt.setp(ax.get_xticklabels(), alpha=alpha)

        # Color the ylabels
        for tick_label in ax.axes.get_yticklabels():
            tick_text = tick_label.get_text()
            tick_label.set_color(color_dict[tick_text])
        # Remove the borders
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(axis=u'both', which=u'both',length=0)

    
    ax = axes[4,1]
    # Create the legend
    handles = []
    for att, color in cols_classes.items():
        handles.append(mpatches.Patch(color=color, label=att))
    legend = ax.legend(handles=handles, frameon=True, fancybox=True, facecolor="white", edgecolor="grey")
    for text in legend.get_texts():
        text.set_color("grey")
        
        
    fig.set_size_inches(10, 11.7)
    fig.tight_layout()
    plt.savefig("all_regressions.png", dpi=200, bbox_inches="tight")
          

def plot_all_signatures_swarm(sig_plot_df, color_dict):
    """
    Plots the signatures seperated by the clusters
    """
    alpha=0.6
    fig, axes = plt.subplots(nrows=6, ncols=1, sharex=True)
    signatures = list(sig_plot_df.columns[:-1])
    units = {"Mean half-flow date":"[day of year]", "Mean summer discharge":"[mm $d^{-1}$]",
             "Mean winter discharge": "[mm $d^{-1}$]", "Q95 (high flow)":"[mm $d^{-1}$]",
             "Runoff ratio": "[-]", "Mean annual discharge":"[mm $d^{-1}$]"}
    for i, sig in enumerate(sorted(signatures)):

        ax = axes[i-1]
        ax.yaxis.grid(color="grey", zorder=0)
        ax.set_axisbelow(True)

        # Get the five attributes with the lowest range
        ax = sns.boxplot(y=sig_plot_df[sig], x=sig_plot_df["Cluster"], zorder=10, 
                        palette=["#e6194B", "#f58231", "#fffac8", "#bfef45",  "#3cb44b", 
             "#42d4f4", "#4363d8", "#911eb4", "#a9a9a9", "#ffffff"],  whis=100, width=0.9,
                        ax=ax)
        ax.set_xlabel("")
        ax.set_facecolor("white")
        ax.set_xticklabels([str(i) for i in range(1,11)],alpha=alpha)
        ax.set_ylabel(r""+ax.get_ylabel()+"\n"+units[sig], rotation=0, labelpad=70,alpha=alpha)
        plt.setp(ax.get_yticklabels(), alpha=alpha)

        # Remove the borders
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(axis=u'both', which=u'both',length=0)

            
    axes[5].set_xlabel("Cluster",alpha=alpha)
                 
    fig.set_size_inches(6, 30)
    fig.subplots_adjust(hspace=0)

    plt.savefig("cluster_sigs.png", dpi=400, bbox_inches="tight")

def plot_all_attributes_swarm(combined_df, color_dict, cols_classes):
    """
    Plots the 5 catchment attributes with the lowest range"
    """   
    alpha = 0.6
    fig, axes = plt.subplots(nrows=15, ncols=1, sharex=True)
    attributes = ["Aridity", 'Fraction of precipitation\nfalling as snow', 'Frequency of high\nprecipitation events', "Precipitation seasonality",
                  'Subsurface permeability', 'Subsurface porosity',
                 'Clay fraction','Depth to bedrock', 'Sand fraction',
                 'Area', 'Mean elevation', 'Mean slope',
                 'Forest fraction','Green vegetation\nfraction maximum','LAI maximum']
    units = {"Aridity": "[-]", 'Fraction of precipitation\nfalling as snow': "[-]", 'Frequency of high\nprecipitation events':"[days $yr^{-1}$]", "Precipitation seasonality":"[-]",
             'Subsurface permeability': "[cm $h^{-1}$]", 'Subsurface porosity':"[-]",
                 'Clay fraction':"[%]",'Depth to bedrock':"[m]", 'Sand fraction':"[%]",
                 'Area':"[$km^2$]", 'Mean elevation':"[m]", 'Mean slope':"[m $km^{-1}$]",
                 'Forest fraction':"[-]",'Green vegetation\nfraction maximum':"[-]",'LAI maximum':"[-]"}
    
    pads =  {"Aridity": 75, 'Fraction of precipitation\nfalling as snow': 65, 'Frequency of high\nprecipitation events':70,"Precipitation seasonality":70,
             'Subsurface permeability': 70, 'Subsurface porosity':70,
                 'Clay fraction':65,'Depth to bedrock':65, 'Sand fraction':65,
                 'Area':50, 'Mean elevation':60, 'Mean slope':65,
                 'Forest fraction':70,'Green vegetation\nfraction maximum':65,'LAI maximum':70}
    for i, att in enumerate(attributes):

        ax = axes[i]
        # Get the five attributes with the lowest range
        sns.boxplot(y=combined_df[att], x=combined_df["Cluster"], 
                        palette=["#e6194B", "#f58231", "#fffac8", "#bfef45",  "#3cb44b", 
             "#42d4f4", "#4363d8", "#911eb4", "#a9a9a9", "#ffffff"], whis=100, width=0.9,
                        ax=ax)
        ax.set_xlabel("")
        ax.yaxis.grid(color="grey")
        ax.set_axisbelow(True)

        ax.set_facecolor("white")
        ax.set_xticklabels([str(i) for i in range(1,11)], alpha=alpha)
        ax.set_ylabel(r""+att + "\n"+units[att], rotation=0 ,va='center',labelpad=pads[att], color=color_dict[att])
        plt.setp(ax.get_yticklabels(), alpha=alpha)

                # Remove the borders
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(axis=u'both', which=u'both',length=0)

        
    # Create the legend
    handles = []
    for att, color in cols_classes.items():
        handles.append(mpatches.Patch(color=color, label=att))
    
    axes[13].set_xlabel("Cluster",alpha=alpha)
    legend = axes[13].legend(handles=handles,bbox_to_anchor=(-0.05, -0.7), frameon=True, fancybox=True, facecolor="white", edgecolor="grey")
    for text in legend.get_texts():
        text.set_color("grey")
                 
    fig.set_size_inches(6, 30)
   # fig.tight_layout()
    fig.subplots_adjust(hspace=0)
    plt.savefig("cluster_atts.png", dpi=400, bbox_inches="tight")

def calc_coefficient_of_variation(att_df_with_labels):
    """
    Finds coefficient of variation for all combinations of Cluster and Attribute
    """
    # Transform the categories
    att_df_with_labels = regression.cat_to_num(att_df_with_labels)
    cv = pd.DataFrame()
    # Exclude the PCA
    cv["Attributes"] = att_df_with_labels.columns[:-1]
    cv = cv.set_index("Attributes")
    #cv.columns = combined_df["Cluster"]
    for cluster, cluster_df in att_df_with_labels.groupby("Cluster"):
        cv[cluster] = None
        # Remove the cluster column
        del(cluster_df["Cluster"])
        for att in cluster_df.columns:
            # Transform the categories
            # Calculate the coefficient of variation for the current combination of cluster and attribute
            std = cluster_df[att].std()
            mean = abs(cluster_df[att].mean())
            cv_ = std / mean 
            # Also consider the size of the cluster
            # see https://en.wikipedia.org/wiki/Coefficient_of_variation
            cv_ = cv_ * (1 + 1/(4*cluster_df.shape[0]))
            cv.loc[att, cluster] = cv_
    
    return cv
    

def calc_scaled_cv(cv_df):
    """
    Scales the coefficient of variation of the single attributes by the mean coefficient
    of variation of the same attribute. This allows to find the attribute of the
    cluster that has the lowest variation for the cluster im relationship to the
    variation of the variable in the whole dataset
    """
    cv_df_scaled = cv_df.copy(deep=True)
    # Get the mean cv for the attributes
    means = cv_df_scaled.mean(axis=1)
    # Calc
    for cluster in cv_df_scaled.columns:
        cv_df_scaled[cluster] /= means
    return cv_df_scaled
    
    

if __name__ == "__main__":
    # Dictionary for the broad categories
    color_dict = {"Area": "#D64139", "Mean elevation": "#D64139", "Mean slope": "#D64139",
                  "Fraction of precipitation\nfalling as snow": "royalblue", "Aridity": "royalblue", "Frequency of high\nprecipitation events": "royalblue", "Precipitation seasonality":"royalblue",
                  "Depth to bedrock": "#D6BD39", "Sand fraction": "#D6BD39", "Clay fraction": "#D6BD39",
                  "Forest fraction": "forestgreen", "LAI maximum": "forestgreen", "Green vegetation\nfraction maximum": "forestgreen",
                  "Dominant geological class": "grey", "Subsurface porosity": "grey", "Subsurface permeability": "grey"}
    # Dictionary for the catchment classes
    cols_classes = {"Climate": "royalblue", 
                "Geology": "grey", 
                "Soil": "#D6BD39", 
                "Topography": "#D64139",
                "Vegetation": "forestgreen"}
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
    plot_all_regressions(combined_df, color_dict)
    plot_all_attributes_swarm(combined_df,color_dict, cols_classes)
    sig_plot_df = pd.concat([sig_df, combined_df["Cluster"]], axis=1)
    plot_all_signatures_swarm(sig_plot_df, color_dict)
    # cv_att = calc_coefficient_of_variation(pd.concat([att_df, labels], axis=1))
    # cv_att_scaled = calc_scaled_cv(cv_att)
    # cv_sig = calc_coefficient_of_variation(pd.concat([sig_df, labels], axis=1))
    # cv_sig_scaled = calc_scaled_cv(cv_sig)