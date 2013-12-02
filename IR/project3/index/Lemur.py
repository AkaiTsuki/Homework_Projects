class Lemur(object):
	"""docstring for Lemur"""
	def __init__(self):
		super(Lemur, self).__init__()

	def query(self,term,indexPath):
		with open(indexPath) as f:
			for line in f:
				content = line.strip().split()
				if not content[0] == term:
					continue
				else:
					return line[line.find(" ")+1:]
			return ""