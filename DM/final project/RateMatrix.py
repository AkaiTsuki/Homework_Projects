from Review import Review
import numpy
import random

class RateMatrix(object):
	"""docstring for RateMatrix"""
	def __init__(self, reviews):
		super(RateMatrix, self).__init__()
		self.reviews = reviews
		self.uidToIndex = self.getAllUsers()
		self.bidToIndex = self.getAllBusinesses()
		self.R = self.getMatrix()
		self.test = {}
	
	def getMatrix(self):
		U = len(self.uidToIndex)
		B = len(self.bidToIndex)
		R = numpy.zeros((U,B))

		for rid,r in self.reviews.iteritems():
			uid = r.getUID()
			bid = r.getBID()
			rate = r.getRate()
			uIndex = self.uidToIndex[uid]
			bIndex = self.bidToIndex[bid]
			R[uIndex][bIndex] = rate

		return R

	def splitTestSet(self,p=20):
		self.test = {}
		rows,cols = numpy.nonzero(self.R)
		for u,b in zip(rows,cols):
			rand = self.getRandomNumberBetween(1,p)
			if rand == 1:
				self.test[str(u)+" "+str(b)] = self.R[u][b]
				self.R[u][b] = 0.0
		self.testToFile()

	def testToFile(self):
		with open('randomTest.txt','w') as f:
			for key,val in self.test.iteritems():
				f.write(key+" "+str(val)+"\n")
	

	def getRandomNumberBetween(self,start,end):
		return random.randint(start,end)

	def getAllUsers(self):
		users = {}
		uIndex = 0
		for rid,r in self.reviews.iteritems():
			uid = r.getUID()
			if not users.has_key(uid):
				users[uid] = uIndex
				uIndex +=1
		return users

	def getAllBusinesses(self):
		businesses = {}

		index = 0
		for rid,r in self.reviews.iteritems():
			bid = r.getBID()
			if not businesses.has_key(bid):
				businesses[bid] = index
				index +=1

		return businesses
