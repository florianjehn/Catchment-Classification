# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 10:45:36 2020

@author: Florian Jehn
"""

# Get the neccesary packages

import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import folium
from shapely.geometry import Point
from pyproj import CRS


# print("Reading in stuff")
# # Read in the US outlines and remove Alaska, Hawai and Puerto Rico. 
# us = gpd.read_file("cb_2017_us_state_20m/cb_2017_us_state_20m.shp")
# us = us.drop(us[us["NAME"]=="Alaska"].index,axis=0)
# us = us.drop(us[us["NAME"]=="Hawaii"].index,axis=0)
# us = us.drop(us[us["NAME"]=="Puerto Rico"].index,axis=0)

# # Read in teh ecoregions
# eco = gpd.read_file("na_cec_eco_l1/NA_CEC_Eco_Level1.shp")

# # Make sure both have the same crs
# us = us.to_crs(eco.crs)


# print("Clipping")
# # Clip
# eco_us = gpd.overlay(eco, us, how="intersection")
# eco_us = eco_us.dissolve(by="NA_L1NAME")
# eco_us = eco_us.reset_index()

eco_us = gpd.read_file("eco_us.shp")

# Get the catcfhments
catchments = pd.read_csv("gauge_pos_cluster_climate.csv",sep=";")

print("Starting maping the map")
# Create the map instance
m = folium.Map(location=[39.50,-98.35], zoom_start=4, control_scale=True, tiles='Stamen Toner')

# # Add the regions
color_dict = {"EASTERN TEMPERATE FORESTS":"#BCDA8D",
              "GREAT PLAINS":"#F7CE9C",
              "MARINE WEST COAST FOREST":"#46C0BE",
              "MEDITERRANEAN CALIFORNIA":"#D2E6B6",
              "NORTH AMERICAN DESERTS":"#F9DD6A",
              "NORTHERN FORESTS":"#AFDFE5",
              "NORTHWESTERN FORESTED MOUNTAINS":"#5FBC56",
              "SOUTHERN SEMIARID HIGHLANDS":"#DCD493",
              "TEMPERATE SIERRAS":"#BCDA8D",
              "TROPICAL WET FORESTS":"#C675AF",
              "WATER":"#FFFFFF"}
for index, row in eco_us.iterrows():
    print(index)
    style_function=lambda x, fillColor=color_dict[row["NA_L1NAME"]], color="white": {
                "fillColor": fillColor,
                "color": color,
                "fillOpacity":0.9}
    region = gpd.GeoDataFrame(row).transpose()
    region.crs = eco_us.crs
    gjson = folium.features.GeoJson(region, style_function=style_function, name=row["NA_L1NAME"])
    # Creata a popup
    popup = folium.Popup(row["NA_L1NAME"])
    popup.add_to(gjson)
    gjson.add_to(m)
    


# Add the catchments
colors= ["#e6194B", "#f58231", "#fffac8", "#bfef45",  "#3cb44b", 
         "#42d4f4", "#4363d8", "#911eb4", "#a9a9a9", "#ffffff"]
for index, row in catchments.iterrows():
    popup_str = "Index: {} Cluster: {} Aridity: {} Seasonality: {} Snow_Fraction: {}".format(
        int(row["gauge_index"]), int(row["gauge_cluster"]+ 1), round(row["Aridity"],2),
        round(row["seasonality"],2), round(row["precip_as_snow"],2))
    folium.vector_layers.CircleMarker(location= (row["gauge_lat"],row["gauge_lon"]), 
                     popup=popup_str,
                     fill_color= colors[int(row["gauge_cluster"])],
                     color="#353537",
                     fill_opacity=1,
                     opacity=1,
                     radius=8).add_to(m)


        



print("Saving the map")
# Save the map
m.save("map.html")