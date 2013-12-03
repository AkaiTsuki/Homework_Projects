from util.Database import Database
from util.RichReviewJSONParser import RichReviewJSONParser

def main():
	rPath = "training/yelp_training_set_review.json"
	parser = RichReviewJSONParser()
	print 'Read all reviews from json....'
	reviews = parser.getReviews(rPath)
	db = Database(reviews)
	print "Finished"
	print db.statistcInfo()
	print "Get subset of reviews..."
	db.filter(20,10)
	print "Finished"
	print "Write to files..."
	db.richReviewToFile("training.txt","test.txt",10)
	print "Finished"
	db.ratingReport("user.txt","business.txt")

if __name__ == '__main__':
	main()