#!/usr/bin/python
#
# Created by Albert Au Yeung (2010)
#
# An implementation of matrix factorization
#
try:
    import numpy
    from nmf import *
except:
    print "This implementation requires the numpy module."
    exit(0)

###############################################################################

"""
@INPUT:
    R     : a matrix to be factorized, dimension N x M
    P     : an initial matrix of dimension N x K
    Q     : an initial matrix of dimension M x K
    K     : the number of latent features
    steps : the maximum number of steps to perform the optimisation
    alpha : the learning rate
    beta  : the regularization parameter
@OUTPUT:
    the final matrices P and Q
"""
def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
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

def matrix_factorization1(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
    Q = Q.T
    rows,cols = numpy.nonzero(R)
    pair = zip(rows,cols)
    halfBeta = beta/2
    kRange = range(K)
    for step in xrange(steps):
        #print step
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

###############################################################################

if __name__ == "__main__":

    R = [
         [5,3,0,1],
         [4,0,0,1],
         [1,1,0,5],
         [1,0,0,4],
         [0,1,5,4]
        ]





    R = numpy.array(R)
    #R = numpy.random.rand(2000,2000)

    N = len(R)
    M = len(R[0])
    K = 2

    P = numpy.random.rand(N,K)
    Q = numpy.random.rand(M,K)

    #nP, nQ = matrix_factorization1(R, P, Q, K)
    #print numpy.dot(nP,nQ.T)

    R1 = [
         [5,3,-1,1],
         [4,-1,-1,1],
         [1,1,-1,5],
         [1,-1,-1,4],
         [-1,1,5,4]
        ]

    R1 = numpy.array(R1)
    np,nq=nmf(R1, P, Q.T, 0.001, 100, 100)
    print numpy.dot(np,nq)