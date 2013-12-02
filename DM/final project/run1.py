from MatrixFactorization import MatrixFactorization
from App import App
from ReviewTxtParser import ReviewTxtParser
import sys

if __name__ == '__main__':
	K = int(sys.argv[1])
	Iter = int(sys.argv[2])

	app = App()
	app.initDB("dataset/reviews.txt",ReviewTxtParser())
	db = app.getDatabase()
	reviews = db.getReviews()

	app1 = App()
	app1.initDB("dataset/test10p.txt",ReviewTxtParser())
	db1 = app1.getDatabase()
	tests = db1.getReviews()
	print 'total %d tests to run.' % (len(tests))

	mf = MatrixFactorization(reviews,tests)
	mf.run(K,Iter)

