from common.TextFilter import TextFilter
from common.Resource import *
from RichReview import RichReview
from Document import Document

class Indexer(object):
	"""docstring for Indexer"""
	def __init__(self, reviews, stopFile,stemFile):
		super(Indexer, self).__init__()
		self.stop = StopList(stopFile)
		self.stem = Stemming(stemFile)
		self.docRates = {}
		self.docs = self.__getDocs__(reviews)
		self.indexes = self.index(self.docs)
		self.num_doc = len(self.docs)
		self.num_unique_term = len(self.indexes)
		self.num_term =0
		self.avg_doc_len=0
		self.__statistic__()

	def __statistic__(self):
		self.num_term = 0
		for d in self.docs:
			self.num_term += d.getDocLen()

		self.avg_doc_len = self.num_term / self.num_doc
	
	def index(self,docs):
		"""
		For each term, its invert list should be a list of InvertListItems which is 
		[docid,doclen,tf]

		plus ctf which is the total tf in invert list and df which is the 
		number of docs in invert list.
		"""

		# invertList is a dict where key is term, and value is a list of InvertListItems
		indexList = {}
		# for each document in documents
		for doc in docs:
			docId = doc.getDocId()
			print docId
			docLen = doc.getDocLen()
			# get term,tf mapping in this doc
			terms = doc.getTermDict()
			# for each term
			for t,tf in terms.iteritems():
				if not indexList.has_key(t):
					indexList[t] = []	
				indexList[t].append([docId,docLen,tf])

		return indexList

	def writeIndexes(self,path):
		with open(path,'w') as f:
			indexes = self.getIndexes()
			for term in indexes:
				out = self.getTermInvertListPlainText(term,indexes[term])
				f.write(out+"\n")

	def writeDocRates(self,path):
		with open(path,'w') as f:
			for k,v in self.docRates.iteritems():
				output = "%d %f\n" % (k,v)
				f.write(output)

	def writeDBInfo(self,path):
		with open(path,'w') as f:
			output = "%d %d %d %d\n" %(self.num_doc,self.num_term,self.num_unique_term,self.avg_doc_len)
			f.write(output)

	def getTermInvertListPlainText(self,term,termIndexes):
		ctf = 0
		df = len(termIndexes)
		output = ""
		for item in termIndexes:
			output += " %d %d %d" %(item[0],item[1],item[2])
			ctf += item[2]
		summary = "%s %d %d" % (term,ctf,df)
		return summary+output

	def getIndexes(self):
		return self.indexes

	def getDocs(self):
		return self.docs

	def __getDocs__(self,reviews):
		docs = []
		filter = TextFilter(self.stop,self.stem)
		docid = 0
		for k,v in reviews.iteritems():
			print docid
			txt = v.getText()
			rate = v.getRate()
			docName = v.getKey()
			txt = filter.removePunctuation(txt)
			txt = filter.removeStop(txt)
			txt = filter.convertStem(txt)
			self.docRates[docid] = rate
			doc = Document(docid,docName,txt)
			docs.append(doc)
			docid+=1
		return docs




