from index.Indexer import Indexer
from index.Database import Database

if __name__ == '__main__':

	hasStop = 0

	indexer = Indexer("stoplist.txt","k_loose.stemclass","cacm",hasStop)
	docs = indexer.getDocuments()
	indexes = indexer.index(docs)
	database  = Database(docs,indexes)

	print len(docs)
	print len(indexes)
	print database.dbinfo()

	database.writeInvertListToFile("index.txt")
	database.writeDocListToFile("doclist.txt")
