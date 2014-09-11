import unittest

class TestUnitTestTutorial(unittest.TestCase):

	def setUp(self):
		pass

	def test_sample(self):
		x = 10*2
		self.assertEqual(x,200)

	def test_sample2(self):
		self.assertEqual(True,False)

	def test_sample3(self):
		arr = [1,2,3]
		self.assertTrue(1 in arr)
		self.assertTrue(10 in arr, '10 is not in array')

if __name__ == '__main__':
	unittest.main()