from sequence import Sequence
from copy import *
import sys

class PrefixSpan(object):
	"""docstring for PrefixSpan"""
	def __init__(self, path,min_sup,outputFile):
		super(PrefixSpan, self).__init__()
		self.path = path
		self.min_sup = min_sup
		self.debug =0
		self.outputFile = outputFile
		self.seqSize = 0
		self.results = []
		self.outFile = open(self.outputFile,'w')

	def load(self,min_sup):
		db = []
		with open(self.path) as f:
			for line in f:	
				lineData = line.strip().split()
				lineData = map(int,lineData)
				seq = Sequence()
				seq.parseSequence(lineData)
				db.append(seq)
		self.min_sup = len(db) * min_sup
		self.seqSize = len(db)
		return db

	def printdb(self,db):
		for s in db:
			print s

	def projectDb(self,prefix,db,accu):
		
		project = []

		for seq in db:
			s = seq.getProjectSequence(prefix,accu)
			if s:
				post = Sequence()
				post.seq = s
				project.append(post)

		return project

	def prefixSpan(self,iList,project,accu):
		if len(project) <self.min_sup:
			return 
		self.log(iList)
		for k,v in iList.iteritems():
			if v>=self.min_sup:
				seqPattern = self.join(accu,k)
				rs = self.format(seqPattern,v)
				print rs
				self.outFile.write(rs+"\n")
				#self.results.append(rs)
				projectdb=self.projectDb(k, project, seqPattern)
				self.log(str(k)+"-Project DB:")
				self.log(projectdb,1)
				freqItems = self.caculateFreqItems(k,projectdb)
				self.prefixSpan(freqItems,projectdb,seqPattern)

	def caculateFreqItems(self,prefix,db):
		freqItems = {}
		for seq in db:
			items = seq.getUniqueItems(prefix)
			for k in items:
				freqItems[k] = freqItems.get(k,0) + 1

		return freqItems

	def filterFreqItems(self,items):
		filtered = {}
		for k,v in items.iteritems():
			if v >= self.min_sup:
				filtered[k] = v
		return filtered

	def join(self,accu,right):
		left = deepcopy(accu)
		if len(left) == 0:
			left.append([right])
			return left
		if right < 0 :
			left[len(left)-1].append(abs(right))
			return left
		else:
			left.append([right])
			return left		

	def format(self,accu,freq):
		accuStr=""

		for ele in accu:
			accuStr+=str(ele)+' '

		accuStr = accuStr.replace('[','(').replace(']',')').replace(',','')

		freqPortion = freq*1.0/self.seqSize
		freqStr = "%.6f" % freqPortion
		return accuStr+": "+ freqStr

	def printSequentialPattern(self,seqPatter,freq):
		pass

	def log(self,content,type=0):
		if self.debug ==0:
			return
		if type ==1:
			self.printdb(content)
			print
		else:
			print content


	def run(self,min_sup):
		try:
			print "Start Load DB."
			db = self.load(min_sup)
			print "Finish Load DB."
			freqItems = self.caculateFreqItems(-99999,db)

			self.log(db,1)
			self.prefixSpan(freqItems,db,[])
			
		finally:
			self.outFile.close()
		

	def test(self):
		pass

if __name__ == '__main__':
	
	inputFile = sys.argv[1]
	min_sup = float(sys.argv[2])
	outputFile = sys.argv[3]

	path ="500K5K20_a.data"
	test ='test.data'
	test1 = 'test2.data'

	prefixspan = PrefixSpan(inputFile, min_sup,outputFile)
	prefixspan.run(min_sup)

