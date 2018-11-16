# -*- coding: utf-8 -*-
"""
Created on Mai 07 13:54 2018
@author(s): Florian U. Jehn
"""
from spotpy.hydrology import signatures as sig
import pandas as pd


def calculate_signatures(stream_df: pd.DataFrame, transform_to_mm=True,
                         meta_df=None):
    """
    Calculates all signatures for a given streamflow.

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
    # Get all signatures
    signatures = sig.SignatureMethod.find_all()
    sig_df_list = []
    # Get all steam separately to calculate the signatures
    for stream in stream_df.columns:
        print("Calculating signatures for stream: " + str(stream))
        single_stream = pd.Series(stream_df[stream])
        # Calculate all signatures
        res = sig.SignatureMethod.run(signatures, single_stream)
        # Safe all signatures in a series
        stream_sigs_series = pd.Series()
        for sig_name, sig_value in res:
            temp = pd.Series(data=[sig_value], index=[sig_name])
            stream_sigs_series = stream_sigs_series.append(temp)
        stream_sigs_series.name = stream
        sig_df_list.append(stream_sigs_series)
    # Combine all streams into one df
    return pd.concat(sig_df_list, axis=1).transpose()


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
