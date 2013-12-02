import string

class TextFilter(object):
	"""TextFilter will removed the useless text from oringinal text,
		eliminate the stop word according to stop words list, and stem
		the words to terms.
	"""
	def __init__(self, stopList, stemming):
		super(TextFilter, self).__init__()
		self.stopList = stopList
		self.stemming = stemming

	def filter(self,text):
		"""
		Given a text, Returns a list of terms in this text
		"""
		# Remove the content after last line, and split the text to lines
		lines = self.removeUseless(text)
		# Split lines to words
		words = self.splitToWords(lines)
		# remove punctutation from words, especially, for (-:'), translate to whitespace
		words = self.removePunctuation(words)
		# Remove the stop word in words
		words = self.removeStop(words)
		# Convert word to stemming terms
		return self.convertStem(words)

	def removePunctuation(self,words):
		newWords = []
		table = string.maketrans("-:'","   ")
		for word in words:
			w = word.lower().translate(table,"!\"#$%&()*+,./;<=>?@[\]^_`{|}~")

			newWords.extend(w.strip().split())
		return newWords

	def removeUseless(self,text):
		"""
		Given a text, Removes the content after last empty line,
		Returns a list of lines of text
		"""
		txt = text[text.find("<pre>")+len("<pre>"):text.find("</pre>")].strip()
		lines = txt.split('\n')
		last = len(lines) - 1
		
		lastEmpty = -1
		
		for i in xrange(len(lines)):
			line = lines[last-i].strip()
			if len(line)== 0:
				lastEmpty = last - i
				break

		return lines[:lastEmpty+1]

	def splitToWords(self,lines):
		"""
		Given a list of lines, each line has some text,
		Returns a list of words which consist of these lines
		"""
		wordList = []
		for line in lines:
			words = line.strip().split()
			wordList.extend(words)
		return wordList

	def removeStop(self,words):
		return filter(lambda x : not self.stopList.isStop(x),words)

	def convertStem(self,words):
		return map(lambda x: self.stemming.convert(x),words)



			