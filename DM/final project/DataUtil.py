def getUserArray(userDict):
	"""
	Given a user dictionary, Returns a list of arrays that
	each array contains all user information except id and name.
	"""
	array = []
	for k,v in userDict.iteritems():
		user = [v.avgStar,v.reviewCount,v.funny,v.useful,v.cool]
		array.append(user)
	return array