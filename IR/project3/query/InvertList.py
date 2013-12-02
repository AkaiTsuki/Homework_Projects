class InvertList(object):
	"""docstring for InvertList"""
	def __init__(self,word):
		super(InvertList, self).__init__()
		self.word = word
		self.ctf = 0
		self.df = 0
		self.avgLen = 0
		self.indexList = []

	def addRecord(self,record):
		self.indexList.append(record)

	def getAvgLen(self):
		total = 0
		for data in self.indexList:
			total += data[1]
		return total / len(self.indexList)

	def isEmpty(self):
		return len(self.indexList)==0

	def __str__(self):
		return "%s %s %s" % (self.ctf,self.df,self.indexList)