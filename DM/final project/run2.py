from CollaborationFilter import CollaborationFilter
from App import App
from ReviewTxtParser import ReviewTxtParser
import sys

if __name__ == '__main__':
	K = int(sys.argv[1])
	app = App()
	app.initDB("dataset/reviews.txt",ReviewTxtParser())
	db = app.getDatabase()
	reviews = db.getReviews()

	app1 = App()
	app1.initDB("dataset/test10p.txt",ReviewTxtParser())
	db1 = app1.getDatabase()
	tests = db1.getReviews()
	print 'total %d tests to run.' % (len(tests))

	cf = CollaborationFilter(reviews,tests)
	cf.run(K)
