# -*- coding: utf-8 -*-
"""
Created on Wed May 29 14:34:08 2019

@author: gh2668
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
alpha=0.6
real = pd.read_csv("distances_real_world.txt", sep="\t", index_col=0)
sig = pd.read_csv("distances_pca_signatures.csv", sep=",", index_col=0)
closest_df = pd.DataFrame()

for from_catchment in sig.columns:
    to_catchment = sig[from_catchment].idxmin()
    dist = real.loc[int(from_catchment), str(to_catchment)]
    closest_df.loc[int(from_catchment), "nearest"] = dist
    
camels_clusters = pd.read_csv("index_pos_cluster.csv", index_col=0)
camels_clusters = pd.merge(camels_clusters, closest_df, right_index=True, left_index=True)
# convert to km
camels_clusters["nearest"] = camels_clusters["nearest"]/1000
#camels_clusters.groupby("gauge_cluster").median()["nearest"].plot(kind="bar")
#print(camels_clusters.groupby("gauge_cluster").median()["nearest"])
#camels_clusters.groupby("gauge_cluster")["nearest"].plot(kind="box")
ax = sns.swarmplot(x=camels_clusters["gauge_cluster"], y=camels_clusters["nearest"], palette="gist_earth", size=3)
ax.set_ylabel("Distance [km]", alpha=0.6)
ax.set_xlabel("Catchment Cluster", alpha=0.6)
# Make it nice+
plt.setp(ax.get_yticklabels(), alpha=alpha)
plt.setp(ax.get_xticklabels(), alpha=alpha)
ax.tick_params(axis=u'both', which=u'both',length=0)
ax.yaxis.grid(True, color="lightgrey", zorder=0)
for spine in ax.spines.values():
    spine.set_visible(False)
fig = plt.gcf()
fig.set_size_inches(10,4)
fig.tight_layout()
plt.savefig("distances_by_catchment_cluster.png", bbox_inches="tight", dpi=300)

plt.close()
ax = sns.swarmplot(y=camels_clusters["nearest"], size=2, orient="h", edgecolor="gray")
ax.set_xlabel("Distance [km]", alpha=0.6)
# Make it nice+
plt.setp(ax.get_yticklabels(), alpha=alpha)
plt.setp(ax.get_xticklabels(), alpha=alpha)
ax.tick_params(axis=u'both', which=u'both',length=0)
#ax.xaxis.grid(True, color="lightgrey", zorder=0)
for spine in ax.spines.values():
    spine.set_visible(False)
fig = plt.gcf()
fig.set_size_inches(10,1.5)
fig.tight_layout()
plt.savefig("distances.png", bbox_inches="tight", dpi=300)

plt.close()
# Seperate it by west and east
fig, axes = plt.subplots(ncols=2, sharex=True)
axes = axes.flatten()
ax1 = sns.boxplot(y=camels_clusters.loc[camels_clusters["gauge_lon"] < -100, "nearest"], orient="v", ax=axes[0])
ax2 = sns.boxplot(y=camels_clusters.loc[camels_clusters["gauge_lon"] > -100, "nearest"], orient="v", ax=axes[1])













