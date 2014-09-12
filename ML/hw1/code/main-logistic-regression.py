__author__ = 'jiachiliu'

from common.normalizer import *
from model.LinearRegression import *

def runClassifier(train, test):

    label = 58
    featuresCols = range(58)

    lr = LinearRegression(train, featuresCols, label)
    coeff = lr.build()

    # Training error rates
    features = lr.constructX(train, featuresCols)
    actualLabel = lr.constructY(train, label)
    predLabel = lr.predict(features, coeff, False)

    print '=============Train Data Result============'
    actPositive = len(actualLabel[actualLabel == 1])
    actNegtive = len(actualLabel[actualLabel == 0])
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
    features = lr.constructX(test, featuresCols)
    actualLabel = lr.constructY(test, label)
    actPositive = len(actualLabel[actualLabel == 1])
    actNegtive = len(actualLabel[actualLabel == 0])

    predLabel = lr.predict(features, coeff, False)
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
    scaler = ZeroMeanUnitVariation([0,1,2,7,9,10,11,12])
    # scaler = MinMaxScaler([0, 1, 2, 7, 9, 10, 11, 12])
    processor.normalize(data, scaler)
    data = processor.appendNewColumn(data, 1.0, 0)

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
        tr, te = runClassifier(train, test)
        trainAcc += tr
        testAcc += te

    print "average Train Acc: ", trainAcc / K
    print "average Test Acc: ", testAcc / K

if __name__ == '__main__':
    main()

