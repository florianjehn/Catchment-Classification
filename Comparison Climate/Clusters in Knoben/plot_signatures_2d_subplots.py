# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:52:43 2019

@author: gh2668
"""

import pandas as pd
import seaborn
import matplotlib.pyplot as plt
import numpy as np


def read_knoben():
    return pd.read_csv("knoben_climate_jehn_signatures.csv", index_col=0)

def plot_signatures_2d(knoben):
    alpha=0.6
    units = {"Mean half-flow date":"[day of year]", "Mean summer discharge":"[mm $d^{-1}$]",
             "Mean winter discharge": "[mm $d^{-1}$]", "Q95 (high flow)":"[mm $d^{-1}$]",
             "Runoff ratio": "[-]", "Mean annual discharge":"[mm $d^{-1}$]"}
    name_dict= {"Aridity":r"arid$\leftarrow$Aridity$\rightarrow$wet",
                "Seasonality": r"constant$\leftarrow$Seasonality$\rightarrow$seasonal",
                "Precip. as snow": r"no snow$\leftarrow$Precip. as snow$\rightarrow$all snow"}
    knoben["Precip. as snow"] = knoben["Precipitation falling as snow"]
    signatures = list(knoben.columns[:6])
    fig, axes = plt.subplots(nrows=6, ncols=3)
    axes = axes.flatten()
    i = 0
    for signature in signatures:
        for climate_index_x, climate_index_y in zip(["Seasonality", "Seasonality", "Aridity"],["Aridity", "Precip. as snow", "Precip. as snow"]):
                ax = axes[i]
                if i == 1 or i == 4 or i == 7 or i == 10 or i == 13 or i == 16:
                    ax.set_title(signature, alpha=alpha)
                ax.set_ylabel(name_dict[climate_index_y], alpha=alpha, fontsize=8)
                ax.set_xlabel(name_dict[climate_index_x], alpha=alpha, fontsize=8)
                
                i += 1
                scatter = ax.scatter(knoben[climate_index_x], knoben[climate_index_y],   c=np.log(list(knoben[signature])), cmap="plasma", alpha=0.7, zorder=4, edgecolor="black", linewidth=0.3)
                cbar = fig.colorbar(scatter, ax=ax)
                cbar.ax.set_ylabel("log " + units[signature], alpha=alpha)
                plt.setp(cbar.ax.get_yticklabels(), alpha=alpha)
                # Make it nice+
                plt.setp(ax.get_yticklabels(), alpha=alpha)
                plt.setp(ax.get_xticklabels(), alpha=alpha)
                ax.tick_params(axis=u'both', which=u'both',length=0)
                ax.grid(True, color="lightgrey", zorder=0)
                if climate_index_x == "Aridity":
                    ax.set_xlim(-1.1,1.1)
                elif climate_index_x == "Seasonality":
                    ax.set_xlim(-0.1,2.1)
                if climate_index_y == "Aridity":
                    ax.set_ylim(-1.1,1.1)
                elif climate_index_y == "Precip. as snow":
                    ax.set_ylim(-0.1,1.1)
                for spine in ax.spines.values():
                    spine.set_visible(False)
    fig.set_size_inches(15,25)
    fig.tight_layout()
    plt.savefig("signatures_2d.png", dpi=300)
    
knoben = read_knoben()
plot_signatures_2d(knoben)