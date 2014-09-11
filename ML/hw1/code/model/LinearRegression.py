from numpy.linalg import inv

class LinearRegression(object):
    """docstring for LinearRegression"""
    def __init__(self, data, features, label):
        super(LinearRegression, self).__init__()
        self.label = label
        self.X = self.constructX(data, features)
        self.Y = self.constructY(data, label)

    def constructY(self, data, label):
        return data[:,label]

    def constructX(self, data, features):
        return data[:,features]

    def build(self):
        X = self.X
        Y = self.Y
        return inv(X.T.dot(X)).dot(X.T).dot(Y)

    def predict(self, test, coeff):
        return test.dot(coeff)

    def predictOne(self, point, coeff):
        sum = 0;
        for i in range(len(point)):
            sum = sum + coeff[i]*point[i]
        return sum