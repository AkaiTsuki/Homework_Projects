import numpy
from Review import Review
import math
import operator

class CollaborationFilter(object):
	"""docstring for CollaborationFilter"""
	def __init__(self, reviews,tests):
		super(CollaborationFilter, self).__init__()
		self.reviews = reviews
		self.tests = tests
		self.uidToIndex = self.getAllUsers()
		self.bidToIndex = self.getAllBusinesses()
		self.R = self.getMatrix()
		self.memory = {}

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

	def splitTestSet(self):
		for rid,r in self.tests.iteritems():
			uid = r.getUID()
			bid = r.getBID()

			uIndex = self.uidToIndex[uid]
			bIndex = self.bidToIndex[bid]
			self.R[uIndex][bIndex] = 0

	def run(self,K):
		self.splitTestSet()

		rmse = 0.0
		mae = 0.0
		count = 0
		for rid,r in self.tests.iteritems():
			uid = r.getUID()
			bid = r.getBID()
			rate = r.getRate()
			uIndex = self.uidToIndex[uid]
			bIndex = self.bidToIndex[bid]
			er = self.predictRate(uIndex,bIndex,K)
			rmse += abs(er - rate)**2
			mae += abs(er-rate)
			count+=1
			print "%d %f %f" % (count,er,rate)

		print "RMSE: ", math.sqrt(rmse/len(self.tests))
		print "MAE: ", mae/len(self.tests)

	def predictRate1(self,uInx,bInx,K):
		r_users = self.getRelatedUsers(uInx,bInx)

		total = 0.0
		for u in r_users:
			total += self.R[u][bInx]

		return total / len(r_users)

	def getAverageRate(self,bInx,r_users):
		total = 0.0
		for u in r_users:
			total += self.R[u][bInx]

		return total / len(r_users)

	def predictRate(self,uInx,bInx,K):
		r_users = self.getRelatedUsers(uInx,bInx)
		if len(r_users) <= K:
			return self.getAverageRate(bInx,r_users)

		sorted_users = self.getSimilarity(uInx,r_users)
		sorted_users = sorted_users[:K]
		total = 0.0
		for u,v in sorted_users:
			total += self.R[u][bInx]

		return total / len(sorted_users)


	def getRelatedUsers(self,uInx,bInx):
		users = []
		for u in range(len(self.R)):
			if not self.R[u][bInx] == 0:
				users.append(u)
		return users
	
	def getSimilarity(self,uInx,relatedUsers):
		ranks = {}
		C = self.R[uInx,:]
		for u in relatedUsers:
			key = str(uInx)+" "+str(u)
			keyR = str(u)+" "+str(uInx)

			if self.memory.has_key(key):
				ranks[u] = self.memory[key]
				continue

			if self.memory.has_key(keyR):
				ranks[u] = self.memory[keyR]
				continue

			P = self.R[u,:]
			rank = self.calculateSimilarity(C,P)
			self.memory[key] = rank
			self.memory[keyR] = rank
			ranks[u]=rank

		return sorted(ranks.iteritems(), key=operator.itemgetter(1),reverse=True)

	def getSimilarity1(self,uInx,relatedUsers):
		ranks = {}
		for u in relatedUsers:
			ranks[u]=self.calculateSimilarity1(uInx,u)
		return sorted(ranks.iteritems(), key=operator.itemgetter(1),reverse=True)

	def calculateSimilarity(self,C,P):
		term1 = numpy.dot(C,P.T)
		CD = 0.0
		PD = 0.0
		for i in range(len(C)):
			CD += C[i]**2
			PD += P[i]**2
		return term1 / (math.sqrt(CD) * math.sqrt(PD))

	def calculateSimilarity1(self,u1,u2):
		term1 = 0.0
		CD = 0.0
		PD = 0.0
		for i in range(len(self.R[u1])):
			term1 += self.R[u1][i] * self.R[u2][i]
			CD += self.R[u1][i]
			PD += self.R[u2][i]
		return term1 / (math.sqrt(CD) * math.sqrt(PD))
		

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
		