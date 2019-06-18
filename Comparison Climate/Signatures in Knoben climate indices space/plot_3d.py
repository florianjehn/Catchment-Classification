# -*- coding: utf-8 -*-
"""
Created on Tue May 21 14:01:42 2019

@author: gh2668
"""

import pandas as pd
import seaborn
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

df = pd.read_csv("knoben_climate_jehn_signatures.csv", index_col=0)
signatures = list(df.columns[:6])
units = {"Mean half-flow date":"[day of year]", "Mean summer discharge":"[mm $d^{-1}$]",
             "Mean winter discharge": "[mm $d^{-1}$]", "Q95 (high flow)":"[mm $d^{-1}$]",
             "Runoff ratio": "[-]", "Mean annual discharge":"[mm $d^{-1}$]"}

fig = plt.gcf()
fig.set_size_inches(20,20)
for i, kind in enumerate(signatures):
    ax = fig.add_subplot(4, 2, i + 1, projection='3d')
    ax.set_xlabel("\nSeasonality")
    ax.set_ylabel("\nAridity")
    ax.set_zlabel("Prec. Snow")
    p = ax.scatter(df["Seasonality"],
               df["Aridity"],
               df["Precipitation falling as snow"],
               c = np.log(df[kind]),
               cmap=plt.get_cmap("plasma"),
               alpha=0.9,
               s=100,
               edgecolor="black",
               linewidths=0.5)


    ax.set_title(kind)
    cbar = fig.colorbar(p)
    cbar.ax.set_ylabel("log " + units[kind])

fig.tight_layout()
plt.savefig("signatures.png", dpi=300)