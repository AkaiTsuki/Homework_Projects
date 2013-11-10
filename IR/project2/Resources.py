from QueryParser import QueryParser

class Resources(object):
	"""Saving all resources for the project"""
	def __init__(self,db):
		super(Resources, self).__init__()
		self.db = db
		# saving the relationship between external id and internal id
		self.doclist = {}
		# list of stop words
		self.stoplist = []
		# list of stem words. The key is original word, the value is stem word.
		self.stemClasses = {}
		# list of querys
		self.querys =[]

		# db information
		self.db_num_docs = 0
		self.db_num_terms = 0
		self.db_num_unique_terms = 0
		self.db_ave_doclen = 0

		self.dbinfo()

	def dbinfo(self):
		if self.db==3:
			self.db_num_docs = 84678
			self.db_num_terms = 24401877
			self.db_num_unique_terms = 166054
			self.db_ave_doclen = 288

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

	def getTermDF(self,term):
		df = 0;
		for q in self.querys:
			if term in q.terms:
				df += 1
		return df





	