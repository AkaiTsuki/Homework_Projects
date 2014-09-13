__author__ = 'jiachiliu'

from nulearn import cross_validation
from nulearn import tree
from nulearn.validation import mae
from nulearn.validation import mse
from nulearn.validation import rmse
from nulearn.validation import confusion_matrix
from nulearn.dataset import load_spambase
from nulearn.dataset import load_boston_house
from nulearn.tree import print_tree


def decision_tree():
    train, target = load_spambase()
    x_train, y_train, x_target, y_target = cross_validation.train_test_split(train, target, 0.1)

    print "=========Start Train=============="
    classifier = tree.DecisionTree()
    classifier = classifier.fit(x_train, x_target, 5)
    print "=========Finish Train=============="
    print "=========Tree=============="
    print_tree(classifier.root)

    print '=============Train Data Result============'
    er, acc, fpr, tpr = confusion_matrix(x_target, classifier.predict(x_train))
    print "Error rate: ", er, " accuracy: ", acc, " FPR: ", fpr, " TPR: ", tpr

    print '=============Test Data Result============'
    er, acc, fpr, tpr = confusion_matrix(y_target, classifier.predict(y_train))
    print "Error rate: ", er, " accuracy: ", acc, " FPR: ", fpr, " TPR: ", tpr


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
    print "mse: ", mse(predict, train_target), " rmse: ", rmse(predict, train_target), " mae: ", mae(predict, train_target)

    print '=============Test Data Result============'
    predict = classifier.predict(test)
    print "mse: ", mse(predict, test_target), " rmse: ", rmse(predict, test_target), " mae: ", mae(predict, test_target)


def main():
    # regression_tree()
    decision_tree()

if __name__ == '__main__':
    main()