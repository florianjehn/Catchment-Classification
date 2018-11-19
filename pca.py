# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 12:59:09 2018

@author: Florian Ulrich Jehn
"""
import pandas as pd
import read_attributes_signatures
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np


def pca_signatures():
    """
    Does a principal component analysis on the signature dataframe so that the 
    number of principal components accounts for at least 80 % of the total 
    variance of the original variables
    """
    # Get the data
    meta_df = read_attributes_signatures.read_meta()
    att_df, sig_df = read_attributes_signatures.seperate_attributes_signatures(meta_df)
    
    # Perform the pca
    pca = PCA(n_components=0.8, svd_solver="full")
    # Standardize the data, so the PCA makes more sense
    standardized_df = StandardScaler().fit_transform(sig_df)
    # Calculate the components
    principal_components = pca.fit_transform(np.array(standardized_df))
    # Make it a dataframe again
    principal_df = pd.DataFrame(data=principal_components, index=sig_df.index)
    # Give the columns more meaningful names
    principal_df.columns = ["PC " + str(i) for i in range(1, len(principal_df.columns) + 1)]
    return principal_df


if __name__ == "__main__":
    pca_df = pca_signatures()
    print(pca_df.describe())