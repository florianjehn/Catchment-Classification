# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 13:45:37 2018

@author: Florian Ulrich Jehn
"""
import os
import pandas as pd
import sys
import csv
import datetime


def read_meta_data():
    """
    Reads in the meta data and returns them as dataframe.
    
    :return: meta_df
    """
    # Set the cwd to the directory of the file
    os.chdir(os.path.dirname(sys.argv[0]))

    # Read in the files
    list_ = []
    os.chdir(os.pardir + os.sep + "data" +  os.sep + "camels_attributes_v2.0")
    for file in os.listdir(os.getcwd()):
        if file.endswith(".txt"):
            temp_df = pd.read_table(file, sep=";", index_col=0)
            list_.append(temp_df)
    return pd.concat(list_, axis=1)


def read_streamflow_data():
    """
    Reads in the streamflow data and returns them as dataframe.

    :return:  stream_df: Column names are the stream ids. Index is the date.
    """
    # Set the cwd to the directory of the file
    os.chdir(os.path.dirname(sys.argv[0]))

    # Read in the files
    list_ = []
    os.chdir(os.pardir + os.sep + "data" +  os.sep + "usgs_streamflow")
    temp_cwd = os.getcwd()
    # Go through the directory order of the CAMELS data set
    for name in os.listdir(temp_cwd):
        print("Directory = " + name)
        os.chdir(temp_cwd + os.sep + name)
        for file in os.listdir(os.getcwd()):
            if file.endswith(".txt"):
                # Use a regular expression to seperate by different
                # amounts of whitespaces
                temp_df = pd.read_table(file, header=None, sep=r"\s+",
                                        engine="python",
                                        na_values=-999.00)
                # Get the date as index
                temp_df.index = temp_df.apply(
                                lambda x:
                                datetime.datetime.strptime(
                                "{0} {1} {2} 00:00:00".format(
                                            x[1], x[2], x[3]),
                                "%Y %m %d %H:%M:%S"), axis=1)
                name = temp_df[0].unique()
                temp_df = pd.Series(temp_df[4])
                temp_df.name = name[0]
                list_.append(temp_df)
    # Combine all separate streams into one dataframe.
    return pd.concat(list_, axis=1)


def calculate_signatures(stream_df: pd.DataFrame, transform_to_mm=True,
                         meta_df=None):
    """
    Calculates the signatures mean_annual_discharge, mean_winter_discharge and 
	mean_sommer_discharge

    :param stream_df:
    :param transform_to_mm: bool
    :param meta_df:
    :return: Returns a dataframe for all hydrological signatures for all
    catchments, with the catchment name as index and the signatures as
    column.
    """
    # Convert to a unit which is normalized to the catchment area. This
    # avoids a clustering by catchment area
    if transform_to_mm:
        stream_df = cubic_feet_to_mm(stream_df, meta_df)

    sig_df_list = []
    # Get all steam separately to calculate the signatures
    for stream in stream_df.columns:
        print("Calculating signatures for stream: " + str(stream))
        single_stream = pd.Series(stream_df[stream])
        # Safe the mean discharge for the river
        yearly_dis = []
        summer_dis = []
        winter_dis = []
        # Seperate the stream by years
        for year in set(single_stream.index.year):
            stream_year = single_stream.loc[single_stream.index.year == year]
            # skip years without data
            if stream_year.isnull().values.any():
                continue
            sum_year = stream_year.sum()
            yearly_dis.append(sum_year)
            sum_winter = stream_year[stream_year.index.month.isin([11, 12, 1, 2, 3, 4])].sum()
            winter_dis.append(sum_winter)
            sum_summer = stream_year[stream_year.index.month.isin([5, 6, 7, 8, 9, 10])].sum()     
            summer_dis.append(sum_summer)     
        # Combine the signatures
        stream_sigs = pd.DataFrame({"mean_ann_dis":(sum(yearly_dis) / len(yearly_dis)),
                                    "mean_sum_dis":(sum(summer_dis) / len(summer_dis)),
                                    "mean_win_dis":(sum(winter_dis) / len(winter_dis))},
                                    index=[stream])
        sig_df_list.append(stream_sigs)
    # Combine all streams into one df
    return pd.concat(sig_df_list, axis=0)


def cubic_feet_to_mm(stream_df: pd.DataFrame, meta_df: pd.DataFrame):
    """
    Transforms all values from cubic feet per second to mm per day.

    This avoids a clustering by catchment area
    :param stream_df: in cubic feet
    :param meta_df: needed for stream catchment area
    :return: stream_df: in mm
    """
    for stream in stream_df.columns:
        # 0.0283168 = conversion factor from cubic feet to cubic meters
        discharge_cubic_meter_per_second = stream_df[stream] * 0.0283168
        seconds_per_day = 86400
        discharge_cubic_m_per_day = (discharge_cubic_meter_per_second *
                                     seconds_per_day)
        area_square_m = meta_df.loc[stream, "area_geospa_fabric"] * 1e6
        discharge_mm = (discharge_cubic_m_per_day * 1000) / area_square_m
        stream_df[stream] = discharge_mm
    return stream_df


def finish_and_save(to_del):
    """
    Adds the newly calculated signatures to the dataframe and removes all meta
    information and signatures that are unwanted
    """
    # Read in the info
    stream_df = read_streamflow_data()
    meta_df = read_meta_data()
    # Calculate the new signatures
    new_sigs = calculate_signatures(stream_df, meta_df=meta_df)
    # Combine the new and old meta stuff
    meta_df = meta_df.merge(new_sigs, left_index=True, right_index=True)
    # Remove all unwanted stuff
    meta_df.drop(to_del, inplace=True, axis=1)
    # Set the cwd to the directory of the file
    os.chdir(os.path.dirname(sys.argv[0]))
    # Save it
    meta_df.to_csv("meta.csv", sep=";", encoding="utf-8",
              quoting=csv.QUOTE_MINIMAL)

finish_and_save(["lai_diff", "gvf_diff", "soil_porosity", "soil_conductivity",
                 "geol_2nd_class", "glim_2nd_class_frac", "q_mean", "stream_elas",
                 "slope_fdc", "baseflow_index", "q5", "high_q_freq", "high_q_dur",
                 "low_q_freq", "low_q_dur", "zero_q_freq"])
    
    

