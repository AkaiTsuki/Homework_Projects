class User(object):
	"""docstring for User"""
	def __init__(self, id,name,avgStar,reviewCount,funny,useful,cool):
		super(User, self).__init__()
		self.id = id
		self.name = name
		self.avgStar = avgStar
		self.reviewCount = reviewCount
		self.funny=funny
		self.useful=useful
		self.cool=cool

	def __str__(self):
		return "[%s, %s, %f, %d, %d, %d, %d]"\
		 % (self.id,self.name,self.avgStar,self.reviewCount,self.funny,self.useful,self.cool)

	def __repr__(self):
		return "[%s, %s, %f, %d, %d, %d, %d]"\
		 % (self.id,self.name,self.avgStar,self.reviewCount,self.funny,self.useful,self.cool)
		
class Review(object):
	"""docstring for Review"""
	def __init__(self, reviewId,userId,businessId,stars,date,funny,useful,cool,text):
		super(Review, self).__init__()
		self.reviewId = reviewId
		self.userId=userId
		self.businessId=businessId
		self.stars=stars
		self.date=date
		self.funny=funny
		self.useful=useful
		self.cool=cool
		self.text=text

	def getKey(self):
		return "%s%s" % (self.userId,self.businessId)

	def __str__(self):
		return "[%s, %s, %s, %d, %s, %d, %d, %d, %s]"\
		 % (self.reviewId,self.userId,self.businessId,self.stars,\
		 	self.date,self.funny,self.useful,self.cool,self.text)
		
	def __repr__(self):
		return "[%s, %s, %s, %d, %s, %d, %d, %d, %s]"\
		 % (self.reviewId,self.userId,self.businessId,self.stars,\
		 	self.date,self.funny,self.useful,self.cool,self.text)

class Business(object):
	"""docstring for Business"""
	def __init__(self, id,address,isOpen,categories,city,reviewCount,name,neighbor,longitude,latitude,state,stars):
		super(Business, self).__init__()
		self.id = id
		self.address=address
		self.isOpen=isOpen
		self.categories=categories
		self.city=city
		self.reviewCount=reviewCount
		self.name = name
		self.neighbor=neighbor
		self.longitude=longitude
		self.latitude=latitude
		self.state=state
		self.stars=stars

	def __repr__(self):
		return "[%s, %s, %i, %s, %s, %d, %s, %s, %f, %f, %s, %s]"\
		 % (self.id,self.address,self.isOpen,self.categories,\
		 	self.city,self.reviewCount,self.name,self.neighbor,self.longitude,self.latitude,self.state,self.stars)

	def __str__(self):
		return "[%s, %s, %i, %s, %s, %d, %s, %s, %f, %f, %s, %s]"\
		 % (self.id,self.address,self.isOpen,self.categories,\
		 	self.city,self.reviewCount,self.name,self.neighbor,self.longitude,self.latitude,self.state,self.stars)

class CheckIn(object):
	"""
	CheckIn has a business id and a list of check in record.
	A CheckInRecord is a list [int,int,int] where represents
	[day,time,check in count].
	"""
	def __init__(self,businessId):
		super(CheckIn, self).__init__()
		self.businessId = businessId
		self.checkInRecord = []

	def addRecord(self,day,time,count):
		self.checkInRecord.append([day,time,count])
	
	def totalCheckIn(self):
		"""
		Returns the total number of check in
		"""
		total = 0
		for record in self.checkInRecord:
			total += record[2]
		return total

	def totalCheckInOnDay(self,day):
		"""
		returns the total number of check in of a given day
		"""
		total = 0
		for record in self.checkInRecord:
			if record[0] is day:
				total += record[2]
		return total

	def totalCheckInOnTime(self,time):
		"""
		returns the total number of check in of a given time
		"""
		total = 0
		for record in self.checkInRecord:
			if record[1] is time:
				total += record[2]
		return total

	def __str__(self):
		return "%s, %s" % (self.businessId,self.checkInRecord)

	def __repr__(self):
		return "%s, %s" % (self.businessId,self.checkInRecord)
