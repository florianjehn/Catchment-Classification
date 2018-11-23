# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 13:43:02 2018

@author: Florian Ulrich Jehn
"""
import matplotlib.pylab as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import pca
import read_attributes_signatures





if __name__ == "__main__":
    variance = 0.8
    pca_df = pca.pca_signatures(variance)
    meta_df = read_attributes_signatures.read_meta()
    att_df, sig_df = read_attributes_signatures.seperate_attributes_signatures(meta_df)