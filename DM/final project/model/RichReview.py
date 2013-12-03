class RichReview(object):
	"""docstring for RichReview"""
	def __init__(self, uid,bid,stars,txt):
		super(RichReview, self).__init__()
		self.txt = txt
		self.uid = uid
		self.bid = bid
		self.stars = stars * 1.0

	def getText(self):
		return self.txt

	def getUID(self):
		return self.uid

	def getBID(self):
		return self.bid

	def getRate(self):
		return self.stars

	def getKey(self):
		return "%s%s" % (self.getUID(),self.getBID())

	def __str__(self):
		return "[uid: %s, bid: %s, stars: %f, txt: %s]" % (self.getUID(),self.getBID(),self.getRate(),self.getText())