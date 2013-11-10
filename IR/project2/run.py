from Resources import Resources

from Application import Application

if __name__ == '__main__':
	# input parameter
	queryfile = "desc.51-100.short.txt"
	model = 3
	database = 3
	outputfile = "model3test.txt"

	# System file parameter
	docfile ="doclist.txt"
	stemfile ='stem-classes.lst.txt'
	stopfile ="stoplist.txt"

	# Loading the resources
	resources = Resources(database)
	resources.loadDocList(docfile)
	resources.loadStemClasses(stemfile)
	resources.loadStopList(stopfile)
	resources.loadQuerys(queryfile)

	"""
	q57=None
	for q in resources.querys:
		if q.id == '57':
			q57 =q
	resources.querys = [q57]
	print q57
	"""
	#Create Applications based on input parameter
	app = Application(resources,model,database,outputfile)

	app.run()

