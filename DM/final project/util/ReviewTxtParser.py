from model.Review import Review

class ReviewTxtParser(object):
	"""docstring for ReviewTxtParser"""
	def __init__(self):
		super(ReviewTxtParser, self).__init__()
	
	def getReviews(self,path):
		reviews = {}
		count = 0
		with open(path) as f:
			for line in f:
				data = line.strip().split()
				uid = data[0]
				bid = data[1]
				stars = int(data[2])
				reviews[count] = Review(uid,bid,stars)
				count +=1
		return reviews