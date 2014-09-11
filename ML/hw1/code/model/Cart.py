# Process for building a decision tree:
# - Read training & test dataset from csv file:
#
#   reader = CsvFileReader(path)
#   dataset = reader.read()
#
# - Normalize the data on each feature except the label
#
#   normalizer = Normalizer()
#   min_max_scaler = MinMaxScaler(cols)
#   normalizer.normalize(dataset,min_max_scaler)
#
# - Build decision tree:
#   
#   cart = Cart(normalized_dataset)
#   model = cart.build()
#
# - Predict the test data:
#   
#   labels = model.predict(test_dataset)
#   
# - Validate the model
#   

import numpy as np
from model.TreeNode import TreeNode

flag = 1

def debug(info):
    if flag == 1:
        print info

class Cart:
    def __init__(self, data, features, label, el):
        '''
        @param narray data training dataset
        @param narray features a list of column index represents the feature column in dataset
        @param int label the column index of label column 
        @param el expected level
        '''
        self.data = self.sortData(data, label)
        self.features = features
        self.label = label
        self.EL = el
        
    def sortData(self, data, col):
        '''
        Sort the rows in dataset based on the given column order
        @param narray data dataset to be sorted
        @param int col column index
        '''
        return data[data[:,col].argsort()]

    def findAllSplitPoint(self, arr):
        '''
        Find all split point of given array
        @param narray arr a array that will find all split point from
        @return array a array of split point
        '''
        splits = []
        for i in range(1,len(arr)):
            split = (arr[i-1] + arr[i]) / 2.0
            splits.append(split)
        return splits

    def getMse(self, arr):
        '''
        Given a array find the mean square error of the array
        @param narray arr the given array
        @return float the mse
        '''
        mse = 0.0
        if len(arr) == 0:
            return mse

        m = arr.mean()
        for e in arr:
            mse += (e - m) * (e - m)
        #return mse / len(arr)
        return mse

    def tryAllSplits(self, features, labels):
        '''
        Loop through all split point in the given array, find the best
        split which has the minimum mse
        @param narray features a feature array that will be loop through to find the split
        @param narray labels the labels column
        @return the index that represents the split point
                the split value 
                the minimum mse
        '''
        #print self.findAllSplitPoint(features)
        minMse = float("inf")
        split = 0
        splitVal = 0
        for i in range(1,len(features)):
            if features[i-1] == features[i]:
                continue
            left = labels[:i]
            right = labels[i:]
            mse = self.getMse(left) + self.getMse(right)
            if minMse > mse:
                minMse = mse
                split = i
                splitVal = (features[i-1] + features[i]) /2.0
        return split, splitVal, minMse

    def findSplit(self, data, features, label):
        mse = float('inf')
        retF = None
        retVal = None
        for f in features:
            featureAndLabel = data[:,[f,label]]
            sortedFL = self.sortData(featureAndLabel, 0)
            s,v,m = self.tryAllSplits(sortedFL[:,0], sortedFL[:,1])
            if m < mse:
                mse = m
                retF = f
                retVal = v

        return retF, retVal, mse

    def build(self):
        return self.buildTree(self.data, self.features, self.label, 20.0, "root", 0, self.EL)

    def buildTree(self, data, features, label, E, fromPath, level, EL):
        debug("\n")
        debug("data size: "+ str(len(data)) +" features: " + str(features)+" from: "+ fromPath)

        if len(data) == 0:
            return None
        # Only one data
        if len(data) == 1:
            return TreeNode(None, None, label, data[0][label], level)

        # less than expected error rate
        labels = data[:,label]
        # if self.getMse(labels) <= E:
        #     debug("meet error rate: "+str(len(labels)) +" "+ str(labels.mean()))
        #     return TreeNode(None, None, label, labels.mean(),level)

        # greeter than certain level
        if level >= EL:
            return TreeNode(None,None,label, labels.mean(),level)

        # No more features
        if len(features) == 0:
            return TreeNode(None, None, label, labels.mean(),level)

        feature, splitVal, mse = self.findSplit(data, features, label)
        debug("findSplit(feature, splitVal, mse) " + str((feature, splitVal, mse)))
        
        if feature == None and splitVal == None:
            return TreeNode(None, None, label, labels.mean(),level)

        #print "Feature, splitVal: ", feature, splitVal    
        leftData = data[data[:,feature] <= splitVal]
        rightData = data[data[:,feature] > splitVal]
        debug("leftData : rightData = " + str((len(leftData), len(rightData))))

        features.remove(feature)

        n = TreeNode(self.buildTree(leftData, features, label, E, "left", level+1,EL), self.buildTree(rightData, features, label, E, "right", level+1,EL), feature, splitVal, level)
        
        return n;

    def predictOnSingleTuple(self, t, root):
        while root is not None and root.feature != self.label:
            if t[root.feature] < root.val:
                root = root.left
            else:
                root = root.right
        return root.val

    def predict(self, test, node):
        pred = []
        for t in test:
            pred.append(self.predictOnSingleTuple(t,node))
        return pred
