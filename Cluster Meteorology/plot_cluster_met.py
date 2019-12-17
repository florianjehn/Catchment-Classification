# -*- coding: utf-8 -*-
"""
Created on Tue Dec  10 11:11:02 2019

@author: Florian Ulrich Jehn
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot(precip, pet, temp, streamflow, snow_stor, snow_melt, clusters):
    """
    Creates a similarity plot for all clusters for different catchment attributes
    """
    alpha = 0.7
    attributes = {"Precipitation [mm]":precip,  "Temperature [°C]": temp, "Discharge [mm]":streamflow , "Pot. ET [mm]":pet,
                  "Snow Storage [mm]": snow_stor, "Snow Melt [mm]": snow_melt}
    ylim_dict = {"Precipitation [mm]":[0,20],  "Temperature [°C]": [-15,35], "Discharge [mm]":[0,25] ,  "Pot. ET [mm]":[0,10],
                  "Snow Storage [mm]": [0,1000], "Snow Melt [mm]": [0,20]}
    cluster_dict = {'1':"1 (n=230)", '2':"2 (n=101)", '3':"3 (n=7)", '4':"4 (n=52)",
                    '5':"5 (n=9)", '6':"6 (n=18)", '7':"7 (n=23)", '8':"8 (n=90)", 
                    '9':"9 (n=61)", '10':"10 (n=52)"}
    cluster_color_dict =  {'1':"#e6194B", '2':"#f58231", '3':"#fffac8", '4':"#bfef45",
                    '5':"#3cb44b", '6':"#42d4f4", '7':"#4363d8", '8':"#911eb4", 
                    '9':"#a9a9a9", '10':"#F2F2F2"}
    
    fig, axes = plt.subplots(nrows=10,ncols=len(attributes), sharex=True)
    used_catchments = [str(catch) for catch in clusters.gauge_index]    
    # Loop over all kinds of attributes
    for att_counter, (att_name, att_df) in enumerate(attributes.items()):
        print(att_name)
        # change all catchment ids to strings without leading 0
        att_df.columns = [str(int(catch)) for catch in att_df.columns]
        att_df.index = pd.to_datetime(att_df.index)
        # Sort current attribute by cluster
        clustered_attributes = {cluster:[] for cluster in clusters.gauge_cluster.unique()}
        # Loop over all clusters
        for cluster_counter, cluster in enumerate(sorted(clusters.gauge_cluster.unique(), key=lambda x:float(x))):
            print(cluster)
            for catchment in used_catchments:
                if cluster == clusters[clusters["gauge_index"] == catchment]["gauge_cluster"].values[0]:
                    clustered_attributes[cluster].append(att_df[catchment])
            cluster_df = pd.concat(clustered_attributes[cluster],axis=1)
            # Group cluster by doy and calculate mean for doy
            cluster_df["doy"] = cluster_df.index.dayofyear
            cluster_by_doy = cluster_df.groupby("doy").mean()
            ax = axes[cluster_counter, att_counter]
            # Plot all single catchments
            cluster_by_doy.plot(ax=ax, legend=False,  linewidth=0.3, zorder=3)
            # Plot mean of all catchments
            cluster_by_doy.mean(axis=1).plot(ax=ax, color="black", linewidth=1.3, zorder=5)
            # Norm the y axis
            ax.set_ylim(ylim_dict[att_name])
            if cluster_counter == 0:
                ax.set_title(att_name, alpha=alpha)
            if att_counter == 0:
                ax.set_ylabel(cluster_dict[cluster], 
                              backgroundcolor=cluster_color_dict[cluster], 
                              labelpad=5)
            if cluster_counter == 9:
                ax.set_xlabel("Day of year", alpha=alpha)
            # Make nice
            ax.grid(True, color="grey", zorder=0)
            plt.setp(ax.get_yticklabels(), alpha=alpha)
            plt.setp(ax.get_xticklabels(), alpha=alpha)
            ax.tick_params(axis=u'both', which=u'both',length=0)
            for spine in ax.spines.values():
                spine.set_edgecolor("lightgrey")

    fig.set_size_inches(22,22)
    plt.savefig("cluster_met.png", dpi=400, bbox_inches="tight")
    
            
        

def cubic_feet_to_mm(stream_df: pd.DataFrame, meta_df: pd.DataFrame, clusters):
    """
    Transforms all values from cubic feet per second to mm per day.

    This avoids a clustering by catchment area
    :param stream_df: in cubic feet
    :param meta_df: needed for stream catchment area
    :return: stream_df: in mm
    """
    for stream in clusters.gauge_index:
        # 0.0283168 = conversion factor from cubic feet to cubic meters
        discharge_cubic_meter_per_second = stream_df[str(stream)] * 0.0283168
        seconds_per_day = 86400
        discharge_cubic_m_per_day = (discharge_cubic_meter_per_second *
                                     seconds_per_day)
        area_square_m = meta_df.loc[stream, "area_geospa_fabric"] * 1e6
        discharge_mm = (discharge_cubic_m_per_day * 1000) / area_square_m
        stream_df[str(stream)] = discharge_mm
    return stream_df.loc[:,[str(gauge) for gauge in clusters.gauge_index]]
            
if __name__ == "__main__":
    precip = pd.read_csv("precip.csv", sep=";", index_col=0)
    temp = pd.read_csv("temperature.csv", sep=";", index_col=0)
    streamflow = pd.read_csv("streamflow.csv", sep=";", index_col=0)
    pet = pd.read_csv("pet.csv", sep=";", index_col =0)
    snow_stor = pd.read_csv("snow_storage.csv", sep=";", index_col=0)
    snow_melt = pd.read_csv("snow_melt.csv", sep=";", index_col=0)
    meta = pd.read_csv("meta.csv", sep=";", index_col=0)

    clusters = pd.read_csv("gauge_pos_cluster_climate.csv", sep=";")
    clusters["gauge_cluster"] = [str(cluster + 1) for cluster in clusters.gauge_cluster]
    streamflow = cubic_feet_to_mm(streamflow, meta, clusters)
    clusters.gauge_index = [str(gauge) for gauge in clusters.gauge_index]
    #clusters.gauge_cluster = [int(cluster.split("\n")[0]) for cluster in clusters.gauge_cluster]
    plot(precip, pet,temp, streamflow, snow_stor, snow_melt, clusters)
