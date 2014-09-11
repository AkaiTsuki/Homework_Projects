__author__ = 'jiachiliu'

import unittest
import numpy as np
from model.ClassificationTree import ClassificationTree


class TestClassificationTree(unittest.TestCase):
    def testFindAllSplitPointOnNominal(self):
        ct = ClassificationTree()
        D = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [1, 2, 4, 5]], float)
        actual = ct.findAllSplitPointOnNominal(D, 0)
        self.assertListEqual(actual.tolist(), [1, 5])

    def testFindAllSplitPointOnContinue(self):
        ct = ClassificationTree()
        D = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [1, 2, 4, 5]], float)
        actual = ct.findAllSplitPointOnContinue(D, 2)
        self.assertListEqual(actual.tolist(), [3.5, 5.5])

    def testSplitData(self):
        ct = ClassificationTree()
        D = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [1, 2, 4, 5]], float)
        left, right = ct.splitData(D, 2, False, 3.5)
        self.assertListEqual(left.tolist(),[[1.0,2.0,3.0,4.0]])
        self.assertListEqual(right.tolist(),[[5.0, 6.0, 7.0, 8.0], [1.0, 2.0, 4.0, 5.0]])

        left, right = ct.splitData(D, 0, True, 1)
        self.assertListEqual(left.tolist(),[[1.0,2.0,3.0,4.0], [1.0, 2.0, 4.0, 5.0]])
        self.assertListEqual(right.tolist(),[[5.0, 6.0, 7.0, 8.0]])