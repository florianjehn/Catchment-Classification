
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 12:59:18 2018

@author: Florian Ulrich Jehn
"""

import pandas as pd

def read_meta():
    """
    Reads in the file with all the combined meta data and signatures
    """
    meta_df = pd.read_csv("meta.csv", sep=";", index_col=0)
    # Remove all rivers were something is missing
    meta_df.dropna(inplace=True)
    return meta_df


def seperate_attributes_signatures(meta_df):
    """
    Splits the meta file into the catchment attributes and the hydrological
    signatures and returns them in seperate dataframes.
    We only selected the attributes also used by Addor et al 2018
    """
    att_df = meta_df.loc[:, ["area_gages2","elev_mean", "slope_mean", "p_seasonality",
                             "frac_snow", "aridity","high_prec_freq", "soil_depth_pelletier",
                             "sand_frac", "clay_frac", "frac_forest", "lai_max", "gvf_max", 
                             "geol_1st_class", "geol_porostiy", "geol_permeability"
                              ]]
    # Rename the columns
    att_df.columns = ["Area", "Mean elevation", "Mean slope", "Precipitation seasonality",
                      "Fraction of precipitation\nfalling as snow", "Aridity", "Frequency of high\nprecipitation events",
                      "Depth to bedrock", "Sand fraction", "Clay fraction",
                      "Forest fraction", "LAI maximum", "Green vegetation\nfraction maximum",
                      "Dominant geological class",
                      "Subsurface porosity", "Subsurface permeability"]
    # Select the 6 best signatures 
    sig_df = meta_df.loc[:, ["mean_ann_dis", "mean_win_dis", "hfd_mean", "q95", "runoff_ratio", "mean_sum_dis"]]
    
    # Rename the columns
    sig_df.columns = ["Mean annual discharge", "Mean winter discharge", "Mean half-flow date", "Q95 (high flow)", "Runoff ratio", "Mean summer discharge"]
    return att_df, sig_df


if __name__ == "__main__":
    meta_df = read_meta()
    att_df, sig_df = seperate_attributes_signatures(meta_df)
    print("Attributes dataframe")
    print(att_df.describe(include="all"))
    print("Signatures dataframe")
    print(sig_df.describe())
    
    