from DataCenter import DataCenter

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

    dataCenter = DataCenter()
    dataCenter.loadAll(upath,bpath,rpath,cpath)

    print len(dataCenter.getUserData())
    print len(dataCenter.getBusinessData())
    print len(dataCenter.getReviewData())
    print len(dataCenter.getCheckInData())