from common.CsvFileReader import *
from common.normalizer import *
from model.LinearRegression import *
from common.validation import rmse
from common.validation import mae
from common.validation import mse


def main():
    processor = DataProcessor()

    data = processor.readData('data/housing_train.txt', ' ', float)
    # scaler = ZeroMeanUnitVariation([0,1,2,7,9,10,11,12])
    scaler = MinMaxScaler([0, 1, 2, 7, 9, 10, 11, 12])
    processor.normalize(data, scaler)
    data = processor.appendNewColumn(data, 1.0, 0)

    label = 14
    featuresCols = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,13]
    lr = LinearRegression(data, featuresCols, label)
    coeff = lr.build()

    # Training error rates
    features = lr.constructX(data, featuresCols)
    actualLabel = lr.constructY(data, label)
    pred = lr.predict(features, coeff, True)
    print '=========== Training Error Rates ==============='
    print 'MSE: ', mse(pred, actualLabel)
    print 'RMSE: ', rmse(pred, actualLabel)
    print 'MAE: ', mae(pred, actualLabel)

    # Test error rates
    test = processor.readData('data/housing_test.txt', ' ', float)
    processor.normalize(test, scaler)
    test = processor.appendNewColumn(test, 1.0, 0)
    features = lr.constructX(test, featuresCols)
    actualLabel = lr.constructY(test, label)
    pred = lr.predict(features, coeff, True)

    print '=========== Test Error Rates ==============='
    print 'MSE: ', mse(pred, actualLabel)
    print 'RMSE: ', rmse(pred, actualLabel)
    print 'MAE: ', mae(pred, actualLabel)


if __name__ == '__main__':
    main()