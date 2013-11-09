from OKTF import OKTF
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
		