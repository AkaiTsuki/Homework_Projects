from math import log
from InvertListParser import InvertListParser

class JelinekMercer(object):
	"""docstring for JelinekMercer"""
	SMOOTH = 0.2

	def __init__(self, resources,db):
		super(JelinekMercer, self).__init__()
		self.resources = resources
		self.query = None
		self.db = db
		self.docLenDict = {}
		self.docTermDict = {}
		self.termCtf = {}

	def setQuery(self,query):
		self.query = query
		self.docLenDict = {}
		self.docTermDict = {}
		self.termCtf = {}

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
			ctf = self.termCtf[k]
			if ctf==0:
				continue
			x = self.caculateTermLikelihood(v, doclen,ctf)
			total += log(x,2)

		return total


	def caculateTermLikelihood(self,tf,doclen,cf):
		P = (tf*1.0) / doclen 
		Q = (cf*1.0) / self.resources.db_num_terms

		return (JelinekMercer.SMOOTH * P) + ((1-JelinekMercer.SMOOTH) * Q)

	def setupRankData(self):
		parser = InvertListParser()

		for term in self.query.terms:
			index = parser.getInvertIndexList(term,self.db,'p')
			self.termCtf[term] = index.ctf
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