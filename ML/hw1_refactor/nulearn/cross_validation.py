__author__ = 'jiachiliu'

import numpy as np


def train_test_split(data, target, test_size):
    size = len(data) / 10
    indices = np.random.permutation(data.shape[0])
    training_idx, test_idx = indices[size + 1:], indices[:size + 1]
    return data[training_idx, :], data[test_idx, :], target[training_idx, :], target[test_idx, :]
