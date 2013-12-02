class FileReader(object):
	"""Given a path of a file, return a plain text
	in that file
	"""
	def __init__(self, path):
		super(FileReader, self).__init__()
		self.path = path
	
	def read(self):
		text = []
		with open(self.path) as f:
			for line in f:
				text.append(line)
		return "".join(text)
