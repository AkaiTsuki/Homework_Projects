from FileReader import FileReader
from Resource import *
from TextFilter import TextFilter
from Document import Document
from Indexer import Indexer
from Database import Database
from Lemur import Lemur

def testTextFilter(path):
	stopList = StopList("stoplist.txt")
	stemming = Stemming("k_loose.stemclass")

	reader = FileReader(path)
	content = reader.read()
	textFilter = TextFilter(stopList,stemming)
	words = textFilter.filter(content)
	return words

def testDocument(terms):
	return Document(1,"CACM-TEST-001",terms)

if __name__ == '__main__':

	indexer = Indexer("stoplist.txt","k_loose.stemclass","cacm")
	docs = indexer.getDocuments()
	indexes = indexer.index(docs)
	database  = Database(docs,indexes)

	print len(docs)
	print len(indexes)
	print database.dbinfo()

	#database.writeInvertListToFile("index.txt")
	#database.writeDocListToFile("doclist.txt")

	lemur = Lemur()
	print lemur.query("cacm","index.txt")