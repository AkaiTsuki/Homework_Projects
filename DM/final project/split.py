import random
from ReviewTxtParser import ReviewTxtParser
from App import App

if __name__ == '__main__':

	testFile = 'test.txt'
	portion = 10

	app = App()
	app.initDB("dataset/reviews.txt",ReviewTxtParser())
	db = app.getDatabase()
	print db.statistcInfo()

	reviews = db.getReviews()
	
	test = {}

	for rid,r in reviews.iteritems():
		c = random.randint(1,portion)
		if c == 1:
			test[rid] = r

	with open(testFile,'w') as f:
		for rid,r in test.iteritems():
			string = "%s %s %d\n" % (r.getUID(),r.getBID(),r.getRate())
			f.write(string)
