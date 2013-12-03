from model.RichReview import RichReview

class RichReviewTxtParser(object):
	"""docstring for RichReviewTxtParser"""
	def __init__(self):
		super(RichReviewTxtParser, self).__init__()

	def getReviews(self,path):
		reviews = {}
		with open(path) as f:
			for line in f:
				data = line.strip().split()
				uid = data[0]
				bid = data[1]
				stars = int(data[2])
				txt = data[3:]
				r = RichReview(uid,bid,stars,txt)
				reviews[r.getKey()] = r
		return reviews