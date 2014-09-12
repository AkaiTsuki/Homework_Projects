from numpy.linalg import inv
import numpy as np


class LinearRegression(object):
    """docstring for LinearRegression"""

    def __init__(self, data, features, label):
        super(LinearRegression, self).__init__()
        self.label = label
        self.X = self.constructX(data, features)
        self.Y = self.constructY(data, label)

    def constructY(self, data, label):
        return data[:, label]

    def constructX(self, data, features):
        return data[:, features]

    def build(self):
        X = self.X
        Y = self.Y
        return inv(X.T.dot(X)).dot(X.T).dot(Y)

    def logistic(self, X, coeff):
        theta = X.dot(coeff)
        pred = 1.0 / (1 + np.exp(-theta))
        return np.array(map(self.mappingFunc, pred))

    def mappingFunc(self, v):
        if v >= 0.5:
            return 1.0
        else:
            return 0.0

    def predict(self, test, coeff, regression):
        if regression:
            return test.dot(coeff)
        else:
            return self.logistic(test, coeff)

    def predictOne(self, point, coeff):
        sum = 0;
        for i in range(len(point)):
            sum = sum + coeff[i] * point[i]
        return sum