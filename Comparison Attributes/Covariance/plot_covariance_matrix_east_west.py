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
              "Fraction of precipitation\nfalling as snow": "royalblue", "Aridity": "royalblue", "Frequency of high\nprecipitation events": "royalblue", "Precipitation seasonality":"royalblue",
              "Depth to bedrock": "#D6BD39", "Sand fraction": "#D6BD39", "Clay fraction": "#D6BD39",
              "Forest fraction": "forestgreen", "LAI maximum": "forestgreen", "Green vegetation\nfraction maximum": "forestgreen",
              "Dominant geological class": "grey", "Subsurface porosity": "grey", "Subsurface permeability": "grey"}

meta_df = read_attributes_signatures.read_meta()
att_df, sig_df = read_attributes_signatures.seperate_attributes_signatures(meta_df)
att_df['Dominant geological class'] = pd.factorize(att_df['Dominant geological class'])[0]

# Plot for whole dataset
# all_corr = att_df.corr()
#mask = np.zeros_like(corr)
#mask[np.triu_indices_from(mask)] = True

# Plot seperated by ost and west
att_df["gauge_lon"] = meta_df["gauge_lon"]
west = att_df.loc[att_df["gauge_lon"] < -100,:]
east = att_df.loc[att_df["gauge_lon"] > -100,:]
del(west["gauge_lon"])
del(east["gauge_lon"])

fig, axes = plt.subplots(nrows=3)
axes = axes.flatten()
ax1 = axes[0]
ax2 = axes[1]
ax3 = axes[2]
# Plot Western US
sns.heatmap(west.corr(method="spearman"), ax=ax1, cmap="coolwarm", square=True, linewidth=0.5, yticklabels=True, cbar=False, annot=round(west.corr(),1))
ax1.xaxis.tick_top()
plt.setp( ax1.xaxis.get_majorticklabels(), rotation=90)
ax1.text(1.01, 0.5, "a) Western US",
        rotation=270, size=12, weight='bold',
        ha='left', va='center', transform=ax1.transAxes, alpha=alpha)
# Color the ylabels
for tick_label in ax1.axes.get_yticklabels():
    tick_text = tick_label.get_text()
    tick_label.set_color(color_dict[tick_text])
for tick_label in ax1.axes.get_xticklabels():
    tick_text = tick_label.get_text()
    tick_label.set_color(color_dict[tick_text])
# Add rectangles to group attributes
i = 0
while i <= 16:
    if i == 6:
        i += 1
    j = 0
    while j <= 16:
        if j == 6:
            j += 1
        if i == 3 and j == 3:
            ax1.add_patch(Rectangle((i, j), 4, 4, fill=False, edgecolor='black', lw=1))
        elif i == 3 and not j == 3:
            ax1.add_patch(Rectangle((i, j), 4, 3, fill=False, edgecolor='black', lw=1))
        elif not i == 3 and j == 3:
            ax1.add_patch(Rectangle((i, j), 3, 4, fill=False, edgecolor='black', lw=1))
        else:
            ax1.add_patch(Rectangle((i, j), 3, 3, fill=False, edgecolor='black', lw=1))
        j += 3
    i += 3

# Plot Eastern US
sns.heatmap(east.corr(method="spearman"), ax=ax2, cmap="coolwarm", square=True, linewidth=0.5,yticklabels=True, cbar=False, annot=round(east.corr(),1), xticklabels=False)
ax2.text(1.01, -0.5, "b) Eastern US",
        rotation=270, size=12, weight='bold',
        ha='left', va='center', transform=ax1.transAxes, alpha=alpha)
# Add rectangles to group attributes
i = 0
while i <= 16:
    if i == 6:
        i += 1
    j = 0
    while j <= 16:
        if j == 6:
            j += 1
        if i == 3 and j == 3:
            ax2.add_patch(Rectangle((i, j), 4, 4, fill=False, edgecolor='black', lw=1))
        elif i == 3 and not j == 3:
            ax2.add_patch(Rectangle((i, j), 4, 3, fill=False, edgecolor='black', lw=1))
        elif not i == 3 and j == 3:
            ax2.add_patch(Rectangle((i, j), 3, 4, fill=False, edgecolor='black', lw=1))
        else:
            ax2.add_patch(Rectangle((i, j), 3, 3, fill=False, edgecolor='black', lw=1))
        j += 3
    i += 3


# Color the ylabels
for tick_label in ax2.axes.get_yticklabels():
    tick_text = tick_label.get_text()
    tick_label.set_color(color_dict[tick_text])

# calc difference
diff_df = pd.DataFrame()
for column in west.corr():
    diff_df[column] = abs(west.corr(method="spearman")[column] - east.corr(method="spearman")[column])

ax3=axes[2]
sns.heatmap(diff_df, cmap="Blues", annot=round(diff_df,1),yticklabels=True, cbar=False, ax=ax3, linewidth=0.5,square=True)
ax3.text(1.01, -1.51, "c) Differences between East and West",
        rotation=270, size=12, weight='bold',
        ha='left', va='center', transform=ax1.transAxes, alpha=alpha)
# Add rectangles to group attributes
i = 0
while i <= 16:
    if i == 6:
        i += 1
    j = 0
    while j <= 16:
        if j == 6:
            j += 1
        if i == 3 and j == 3:
            ax3.add_patch(Rectangle((i, j), 4, 4, fill=False, edgecolor='black', lw=1))
        elif i == 3 and not j == 3:
            ax3.add_patch(Rectangle((i, j), 4, 3, fill=False, edgecolor='black', lw=1))
        elif not i == 3 and j == 3:
            ax3.add_patch(Rectangle((i, j), 3, 4, fill=False, edgecolor='black', lw=1))
        else:
            ax3.add_patch(Rectangle((i, j), 3, 3, fill=False, edgecolor='black', lw=1))
        j += 3
    i += 3

# Color the ylabels
for tick_label in ax3.axes.get_yticklabels():
    tick_text = tick_label.get_text()
    tick_label.set_color(color_dict[tick_text])
for tick_label in ax3.axes.get_xticklabels():
    tick_text = tick_label.get_text()
    tick_label.set_color(color_dict[tick_text])
    
    
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
legend = ax3.legend(handles=handles,bbox_to_anchor=(-0.02, -0.02), frameon=True, fancybox=True, facecolor="white", edgecolor="grey", title="Attribute Classes")
for text in legend.get_texts():
    text.set_color("grey")
legend.get_title().set_color("grey")
fig.set_size_inches(20,20)

fig.tight_layout()
fig.subplots_adjust(hspace=0.01)
plt.savefig("covariability.png", dpi=250, bbox_inches="tight")
plt.close()