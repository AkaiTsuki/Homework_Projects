from OKTF import OKTF
from OKTFIDF import OKTFIDF
from MaxLikelihood import MaxLikelihood
from JelinekMercer import JelinekMercer
from BM25V1 import BM25V1
import operator

class Application(object):
	"""docstring for Application"""
	def __init__(self, resources,model,db,output):
		super(Application, self).__init__()
		self.resources = resources
		self.model = model
		self.db = db
		self.output = output

	def loadModel(self):
		if self.model==1:
			return OKTF(self.resources,self.resources.querys,self.db)
		elif self.model==2:
			return OKTFIDF(self.resources,self.resources.querys,self.db)
		elif self.model==3:
			return MaxLikelihood(self.resources,self.db)
		elif self.model ==4:
			return JelinekMercer(self.resources,self.db)
		elif self.model ==5:
			return BM25V1(self.resources,self.db)
		else:
			return None

	def writeToFile(self,result):
		with open(self.output,'w') as f:
			for o in result:
				s = "%s %s %s %s %s %s\n" % (o[0],o[1],o[2],o[3],o[4],o[5])
				f.write(s)
		f.close()

	def format(self,ranks,queryNum):
		doclist = self.resources.doclist
		sorted_ranks = sorted(ranks.iteritems(), key=operator.itemgetter(1),reverse=True)
		top1000 = sorted_ranks[:1000]
		r = []
		rank =1
		for item in top1000:
			docid = doclist[item[0]]
			score = item[1]
			r.append([queryNum,"Q0",docid,rank,score,"EXP"])
			rank +=1
		return r


	def run(self):
		model = self.loadModel()
		output =[]

		count = 1
		for q in self.resources.querys:
			print count
			model.setQuery(q)
			ranks = model.rank()
			output += self.format(ranks,q.id)
			count+=1

		self.writeToFile(output)

	def test(self):
		model = self.loadModel()
		for q in self.resources.querys:
			model.setQuery(q)
			model.rank()



		