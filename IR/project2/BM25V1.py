from InvertListParser import InvertListParser
from math import log

class BM25V1(object):
	"""docstring for BM25V1"""
	K1 = 1.2
	K2 = 100
	B = 0.75

	def __init__(self,resources,db):
		super(BM25V1, self).__init__()
		self.resources = resources
		self.db = db
		self.query = None


	def setQuery(self,query):
		self.query = query

	def rank(self):
		ranks = {}
		for term in self.query.terms:
			self.rankTermOnDoc(term,ranks)
		return ranks

	def rankTermOnDoc(self,term,ranks):
		parser = InvertListParser()
		index = parser.getInvertIndexList(term,self.db,'p')
		termQueryFreq = self.query.getTermFrequency(term)
		if not index.isEmpty():
			term1 = self.caculateLog(index.df)
			for item in index.indexList:
				docid = item[0]
				doclen = item[1]
				tf = item[2]
				K = self.caculateK(doclen)
				
				term2 = ((BM25V1.K1 + 1.0) * tf) / (K + tf)
				term3 = ((BM25V1.K2 +1.0)*termQueryFreq) / (BM25V1.K2 + termQueryFreq)
				score =  term1 * term2 * term3
				ranks[docid] = ranks.get(docid,0) + score

	def caculateK(self,doclen):
		portion = (doclen*1.0) / self.resources.db_ave_doclen
		return BM25V1.K1 * ((1-BM25V1.B) + BM25V1.B * portion)

	def caculateLog(self,df):
		v = (df+0.5) / (self.resources.db_num_docs - df +0.5)
		x = 1.0 / v
		return log(x,2) 


		