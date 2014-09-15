__author__ = 'jiachiliu'

from numpy.linalg import inv
import numpy as np


class LinearRegression(object):
    """docstring for LinearRegression"""

    def __init__(self):
        self.coeff = None

    def fit(self, train, target):
        self.coeff = inv(train.T.dot(train)).dot(train.T).dot(target)
        return self

    def predict(self, test):
        return test.dot(self.coeff)


class LogisticRegression(LinearRegression):
    def __init__(self):
        super(LogisticRegression, self).__init__()

    def predict(self, test):
        predict_vals = test.dot(self.coeff)
        predict_vals = 1.0 / (1 + np.exp(-predict_vals))
        for i in range(len(predict_vals)):
            if predict_vals[i] < 0.5:
                predict_vals[i] = 0
            else:
                predict_vals[i] = 1
        return predict_vals