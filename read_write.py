# -*- coding: utf-8 -*-
"""
Created on Mai 17 15:05 2018
@author(s): Florian U. Jehn
"""
import os
import pandas as pd
import sys
import csv
import datetime


def read_meta_data():
    """
    Reads in the meta data and returns them as dataframe.

    Expects to be in the dir were the data is stored.

    :return: meta_df
    """
    # Set the cwd to the directory of the file
    os.chdir(os.path.dirname(sys.argv[0]))
    cwd = os.getcwd()

    # Read in the files
    list_ = []
    os.chdir(cwd + os.sep + "meta_data")
    for file in os.listdir(os.getcwd()):
        if file.endswith(".txt"):
            temp_df = pd.read_table(file, sep=";", index_col=0)
            list_.append(temp_df)
    return pd.concat(list_, axis=1)


def save_signature_df(sig_df: pd.DataFrame):
    """
    Saves the signature dataframe as a file
    :param sig_df:
    :return: None
    """
    sig_df.to_csv("signatures.csv", sep=";", encoding="utf-8",
                  quoting=csv.QUOTE_MINIMAL)


def read_signatures():
    """
    Reads in the signature data and returns them as dataframe.

    Expects to be in the dir were the data is stored.

    :return: sig_df
    """
    # Set the cwd to the directory of the file
    os.chdir(os.path.dirname(sys.argv[0]))
    sig_df = pd.read_csv("signatures.csv", sep=";", header=0, index_col=0)
    return sig_df


def read_streamflow_data():
    """
    Reads in the streamflow data and returns them as dataframe.

    Expects to be in the dir were the data is stored.

    :return:  stream_df: Column names are the stream ids. Index is the date.

    """
    # Set the cwd to the directory of the file
    os.chdir(os.path.dirname(sys.argv[0]))
    cwd = os.getcwd()

    # Read in the files
    list_ = []
    os.chdir(cwd + os.sep + "usgs_streamflow")
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


def remove_no_flow_rivers(stream_df: pd.DataFrame, meta_df: pd.DataFrame,
                          frac_0=0.25):
    """
    Removes all rivers from stream_df where more than frac_0 of days have 0
    flow.

    :param stream_df:
    :param frac_0:
    :return:
    """
    print("bla")
    start_len = len(list(stream_df.columns))
    for stream in stream_df.columns:
        if stream_df[stream].quantile(q=frac_0) == 0:
            del stream_df[stream]
            del meta_df[stream]
    end_len = len(list(stream_df.columns))
    print("With quantile {} {} streams were removed".format(
                                                        frac_0,
                                                        (start_len - end_len)))
    return stream_df


def save_location_with_groups(meta_df: pd.DataFrame, groups):
    """

    :param meta_df:
    :param groups:
    :return:
    """
    loc_df = meta_df[["gauge_lat", "gauge_lon"]]
    loc_df["groups"] = groups
    loc_df.to_csv("loc_n_groups.csv", sep=";", encoding="utf-8",
                  quoting=csv.QUOTE_MINIMAL)
