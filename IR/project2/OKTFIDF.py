from math import log
from InvertListParser import InvertListParser

class OKTFIDF(object):
	"""docstring for OKTFIDF"""
	def __init__(self, resources,query,db):
		super(OKTFIDF, self).__init__()
		self.resources=resources
		self.query = query
		self.db = db

	def setQuery(self,query):
		self.query = query

	def idf(self,df):
		x = self.resources.db_num_docs / df
		return log(x,2)

	def queryIDF(self,df):
		x = 25.0 / df
		return log(x,2)

	def rank(self):
		queryAvgLen = self.resources.caculateQueryAvgLength()
		ranks = {}
		for term in self.query.terms:
			#qdf = self.resources.getTermDF(term)
			termOKTF = self.caculateTermOKTF(term,self.query,queryAvgLen)
			self.rankTermOnDoc(term,termOKTF,ranks)

		return ranks

	def rankTermOnDoc(self,term,termOKTF,ranks):
		parser = InvertListParser()
		index = parser.getInvertIndexList(term,self.db,'p')

		if not index.isEmpty():
			avgLen = index.getAvgLen()
			for item in index.indexList:
				docid = item[0]
				doclen = item[1]
				tf = item[2]
				score = termOKTF * self.caculateDocOKTF(avgLen,tf,doclen) * self.idf(index.df)
				ranks[docid] = ranks.get(docid,0) + score
		
	def caculateDocOKTF(self,avgLen,tf,docLen):
		return tf/(tf+0.5+((1.5 * docLen) / avgLen))

	def caculateTermOKTF(self,term,query,queryAvgLen):
		tf = query.getTermFrequency(term)
		return tf/(tf+0.5+((1.5 * query.length())/queryAvgLen))

		