from DataCenter import DataCenter
from DataUtil import *

if __name__ == '__main__':
    """
    upath = 'userTest.json'
    bpath = 'businessTest.json'
    rpath = 'reviewTest.json'
    cpath = 'checkinTest.json'
    """
    upath = 'yelp_training_set_user.json'
    bpath = 'yelp_training_set_business.json'
    rpath = 'yelp_training_set_review.json'
    cpath = 'yelp_training_set_checkin.json'

    # Initialize the data center object
    dataCenter = DataCenter()
    # load all json data to the data center
    dataCenter.loadAll(upath,bpath,rpath,cpath)
    
    # get data from data center
    # the following 4 data are all dictionary
    users = dataCenter.getUserData()
    business = dataCenter.getBusinessData()
    reviews = dataCenter.getReviewData()
    checkIn = dataCenter.getCheckInData()

    print len(users)
    print len(business)
    print len(reviews)
    print len(checkIn)

    print getUserArray(users)[0]