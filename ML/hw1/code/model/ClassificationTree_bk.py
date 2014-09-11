__author__ = 'jiachiliu'

'''
Entropy based classification tree, this is a binary D.T

Denote:
D: is the training dataset
F: is the list of features
C: is the list of class labels
H(S) is the entropy on dataset S

STEPS to create a D.T:
METHOD: buildTree(D,F):
1. create a node N
2. if tuples in D are all same label:
    return N as a leaf labeled with C_i
3. if F is empty:
    return N as a leaf labeled with the majority of class in D
4. apply feature_split_method(D, F) to find the best splitting_criterion
5. Label N with splitting_criterion, remove the splitting feature from F
6. Split D into D_i based on splitting_criterion, for binary tree, it will be D_1 and D_2
7. for each data partition D_i:
    if D_i is empty:
        attach a leaf node label with majority class in D to N
    else:
        attach the return node from buildTree(D_i,F) as child of N

STEPS to find best splitting_criterion:
METHOD feature_split_method(D, F):
Denote the splitting_criterion be a tuple (f,v)
Denote (Value, Information_gain) as (v,i)

* (bestf,bestv) = (None, None)
* for each f in F:
    (v,i) = findBestSplitOnFeature(D,f)
    if maxI < i:
        maxI = i
        bestv = v
        bestf = f
* return (bestf,bestv)

STEPS to find best split on feature
METHOD findBestSplitOnFeature(D,F):

Two types of feature: Nominal and Numeric

Split Measuring Method: Information Gain
Entropy:
H(D) = -sum(p*log2(p))
H(D,A) = sum((D_j/D)*H(D_j))
I(A) = H(D) - H(D,A)
The maximum of I(A) is the best splitting feature

For Nominal Data:
Since we use binary tree,
denote V as all unique value for feature f

for each v_i in V:
    D can be split to two partition, D_1 and D_2 where
    D_1 is all data point that f = v_i
    D_2 is all data point that f != v_i
    use the split measuring method to find the best v_i to split
return (v_i, I(A))

For Numeric feature:
* sort the feature
* for each split_point v_i where v_i = (v_i+v_i-1) / 2:
    D can be split to two partition, D_1 and D_2 where
    D_1 is all data point that f <= v_i
    D_2 is all data point that f > v_i
    use the split measuring method to find the best v_i to split
return (v_i, I(A))

METHOD: find_all_split_point(D, f):
    if f is nominal:
        return all unique values in column f
    if f is numeric:
        return [v for v = (v_i + v_i-1)/2]

'''

import numpy as np
from model.TreeNode import TreeNode


class ClassificationTree:
    def __init__(self, D, features, label, featureTypes, maxSize):
        self.l = label
        self.labels = self.findAllSplitPointOnNominal(D, label)
        self.D = D
        self.features = features
        self.featureTypes = featureTypes
        self.MAX_SIZE = maxSize
        print "init: "
        print "all labels: ", self.labels
        print "max_level: ", self.MAX_SIZE
        print "label_index: ", self.l
        print ""

    def build(self):
        return self.buildTree(self.D, self.features, self.featureTypes, 0)

    def buildTree(self, D, features, featureTypes, level):
        print "Data size: ", len(D), " features: ", features, "level: ", level

        if self.isAllSameLabel(D):
            return TreeNode(None, None, self.l, D[:, self.l][0], level)

        if len(features) == 0:
            return TreeNode(None, None, self.l, self.majority(D), level)

        if level > self.MAX_SIZE:
            return TreeNode(None, None, self.l, self.majority(D), level)

        (f, s) = self.findBestSplitFeature(D, features, featureTypes)
        print "Best split feature: ", (f, s)

        (left, right) = self.splitData(D, f, False, s)
        print "(left, right) = ", (len(left), len(right))

        features.remove(f)

        if len(left) == 0:
            leftTree = TreeNode(None, None, self.l, self.majority(D), level)
        else:
            leftTree = self.buildTree(left, features, featureTypes, level + 1)

        if len(right) == 0:
            rightTree = TreeNode(None, None, self.l, self.majority(D), level)
        else:
            rightTree = self.buildTree(right, features, featureTypes, level + 1)

        return TreeNode(leftTree, rightTree, f, s, level)

    def isAllSameLabel(self, D):
        labels = D[:, self.l]
        l = labels[0]
        for v in labels:
            if l != v:
                return False
        return True

    def majority(self, D):
        labels = D[:, self.l]
        maxCount = 0
        l = labels[0]

        for v in self.labels:
            c = len(labels[labels == v])
            if maxCount < c:
                maxCount = c
                l = v
        return l

    def findBestSplitFeature(self, D, features, featureTypes):
        bestFeature = None
        bestSplitValue = None
        maxIA = 0.0

        for f in features:
            print "findBestSplitFeature on feature ", f
            # featureType = featureTypes[f]
            (bestSplit, ia) = self.findBestSplitOnFeature(D, f, False)
            print "result: (bestSplit, ia)", (bestSplit, ia)
            if maxIA <= ia:
                maxIA = ia
                bestFeature = f
                bestSplitValue = bestSplit
        print "findBestSplitFeature: ", (bestFeature, bestSplitValue)
        return bestFeature, bestSplitValue

    def findBestSplitOnFeature(self, D, f, isNominal):
        splits = self.findAllSplitPoint(D, f, isNominal)
        print "total splits ", len(splits)
        H_D = self.entropy(D, self.l, self.labels)
        maxIA = 0.0
        bestSplit = None
        for split in splits:
            left, right = self.splitData(D, f, isNominal, split)
            if len(left) == 0 or len(right) == 0:
                print "findBestSplitOnFeature: split on", split, ": (left,right)=", (len(left), len(right))

            H_left = ((len(left) * 1.0) / len(D)) * self.entropy(left, self.l, self.labels)
            H_right = ((len(right) * 1.0) / len(D)) * self.entropy(right, self.l, self.labels)
            H_A = H_left + H_right
            I_A = H_D - H_A
            if I_A <= 0:
                print "I_A <= 0"
            if maxIA <= I_A:
                maxIA = I_A
                bestSplit = split
                # print "New best split point(bestSplit, maxIA): ", bestSplit, maxIA
        print "Best split point(bestSplit, maxIA): ", bestSplit, maxIA
        return bestSplit, maxIA

    def entropy(self, D, l, labels):
        info = 0.0
        T = len(D) * 1.0
        if T == 0:
            return info

        for val in labels:
            D_val = D[D[:, l] == val]
            T_val = len(D_val)
            if T_val == 0:
                info += 0
            else:
                info += -(T_val / T) * np.log2(T_val / T)
        return info

    def splitData(self, D, f, isNominal, split):
        if isNominal:
            return D[D[:, f] == split], D[D[:, f] != split]
        else:
            return D[D[:, f] <= split], D[D[:, f] > split]

    def findAllSplitPoint(self, D, f, isNominal):
        if isNominal:
            return self.findAllSplitPointOnNominal(D, f)
        else:
            return self.findAllSplitPointOnContinue(D, f)

    def findAllSplitPointOnNominal(self, D, f):
        return np.unique(D[:, f])

    def findAllSplitPointOnContinue(self, D, f):
        arr = np.sort(D[:, f])
        splits = []
        for i in range(1, len(arr)):
            if arr[i - 1] == arr[i]:
                continue
            split = (arr[i - 1] + arr[i]) / 2.0
            splits.append(split)
        return np.array(splits)

    def sortData(self, data, col):
        '''
        Sort the rows in dataset based on the given column order
        @param narray data dataset to be sorted
        @param int col column index
        '''
        return data[data[:, col].argsort()]

    def predictOnSingleTuple(self, t, root):
        while root is not None and root.feature != self.l:
            if t[root.feature] <= root.val:
                root = root.left
            else:
                root = root.right
        return root.val

    def predict(self, test, node):
        pred = []
        for t in test:
            pred.append(self.predictOnSingleTuple(t, node))
        return pred