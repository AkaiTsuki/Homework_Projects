import urllib
from InvertList import InvertList
from Lemur import Lemur

class InvertListParser(object):
	"""docstring for RetrieveModel"""
	QUERY_URL = "http://fiji4.ccs.neu.edu/~zerg/lemurcgi/lemur.cgi?"

	def __init__(self):
		super(InvertListParser, self).__init__()

	def getUrl(self,word,db,mode):
		url = InvertListParser.QUERY_URL+"g="+mode+"&d="+str(db)+"&v="+word
		return url

	def getInvertIndexListArray(self,word,db,mode):
		lemur = Lemur()
		txt = lemur.query(word,'index.txt')
		return txt.split()

	def getInvertIndexList(self,word,db,mode):
		invertList = InvertList(word)

		invertListArray=self.getInvertIndexListArray(word, db, mode)
		if len(invertListArray)==0:
			return invertList
			
		summary = invertListArray[:2];
		detail = invertListArray[2:]

		invertList.ctf = int(summary[0])
		invertList.df = int(summary[1])

		for i in range(len(detail)):
			if i%3 == 0:
				invertList.addRecord([detail[i],int(detail[i+1]),int(detail[i+2])])
		return invertList
