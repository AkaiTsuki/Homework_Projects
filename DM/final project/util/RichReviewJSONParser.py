from model.RichReview import RichReview
import json

class RichReviewJSONParser(object):
	"""docstring for RichReviewJSONParser"""
	def __init__(self):
		super(RichReviewJSONParser, self).__init__()

	def getReviews(self,path):
		"""
		Given the path of json file, returns a list of reviews
		"""
		jsonObjs = self.parse(path)
		reviews = {}

		for obj in jsonObjs:
			review = self.getReview(obj)
			key = review.getKey()
			reviews[key] = review
				
		return reviews

	def getReview(self,obj):
		uid = obj['user_id'].encode('utf8')
		bid = obj['business_id'].encode('utf8')
		stars = float(obj['stars'])
		txt = obj['text'].encode('utf8')
		return RichReview(uid,bid,stars,txt)

	def parse(self,path):
		"""
		Given a json file path, returns a list of json object.
		"""
		lst = []
		with open(path) as f:
			for line in f:
				obj = json.loads(line);
				lst.append(obj)
		return lst
