import unittest
import numpy as np

class TestNumpyFeature(unittest.TestCase):
	def testFilter(self):
		arr = np.array([[1,2,3],[4,5,6],[7,8,9]])
		b = (arr % 2 == 0)
		even = arr[b]
		print even

if __name__ == '__main__':
	unittest.main()
