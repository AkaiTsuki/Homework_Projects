__author__ = 'jiachiliu'

from nulearn.preprocessing import normalize
from nulearn.dataset import load_boston_house
from nulearn.linear_model import LinearRegression
from nulearn.validation import mae
from nulearn.validation import mse
from nulearn.validation import rmse


def linear_regression():
    train, train_target, test, test_target = load_boston_house()

    normalize_columns = [0, 1, 2, 6, 7, 9, 10, 11, 12]
    normalize(train, normalize_columns)
    normalize(test, normalize_columns)

    lr = LinearRegression()
    lr.fit(train, train_target)

    print '=============Train Data Result============'
    predict = lr.predict(train)
    print "mse: ", mse(predict, train_target), " rmse: ", rmse(predict, train_target), " mae: ", mae(predict,
                                                                                                     train_target)
    print '=============Test Data Result============'
    predict = lr.predict(test)
    print "mse: ", mse(predict, test_target), " rmse: ", rmse(predict, test_target), " mae: ", mae(predict, test_target)


def main():
    linear_regression()


if __name__ == '__main__':
    main()