# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 12:16:31 2018

@author: Florian Ulrich Jehn
"""
import pca
import pandas as pd
import read_attributes_signatures
from sklearn.metrics import calinski_harabaz_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


def calculate_cluster_metrics(pca_df: pd.DataFrame, att_df: pd.DataFrame, num_classes):
    """
    Calculates the calinski harabaz score for all catchment attributes to
    determine the quality of the clustering.
    """
    att_cat_df = categories_meta(att_df, num_classes)
    ch_score_list = []
    for attribute in att_cat_df.columns:
        drop_df = pd.concat([pca_df, att_cat_df[attribute]], axis=1)
        # Drop Nan so the score can be calculated (only happens in geologic
        # porosoty. Do it seperately, so not all calculations are affected
        drop_df = drop_df.dropna()
        X = drop_df[["PC 1", "PC 2"]]
        X = StandardScaler().fit_transform(X)
        labels = drop_df[attribute]
        ch_score = calinski_harabaz_score(X=X, labels=labels)
        ch_score_list.append(ch_score)
    chs_df = pd.DataFrame({"Attributes": att_cat_df.columns,"Calinski-Harabaz Score": ch_score_list})
    chs_df.set_index("Attributes", inplace=True)
    return chs_df


def categories_meta(meta_df: pd.DataFrame, num_classes):
    """
    Sorts all parameters of the meta dataframe into categories. All
    categories are equal sized (except the already categorical like land cover)

    :param meta_df: Meta information for all catchments
    :return: meta_df where all parameters are classified
    """
    temp_df = meta_df.copy()
    for column in temp_df.columns:
        # Avoid already categorized data
        if column == "Dominant land cover":
            continue
        elif column == "Dominant geological class":
            continue
        elif column == "Timing of high\nprecipitation events":
            continue
        elif column == "Timing of low\nprecipitation events":
            continue
        else:
            # Difficult to determine the amount of classes
            temp_df.loc[temp_df.index, column] = (pd.qcut(temp_df[column], 
                                                  q=num_classes,
                                                  precision=1,
                                                  duplicates="drop"))
    return temp_df


def bar_plots_chs(chs_df, num_class):
    """
    Creates and saves bar plots of the chs scores
    """
    bars = chs_df.sort_values(by="Calinski-Harabaz Score").plot(kind="barh")
    fig = plt.gcf()
    fig.tight_layout()
    fig.set_size_inches(8.3, 11.7)
    plt.savefig("chs_"+str(num_class)+"_classes")
    plt.close()
    
    
    
    
    

if __name__ == "__main__":
    variance = 0.8
    pca_df = pca.pca_signatures(variance)
    meta_df = read_attributes_signatures.read_meta()
    att_df, sig_df = read_attributes_signatures.seperate_attributes_signatures(meta_df)

    
    for i in range(3, 31):
        chs_df = calculate_cluster_metrics(pca_df, att_df, i)
        bar_plots_chs(chs_df, i)

        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
