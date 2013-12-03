class Document(object):
	"""docstring for Document"""
	def __init__(self, docid,docname,terms):
		super(Document, self).__init__()
		self.docid = docid
		self.docname = docname
		self.terms = terms
		self.doclen = len(self.terms)
		# a termDict is a dict where key=term,value = tf,
		# tf is number of ocurrence of this term in this
		# doc
		self.termDict = self.__createTermDict__()

	def __createTermDict__(self):
		termDict = {}

		for term in self.getTerms():
			if termDict.has_key(term):
				termDict[term] += 1
			else:
				termDict[term] = 1
		return termDict

	def getDocLen(self):
		return self.doclen

	def getDocId(self):
		return self.docid

	def getDocName(self):
		return self.docname
	
	def getTerms(self):
		return self.terms

	def getTermDict(self):
		return self.termDict

	def __str__(self):
		string = ""
		string += "docid: %d\n" % self.getDocId()
		string += "docname: "+self.getDocName()+"\n"
		string += "doclen: %d\n" % self.getDocLen()
		string += "termDict: %s\n" % self.getTermDict()
		string += "termDict length: %d\n" % len(self.getTermDict())
		return string
