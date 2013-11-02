import numpy
import scipy.optimize as optimization

visited = {}

totalWords = 0
uniqueWords = 0

totalWordsList = []
uniqueWordsList = []

result = []

with open("output") as f:
	for line in f:
		word = line.strip()
		if word in visited:
			visited[word] +=1
		else:
			visited[word] = 1
		totalWords = totalWords + 1
		uniqueWords = len(visited)
		totalWordsList.append(totalWords)
		uniqueWordsList.append(uniqueWords)
		result.append((totalWords,uniqueWords))

xdata = numpy.array(totalWordsList)
ydata = numpy.array(uniqueWordsList)

def func(n,k,c):
	return k*(n**c)

print optimization.curve_fit(func, xdata, ydata)