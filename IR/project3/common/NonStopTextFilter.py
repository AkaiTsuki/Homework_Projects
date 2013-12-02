from TextFilter import TextFilter

class NonStopTextFilter(TextFilter):
	"""docstring for NonStopTextFilter"""
	def __init__(self, stop, stem):
		super(NonStopTextFilter, self).__init__(stop,stem)

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
		# Convert word to stemming terms
		return self.convertStem(words)