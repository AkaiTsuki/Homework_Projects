import json
from Beans import User
from Beans import Review
from Beans import Business
from Beans import CheckIn

class JSONParser(object):
	"""docstring for JSONParser"""
	def __init__(self):
		super(JSONParser, self).__init__()


	def parse(self,path):
		"""
		Given a json file path, returns a list of json object.
		"""
		lst = []
		with open(path) as f:
			for line in f:
				obj = json.loads(line);
				lst.append(obj)
		return lst

class JSONUserParser(JSONParser):
	"""docstring for JSONUserParser"""
	def __init__(self):
		super(JSONUserParser, self).__init__()

	def getUsers(self,path):
		"""
		Given the path of json file, returns a list of users
		"""
		jsonObjs = self.parse(path)
		users = {}
		for obj in jsonObjs:
			user = self.getUser(obj)
			users[user.id] = user
		return users
	
	def getUser(self,obj):
		"""
		Given a json object, 
		returns a user object according to the information in json
		"""
		return User(obj['user_id'],obj['name'],obj['average_stars'],\
                obj['review_count'],obj['votes']['funny'],\
                obj['votes']['useful'],obj['votes']['cool'])

class JSONReviewParser(JSONParser):
	"""docstring for JSONReviewParser"""
	def __init__(self):
		super(JSONReviewParser, self).__init__()

	def getReviews(self,path):
		"""
		Given the path of json file, returns a list of reviews
		"""
		jsonObjs = self.parse(path)
		reviews = {}
		for obj in jsonObjs:
			review = self.getReview(obj)
			key = review.getKey()
			reviews[key] = review
		return reviews

	def getReview(self,obj):
		return Review(obj['review_id'],obj['user_id'],obj['business_id'],\
			obj['stars'],obj['date'],obj['votes']['funny'],obj['votes']['useful'],obj['votes']['cool'],\
			obj['text'])

class JSONBusinessParser(JSONParser):
	"""docstring for JSONBusinessParser"""
	def __init__(self):
		super(JSONBusinessParser, self).__init__()

	def getBusinesses(self,path):
		jsonObjs = self.parse(path)
		dic = {}
		for obj in jsonObjs:
			b=self.getBusiness(obj)
			dic[b.id] = b
		return dic
	
	def getBusiness(self,obj):
		return Business(obj['business_id'],obj['full_address'],obj['open'],obj['categories'],\
			obj['city'],obj['review_count'],obj['name'],obj['neighborhoods'],obj['longitude'],\
			obj['latitude'],obj['state'],obj['stars'])

class JSONCheckInParser(JSONParser):
	"""docstring for JSONCheckInParser"""
	def __init__(self):
		super(JSONCheckInParser, self).__init__()
	
	def getCheckIns(self,path):
		jsonObjs = self.parse(path)
		dic={}
		for obj in jsonObjs:
			c = self.getCheckIn(obj)
			dic[c.businessId]=c
		return dic

	def getCheckIn(self,obj):
		checkIn = CheckIn(obj['business_id'])
		checkInInfo = obj['checkin_info']
		for k,v in checkInInfo.iteritems():
			time,day = k.split('-')
			checkIn.addRecord(int(day),int(time),v)
		return checkIn
