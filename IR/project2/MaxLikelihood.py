from math import log
from InvertListParser import InvertListParser

class MaxLikelihood(object):
	"""docstring for MaxLikelihood"""
	def __init__(self,resources,db):
		super(MaxLikelihood, self).__init__()
		self.resources = resources
		self.query = None
		self.db = db
		self.docLenDict = {}
		self.docTermDict = {}

	def setQuery(self,query):
		self.query = query
		self.docLenDict = {}
		self.docTermDict = {}

	def check(self,term):
		total = 0
		for docid,terms in self.docTermDict.iteritems():
			total +=terms[term]
			print "%s %s" % (docid,terms[term])
		print total
		

	def rank(self):
		self.setupRankData()
		#self.check('system')

		ranks = {}
		for k,v in self.docTermDict.iteritems():
			ranks[k] = self.caculateDocLikelihood(v,self.docLenDict[k])
		return ranks

	def caculateDocLikelihood(self,terms,doclen):
		total = 0.0

		for k,v in terms.iteritems():
			x = self.caculateTermLikelihood(v, doclen)
			total += log(x,2)

		return total

	def caculateTermLikelihood(self,tf,doclen):
		return (tf+1.0) / (doclen+self.resources.db_num_unique_terms)

	def setupRankData(self):
		parser = InvertListParser()

		for term in self.query.terms:
			index = parser.getInvertIndexList(term,self.db,'p')
			for item in index.indexList:
				docid = item[0]
				doclen = item[1]
				tf = item[2]
				self.addTerm(docid,term,tf)
				self.addDocLen(docid,doclen)
		
		for k,v in self.docTermDict.iteritems():
			for terms in self.query.terms:
				if v.get(terms) == None:
					v[terms] = 0
					self.docTermDict[k] = v


	def addTerm(self,docid,term,tf):
		terms = self.docTermDict.get(docid)
		if terms == None:
			terms = {}
		terms[term]=terms.get(term,tf)
		self.docTermDict[docid] = terms

	def addDocLen(self,docid,doclen):
		self.docLenDict[docid] = doclen

			