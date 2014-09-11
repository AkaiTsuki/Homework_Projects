from common.CsvFileReader import CsvFileReader
import unittest

class TestCsvFileReader(unittest.TestCase):
	def testRead(self):
		reader = CsvFileReader('test/data/csvFileReaderTestData.txt')
		lines = reader.read(' ', float)
		self.assertListEqual(lines.tolist(), [[1,2,3],[42,5,16]])
		lines = reader.read(' ', int)
		self.assertListEqual(lines.tolist(), [[1,2,3],[42,5,16]])