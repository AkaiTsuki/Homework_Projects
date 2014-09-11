import unittest
from model.Cart import Cart
import numpy as np

class TestCart(unittest.TestCase):
	def testSortData(self):
		data = np.array([[4,5,6],[1,2,3],[7,8,9]]);
		cart = Cart(data,[0,1],2,1)
		act = cart.sortData(data,2)
		self.assertListEqual(act.tolist(),[[1,2,3],[4,5,6],[7,8,9]])

	def testInitCart(self):
		data = np.array([[4,5,6],[1,2,3],[7,8,9]]);
		cart = Cart(data,[0,1],2,1)
		self.assertListEqual(cart.data.tolist(),[[1,2,3],[4,5,6],[7,8,9]])
		self.assertListEqual(cart.features,[0,1])
		self.assertEqual(cart.label,2)

	def testFindAllSplitPoint(self):
		data = np.array([[4,5,6],[1,2,3],[7,8,9]],float);
		cart = Cart(data,[0,1],2,1)
		splits = cart.findAllSplitPoint([3,6,9])
		self.assertListEqual(splits,[4.5,7.5])

	def testGetMse(self):
		data = np.array([[4,5,6],[1,2,3],[7,8,9]],float);
		cart = Cart(data,[0,1],2,1)
		self.assertEquals(cart.getMse(np.array([1,2,3,4],float)), 5)
		self.assertEquals(cart.getMse(np.array([],float)),0)

	def testTryAllSplits(self):
		data = np.array([[1,2,3],[4,5,6],[7,8,9]],float);
		cart = Cart(data,[0,1],2,1)
		index, val, mse = cart.tryAllSplits([1,2,4],np.array([1,2,4],float))
		self.assertEqual(index, 2)
		self.assertEqual(val,3)
		self.assertEqual(mse,0.5)