import unittest
from common.normalizer import *
import numpy as np

class TestMinMaxScaler(unittest.TestCase):

	def testFindMinAndMaxOnColumn(self):
		data = np.array([[1,2,3],[4,5,6],[7,8,9]])
		scaler = MinMaxScaler([0])
		(minVal, maxVal) = scaler.findMinAndMaxOnColumn(data,0)
		self.assertTupleEqual((minVal, maxVal),(1,7))

		data = np.array([[10,2,3],[42,5,6],[7,8,9]])
		scaler = MinMaxScaler([0])
		(minVal, maxVal) = scaler.findMinAndMaxOnColumn(data,0)
		self.assertTupleEqual((minVal, maxVal),(7,42))

	def testFindMinAndMaxForColumns(self):
		data = np.array([[10,2,3],[42,5,6],[7,8,9]])
		scaler = MinMaxScaler([0,1,2])
		scaler.findMinAndMaxForColumns(data)
		self.assertTupleEqual(scaler.minMaxArr[0],(7,42))
		self.assertTupleEqual(scaler.minMaxArr[1],(2,8))
		self.assertTupleEqual(scaler.minMaxArr[2],(3,9))

	def testScaleOnColumn(self):
		data = np.array([[10,2,3],[42,5,6],[7,8,9]],float)
		scaler = MinMaxScaler([0,1,2])
		scaler.scaleOnColumn(data, 0, 7.0, 42.0)
		self.assertListEqual(data.tolist(), [[(10-7)/(42.0-7.0),2,3],[1.0,5,6],[0,8,9]])

	def testScale(self):
		data = np.array([[1.0,2.0,3.0],[4.0,5.0,6.0],[7.0,8.0,9.0]],float)
		scaler = MinMaxScaler([0,1,2])
		scaler.scale(data)
		expect = [
			[0,0,0],
			[0.5,0.5,0.5],
			[1,1,1]
		]

		self.assertListEqual(data.tolist(),expect)
