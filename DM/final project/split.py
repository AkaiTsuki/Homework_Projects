import random
from util.ReviewTxtParser import ReviewTxtParser

if __name__ == '__main__':
	"""
	This script will split the test data from training set.
	NOTE: It will not delete the test data from training set since
	we still need the test data to create rating matrix.
	"""
	testFile = 'test.txt'
	portion = 10

	parser = ReviewTxtParser()
	reviews = parser.getReviews("dataset/reviews.txt")
	
	test = {}

	for rid,r in reviews.iteritems():
		c = random.randint(1,portion)
		if c == 1:
			test[rid] = r

	with open(testFile,'w') as f:
		for rid,r in test.iteritems():
			string = "%s %s %d\n" % (r.getUID(),r.getBID(),r.getRate())
			f.write(string)
