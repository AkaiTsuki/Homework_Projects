import unittest
import numpy as np
from model.LinearRegression import LinearRegression

class TestLinearRegression(unittest.TestCase):
	def testConstructY(self):
		data = np.array([[1,2,3],[4,5,6],[7,8,9]],float)
		label = 2
		lr = LinearRegression(data, [0,1], label)
		self.assertListEqual(lr.Y.tolist(),[3,6,9])

	def testConstructX(self):
		data = np.array([[1,2,3],[4,5,6],[7,8,9]],float)
		label = 2
		lr = LinearRegression(data, [0,1], label)
		self.assertListEqual(lr.X.tolist(),[[1,2],[4,5],[7,8]])

	def testBuild(self):
		data = np.array([[1,2,3],[4,5,6],[7,8,9]],float)
		label = 2
		lr = LinearRegression(data,[0,1], label)
		np.testing.assert_almost_equal(lr.build().tolist(),[-1,2])
