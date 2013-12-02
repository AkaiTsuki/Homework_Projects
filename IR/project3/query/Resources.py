from QueryParser import QueryParser
from common.Resource import *

class Resources(object):
	"""Saving all resources for the project"""
	def __init__(self,db):
		super(Resources, self).__init__()
		self.db = db
		# saving the relationship between external id and internal id
		self.doclist = {}
		# list of stop words
		self.stoplist = []
		# list of stem words. The key is original word, the value is stem word.
		self.stemClasses = {}
		# list of querys
		self.querys =[]

		# db information
		self.db_num_docs = 0
		self.db_num_terms = 0
		self.db_num_unique_terms = 0
		self.db_ave_doclen = 0

		self.dbinfo()

	def dbinfo(self):
		if self.db==3:
			self.db_num_docs = 84678
			self.db_num_terms = 24401877
			self.db_num_unique_terms = 166054
			self.db_ave_doclen = 288
		elif self.db ==2:
			self.db_num_docs = 84678
			self.db_num_terms = 24401877
			self.db_num_unique_terms = 207224
			self.db_ave_doclen = 288
		elif self.db==1:
			self.db_num_docs = 84678
			self.db_num_terms = 41802513
			self.db_num_unique_terms = 166242
			self.db_ave_doclen = 493
		elif self.db==0:
			self.db_num_docs = 84678
			self.db_num_terms = 41802513
			self.db_num_unique_terms = 207615
			self.db_ave_doclen = 493
		elif self.db==4:
			self.db_num_docs = 3204
			self.db_num_terms = 164420
			self.db_num_unique_terms = 12112
			self.db_ave_doclen = 51

	def loadDocList(self,path):
		with open(path) as f:
			for line in f:
				internal,external = line.split();
				self.doclist[internal.strip()] = external.strip()

	def loadStopList(self,path):
		self.stoplist = StopList(path)

	def loadStemClasses(self,path):
		self.stemClasses = Stemming(path)

	def loadQuerys(self,path):
		# Parse the query file
		queryParser = QueryParser(path,self.db)
		self.querys = queryParser.load(self.stoplist,self.stemClasses)
		
		#cleanedRaw = queryParser.process(raw, self.stoplist,self.stemClasses)
		# querys is a list of Query
		#self.querys = queryParser.generateQueryList(cleanedRaw)

	def caculateQueryAvgLength(self):
		total = 0

		for q in self.querys:
			total += q.length()
		
		return total/len(self.querys)

	def getTermDF(self,term):
		df = 0;
		for q in self.querys:
			if term in q.terms:
				df += 1
		return df





	