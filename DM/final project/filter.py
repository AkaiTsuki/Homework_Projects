from App import App
from ReviewJSONParser import ReviewJSONParser
import sys

# This script is for filtering the original dataset
# It will preserve those users that have more than 20 reviews
# and businesses that have more than 10 reviews

if __name__ == '__main__':

	# File that saves all filtered reviews
	rout = sys.argv[1]
	# File that saves all users in reviews
	uout = sys.argv[2]
	# File that saves all business in reviews
	bout = sys.argv[3]

	app = App()
	rPath = "training/yelp_training_set_review.json"

	print 'Start loading original dataset'
	app.initDB(rPath,ReviewJSONParser())
	print 'Finished'

	db = app.getDatabase()
	print db.statistcInfo()
	print 'Start filter data'
	db.filter(20,10)
	print 'Finished'
	
	db.reviewToFile(rout)
	db.ratingReport(uout,bout)

	