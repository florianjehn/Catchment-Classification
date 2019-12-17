# -*- coding: utf-8 -*-
"""
Created on Wed May 29 09:52:25 2019

@author: gh2668
"""

import pandas as pd
import matplotlib.pyplot as plt
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  
from matplotlib import gridspec
import seaborn as sns
import numpy as np

import matplotlib.patches as mpatches


def plot_koeppen(beck, ax):
    """
    Plots the koeppen geiger classification as stacked bar plots
    """
    alpha=0.6
    # Create the right colros for Koeppen Geiger
    climate_dict = {"1": "Tropical, rainforest" , "2": "Tropical, monsoon", "3": "Tropical, savannah",
                    "4": "Arid, desert, hot", "5": "Arid, desert, cold", "6": "Arid, steppe, hot",
                    "7": "Arid, steppe, cold", "8": "Temperate, dry summer, hot summer", 
                    "9": "Temperate, dry summer, warm summer", "10": "Temperate, dry summer, cold summer",
                    "11": "Temperate, dry winter, hot summer", "12": "Temperate, dry winter, warm summer",
                    "13": "Temperate, dry winter, cold summer", "14": "Temperate, no dry season, hot summer",
                    "15": "Temperate, no dry season, warm summer", "16": "Temperate, no dry season, cold summer",
                    "17": "Cold, dry summer, hot summer", "18": "Cold, dry summer, warm summer",
                    "19": "Cold, dry summer, cold summer", "20": "Cold, dry summer, very cold winter",
                    "21": "Cold, dry winter, hot summer", "22": "Cold, dry winter, warm summer", 
                    "23": "Cold, dry winter, cold summer", "24": "Cold, dry winter, very cold winter",
                    "25": "Cold, no dry season, hot summer", "26": "Cold, no dry season, warm summer",
                    "27": "Cold, no dry season, cold summer", "28": "Cold, no dry season, very cold winter",
                    "29": "Polar, tundra", "30": "Polar, frost"}
    color_dict = {"1": "[0 0 255]" , "2": "[0 120 255]", "3": "[70 170 250]",
                    "4": "[255 0 0]", "5": "[255 150 150]", "6": "[245 165 0]",
                    "7": "[255 220 100]", "8": "[255 255 0]", 
                    "9": "[200 200 0]", "10": "[150 150 0]",
                    "11": "[150 255 150]", "12": "[100 200 100]",
                    "13": "[50 150 50]", "14": "[200 255 80]",
                    "15": "[100 255 80]", "16": "[50 200 0]",
                    "17": "[255 0 255]", "18": "[200 0 200]",
                    "19": "[150 50 150]", "20": "[150 100 150]",
                    "21": "[170 175 255]", "22": "[90 120 220]", 
                    "23": "[75 80 180]", "24": "[50 0 135]",
                    "25": "[0 255 255]", "26": "[55 200 255]",
                    "27": "[0 125 125]", "28": "[0 70 95]",
                    "29": "[178 178 178]", "30": "[102 102 102]"}
    for key in color_dict.keys():
        color = color_dict[key]
        color = color.replace("[","").replace("]","").split(" ")
        color = [int(val)/255 for val in color] +[1]
        color_dict[key] = color
      
    climate_to_color = {climate_dict[key] : value for key, value in color_dict.items()}
    
    beck["Climatic Regions"] = beck["RASTERVALU"].astype(str)
    beck.replace({"Climatic Regions":climate_dict}, inplace=True)
    
    def color_for_label(label):
        return [climate_to_color[x] for x in label]
    
    # As percentag
    #df = beck.groupby(["gauge_clus",'Climatic Regions']).size().groupby(level=0).apply(
    #    lambda x: 100 * x / x.sum()).unstack()
    # Group the dataframe
    df = beck.groupby(["gauge_clus",'Climatic Regions']).size().unstack()
    # Plotting
    ax = df.plot(kind="bar", stacked=True, color=color_for_label(df.columns.values), alpha=1, ax = ax, zorder=4)
 #   ax.set_title("a) Membership of Koeppen-Geiger clusters (Beck et al. (2018)) in the hydrological clusters", loc="left", alpha=alpha)
    ax.set_xlabel("Hydrological Cluster", alpha=alpha)
    ax.set_ylabel("Number of Catchments", alpha=alpha)
    legend = ax.legend(ncol=2, title="Climatic Cluster")
    for text in legend.get_texts():
        text.set_color("grey")
    legend.get_title().set_color("grey")
    # Make it nicer
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.yaxis.grid(True, color="lightgrey", zorder=0)
    plt.setp(ax.get_yticklabels(), alpha=alpha)
    plt.setp(ax.get_xticklabels(), alpha=alpha, rotation=0)
    ax.tick_params(axis=u'both', which=u'both',length=0)

#   
def read_koeppen():
    beck = beck = pd.read_csv("camels_clusters_in_koeppen_geiger.csv", sep=",")
    del beck["FID"]
    beck.set_index("gauge_inde", inplace=True)
    
    beck = beck[['RASTERVALU', 'gauge_clus']]
    beck["gauge_clus"] = beck["gauge_clus"].add(1).astype("category")
    beck["RASTERVALU"] = beck["RASTERVALU"].astype("category")
    
    return beck



beck = read_koeppen()

#fig = plt.figure(figsize=(13, 17)) 
ax = plt.gca()
fig=plt.gcf()
plot_koeppen(beck, ax)
fig.set_size_inches(13,4)
fig.tight_layout()
plt.savefig("clusters_koeppen.png", bbox_inches="tight", dpi=300)



