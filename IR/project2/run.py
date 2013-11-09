from Resources import Resources
from QueryParser import QueryParser
from SpaceVectorModel import SpaceVectorModel
from InvertListParser import InvertListParser
import operator

def outputRanks(ranks,queryNum,doclist):
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

if __name__ == '__main__':
	r = Resources()
	r.loadStopList('stoplist.txt')
	r.loadDocList('doclist.txt')
	r.loadStemClasses('stem-classes.lst.txt')

	q = QueryParser('desc.51-100.short.txt')
	raw_lst = q.load()
	lst=q.process(raw_lst, r.stoplist, r.stemClasses)
	querys = q.generateQueryList(lst)

	spaceVector = SpaceVectorModel(querys)
	spaceVector.caculateQueryOKTFs()

	output = []
	for q in spaceVector.querys:
		ranks = spaceVector.getRankedDocuments(q)
		qoutput = outputRanks(ranks,q.id,r.doclist)
		output += qoutput
		
	for o in output:
		print o[0],o[1],o[2],o[3],o[4],o[5]
