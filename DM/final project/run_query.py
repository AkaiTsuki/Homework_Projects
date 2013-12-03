from model.QueryModel import *

from util.RichReviewTxtParser import RichReviewTxtParser
import sys

def main():
	testFile = sys.argv[1]
	K = int(sys.argv[2])

	parser = RichReviewTxtParser()
	reviews = parser.getReviews(testFile)
	query = Query(reviews,"common/stoplist.txt","common/k_loose.stemclass","doclist.txt")
	query.loadDB("db.txt")
	print query.dbinfo()
	query.loadIndexes("index.txt")
	query.initQueries()

	print query.avg_query_len
	query.predictAll(K)



if __name__ == '__main__':
	main()