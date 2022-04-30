#!/usr/bin/env python3
# encoding: utf-8

from os import path
from pickle import load

from sklearn.preprocessing import normalize
import pandas as pd
import numpy as np

"""
Encapsulates the model and its predictions
"""
class Predictor:
    def __init__(self, model_path, features):
        full_path = path.abspath(model_path)
        infile = open(full_path, 'rb')
        full_model = load(infile)
        infile.close()

        self.model = full_model[0]
        self.encoder = full_model[1]
        self.features = features

    def predict(self, house):
        """
        Predict the price for a single item.
        """
        # create DataFrame
        df = pd.DataFrame(house, index=[0])

        # set the columns in the correct order
        df = df.reindex(columns=self.features)

        # one-hot encode the ocean proximity
        prox = df['ocean_proximity'].values.reshape(-1, 1)
        ocean_proximity_train = self.encoder.transform(prox).toarray()

        # replace the categorical value with the encoded array
        df = df.drop('ocean_proximity', axis=1)
        X = np.concatenate((df, ocean_proximity_train),axis=1)

        # normalize data
        X = normalize(X)

        # predict the price
        Y = self.model.predict(X)            
        price = Y[0]

        return price