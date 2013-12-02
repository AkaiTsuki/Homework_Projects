from os import listdir
from os.path import isfile, join, splitext
from FileReader import FileReader
from common.Resource import *
from common.TextFilter import TextFilter
from Document import Document

class Indexer(object):
	"""docstring for Indexer"""
	def __init__(self, stopPath,stemPath,docDir):
		super(Indexer, self).__init__()
		self.stopList = StopList(stopPath)
		self.stemClass = Stemming(stemPath)
		self.textFilter = TextFilter(self.stopList,self.stemClass)
		self.docDir = docDir
		self.docList = self.__getAllDocFiles__()
		self.docTotalNum = len(self.docList)

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
			docLen = doc.getDocLen()
			# get term,tf mapping in this doc
			terms = doc.getTermDict()
			# for each term
			for t,tf in terms.iteritems():
				if not indexList.has_key(t):
					indexList[t] = []	
				indexList[t].append([docId,docLen,tf])

		return indexList

	def getDocTotalNum(self):
		return self.docTotalNum


	def getDocuments(self):
		docList = self.getDocList()
		count = 1
		docs = []
		for docFile in docList:
			docs.append(self.getDocument(docFile,count))
			count+=1
		return docs

	def getDocument(self,docName,docid):
		docPath  = self.__getDocPath__(docName)
		docNameNoExt = splitext(docName)[0]
		reader = FileReader(docPath)
		content = reader.read()
		terms = self.textFilter.filter(content)
		return Document(docid,docNameNoExt,terms)

	def getDocList(self):
		return self.docList

	def __getDocPath__(self,docName):
		return self.docDir+"/"+docName

	def __getAllDocFiles__(self):
		return [f for f in listdir(self.docDir) if isfile(join(self.docDir,f))]