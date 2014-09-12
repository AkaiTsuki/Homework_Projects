from common.CsvFileReader import *
import numpy as np

class DataProcessor:
    def __init__(self):
        pass

    def normalize(self, dataset, scaler):
        scaler.scale(dataset)

    def appendNewColumn(self, dataset, values, pos):
        return np.insert(dataset, pos, values=values, axis=1)

    def readData(self, path, sep, dataType):
        reader = CsvFileReader(path)
        return reader.read(sep, dataType);

    def getFeatures(self, data, cols):
        return data[:, cols]

    def getLabels(self, data, label):
        return data[:, label]


class ZeroMeanUnitVariation:
    def __init__(self, cols):
        self.cols = cols
        self.meta = {}

    def scale(self, dataset):
        for col in self.cols:
            colVals = dataset[:, col]
            mean = colVals.mean()
            std = colVals.std()
            self.meta[col] = (mean, std)

        for i in range(dataset.shape[0]):
            for c in self.cols:
                dataset[i][c] = (dataset[i][c] - self.meta[c][0]) / self.meta[c][1]


class MinMaxScaler:
    '''
    X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
    '''

    def __init__(self, cols):
        self.cols = cols
        self.minMaxArr = {}

    def scale(self, dataset):
        # find min and max for each column
        self.findMinAndMaxForColumns(dataset)
        # caculate standard value for each value in dataset
        self.scaleOnDataset(dataset)

    def scaleOnDataset(self, dataset):
        for col in self.cols:
            (minVal, maxVal) = self.minMaxArr[col]
            self.scaleOnColumn(dataset, col, minVal, maxVal)

    def scaleOnColumn(self, dataset, col, minVal, maxVal):
        for i in range(self.getRowCount(dataset)):
            dataset[i][col] = (dataset[i][col] - minVal) / (maxVal - minVal)

    def findMinAndMaxForColumns(self, dataset):
        for col in self.cols:
            self.findMinAndMaxOnColumn(dataset, col)

    def findMinAndMaxOnColumn(self, dataset, col):
        minVal = min(dataset[:, col])
        maxVal = max(dataset[:, col])
        self.minMaxArr[col] = (minVal, maxVal)
        return self.minMaxArr[col]

    def getColumnCount(self, dataset):
        return dataset.shape[1]

    def getRowCount(self, dataset):
        return dataset.shape[0]