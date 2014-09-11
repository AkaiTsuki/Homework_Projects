import numpy as np

class CsvFileReader:
	'''
	CsvFileReader will read data from csv file
	'''
	def __init__(self, path):
		self.path = path

	def read(self, delimiter, converter):
		f = open(self.path)
		lines = f.readlines()
		return self.parseLines(lines,delimiter, converter)

	def parseLines(self, lines, delimiter, converter):
		data = []
		for line in lines:
			if line.strip():
				row = [s.strip() for s in line.strip().split(delimiter) if s.strip()];
				data.append(row)
		return np.array(data, converter)