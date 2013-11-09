from InvertListParser import InvertListParser

class SpaceVectorModel(object):
	"""docstring for SpaceVectorModel"""
	def __init__(self, querys):
		super(SpaceVectorModel, self).__init__()
		self.querys = querys
		self.caculateQueryOKTFs()

	def caculateQueryOKTFs(self):
		avgLen = self.getQueryAvgLen()

		for query in self.querys:
			query.caculateOKTF(avgLen)

	def getQueryAvgLen(self):
		totalLen = 0
		for query in self.querys:
			totalLen += query.getDocLen()
		avgLen = totalLen / len(self.querys)
		return avgLen

	def getRankedDocuments(self,query):
		ranks ={}
		parser = InvertListParser()

		for term in query.terms:
			invertList = parser.getInvertIndexList(term,3,'p')
			if not invertList.isEmpty():
				self.caculateRankOnTerm(term,query.oktf[term],invertList,ranks)
				
		return ranks

	def caculateRankOnTerm(self,term,termOKTF,invertList,ranks):
		docavglen = invertList.getAvgLen()
		for item in invertList.indexList:
			docid = item[0]
			doclen = item[1]
			tf = item[2]

			docOKTF = self.caculateDocOKTF(docavglen, tf, doclen)
			score = self.caculateRankScoreModel1(docOKTF,termOKTF)
			ranks[docid] = ranks.get(docid,0) + score

	def caculateRankScoreModel1(self,docOKTF,termOKTF):
		return docOKTF*termOKTF


	def caculateDocOKTF(self,avgLen,tf,docLen):
		return tf/(tf+0.5+((1.5 * docLen) / avgLen))
		





		