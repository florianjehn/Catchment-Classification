# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 08:56:58 2019

@author: Florian Ulrich Jehn
"""

import pandas as pd
import numpy as np


def snow_model(precip:pd.Series, t_mean:pd.Series):
    """
    Calculates the snow based on a simple temperature based model as described
    in Massmann (2019) "Modelling snow in ungauged catchments" with fixed values
    for the snow melt threshold and the degree day factor
    """
    degree_day = 4 # mm per °C per day
    t_tresh = 1.7 # °C treshold for precipitation being considered snow
    t_melt = 0 # °C melting temperature for snow
    snow_storage = pd.Series(index = precip.index)
    snow_melt = pd.Series(index = precip.index)
    for day in precip.index:
        # Initialize for first day
        if day == precip.index[0]:
            # If its cold precip comes as snow
            if t_mean[day] <= t_tresh:
                snow_storage[day] = round(precip[day],1)
            else:
                snow_storage[day] = 0
            # We do not know how much snow there is at the first day, so nothing can melt
            snow_melt[day] = 0
        else:
            # If not the first day, calculate how much the snow  melts
            if t_mean[day] >= t_melt:
                # Calculate how much can melt based on the temperature
                snow_melt[day] = round(degree_day * (t_mean[day] - t_melt),1)
                # Not more snow can melt, than there is in the storage
                if snow_melt[day] > snow_storage.iloc[snow_storage.index.get_loc(day) - 1]:
                    snow_melt[day] = round(snow_storage.iloc[snow_storage.index.get_loc(day) - 1],1)
            else:
                # Nothing melts when its cold
                snow_melt[day] = 0
            if t_mean[day] <= t_tresh:
                # If its cold precip comes as snow
                snow_storage[day] = round(snow_storage.iloc[snow_storage.index.get_loc(day) - 1] + precip[day] - snow_melt[day],1)
            else:
                snow_storage[day] = round(snow_storage.iloc[snow_storage.index.get_loc(day) - 1] - snow_melt[day],1)
            # We cannot have negative snow storage
            if snow_storage[day] < 0:
                snow_storage[day] = 0
    return snow_storage, snow_melt
        
        
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    np.random.seed(5)
    precip = pd.Series([np.random.randint(0,10) for i in range(50)])
    t_mean = pd.Series([5.9359, 7.0897,8.2436,8.6282,7.4744,0.5513,-2.141,-6.3718,
                       -9.8333,-14.8333,-15.218,-12.5256,-9.8333,-2.9103,2.859,10.1667,
                       13.6282,13.6282,14.3974,14.3974,14.3974,14.3974,14.0128,15.1667,
                       17.859,19.782,14.6282,5.2436,5.9359,3.859,12.0897,5.9359,
                       1.3205,-2.5256,-4.8333,-4.4487,0.5513,4.3974,8.6282,10.5513,
                       2.3205,10.3974,-5.782,-3.859,10.0128,14.3974,7.0897,-4.8333,
                       13.6282,20.1667])
    
    snow_storage, snow_melt = snow_model(precip, t_mean)
    ax = plt.gca()
    ax.plot(precip, label="precip")
    ax.plot(t_mean, label="tmean")
    ax.plot(snow_storage, label="snow storage")
    ax.plot(snow_melt, label = "snow melt")    
    ax.legend()