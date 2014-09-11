import math

def mse(pred, act):
	mse = 0.0
	E = abs(pred - act)
	for i in range(len(E)):
		mse += E[i] ** 2
	return mse / len(E)

def rmse(pred, act):
	return math.sqrt(mse(pred, act))

def mae(pred, act):
	mae = 0.0
	E = abs(pred - act)
	for i in range(len(E)):
		mae += abs(E[i])
	return mae/len(E)