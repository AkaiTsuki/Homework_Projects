from ReviewJSONParser import ReviewJSONParser
from Database import Database
from sets import Set
from nmf import *
import numpy

class App(object):
	"""docstring for App"""
	def __init__(self):
		super(App, self).__init__()
		self.db = None
		self.uidToUIndx = {}
		self.bidToBIndx = {}
		self.uIndxToUid = {}
		self.bIndxToBid = {}


	def initDB(self,rPath,parser):
		reviews = parser.getReviews(rPath)
		self.db = Database(reviews)

	def predict(self,u,b):
		db = self.getDatabase()
		relUsers = Set()
		# add current user to user set
		relUsers.add(u)
		# add all users that already rated b to user set
		relUsers=relUsers.union(db.getRelatedUsers(b))
		relBusinesses = Set()
		# get all businesses that a user rated in user set
		for user in relUsers:
			relBusinesses = relBusinesses.union(db.getRelatedBusinesses(user))
		
		self.setUpMatrixDimension(relUsers,relBusinesses)
		#self.printDimension()

		matrix = self.getRatingMatrix()
		R = numpy.array(matrix)
		print R
		R[2][1] = 0
		print R

		N = len(R)
		M = len(R[0])
		K = 4
		P = numpy.random.rand(N,K)
		Q = numpy.random.rand(M,K)
		nP, nQ = self.matrix_factorization(R,P,Q,K,steps=100)
		print numpy.dot(nP,nQ.T)

	def matrix_factorization(self,R, P, Q, K, steps=5000, alpha=0.002, beta=0.02):
	    Q = Q.T
	    for step in xrange(steps):
	        #print step
	        for i in xrange(len(R)):
	            for j in xrange(len(R[i])):
	                if R[i][j] > 0:
	                    eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])
	                    for k in xrange(K):
	                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
	                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
	        #eR = numpy.dot(P,Q)
	        e = 0
	        for i in xrange(len(R)):
	            for j in xrange(len(R[i])):
	                if R[i][j] > 0:
	                    e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)
	                    for k in xrange(K):
	                        e = e + (beta/2) * ( pow(P[i][k],2) + pow(Q[k][j],2) )
	        if e < 0.001:
	            break
	    return P, Q.T

	def clearDimension(self):
		self.uidToUIndx = {}
		self.bidToBIndx = {}
		self.uIndxToUid = {}
		self.bIndxToBid = {}

	def printDimension(self):
		print self.uidToUIndx 
		print self.bidToBIndx 
		print self.uIndxToUid 
		print self.bIndxToBid 

	def setUpMatrixDimension(self,users,businesses):
		self.clearDimension()

		index = 0
		for u in users:
			self.uidToUIndx[u] = index
			self.uIndxToUid[index] = u
			index +=1

		index = 0
		for b in businesses:
			self.bidToBIndx[b] = index
			self.bIndxToBid[index] = b
			index +=1
		
	def getRatingMatrix(self):
		matrix = []

		M = len(self.uidToUIndx)
		N = len(self.bidToBIndx)

		for i in range(M):
			matrix.append([0]*N)

		for i in range(M):
			for j in range(N):
				uid = self.uIndxToUid[i]
				bid = self.bIndxToBid[j]
				rate = self.db.getUserRate(uid,bid)
				matrix[i][j] = rate
		return matrix

	def getDatabase(self):
		return self.db

	def getReviews(self):
		return self.reviews