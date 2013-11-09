class Query(object):
	"""docstring for Query"""
	INVALID_TERM = ['document','detat','u.s.']
	INVALID_TERM1 = ['document','discuss','report','include','identify','cite','describe']

	def __init__(self, id):
		super(Query, self).__init__()
		self.id = id;
		self.terms = []

	def addTerm(self,term):
		if not self.filter(term):
			self.terms.append(term)

	def filter(self,term):
		return term in Query.INVALID_TERM1

	def length(self):
		return len(self.terms)

	def getTermFrequency(self,term):
		count=0
		for t in self.terms:
			if t==term:
				count +=1
		return count

	def __str__(self):
		return "[%s %s]" % (self.id,self.terms)