from sets import Set

class Sequence(object):
	"""docstring for Sequence"""
	def __init__(self):
		super(Sequence, self).__init__()
		self.seq = []
		#self.parseSequence(linedata)

	def prune(self,freqItems,min_sup):
		seq = Sequence()
		for ele in self.seq:
			newEle = []
			for item in ele:
				if freqItems[item] >= min_sup:
					newEle.append(item)
			if len(newEle) > 0:
				seq.seq.append(newEle)
		return seq

	def parseSequence(self,data):
		start =1
		while start<len(data):
			l = data[start]
			pos = start+1
			e = self.parseElement(data, pos, l)
			self.seq.append(e)
			start = l+pos

	def parseElement(self,data,start,length):
		e = []
		for i in xrange(start,start+length):
			e.append(data[i])
		return e

	def getELement(self,pos):
		return self.seq[pos]

	def getItem(self,x,y):
		return self.seq[x][y]

	def getPrefixPos(self,last,accu):
		prefix = last
		if last < 0:
			e = self.seq[0]
			for i in range(len(e)):
				if e[i] == last:
					return (0,i)

		prefix = abs(last)
		for k in range(len(self.seq)):
			e = self.seq[k]
			for i in range(len(e)):
				item = e[i]
				if item == prefix:
					if last > 0:
						return (k,i)
					else:
						if self.checkPrefix(accu[-1],e,i):
							return (k,i)
		return (None,None)

	def checkPrefix(self,prefixLastELement,e,pos):
		i = len(prefixLastELement)-1
		j = pos

		while i>=0:
			if j== -1:
				return False
			if e[j] != prefixLastELement[i]:
				return False
			else:
				i-=1
				j-=1
		return True


	def getProjectSequence(self,prefix,accu):
		postfix = []
		

		pos = self.getPrefixPos(prefix,accu)

		x = pos[0]
		y = pos[1]

		if x == None:
			return []

		e = self.getELement(x)
		if y == len(e)-1 :
		 	return  self.seq[x+1:]
		else:
			postfix = self.seq[x:]
			ele = postfix[0]
			newEle = ele[y+1:]

			for i in range(len(newEle)):
				if newEle[i]>0:
					newEle[i] = -newEle[i]
		
			postfix[0] = newEle
			return postfix
	
	def getUniqueItems(self,prefix):
		items = Set()

		for i in range(len(self.seq)):
			e = self.seq[i]
			# two types of prefix y
			# y
			if prefix > 0:
				pointer = 99999
				for j in range(len(e)):
					item  = e[j]
					
					if len(e) == 1:
						items.add(item)
					else:				
						items.add(item)
						if item == prefix:
							pointer = j
						if j > pointer:		
							items.add(-item)
				pointer = 99999
				# (_y)
			else:
				pointer = 99999
				for j in range(len(e)):
					item = e[j]
					items.add(item)
					if item == abs(prefix):
						pointer = j
					if j>pointer:
						items.add(-item)

				pointer = 99999


		return items

	def getUniqueItemsV1(self,prefix):
		items = Set()
		for i in range(len(self.seq)):
			e = self.seq[i]
			for j in range(len(e)):
				item = e[j]

				items.add(item)
				if item == prefix:
					for k in range(j+1,len(e)):
						items.add(-e[k])

			

		return items

	def __str__(self):
		return str(self.seq)
		
s = Sequence()
s.seq=[[-3],[1,2,3],[4],[3,6]]
#print s.getUniqueItemsV1(-2)
