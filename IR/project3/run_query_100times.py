from query.Resources import Resources
from query.Application import Application
import sys

def main():
	database = 4
	model = int(sys.argv[1])
	outputfile = sys.argv[2]
	
	#model = 1
	#outputfile = 'outputTest.txt'

	queryfile = "cacm.query"
	docfile ="doclist.txt"
	stemfile ='k_loose.stemclass'
	stopfile ="stoplist.txt"

	resources = Resources(database)
	resources.loadDocList(docfile)
	resources.loadStemClasses(stemfile)
	resources.loadStopList(stopfile)
	resources.loadQuerys(queryfile,1)

	app = Application(resources,model,database,outputfile)
	for i in range(100):
		print "LOOP: %d\n" % i
		app.run()


if __name__ == '__main__':
	main()