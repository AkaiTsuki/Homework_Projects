from model.CollaborationFilter import CollaborationFilter
from util.ReviewTxtParser import ReviewTxtParser
import sys

if __name__ == '__main__':
	"""
	This script is for CollaborationFilter model
	"""
	K = int(sys.argv[1])

	parser = ReviewTxtParser()
	reviews = parser.getReviews("dataset/reviews.txt")
	tests = parser.getReviews("dataset/test10p.txt")

	print 'total %d tests to run.' % (len(tests))

	cf = CollaborationFilter(reviews,tests)
	cf.run(K)
