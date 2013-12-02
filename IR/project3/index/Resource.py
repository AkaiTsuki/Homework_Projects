class StopList(object):
	"""Saving the stop word information and provide
	query method on stop words
	"""
	def __init__(self, path):
		super(StopList, self).__init__()
		self.stop = self.loadStopList(path)
	
	def loadStopList(self,path):
		stopList = {}
		with open(path) as f:
			for line in f:
				stop = line.strip()
				stopList[stop] = 1
		return stopList

	def getStopList(self):
		return self.stop

	def isStop(self,term):
		stopList = self.getStopList()
		return stopList.has_key(term)

	def __str__(self):
		string = []
		for stop in self.getStopList():
			string.append(stop+'\n')
		return ''.join(string)

class Stemming(object):
	"""docstring for Stemming"""
	def __init__(self, path):
		super(Stemming, self).__init__()
		self.stemming = self.loadStemming(path)

	def loadStemming(self,path):
		dic ={}
		with open(path) as f:
			for line in f:
				terms = line.strip().split()
				root = terms[0]
				for term in terms[1:]:
					dic[term] = root
		return dic

	def getStemming(self):
		return self.stemming

	def convert(self,word):
		stemming = self.getStemming()
		if stemming.has_key(word):
			return stemming[word]
		else:
			return word

	def __str__(self):
		string = []
		for k,v in self.getStemming().iteritems():
			string.append(k+' '+v+'\n')
		return ''.join(string)
