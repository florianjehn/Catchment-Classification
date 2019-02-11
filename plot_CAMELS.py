# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 09:28:17 2018

@author: Florian Ulrich Jehn
"""

import seaborn as sns
import pandas as pd
import read_attributes_signatures
import matplotlib.pyplot as plt


def plot_CAMELS(att_df):
    """
    Plots all the attributes of CAMELS in one figure
    """
    fig, axes = plt.subplots(nrows=5, ncols=3)#, gridspec_kw = {'wspace':0.5, 'hspace':2})
    axes = axes.reshape(-1)
    for i, att in enumerate(att_df.columns):
        # skip non numerical
        if att_df[att].dtype != float:
            continue
        ax = axes[i]
        ax.yaxis.label.set_visible(False)
        ax.set_title(att)
        sns.violinplot(y=att_df[att], ax=ax, cut=0)
    
    fig.tight_layout()
    plt.savefig("atts_CAMELS.png", dpi=200)

if __name__ == "__main__":
    # Get the catchment attributes
    meta_df = read_attributes_signatures.read_meta()
    att_df, sig_df = read_attributes_signatures.seperate_attributes_signatures(meta_df)
    plot_CAMELS(att_df)
        
    