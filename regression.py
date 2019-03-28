# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 13:43:02 2018

@author: Florian Ulrich Jehn
"""
import matplotlib.pylab as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import pca
import read_attributes_signatures
import pandas as pd
import seaborn as sns
import matplotlib.patches as mpatches


def calc_poly_linear_regression(independent, dependent):
    """
    Calculates the coefficient of determination of a linear regresssion
    for an independent and an dependent variable and returns it
    """
    # Reshape for sklearn
    independent = independent.values.reshape(-1,1)
    dependent = dependent.values.reshape(-1,1)
    # Make the whole thing poly
    poly = PolynomialFeatures(degree=2)
    independent_ = poly.fit_transform(independent)
    # Do the linear regression
    model = LinearRegression()
    model.fit(independent_, dependent)
    # Calculate R2
    return model.score(independent_, dependent)


def cat_to_num(att_df):
    """
    Changes categorical variables in a dataframe to numerical
    """
    att_df_encode = att_df.copy(deep=True)
    for att in att_df_encode.columns:
        if att_df_encode[att].dtype != float:
            att_df_encode[att] = pd.Categorical(att_df_encode[att])
            att_df_encode[att] = att_df_encode[att].cat.codes
    return att_df_encode


def calc_all_linear_regressions(pca_df, att_df):
    """
    Calculates all linear regressions between two dataframes
    """
    r2_df = pd.DataFrame()
    for j, pc in enumerate(pca_df.columns):
        # Calculate all the r2 for a principal component
        pc_list = []
        for att in att_df.columns:
            # Calculate the single r2 score for one principal component 
            # and one catchment attribute
            r2_score = calc_poly_linear_regression(att_df[att], pca_df[pc])
            pc_list.append(r2_score)
        # Create the dataframe that contains the results
        current_pc = pd.DataFrame.from_records([pc_list], columns=att_df.columns)
        r2_df = pd.concat([r2_df, current_pc], axis=0)
    r2_df.index = pca_df.columns
    return r2_df


def weight_regression_by_var(r2_df, var_percents):
    """
    Weight the r2 scores of the different variables with principal components 
    by the explained variance in percent
    """
    # Transpose for easier looping
    r2_df = r2_df.transpose()
    for pc, var in zip(r2_df.columns, var_percents): 
        r2_df[pc] *= var
    r2_df["r2_weighted"] = r2_df.sum(axis=1)
    return r2_df["r2_weighted"]
    

def plot_regressions(r2_df_weighted, describer, color_dict, cols_classes):
    """
    Plots the weighted coefficient of determination
    """
    alpha=0.5
    ax = plt.gca()
    r2_df_weighted.sort_values().plot(ax=ax, kind="barh", color="#4C72B0",zorder=3)
    fig = plt.gcf()
    fig.tight_layout()
    fig.set_size_inches(10, 11.7)
    plt.xlim(0,1)
    for tick_label in ax.axes.get_yticklabels():
        tick_text = tick_label.get_text()
        tick_label.set_fontsize(14)
        tick_label.set_color(color_dict[tick_text])
    ax.xaxis.grid(color="grey", zorder=0)
    ax.set_facecolor("white")
    plt.xlabel("Weigthed Coefficient of Determination", alpha=alpha, fontsize=14)
    plt.ylabel("Catchment Attributes", alpha=alpha, fontsize=14)
    plt.setp(ax.get_xticklabels(), alpha=alpha)
    # Remove the borders
    for spine in ax.spines.values():
        spine.set_visible(False)
        
    # Create the legend
    handles = []
    for att, color in cols_classes.items():
        handles.append(mpatches.Patch(color=color, label=att))
    legend = ax.legend(handles=handles, frameon=True, fancybox=True, facecolor="white", edgecolor="grey",  fontsize=14)
    for text in legend.get_texts():
        text.set_color("grey")
    plt.savefig("r2_scores_ " + describer + ".png")
    

if __name__ == "__main__":
    # Dictionary for the broad categories
    color_dict = {"Area": "#D64139", "Mean elevation": "#D64139", "Mean slope": "#D64139",
                  "Fraction of precipitation\nfalling as snow": "royalblue", "Aridity": "royalblue", "Frequency of high\nprecipitation events": "royalblue",
                  "Depth to bedrock": "#D6BD39", "Sand fraction": "#D6BD39", "Clay fraction": "#D6BD39",
                  "Forest fraction": "forestgreen", "LAI maximum": "forestgreen", "Green vegetation\nfraction maximum": "forestgreen",
                  "Dominant geological class": "grey", "Subsurface porosity": "grey", "Subsurface permeability": "grey"}
    
    cols_classes = {"Climate": "royalblue", 
                    "Geology": "grey", 
                    "Soil": "#D6BD39", 
                    "Topography": "#D64139",
                    "Vegetation": "forestgreen"}
    
    variance = 0.8
    pca_df = pca.pca_signatures(variance)
    meta_df = read_attributes_signatures.read_meta()
    att_df, sig_df = read_attributes_signatures.seperate_attributes_signatures(meta_df)
    att_df_encode = cat_to_num(att_df)
    r2_df = calc_all_linear_regressions(pca_df, att_df_encode)
    var_percents = [0.74567053, 0.18828154]
    r2_df_weighted = weight_regression_by_var(r2_df, var_percents)
    plot_regressions(r2_df_weighted, "all", color_dict, cols_classes)
    
