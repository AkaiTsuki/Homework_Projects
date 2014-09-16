__author__ = 'jiachiliu'

import numpy as np
from nulearn import tree
import unittest


class TestDecisionTree(unittest.TestCase):
    def test_is_all_same_label(self):
        cf = tree.DecisionTree()
        self.assertTrue(cf.is_all_same_label(np.array([1, 1, 1, 1, 1])))
        self.assertFalse(cf.is_all_same_label(np.array([1, 1, 10, 1, 1])))

    def test_majority_vote(self):
        cf = tree.DecisionTree()
        self.assertEqual(cf.majority_vote(np.array([1, 2, 2, 2, 2, 2, 1, 3, 3])), 2)

    def test_get_sorted_feature_and_target(self):
        cf = tree.DecisionTree()
        features = np.array([1, 2, 3, 2, 1])
        target = np.array([1, 1, 0, 0, 0])
        sorted_features, sorted_targets = cf.get_sorted_feature_and_target(features, target)
        self.assertListEqual(sorted_features.tolist(), [1, 1, 2, 2, 3])
        self.assertListEqual(sorted_targets.tolist(), [1, 0, 1, 0, 0])

    def test_entropy(self):
        cf = tree.DecisionTree()
        en = cf.entropy(np.array([1, 1, 1, 1, 0, 0]))
        expect = -4.0/6 * np.log2(4.0/6) - 2.0/6 * np.log2(2.0/6)
        np.testing.assert_almost_equal(en, expect)

        en = cf.entropy(np.array([1, 1, 1, 1]))
        expect = 0
        np.testing.assert_almost_equal(en, expect)

        en = cf.entropy(np.array([]))
        expect = 0
        np.testing.assert_almost_equal(en, expect)



