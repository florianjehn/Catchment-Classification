# -*- coding: utf-8 -*-
"""
Created on Tue May 21 12:10:32 2019

@author: gh2668
"""
import pandas as pd
import read_attributes_signatures

def read_data():
    meta_df = read_attributes_signatures.read_meta()
    att_df, sig_df = read_attributes_signatures.seperate_attributes_signatures(meta_df)
    knoben = pd.read_csv("catchment_clusters_with_continoues_climate.csv", index_col=1)
    df = pd.merge(sig_df, knoben, right_index=True, left_index=True)
    df.drop(["FID", "gauge_lat", "gauge_lon", "b1_", "b2_", "b3_"], axis=1, inplace=True)
    df.columns = ['Mean annual discharge', 'Mean winter discharge', 'Mean half-flow date',
       'Q95 (high flow)', 'Runoff ratio', 'Mean summer discharge', "Catchment Cluster", "Aridity", "Seasonality", "Precipitation falling as snow"]
    # Rescale the data to the original values of Wouter
    # Find the new min max values by looking how far the current min max values 
    # are away to the min max of the range.
    df["Aridity"] = rescaler(df["Aridity"], 0, 1,  1, -1)
    df["Seasonality"] = rescaler(df["Seasonality"], 1, 0, 2, 0)

    
    return df


def rescaler(series, max_range_old, min_range_old ,max_range_new, min_range_new):
    """Rescales a series, while maintaining the distance of the highest 
    and lowest value in the data to the highest and lowest vlaue of the desired 
    rnage."""
    from sklearn.preprocessing import MinMaxScaler
    min_series_old = series.min()
    max_series_old = series.max()
#    print(max_series)
    minmax_to_mid_old = abs(max_range_old) - abs((max_range_old + min_range_old) / 2)
    minmax_to_mid_new = abs(max_range_new) - abs((max_range_new + min_range_new) / 2)
    # Calculate how big the max and min in the series are compared to the
    # maximal values possible
    diff_range_series_max_old = abs(max_range_old) - abs(max_series_old)
    diff_range_series_min_old = abs(min_range_old) - abs(min_series_old)
    #
    frac_to_max = diff_range_series_max_old / minmax_to_mid_old
    frac_to_min = diff_range_series_min_old / minmax_to_mid_old
    #
    diff_range_series_max_new = frac_to_max * minmax_to_mid_new
    diff_range_series_min_new = frac_to_min * minmax_to_mid_new
    #
    max_series_new = max_range_new - diff_range_series_max_new
    min_series_new = min_range_new - diff_range_series_min_new
   

    # Scale the data
    series = MinMaxScaler(feature_range=[min_series_new, max_series_new]).fit_transform(series.to_numpy().reshape(-1,1))
    return series   


df = read_data()
df.to_csv("knoben_climate_jehn_signatures_test.csv")