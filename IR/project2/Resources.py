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




	