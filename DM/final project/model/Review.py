class Review(object):
	"""docstring for Review"""
	def __init__(self,uid,bid,stars):
		super(Review, self).__init__()
		self.uid = uid
		self.bid = bid
		self.stars = stars * 1.0

	def getUID(self):
		return self.uid

	def getBID(self):
		return self.bid

	def getRate(self):
		return self.stars

	def getKey(self):
		return "%s%s" % (self.getUID(),self.getBID())

	def __str__(self):
		return "[uid: %s, bid: %s, stars: %f]" % (self.getUID(),self.getBID(),self.getRate())
		