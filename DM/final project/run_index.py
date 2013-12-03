
from util.RichReviewTxtParser import RichReviewTxtParser
from model.Indexer import Indexer



if __name__ == '__main__':

	rpath = "training.txt"
	#rpath = "train-small.txt"
	tpath = 'test.txt'
	parser = RichReviewTxtParser()

	reviews = parser.getReviews(rpath)
	indexer = Indexer(reviews,"common/stoplist.txt","common/k_loose.stemclass")
	
	indexer.writeIndexes("index.txt")
	indexer.writeDocRates("doclist.txt")
	indexer.writeDBInfo("db.txt")