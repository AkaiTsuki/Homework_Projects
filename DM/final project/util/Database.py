from sets import Set
import operator

class Database(object):
	"""docstring for Database"""
	def __init__(self, reviews):
		super(Database, self).__init__()
		self.reviews = reviews
		self.users = self.__getAllUsers__()
		self.businesses = self.__getAllBusinesses__()


	def __getAllUsers__(self):
		users = Set()

		for rid,r in self.getReviews().iteritems():
			users.add(r.getUID())

		return users

	def __getAllBusinesses__(self):
		businesses = Set()

		for rid,r in self.getReviews().iteritems():
			businesses.add(r.getBID())

		return businesses

	def filter(self,uMin,bMin):
		"""
		Given a minRate, returns reviews that all users rated
		no less than minRate.
		"""
		userRate = self.__usersRating__()
		newReviews = {}
		oldReviews = self.getReviews()

		for rid,r in oldReviews.iteritems():
			uid = r.getUID()
			if userRate.has_key(uid) and userRate[uid] >= uMin:
				newReviews[rid] = r
		self.reviews = newReviews

		bRate = self.__businessRating__()
		newReviews = {}
		oldReviews = self.getReviews()
		for rid,r in oldReviews.iteritems():
			bid = r.getBID()
			if bRate.has_key(bid) and bRate[bid] >= bMin:
				newReviews[rid] = r
		self.reviews = newReviews


	def getUsers(self):
		return self.users

	def getBusinesses(self):
		return self.businesses

	def getRelatedUsers(self,b):
		"""
		Given a business, returns all users that rated this business
		"""
		users = Set()
		for rid,r in self.getReviews().iteritems():
			if r.getBID() == b:
				users.add(r.getUID())
		return users

	def getRelatedBusinesses(self,u):
		"""
		Given a user, returns all businesses that this user rated
		"""
		businesses = Set()
		for rid,r in self.getReviews().iteritems():
			if r.getUID()==str(u):
				businesses.add(r.getBID())
		return businesses

	def getReviews(self):
		return self.reviews

	def getReviewCount(self):
		return len(self.reviews)

	def getUserRate(self,u,b):
		reviews = self.getReviews()
		key = "%s%s" %(u,b)
		if reviews.has_key(key):
			return reviews[key].getRate()
		else:
			return 0

	def ratingReport(self,upath,bpath):
		"""
		Write the rating statistic information to file
		"""
		userRate,businessRate = self.__StatisticRating__()
		sortedx = sorted(userRate.iteritems(), key=operator.itemgetter(1), reverse=True)
		sortedxy = sorted(businessRate.iteritems(), key=operator.itemgetter(1), reverse=True)
		with open(upath,'w') as f:
			for item in sortedx:
				string = "%s %d\n" %(item[0],item[1])
				f.write(string)

		with open(bpath,'w') as b:
			for item in sortedxy:
				string = "%s %d\n" %(item[0],item[1])
				b.write(string)

	def reviewToFile(self,path):
		with open(path,'w') as f:
			for rid,r in self.getReviews().iteritems():
				string = "%s %s %d\n" % (r.getUID(),r.getBID(),r.getRate())
				f.write(string)

	def __usersRating__(self):
		userRate = {}
		for rid,r in self.getReviews().iteritems():
			uid = r.getUID()
			
			if userRate.has_key(uid):
				userRate[uid] += 1
			else:
				userRate[uid] = 1
		return userRate

	def __businessRating__(self):
		bRate = {}
		for rid,r in self.getReviews().iteritems():
			bid = r.getBID()
			
			if bRate.has_key(bid):
				bRate[bid] += 1
			else:
				bRate[bid] = 1
		return bRate

	def __StatisticRating__(self):
		"""
		Statistic the number of businesses that each user rated.
		"""
		userRate = {}
		businessRate = {}

		for rid,r in self.getReviews().iteritems():
			uid = r.getUID()
			bid = r.getBID()
			
			if userRate.has_key(uid):
				userRate[uid] += 1
			else:
				userRate[uid] = 1

			if businessRate.has_key(bid):
				businessRate[bid] += 1
			else:
				businessRate[bid] = 1

		return userRate,businessRate

	def statistcInfo(self):
		string = "===========Statistic Information===========\n"
		string += "total # of reivews: %d\n" % self.getReviewCount()
		string += "total # of users: %d\n" % len(self.getUsers())
		string += "total # of businesses: %d\n" % len(self.getBusinesses())
		string += "average # of reviews user has: %d\n" % (self.getReviewCount()*1.0/len(self.getUsers()))
		string += "average # of reviews business has: %d\n" % (self.getReviewCount()*1.0/len(self.getBusinesses()))
		return string