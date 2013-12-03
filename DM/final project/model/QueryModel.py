from math import log
import math
from RichReview import RichReview
from common.Resource import *
from common.TextFilter import TextFilter
import operator

class InvertList(object):
	"""docstring for InvertList"""
	def __init__(self,word):
		super(InvertList, self).__init__()
		self.word = word
		self.ctf = 0
		self.df = 0
		self.avgLen = 0
		self.indexList = []

	def addRecord(self,record):
		self.indexList.append(record)

	def getAvgLen(self):
		total = 0
		for data in self.indexList:
			total += data[1]
		return total / len(self.indexList)

	def isEmpty(self):
		return len(self.indexList)==0

	def __str__(self):
		return "%s %s %s" % (self.ctf,self.df,self.indexList)

class OKTFIDF(object):
	"""docstring for OKTFIDF"""
	def __init__(self, indexes,avg_query_len,db_num_docs):
		super(OKTFIDF, self).__init__()
		self.indexes = indexes
		self.query = None
		self.avg_query_len = avg_query_len
		self.db_num_docs = db_num_docs

	def setQuery(self,query):
		self.query = query

	def idf(self,df):
		x = self.db_num_docs / df
		return log(x,2)

	def rank(self):
		queryAvgLen = self.avg_query_len
		ranks = {}
		for term in self.query:
			#qdf = self.resources.getTermDF(term)
			termOKTF = self.caculateTermOKTF(term,self.query,queryAvgLen)
			self.rankTermOnDoc(term,termOKTF,ranks)

		return ranks

	def rankTermOnDoc(self,term,termOKTF,ranks):		
		if self.indexes.has_key(term):
			index = self.indexes[term]
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
		tf = self.getTermFrequency(term,query)
		return tf/(tf+0.5+((1.5 * len(query))/queryAvgLen))

	def getTermFrequency(self,term,query):
		count =0
		for t in query:
			if t==term:
				count+=1
		return count


class Query(object):
	"""docstring for Query"""
	def __init__(self, tests,stopFile,stemFile,doclist):
		super(Query, self).__init__()
		self.stop = StopList(stopFile)
		self.stem = Stemming(stemFile)
		self.docRates = {}
		self.__loadDocRates__(doclist)

		self.tests = tests
		self.queries = {}
		self.avg_query_len = 0

		self.num_doc = 0
		self.num_unique_term = 0
		self.num_term =0
		self.avg_doc_len=0
		self.indexes = {}

	def __loadDocRates__(self,path):
		with open(path) as f:
			for line in f:
				data = line.split()
				docid = int(data[0])
				rate = float(data[1])
				self.docRates[docid] = rate

	def predictAll(self,K):
		oktfidf = OKTFIDF(self.indexes,self.avg_query_len,self.num_doc)
		e = 0.0
		count = 1
		for k,v in self.queries.iteritems():
			oktfidf.setQuery(v)
			ranks = oktfidf.rank()
			ranks = sorted(ranks.iteritems(),key=operator.itemgetter(1),reverse=True)
			ranks = ranks[:K]
			total = 0.0
			for docid,score in ranks:
				total += self.docRates[int(docid)]
			er = total / K
			r = self.tests[k].getRate()
			e += abs(er - r) ** 2
			print "%d %s %f %f" % (count,k, er, r)
			count+=1

		print "RMSE: ", math.sqrt(e/len(self.tests))

	def initQueries(self):
		total = 0
		for k,v in self.tests.iteritems():
			terms = self.getQueryTerms(v)
			self.queries[k] = terms
			total += len(terms)

		self.avg_query_len = total / len(self.tests)

	def getQueryTerms(self,review):
		txt = review.getText()
		filter = TextFilter(self.stop,self.stem)
		txt = filter.removePunctuation(txt)
		txt = filter.removeStop(txt)
		txt = filter.convertStem(txt)
		return txt

	def loadIndexes(self,path):
		with open(path) as f:
			count = 0
			for line in f:
				print count
				data = line.split()
				term = data[0]
				il = InvertList(term)
				il.ctf = int(data[1])
				il.df = int(data[2])
				detail = data[3:]

				for i in range(len(detail)):
					if i%3 == 0:
						il.addRecord([detail[i],int(detail[i+1]),int(detail[i+2])])
				self.indexes[term] = il
				count+=1

	def loadDB(self,path):
		with open(path) as f:
			for line in f:
				data = line.split()
				self.num_doc = int(data[0])
				self.num_term = int(data[1])
				self.num_unique_term = int(data[2])
				self.avg_doc_len = int(data[3])
				break

	def dbinfo(self):
		info = "STOP STEM "
		info += "NUM_DOCS = %d " % self.num_doc
		info += "NUM_TERMS = %d " % self.num_term
		info += "NUM_UNIQUE_TERMS = %d " % self.num_unique_term
		info += "AVG_DOC_LEN = %d" % self.avg_doc_len

		return info
