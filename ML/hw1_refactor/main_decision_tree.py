__author__ = 'jiachiliu'

from nulearn import cross_validation
from nulearn import tree
from nulearn.validation import mae
from nulearn.validation import mse
from nulearn.validation import rmse
from nulearn.validation import confusion_matrix
from nulearn.validation import confusion_matrix_analysis
from nulearn.dataset import load_spambase
from nulearn.dataset import load_boston_house
from nulearn.tree import print_tree
import numpy as np
import logging


def decision_tree():
    train, target = load_spambase()

    # 10 fold cross validation
    train_size = len(train)
    k = 10
    test_index_generator = cross_validation.k_fold_cross_validation(train_size, k)
    fold = 0
    train_accuracy = 0
    test_accuracy = 0

    for start, end in test_index_generator:
        train_left = train[range(0, start)]
        train_right = train[range(end, train_size)]
        k_fold_train = np.vstack((train_left, train_right))
        test = train[range(start, end)]

        target_left = target[range(0, start)]
        target_right = target[range(end, train_size)]
        train_target = np.append(target_left, target_right)
        test_target = target[range(start, end)]

        cf = tree.DecisionTree()
        cf = cf.fit(k_fold_train, train_target, 5)
        print "=========Tree=============="
        print_tree(cf.root)

        print '=============Train Data Result============'
        cm = confusion_matrix(train_target, cf.predict(k_fold_train))
        print "confusion matrix: ", cm
        er, acc, fpr, tpr = confusion_matrix_analysis(cm)
        print 'Error rate: %f, accuracy: %f, FPR: %f, TPR: %f' % (er, acc, fpr, tpr)
        train_accuracy += acc

        print '=============Test Data Result============'
        cm = confusion_matrix(test_target, cf.predict(test))
        print "confusion matrix: ", cm
        er, acc, fpr, tpr = confusion_matrix_analysis(cm)
        print 'Error rate: %f, accuracy: %f, FPR: %f, TPR: %f' % (er, acc, fpr, tpr)
        test_accuracy += acc
        fold += 1

    print "Average train acc: %f, average test acc: %f" % (train_accuracy / fold, test_accuracy / fold)


def regression_tree():
    print "=========Start Train=============="
    train, train_target, test, test_target = load_boston_house()
    print len(train), len(test)
    classifier = tree.RegressionTree()
    classifier = classifier.fit(train, train_target, 2, -1)

    print "=========Finish Train=============="
    print "=========Tree=============="
    print_tree(classifier.root)

    print '=============Train Data Result============'
    predict = classifier.predict(train)
    print "mse: ", mse(predict, train_target), " rmse: ", rmse(predict, train_target), " mae: ", mae(predict,
                                                                                                     train_target)

    print '=============Test Data Result============'
    predict = classifier.predict(test)
    print "mse: ", mse(predict, test_target), " rmse: ", rmse(predict, test_target), " mae: ", mae(predict, test_target)


def main():
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s", level=logging.DEBUG)
    # regression_tree()
    decision_tree()


if __name__ == '__main__':
    main()