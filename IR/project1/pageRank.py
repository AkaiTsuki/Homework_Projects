import math
import operator

class WebGraph(object):
    """docstring for WebGraph"""
    def __init__(self, path):
        super(WebGraph, self).__init__()
        # graph file path
        self.path = path
        # adjacent list for graph
        self.adjlist = {}
        # saves number of outlinks for all nodes
        self.allNodesDict = {}
        # saves number of inlinks for all nodes
        self.inlinkDict = {}

    def parse(self):
        """
        Read the file in given path, parse the file to graph adjacent list
        """
        #log('start parse from file...')
        with open(self.path) as f:
            for line in f:
                l = line.strip()
                if len(l)==0:
                    continue

                nodes = line.strip().split(' ')
                if nodes[0] not in self.adjlist:
                    self.adjlist[nodes[0]] = nodes[1:]
                else:
                    self.adjlist[nodes[0]] += nodes[1:]
        #log('finish parse!')

    def totalNodes(self):
        """
        Returns the total number of nodes in graph
        """
        return len(self.adjlist)

    def allNodes(self):
        """
        Returns a list of all nodes in graph
        """
        return self.adjlist.keys()

    def statistic(self):
        """
        Statistic the number of outlinks for each node
        """
        #log('start statistic outlinks for all nodes...')
        
        self.allNodesDict = dict.fromkeys(self.adjlist,0)
        for key,val in self.adjlist.items():
            self.inlinkDict[key] = len(val)
            for node in val:
                self.allNodesDict[node] += 1
        
        #log('finish statistic!')

    def sinkNodes(self):
        """
        Returns a list of nodes that has no outlink
        """
        result = []
        for key,val in self.allNodesDict.items():
            if(val==0):
                result.append(key)
        return result

    def linkTo(self, node):
        """
        @param node:   the target node
        @type  node:  String
        
        @return:  the set of pages that link to page p
        @rtype :  list of string
        
        """
        return self.adjlist[node]


class PageRank(object):
    """docstring for PageRank"""
     # maximum iteration times
    (MAX_ITERATION) = (100)
    def __init__(self, graph):
        super(PageRank, self).__init__()
        # Web graph
        self.graph = graph
        # rank value for each page
        self.ranks = self.pagerank()
        # counter for iteration time
        self.counter = 0
               
    def pagerank(self):
        """
        Construct a list of ranks for each page according to the web graph,
        Initial the rank value to 1/N where N is the total number of nodes
        """
        return dict.fromkeys(self.graph.adjlist,1.0/self.graph.totalNodes());

    def rank(self,calcType,damp=0.85):
        """
        Iterately caculate the rank for each page, stop until converged
        """
        # all pages
        pages = self.graph.allNodes()
        # total number of pages
        N = len(pages)
        # all sink nodes
        sinks = self.graph.sinkNodes()
        # reset the counter
        self.counter = 0
        # records of perplexity for last 4 iterations
        perplexityList = [None,None,None,None]
        
        while not self.isFinished(perplexityList,calcType):
            perpl = self.perplexity()

            # print perplexity for q2
            if calcType == "q2":
                print perpl

            perplexityList[self.counter % 4] = perpl
            sinkPR = 0
            newPR = {}

            for p in sinks:
                sinkPR +=self.ranks[p]

            for p in pages:
                newPR[p] = (1-damp)/N
                newPR[p] += damp * sinkPR / N
                for q in self.graph.linkTo(p):
                    newPR[p] += damp * self.ranks[q] / self.graph.allNodesDict[q]

            for p in pages:
                self.ranks[p]=newPR[p]

            self.counter += 1

    def sort(self,dictionary):
        """docstring for sort"""
        return sorted(dictionary.iteritems(), key=operator.itemgetter(1),reverse=True)

    def perplexityFinished(self,perplexities):
        """docstring for perplexityFinshed"""
        #print perplexities

        if None in perplexities:
            return False
        p0 = int(perplexities[0])
        p1 = int(perplexities[1])
        p2 = int(perplexities[2])
        p3 = int(perplexities[3])
        return p0==p1 and p1==p2 and p2==p3 and (not p0==None)

    def iterationFinish(self):
        """docstring for fname"""
        if self.counter==1 or self.counter==10 or self.counter==100:
            print "iteration after ",self.counter
            print self.ranks
        return self.counter >= PageRank.MAX_ITERATION
    
    def isFinished(self,perplexities,calcType):
        """docstring for isFinished"""
        if calcType=="q2":
            return self.perplexityFinished(perplexities)
        else:
            return self.iterationFinish()


    def perplexity(self):
        entropy = self.entropy()
        return 2.0**entropy

    def entropy(self):
        """docstring for entropy"""
        entropy = 0
        for key,val in self.ranks.items():
            entropy += val*math.log(val,2)
        return -1.0 * entropy


    def printTopRankInfo(self,ranks):
        """docstring for printRanks"""
        for k,v in ranks:
            print k,v


def log(msg):
    print msg

def printList(turples):
    for k,v in turples:
        print k,v


