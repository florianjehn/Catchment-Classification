# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 16:02:02 2019

@author: gh2668
"""

import pandas as pd
import read_attributes_signatures
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches


alpha=0.7
# Dictionary for the broad categories
color_dict = {"Area": "#D64139", "Mean elevation": "#D64139", "Mean slope": "#D64139",
              "Fraction of precipitation\nfalling as snow": "royalblue", "Aridity": "royalblue", "Frequency of high\nprecipitation events": "royalblue",
              "Depth to bedrock": "#D6BD39", "Sand fraction": "#D6BD39", "Clay fraction": "#D6BD39",
              "Forest fraction": "forestgreen", "LAI maximum": "forestgreen", "Green vegetation\nfraction maximum": "forestgreen",
              "Dominant geological class": "grey", "Subsurface porosity": "grey", "Subsurface permeability": "grey"}
# Get the right data
meta_df = read_attributes_signatures.read_meta()
att_df, sig_df = read_attributes_signatures.seperate_attributes_signatures(meta_df)
att_df['Dominant geological class'] = pd.factorize(att_df['Dominant geological class'])[0]
labels = pd.read_csv("labels_loc.txt", index_col=0)
att_df["Cluster"] = labels["Cluster"] + 1
# Plot the single clusters
cluster = 10
cluster_df = att_df.loc[att_df["Cluster"] == cluster,:]
del(cluster_df["Cluster"])
num_catchments = cluster_df.shape[0]
ax = sns.heatmap(cluster_df.corr(), cmap="coolwarm", square=True, linewidth=0.5, yticklabels=True, cbar=False, annot=True)
ax.set_title("Cluster " + str(cluster) + " (n=" + str(num_catchments) + ")", alpha=alpha)
# Color the ylabels
for tick_label in ax.axes.get_yticklabels():
    tick_text = tick_label.get_text()
    tick_label.set_color(color_dict[tick_text])
for tick_label in ax.axes.get_xticklabels():
    tick_text = tick_label.get_text()
    tick_label.set_color(color_dict[tick_text])
# Add rectangles to group attributes
for i in range(0, 16, 3):
    for j in range(0,16,3):        
        ax.add_patch(Rectangle((i, j), 3, 3, fill=False, edgecolor='black', lw=1))

# Create the legend
# Dictionary for the catchment classes
cols_classes = {"Climate": "royalblue", 
            "Geology": "grey", 
            "Soil": "#D6BD39", 
            "Topography": "#D64139",
            "Vegetation": "forestgreen"}
handles = []
for att, color in cols_classes.items():
    handles.append(mpatches.Patch(color=color, label=att))
legend = ax.legend(handles=handles,bbox_to_anchor=(-0.02, -0.02), frameon=True, fancybox=True, facecolor="white", edgecolor="grey", title="Attribute Classes")
for text in legend.get_texts():
    text.set_color("grey")
legend.get_title().set_color("grey")

#Save
fig = plt.gcf()
fig.set_size_inches(10,10)
fig.tight_layout()
plt.savefig("covariability_cluster_"+str(cluster)+".png", dpi=200, bbox_inches="tight")
