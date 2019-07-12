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

s=70    
def plot_knoben(knoben, ax1, ax2, ax3):
    """Plots my catchment clusters in wouters climate space
    """
    alpha = 0.6
    # https://stackoverflow.com/questions/19913659/pandas-conditional-creation-of-a-series-dataframe-column     
    conditions= [
            knoben["Catchment Cluster"] == 1,
            knoben["Catchment Cluster"] == 2,
            knoben["Catchment Cluster"] == 3,
            knoben["Catchment Cluster"] == 4,
            knoben["Catchment Cluster"] == 5,
            knoben["Catchment Cluster"] == 6,
            knoben["Catchment Cluster"] == 7,
            knoben["Catchment Cluster"] == 8,
            knoben["Catchment Cluster"] == 9,
            knoben["Catchment Cluster"] == 10]
    choices = ["#e6194B", "#f58231", "#fffac8", "#bfef45",  "#3cb44b", 
             "#42d4f4", "#4363d8", "#911eb4", "#a9a9a9", "#ffffff"]
    knoben['color'] = np.select(conditions, choices, default='black')
    
    # First plot Seasonality, Aridity
    ax1.scatter(knoben["Seasonality"], knoben["Aridity"], c=list(knoben["color"]), zorder=4, edgecolor="black", linewidth=0.3, s=s)
    ax1.set_xlabel(r"constant$\longleftarrow$Seasonality$\longrightarrow$seasonal", alpha=alpha)
    ax1.set_ylabel(r"arid$\longleftarrow$Aridity$\longrightarrow$wet", alpha=alpha)
    ax1.set_title("a) Hydrological clusters in climate index space of Knoben et al. (2018)", loc="left", alpha=alpha, fontsize=10)

    # Second plot Seasonality, Snow
    ax2.scatter(knoben["Seasonality"], knoben["Precipitation falling as snow"],   c=list(knoben["color"]), zorder=4, edgecolor="black", linewidth=0.3, s=s)
    ax2.set_xlabel(r"constant$\longleftarrow$Seasonality$\longrightarrow$seasonal", alpha=alpha)
    ax2.set_ylabel(r"no snow$\longleftarrow$Precip. as snow$\longrightarrow$all snow", alpha=alpha)
    handles = []
    for i, color in enumerate(choices):
        handles.append(mpatches.Patch(facecolor=color, edgecolor="black", label=str(i+1), linewidth=0.3))
    legend = ax2.legend(handles=handles, ncol=5, title="Hydrological Cluster")
    for text in legend.get_texts():
        text.set_color("grey")
    title_legend = legend.get_title()
    title_legend.set_color("grey")

    # Third plot Snow, Aridity
    ax3.scatter(knoben["Aridity"],knoben["Precipitation falling as snow"],   c=list(knoben["color"]), zorder=4, edgecolor="black", linewidth=0.3, s=s)
    ax3.set_xlabel(r"arid$\longleftarrow$Aridity$\longrightarrow$wet", alpha=alpha)
    ax3.set_ylabel(r"no snow$\longleftarrow$Precip. as snow$\longrightarrow$all snow", alpha=alpha)  

    # Make it nice+
    for ax in [ax1, ax2, ax3]:
        plt.setp(ax.get_yticklabels(), alpha=alpha)
        plt.setp(ax.get_xticklabels(), alpha=alpha, rotation=0)
        ax.tick_params(axis=u'both', which=u'both',length=0)
        ax.grid(True, color="lightgrey", zorder=0)
        for spine in ax.spines.values():
            spine.set_visible(False)


def read_knoben():
    return pd.read_csv("knoben_climate_jehn_signatures.csv", index_col=0)


def plot_signatures(knoben, ax1, ax2, ax3):
    alpha=0.6
    units = {"Mean half-flow date":"[day of year]", "Mean summer discharge":"[mm $d^{-1}$]",
             "Mean winter discharge": "[mm $d^{-1}$]", "Q95 (high flow)":"[mm $d^{-1}$]",
             "Runoff ratio": "[-]", "Mean annual discharge":"[mm $d^{-1}$]"}
    name_dict= {"Aridity":r"arid$\longleftarrow$Aridity$\longrightarrow$wet",
                "Seasonality": r"constant$\longleftarrow$Seasonality$\longrightarrow$seasonal",
                "Precip. as snow": r"no snow$\longleftarrow$Precip. as snow$\longrightarrow$all snow"}
    mean_annual = knoben["Mean annual discharge"]
    knoben["Precip. as snow"] = knoben["Precipitation falling as snow"]
    
    for climate_index_x, climate_index_y, ax in zip(["Seasonality", "Seasonality", "Aridity"],["Aridity", "Precip. as snow", "Precip. as snow"], [ax1, ax2, ax3]):
            ax.set_ylabel(name_dict[climate_index_y], alpha=alpha)
            ax.set_xlabel(name_dict[climate_index_x], alpha=alpha)
            scatter = ax.scatter(knoben[climate_index_x], knoben[climate_index_y],   c=np.log(list(mean_annual)), cmap="plasma", alpha=1, zorder=4, edgecolor="black", linewidth=0.3, s=s)
            cbar = fig.colorbar(scatter, ax=ax)
            cbar.ax.set_ylabel("log " + units["Mean annual discharge"], alpha=alpha)
            plt.setp(cbar.ax.get_yticklabels(), alpha=alpha)
            # Make it nice+
            plt.setp(ax.get_yticklabels(), alpha=alpha)
            plt.setp(ax.get_xticklabels(), alpha=alpha)
            ax.tick_params(axis=u'both', which=u'both',length=0)
            ax.grid(True, color="lightgrey", zorder=0)
            for spine in ax.spines.values():
                spine.set_visible(False)
    ax1.set_title("b) Mean annual discharge in climate index space of Knoben et al. (2018)", loc="left", alpha=alpha, fontsize=10) 


knoben = read_knoben()
knoben["Catchment Cluster"] = knoben["Catchment Cluster"] + 1

#fig = plt.figure(figsize=(13, 17)) 
fig = plt.figure(figsize=(12, 17)) 
gs = gridspec.GridSpec(3, 2, height_ratios=[1,1,1], width_ratios=[1, 1.2]) 
ax0 = plt.subplot(gs[0])
ax1 = plt.subplot(gs[1])
ax2 = plt.subplot(gs[2])
ax3 = plt.subplot(gs[3])
ax4 = plt.subplot(gs[4])
ax5 = plt.subplot(gs[5])


plot_knoben(knoben, ax0, ax2, ax4)
plot_signatures(knoben, ax1, ax3, ax5)
fig.subplots_adjust(wspace=-0.5)

fig.tight_layout()
plt.savefig("clusters_together.png", bbox_inches="tight", dpi=300)



