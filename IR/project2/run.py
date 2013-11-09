from Resources import Resources

from Application import Application

if __name__ == '__main__':
	# input parameter
	queryfile = "desc.51-100.short.txt"
	model = 1
	database = 3
	outputfile = "model1.txt"

	# System file parameter
	docfile ="doclist.txt"
	stemfile ='stem-classes.lst.txt'
	stopfile ="stoplist.txt"

	# Loading the resources
	resources = Resources()
	resources.loadDocList(docfile)
	resources.loadStemClasses(stemfile)
	resources.loadStopList(stopfile)
	resources.loadQuerys(queryfile)

	#Create Applications based on input parameter
	app = Application(resources,model,database,outputfile)

	app.run()