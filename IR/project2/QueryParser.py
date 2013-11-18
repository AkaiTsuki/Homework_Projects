from Query import Query

class QueryParser(object):
	"""docstring for Query"""
	signs = [',','.','\'','-']

	def __init__(self, path,db):
		super(QueryParser, self).__init__()
		self.path = path
		self.db = db

	def load(self):
		"""
		load query from file, returns a raw query list for 
		further processing.
		"""
		raw_lst = []
		with open(self.path) as f:
			for line in f:
				l = line.strip()
				if len(l)>0:
					raw_lst.append(l)
		return raw_lst

	def removeSpecialCharacters(self,raw_lst):
		processed_lst = []
		for line in raw_lst:
			l=line.translate(None,"(),\'\"")
			l = l.replace('-',' ').lower()
			processed_lst.append(l[:-1])
		return processed_lst

	def getWords(self,lst):
		words = []
		for line in lst:
			l = line.split()
			l[0] = l[0].replace('.','')
			words.append(l)
		return words

	def removeStopWordInQuery(self,query,stopList):
		words = []
		for word in query:
			if word not in stopList:
				words.append(word)
		return words

	def removeStops(self,lst,stopList):
		result = []
		for query in lst:
			result.append(self.removeStopWordInQuery(query, stopList))
		return result

	def processStem(self,lst,stemList):
		result = []
		for query in lst:
			result.append(self.processQueryStem(query, stemList))
		return result

	def processQueryStem(self,query,stemList):
		words=[]
		for w in query:
			stem = stemList.get(w)
			if stem is None:
				words.append(w)
			else:
				words.append(stem)
		return words

	def generateQueryList(self,querys):
		lst = []
		for query in querys:
			lst.append(self.getQuery(query))
		return lst

	def getQuery(self,lst):
		q = Query(lst[0])
		for i in range(1,len(lst)):
			q.addTerm(lst[i])
		return q

	def process(self,raw_lst,stoplist,stemList):
		lst = self.removeSpecialCharacters(raw_lst)
		lst = self.getWords(lst)
		#if self.db == 2 or self.db == 3:
		lst = self.removeStops(lst,stoplist)
		#if self.db == 1 or self.db == 3:
		lst = self.processStem(lst, stemList)
		return lst