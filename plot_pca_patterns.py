# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 14:26:49 2018

@author: Florian Ulrich Jehn
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pca
import read_attributes_signatures
import scipy.stats as stats
import os
import sys
import matplotlib.cm as cm
import matplotlib.colors as mcolors



def plot_pca(plotting_df: pd.DataFrame, describers: list):
    """
    Plots the results of the PCA, colored by
    :return:
    """
    # Basic set up
    alpha = 0.6
    fig = plt.Figure()

    # Plotting
    for describer in describers:
        sns.lmplot(x="PC 1",
                   y="PC 2",
                   data=plotting_df,
                   hue=describer,
                   fit_reg=False,
                   legend=False,
                   palette="inferno",
                   scatter_kws={"s": 10})
        ax = plt.gca()
        # Put the legend out of the figure
        if plotting_df[describer].dtype == float:
            normalize = mcolors.Normalize(vmin=plotting_df[describer].min(), vmax=plotting_df[describer].max())
            scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=cm.inferno)
            scalarmappaple.set_array(plotting_df[describer])
            plt.colorbar(scalarmappaple)
        else:
            legend = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,
                       frameon=True, fancybox=True)
            legend.get_frame().set_edgecolor("grey")
            legend.get_frame().set_facecolor("white")

        # Make plot nicer by removing the borders
        ax.set_facecolor("white")
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Add correct descriptions
        ax.set_title(describer, alpha=alpha)
        ax.set_ylabel("PC 2", alpha=alpha)
        ax.set_xlabel("PC 1", alpha=alpha)
        ax.grid(color="grey", alpha=alpha)
        plt.setp(ax.get_yticklabels(), alpha=alpha)
        plt.setp(ax.get_xticklabels(), alpha=alpha)

        # Save the plot
        fig.tight_layout()
        plt.savefig(describer.replace("\n","") + ".png",  bbox_inches="tight")
        plt.close()


if __name__ == "__main__":
    variance = 0.8
    pca_df = pca.pca_signatures(variance)
    meta_df = read_attributes_signatures.read_meta()
    att_df, sig_df = read_attributes_signatures.seperate_attributes_signatures(meta_df)
    plotting_df = pd.concat([pca_df, att_df], axis=1)
    plot_pca(plotting_df, att_df.columns)