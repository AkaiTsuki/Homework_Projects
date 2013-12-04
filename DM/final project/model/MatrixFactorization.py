import numpy
from Review import Review
import math

class MatrixFactorization(object):
	"""docstring for MatrixFactorization"""
	def __init__(self, reviews,tests):
		super(MatrixFactorization, self).__init__()
		self.reviews = reviews
		self.tests = tests
		self.uidToIndex = self.getAllUsers()
		self.bidToIndex = self.getAllBusinesses()
		self.R = self.getMatrix()

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

	def run(self,K,iter):
		self.splitTestSet()
		R = self.R
		U = len(self.uidToIndex)
		B = len(self.bidToIndex)
		P = numpy.random.rand(U,K)
		Q = numpy.random.rand(B,K)
		print "Create Model"
		nP, nQ = self.matrix_factorization(R, P, Q, K,steps=iter)
		ER  = numpy.dot(nP,nQ.T)
		
		print "Evaluation"
		rmse = 0.0
		mae = 0.0

		for rid,r in self.tests.iteritems():
			uid = r.getUID()
			bid = r.getBID()
			rate = r.getRate()
			uIndex = self.uidToIndex[uid]
			bIndex = self.bidToIndex[bid]
			eRate = ER[uIndex][bIndex]
			rmse += abs(eRate - rate) ** 2
			mae += abs(eRate - rate)
		
		print "RMSE: ", math.sqrt(rmse/len(self.tests))
		print "MAE: ", mae/len(self.tests)


	def matrix_factorization(self,R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
	    Q = Q.T
	    rows,cols = numpy.nonzero(R)
	    pair = zip(rows,cols)
	    halfBeta = beta/2
	    kRange = range(K)
	    for step in xrange(steps):
	        print step
	        e = 0
	        for i,j in pair:
	            eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])
	            e += eij**2
	            doubleEij = 2*eij

	            for k in kRange:
	                e += halfBeta * (P[i][k]**2 + Q[k][j]**2)
	                P[i][k] = P[i][k] + alpha * (doubleEij * Q[k][j] - beta * P[i][k])
	                Q[k][j] = Q[k][j] + alpha * (doubleEij * P[i][k] - beta * Q[k][j])

	        if e < 0.1:
	            break
	        
	    return P, Q.T


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

		