from math import log
from InvertListParser import InvertListParser

class BM25(object):
	"""docstring for BM25"""
	K1 = 1.2
	K2 = 100
	B = 0.75
	def __init__(self, resources,db):
		super(BM25, self).__init__()
		self.resources = resources
		self.query = None
		self.db = db
		self.docLenDict = {}
		self.docTermDict = {}
		self.termDf = {}
		self.termidf ={}

	def setQuery(self,query):
		self.query = query
		self.docLenDict = {}
		self.docTermDict = {}
		self.termDf = {}
		self.termidf ={}

	def rank(self):
		self.setupRankData()
		#self.check('system')
		avgdoclen = self.resources.db_ave_doclen
		ranks = {}
		count = 1
		for k,v in self.docTermDict.iteritems():
			#print "process %s" % (count)
			self.K = self.caculateK(self.docLenDict[k],avgdoclen)
			ranks[k] = self.caculateDocScore(v,self.docLenDict[k])
			count +=1
		return ranks

	def caculateDocScore(self,terms,doclen):
		total = 0.0
		
		for k,v in terms.iteritems():
			idf = self.caculateTermIDF(k)
			x = self.caculateTermScore(v,idf,k)
			total += x

		return total

	def caculateTermIDF(self,term):
		if self.termidf.get(term) != None:
			return self.termidf[term]
		else:
			df = self.termDf[term]
			x = 1.0 / ((df + 0.5) / (self.resources.db_num_docs - df +0.5))
			self.termidf[term] = log(x,2)
			return self.termidf[term]

	def caculateTermScore(self,tf,idf,term):
		
		x1 = (BM25.K1 + 1.0)*tf / (self.K +tf)
		termFreq = self.query.getTermFrequency(term)
		x2 = ((BM25.K2 + 1.0) * termFreq) / (BM25.K2 + termFreq)
		return idf * x1 * x2

	def caculateK(self,doclen,avgdoclen):
		x = BM25.K1 * ((1-BM25.B) + BM25.B * (doclen / avgdoclen))
		return x

	def culateAvgDocLen(self):
		total = 0
		for k,v in self.docLenDict.iteritems():
			total += v
		return v*1.0 / len(self.docLenDict)

	def setupRankData(self):
		parser = InvertListParser()

		for term in self.query.terms:
			index = parser.getInvertIndexList(term,self.db,'p')
			self.termDf[term] = index.df
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
		