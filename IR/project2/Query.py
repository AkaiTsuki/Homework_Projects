class Query(object):
	"""docstring for Query"""
	INVALID_TERM = ['document','detat','u.s.']
	INVALID_TERM1 = ['document','discuss','report','include','identify','cite','describe']

	def __init__(self, id):
		super(Query, self).__init__()
		self.id = id;
		self.terms = []
		self.oktf = {}

	def addTerm(self,term):
		if not self.filter(term):
			self.terms.append(term)

	def filter(self,term):
		return term in Query.INVALID_TERM1

	def caculateOKTF(self,avgLen):
		for term in self.terms:
			oktf = self.caculateTermOKTF(term,avgLen)
			self.oktf[term] = oktf

	def caculateTermOKTF(self,term,avgLen):
		tf = self.getTermFrequency(term)
		return tf/(tf+0.5+((1.5 * self.getDocLen())/avgLen))

	def getDocLen(self):
		return len(self.terms)

	def getTermFrequency(self,term):
		count=0
		for t in self.terms:
			if t==term:
				count +=1
		return count

	def __str__(self):
		return "[%s %s] \n %s" % (self.id,self.terms,self.oktf)