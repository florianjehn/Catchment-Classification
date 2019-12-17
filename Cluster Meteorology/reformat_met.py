# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 14:05:45 2019

@author: Florian Ulrich Jehn
"""

import pandas as pd
import os
import sys
import datetime
import simple_snowmelt


def read_met_data():
    """
    Reads in the streamflow data and returns them as dataframe.

    Expects to be in the dir were the data is stored.

    :return:  stream_df: Column names are the stream ids. Index is the date.

    """
    # Set the cwd to the directory of the file
    os.chdir(os.path.dirname(sys.argv[0]))

    # Read in the files
    list_prec = []
    list_temp = []
    list_et = []
    list_snowmelt = []
    list_snow_stor = []
    os.chdir(org_os + os.sep + "basin_dataset_public_v1p2" + os.sep + "basin_mean_forcing" + os.sep + "daymet")
    temp_cwd = os.getcwd()
    
    # Go through the directory order of the CAMELS data set
    for name in os.listdir(temp_cwd):
        print("Directory = " + name)
        os.chdir(temp_cwd + os.sep + name)
        for file in os.listdir(os.getcwd()):
            print(file)
            if file.endswith(".txt"):
                # Use a regular expression to seperate by different
                # amounts of whitespaces
                temp_df = pd.read_csv(file, skiprows=4, sep="\t", header=None,
                                        engine="python",
                                        na_values=-999.00, index_col=0)
                # Get the date as index
                temp_df.index = pd.to_datetime(temp_df.index)
                temp_df.columns = ["dayl(s)","prcp(mm/day)", "srad(W/m2)", "swe(mm)",  "tmax(C)", "tmin(C)","vp(Pa)"]
                temp_df["tmean(C)"] = (temp_df["tmax(C)"] + temp_df["tmin(C)"]) / 2 
                prec_df = temp_df["prcp(mm/day)"]
                prec_df.name = file.split("_")[0]
                temperature_df = temp_df["tmean(C)"]
                temperature_df.name = file.split("_")[0]
                et_rad = watt_to_MJ(temp_df["srad(W/m2)"])
                et_df = hargreaves(temp_df["tmin(C)"], temp_df["tmax(C)"], temp_df["tmean(C)"], et_rad)
                et_df.name = file.split("_")[0]
                snow_storage_df, snow_melt_df = simple_snowmelt.snow_model(prec_df, temperature_df)
                snow_storage_df.name = file.split("_")[0]
                snow_melt_df.name = file.split("_")[0]

                list_prec.append(prec_df)
                list_temp.append(temperature_df)
                list_et.append(et_df)
                list_snowmelt.append(snow_melt_df)
                list_snow_stor.append(snow_storage_df)
    
    # Combine all separate streams into one dataframe.
    return [pd.concat(dfs, axis=1) for dfs in [list_prec, list_temp, list_et, list_snow_stor, list_snowmelt]]


def hargreaves(tmin, tmax, tmean, et_rad):
    """
    Calculates hargreaves PET based on equation 52 in Allen et al (1998).
    :param tmin: Minimum daily temperature [deg C]
    :param tmax: Maximum daily temperature [deg C]
    :param tmean: Mean daily temperature [deg C]. If emasurements not
        available it can be estimated as (*tmin* + *tmax*) / 2.
    :param et_rad: Extraterrestrial radiation (Ra) [MJ m-2 day-1]. Can be
        estimated using ``et_rad()``.
    :return: Reference evapotranspiration over grass (ETo) [mm day-1]
    :rtype: float
    """
    # Note, multiplied by 0.408 to convert extraterrestrial radiation could
    # be given in MJ m-2 day-1 rather than as equivalent evaporation in
    # mm day-1
    return 0.0023 * (tmean + 17.8) * (tmax - tmin) ** 0.5 * 0.408 * et_rad


def watt_to_MJ(watt_m2):
    """
    Transform watt per m² to MJ per m² per day
    """
    joule_m2_s = watt_m2
    joule_m2_day = joule_m2_s * 86400
    mjoule_m2_day = joule_m2_day / 1000000
    return mjoule_m2_day


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
    os.chdir(cwd +  os.sep + "basin_dataset_public_v1p2" + os.sep + "usgs_streamflow")
    temp_cwd = os.getcwd()
    # Go through the directory order of the CAMELS data set
    for name in os.listdir(temp_cwd):
        print("Directory = " + name)
        os.chdir(temp_cwd + os.sep + name)
        for file in os.listdir(os.getcwd()):
            if file.endswith(".txt"):
                # Use a regular expression to seperate by different
                # amounts of whitespaces
                temp_df = pd.read_csv(file, header=None, sep=r"\s+",
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
    

    
    
if __name__ == "__main__":
    used_catchments = pd.read_csv("gauge_pos_cluster_climate.csv", sep=";")
    org_os = os.getcwd()
 #   streamflow = read_streamflow_data()
    precip, temp, pet, snow_stor, snow_melt = read_met_data()
    os.chdir(org_os)
 #   streamflow.to_csv("streamflow.csv", sep=";")
    precip.to_csv("precip.csv",sep=";")
    pet.to_csv("pet.csv", sep=";")
    temp.to_csv("temperature.csv", sep=";")
    snow_stor.to_csv("snow_storage.csv", sep=";")
    snow_melt.to_csv("snow_melt.csv", sep=";")