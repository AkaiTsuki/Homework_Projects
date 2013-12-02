import os

class Database(object):
	"""docstring for Database"""
	def __init__(self, docs, indexes):
		super(Database, self).__init__()
		self.docs = docs
		self.indexes = indexes
		self.num_doc = len(self.docs)
		self.num_term = 0
		self.num_unique_term = len(self.indexes)
		self.avg_doc_len = 0
		self.__statistic__()

	def __statistic__(self):
		self.num_term = 0
		for d in self.docs:
			self.num_term += d.getDocLen()

		self.avg_doc_len = self.num_term / self.num_doc

	def dbinfo(self):
		info = "STOP STEM "
		info += "NUM_DOCS = %d " % self.getNumDocs()
		info += "NUM_TERMS = %d " % self.getNumTerms()
		info += "NUM_UNIQUE_TERMS = %d " % self.getNumUniqueTerm()
		info += "AVG_DOC_LEN = %d" % self.getAvgDocLen()

		return info

	def writeDocListToFile(self,path):
		with open(path,'w') as f:
			for doc in self.getDocuments():
				docid = doc.getDocId()		
				docName = os.path.splitext(doc.getDocName())[0]
				out = "%s \t %s\n" % (docid,docName)
				f.write(out)


	def writeInvertListToFile(self,path):
		with open(path,'w') as f:
			indexes = self.getIndexes()
			for term in indexes:
				out = self.getTermInvertListPlainText(term)
				f.write(out+"\n")

	def getTermInvertListPlainText(self,term):
		indexes = self.getIndexes()
		ctf = 0
		df = 0

		if not indexes.has_key(term):
			return self.__formatOutput__(ctf,df,None,term)
		else:
			indexes = indexes[term]
			df = len(indexes)
			# calculate ctf
			for item in indexes:
				tf = item[2]
				ctf += tf

			return self.__formatOutput__(ctf,df,indexes,term)

	def __formatOutput__(self,ctf,df,indexes,term):
		if indexes==None:
			return ""
		else:
			output = "%s %d %d" % (term,ctf,df)
			for item in indexes:
				output += " %d %d %d" %(item[0],item[1],item[2])
			return output

	def getDocuments(self):
		return self.docs

	def getIndexes(self):
		return self.indexes

	def getNumDocs(self):
		return self.num_doc

	def getNumTerms(self):
		return self.num_term

	def getNumUniqueTerm(self):
		return self.num_unique_term

	def getAvgDocLen(self):
		return self.avg_doc_len
		