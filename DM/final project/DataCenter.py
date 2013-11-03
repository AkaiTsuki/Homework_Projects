from JSONParser import *

class DataCenter(object):
	"""Store all data in this class"""
	def __init__(self):
		super(DataCenter, self).__init__()
		# a dictionary that saves all business record
		# where business_id is the key and business bean
		# is the value
		self.business = {}

		# a dictionary that saves all users record
		# where user_id is the key and user bean
		# is the value
		self.users = {}

		# a dictionary that saves all reivew record
		# where user_id + business_id is the key and review bean
		# is the value
		self.review = {}

		# a dictionary that saves all checkin record
		# where business_id is the key and checkin bean
		# is the value
		self.checkin = {}
	
	def loadData(self,table,path):
		"""
		Load the json data according to the type of table
		"""
		if table is 'User':
			self.loadUsers(path)
		elif table is 'Business':
			self.loadBusiness(path)
		elif table is 'Review':
			self.loadReviews(path)
		elif table is "CheckIn":
			self.loadCheckIn(path)
		else:
			raise Exception('Invalid talbe, data not existed!')

	def loadAll(self,user,business,review,checkin):
		"""
		Load all json data
		@param user : the path of user json file 
		@param business : the path of business json file 
		@param review : the path of review json file 
		@param checkin : the path of checkin json file
		"""
		print 'Loading user info...',
		self.loadUsers(user)
		print 'done'
		print 'Loading business info...',
		self.loadBusiness(business)
		print 'done'
		print 'Loading review info...',
		self.loadReviews(review)
		print 'done'
		print 'Loading checkin info...',
		self.loadCheckIn(checkin)
		print 'done'

	def loadBusiness(self,path):
		"""
		Load business data from json file
		"""
		parser = JSONBusinessParser()
		self.business=parser.getBusinesses(path)

	def loadUsers(self,path):
		"""
		Load user data from json file
		"""
		p = JSONUserParser()
		self.users=p.getUsers(path)

	def loadReviews(self,path):
		"""
		Load review data from json file
		"""
		p = JSONReviewParser()
		self.reviews=p.getReviews(path)

	def loadCheckIn(self,path):
		"""
		Load checkin data from json file
		"""
		p = JSONCheckInParser()
		self.checkin = p.getCheckIns(path)

	def getUserData(self):
		return self.users

	def getBusinessData(self):
		return self.business

	def getReviewData(self):
		return self.reviews

	def getCheckInData(self):
		return self.checkin