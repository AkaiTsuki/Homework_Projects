from common.normalizer import *
from model.Cart import *
from common.validation import rmse
from common.validation import mae
from common.validation import mse


def printTree(root):
    if root:
        print root
        printTree(root.left)
        printTree(root.right)


def main():
    processor = DataProcessor()

    data = processor.readData('data/housing_train.txt', ' ', float)
    # processor.normalize(data, MinMaxScaler([0,1,2,7,9,10,11,12]))

    label = 13
    featuresCols = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    cart = Cart(data, featuresCols, label, 6)
    root = cart.build()
    print '=================Tree==============='
    printTree(root)

    actualLabel = data[:, label]
    pred = cart.predict(data, root)
    print '=========== Train Error Rates ==============='
    print 'MSE: ', mse(pred, actualLabel)
    print 'RMSE: ', rmse(pred, actualLabel)
    print 'MAE: ', mae(pred, actualLabel)

    # Test error rates
    test = processor.readData('data/housing_test.txt', ' ', float)
    #processor.normalize(test, MinMaxScaler([0,1,2,7,9,10,11,12]))

    actualLabel = test[:, label]
    pred = cart.predict(test, root)
    print '=========== Test Error Rates ==============='
    print 'MSE: ', mse(pred, actualLabel)
    print 'RMSE: ', rmse(pred, actualLabel)
    print 'MAE: ', mae(pred, actualLabel)


if __name__ == '__main__':
    main()