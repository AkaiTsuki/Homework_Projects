from util.ReviewJSONParser import ReviewJSONParser
from util.Database import Database
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

	rPath = "training/yelp_training_set_review.json"

	print 'Start loading original dataset'
	parser = ReviewJSONParser()
	reviews = parser.getReviews(rPath)
	db = Database(reviews)
	print 'Finished'

	print db.statistcInfo()
	print 'Start filter data'
	db.filter(20,10)
	print 'Finished'
	
	db.reviewToFile(rout)
	db.ratingReport(uout,bout)