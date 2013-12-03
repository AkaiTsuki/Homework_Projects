from model.MatrixFactorization import MatrixFactorization
from util.ReviewTxtParser import ReviewTxtParser
import sys

if __name__ == '__main__':
	"""
	This script is for MatrixFactorization model
	"""
	K = int(sys.argv[1])
	Iter = int(sys.argv[2])

	parser = ReviewTxtParser()
	reviews = parser.getReviews("dataset/reviews.txt")
	tests = parser.getReviews("dataset/test10p.txt")

	print 'total %d tests to run.' % (len(tests))

	mf = MatrixFactorization(reviews,tests)
	mf.run(K,Iter)

