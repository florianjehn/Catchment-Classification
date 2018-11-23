# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 13:43:02 2018

@author: Florian Ulrich Jehn
"""
import matplotlib.pylab as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import pca
import read_attributes_signatures


def calc_poly_linear_regression(independent, dependent):
    """
    Calculates the coefficient of determination of a linear regresssion
    for an independent and an dependent variable and returns it
    """
    independent = independent.reshape(-1,1)
    dependent = dependent.reshape(-1,1)
    poly = PolynomialFeatures(degree=2)
    independent_ = poly.fit_transform(independent)
    model = LinearRegression()
    # Fit the model
    model.fit(independent_, dependent)
    print(model.score(independent_, dependent))

def cat_to_num:
    """
    Changes categorical variables to numerical
    """
    pass


if __name__ == "__main__":
    variance = 0.8
    pca_df = pca.pca_signatures(variance)
    meta_df = read_attributes_signatures.read_meta()
    att_df, sig_df = read_attributes_signatures.seperate_attributes_signatures(meta_df)
    for att in att_df.columns:
        if att_df[att].dtype == float:

            print(att)
        
            calc_poly_linear_regression(att_df[att], pca_df["PC 2"])