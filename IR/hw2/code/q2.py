class DocumentDictItem(object):
	"""docstring for DocumentDictItem"""
	def __init__(self, word, frequency):
		super(DocumentDictItem, self).__init__()
		# the word
		self.word = word
		# the number of occurrance
		self.frequency = frequency
		# the rank in frequency decreasing order
		self.rank = -1
		# the probability of occurrence in artical
		self.probability = 0
		# the product of probability and rank
		self.product = 0
		# the product of frequency and rank
		self.FRProduct = 0

	def statistic(self,rank,total):
		self.rank = rank
		self.probability = self.caculateProbability(self.frequency,total)
		self.product = self.probability * self.rank
		self.FRProduct = self.frequency * self.rank

	def caculateProbability(self,part,whole):
		return float(part) / float(whole)

	def __str__(self):
		return "[ "+str(self.rank)+", "+self.word+", "+str(self.frequency)+", "+str(self.probability)+", "+str(self.product)+", "+str(self.FRProduct)+" ]"


class DocumentDict(object):
	"""
	This class will create a dictionary for the given document.
	The information in dictionary will contain total number of words, total number of 
	unique words, frequency of each word, the probability of occurrence and the product
	of he rank and the probability.

	This document that will be statistic should be a plain text file that contains a list
	of words and for each line it has only one word.

	"""
	def __init__(self,fileDir):
		"""
		Initialize the class and parse the input file
		"""
		super(DocumentDict, self).__init__()

		self.dictItems =[]
		self.totalWords = 0
		self.totalUniqueWords = 0
		
		raw = self.parseFile(fileDir)
		self.totalUniqueWords = len(raw)

		sortedRaw = sorted(raw.items(), key=lambda x: x[1], reverse=True)
		self.__createDictionary__(sortedRaw)


	def parseFile(self,fileDir):
		"""
		Given a file directory,
		Read the input file and statistic 
		the total number of words and the frequency of each word
		Returns a dictionary of the word and its frequency
		"""
		with open(fileDir) as f:
			rawItems = {}
			for line in f:
				word = line.strip()
				if word in rawItems:
					rawItems[word] += 1
				else:
					rawItems[word] = 1
				self.totalWords+=1
			return rawItems

	def __createDictionary__(self,sortedRawList):
		for i,turple in enumerate(sortedRawList): 
			item = DocumentDictItem(turple[0],turple[1])
			item.statistic(i+1, self.totalWords)
			self.dictItems.append(item)
	
		
	def topFrequentedWords(self,top=25,offset=0,start=None):
		if start is None:
			return self.topNFrequentlyWords(top,offset)
		else:
			return self.topNFrequentlyWordsStartWith(top,offset,start)
			

	def topNFrequentlyWords(self,top=25,offset=0):
		"""
		Given a number that specify the number of top words,
		Returns a list that contains the top N frequency words from the offset of sortedList
		"""
		return self.dictItems[offset:offset+top]

	def topNFrequentlyWordsStartWith(self,top,offset,start):
		"""
		@param top the top n words
		@param offset the start position of sortedList
		@param start the prefix of the word
		Find the top n words start with the prefix based on the frequency 
		"""
		visited = 0
		result = []

		for i in range(offset,len(self.dictItems)):
			if(visited>=top):
				break
			item = self.dictItems[i]
			word = item.word
			if word.startswith(start):
				result.append(item)
				visited+=1

		return result

	def omit(self,frequency):
		"""
		Given a frequency, 
		returns a list of DocumentDictItems that its frequency is equal to the
		given frequency
		"""
		result = []
		for item in self.dictItems:
			if item.frequency == frequency:
				result.append(item)
		return result

	def totalOmit(self,omitList):
		"""
		Given a list of omitted words,
		returns the total number of frequency for these words
		"""
		total = 0;
		for item in omitList:
			total += item.frequency
		return total

	
	def printDict(self,dictionary):
		for item in dictionary:
			print item


def q2():
	# Initial the dictionary
	w = DocumentDict("output")

	# Program for question a)
	print "Question a) answer: "
	print "Top 25 words:"
	print "========================="
	top25 = w.topFrequentedWords(25)
	w.printDict(top25)
	print ""

	print "Next Top 25 words start with \'f\':"
	print "========================="
	top25f = w.topFrequentedWords(25,25,'f')
	w.printDict(top25f)
	print ""

	print "Total words:",w.totalWords
	print "Vocabulary Size:",w.totalUniqueWords
	print ""

	# Program for question b)
	print "Question b) answer: "
	print "Words that omitted: "
	print "========================="
	
	actualTotalOmitPercentage = 0
	estimatedTotalOmitProportion = 0

	for i in range(4):
		omit = w.omit(i+1)
		#w.printDict(omit)
		actualOmit = len(omit)
		actualOmitPercentage = float(len(omit)) / float(len(w.dictItems))
		estimatedOmitPercentage = 1.0/(float(i+1)*float(i+2))
		actualTotalOmitPercentage += actualOmitPercentage
		estimatedTotalOmitProportion += estimatedOmitPercentage
		print "Total omit vocabulary (occur ==",i+1,"):",actualOmit
		print "Actual omit proportion:", actualOmitPercentage
		print "Estimate omit proportion:", estimatedOmitPercentage
		print ""

	print "Total actual omit proportion: ", actualTotalOmitPercentage
	print "Total estimated omit proportion: ", estimatedTotalOmitProportion
	

if __name__ == '__main__':
	q2()


	