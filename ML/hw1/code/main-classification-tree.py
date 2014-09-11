__author__ = 'jiachiliu'

from common.normalizer import *
from model.ClassificationTree import *
from common.validation import rmse
from common.validation import mae
from common.validation import mse


def printTree(root):
    if root:
        print root
        printTree(root.left)
        printTree(root.right)


def runClassifier(train, test, maxLevel):
    label = 57
    featuresCols = range(57)

    cart = ClassificationTree(train, featuresCols, label, {}, maxLevel)
    root = cart.build()
    print '=================Tree==============='
    printTree(root)

    print '=============Train Data Result============'
    actualLabel = train[:, label]
    actPositive = len(actualLabel[actualLabel == 1])
    actNegtive = len(actualLabel[actualLabel == 0])
    predLabel = cart.predict(train, root)
    predPositive = len(predLabel[predLabel == 1])
    predNegative = len(predLabel[predLabel == 0])

    print "actPositive: ", actPositive, " actNeg: ", actNegtive, " predPos: ", predPositive, "predNeg: ", predNegative

    missClass = 0
    for i in range(len(actualLabel)):
        if actualLabel[i] != predLabel[i]:
            missClass += 1
            # print "(act, pred) = ", (actualLabel[i], predLabel[i])
    trainAcc = 1.0 * (len(actualLabel) - missClass) / len(actualLabel)
    print "Total data: ", len(actualLabel), "Total error: ", missClass, "accuracy: ", trainAcc

    print '=============Test Data Result============'
    actualLabel = test[:, label]
    actPositive = len(actualLabel[actualLabel == 1])
    actNegtive = len(actualLabel[actualLabel == 0])
    predLabel = cart.predict(test, root)
    predPositive = len(predLabel[predLabel == 1])
    predNegative = len(predLabel[predLabel == 0])
    print "actPositive: ", actPositive, " actNeg: ", actNegtive, " predPos: ", predPositive, "predNeg: ", predNegative
    missClass = 0
    for i in range(len(actualLabel)):
        if actualLabel[i] != predLabel[i]:
            missClass += 1
            # print "(act, pred) = ", (actualLabel[i], predLabel[i])
    testAcc = 1.0 * (len(actualLabel) - missClass) / len(actualLabel)
    print "Total data: ", len(actualLabel), "Total error: ", missClass, "accuracy: ", testAcc

    return trainAcc, testAcc


def main():
    processor = DataProcessor()
    data = processor.readData('data/spambase.data', ',', float)
    K = 10
    par = len(data) / K

    trainAcc = 0
    testAcc = 0

    for i in range(K):
        allRows = range(len(data))
        trainingIndices = []
        testIndices = []
        for j in allRows:
            if i * par <= j < i * par + par:
                testIndices.append(j)
            else:
                trainingIndices.append(j)
        train = data[trainingIndices]
        test = data[testIndices]

        print "Run Classifier on batch ", i
        tr, te = runClassifier(train, test, 3)
        trainAcc += tr
        testAcc += te

    print "average Train Acc: ", trainAcc / K
    print "average Test Acc: ", testAcc / K

    # processor.normalize(data, MinMaxScaler([0,1,2,7,9,10,11,12]))


if __name__ == '__main__':
    main()