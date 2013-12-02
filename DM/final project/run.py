from App import App
from ReviewTxtParser import ReviewTxtParser
from RateMatrix import RateMatrix
import numpy
import math
import sys

def matrix_factorization1(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
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

def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
	Q = Q.T
	for step in xrange(steps):
		print step
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

if __name__ == '__main__':
	output = sys.argv[1]
	step = int(sys.argv[2])
	K = int(sys.argv[3])

	app = App()
	app.initDB("dataset/reviews.txt",ReviewTxtParser())
	db = app.getDatabase()

	print db.statistcInfo()
	
	rm = RateMatrix(db.getReviews())
	print len(rm.uidToIndex)
	print len(rm.bidToIndex)

	rm.splitTestSet(p=5)
	
	R =rm.R

	U = len(rm.uidToIndex)
	B = len(rm.bidToIndex)


	P = numpy.random.rand(U,K)
	Q = numpy.random.rand(B,K)

	print "Create Model"
	nP, nQ = matrix_factorization1(R, P, Q, K,steps=step)
	ER  = numpy.dot(nP,nQ.T)

	print "Evaluation"
	test = rm.test
	result = []
	for pos,score in test.iteritems():
		posxy = pos.split()
		ui = int(posxy[0])
		bi = int(posxy[1])
		es = ER[ui][bi]
		result.append([es,score])

	esm = 0.0
	
	with open(output,"w") as f:
		for i in result:
			esm += abs(i[0] - i[1])**2
			string = "%f %f\n" % (i[0],i[1])
			f.write(string)
	print "ESM: ", math.sqrt(esm/len(result))



