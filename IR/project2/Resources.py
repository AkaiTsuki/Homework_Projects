from QueryParser import QueryParser

class Resources(object):
	"""Saving all resources for the project"""
	def __init__(self):
		super(Resources, self).__init__()
		# saving the relationship between external id and internal id
		self.doclist = {}
		# list of stop words
		self.stoplist = []
		# list of stem words. The key is original word, the value is stem word.
		self.stemClasses = {}
		# list of querys
		self.querys =[]

	def loadDocList(self,path):
		with open(path) as f:
			for line in f:
				internal,external = line.split();
				self.doclist[internal.strip()] = external.strip()

	def loadStopList(self,path):
		with open(path) as f:
			for line in f:
				self.stoplist.append(line.strip())

	def loadStemClasses(self,path):
		with open(path) as f:
			for line in f:
				stem, words = line.split('|')
				wordList = words.split()
				for w in wordList:
					self.stemClasses[w.strip()] = stem.strip()

	def loadQuerys(self,path):
		# Parse the query file
		queryParser = QueryParser(path)
		raw = queryParser.load()
		cleanedRaw = queryParser.process(raw, self.stoplist,self.stemClasses)
		# querys is a list of Query
		self.querys = queryParser.generateQueryList(cleanedRaw)

	def caculateQueryAvgLength(self):
		total = 0

		for q in self.querys:
			total += q.length()
		
		return total/len(self.querys)




	