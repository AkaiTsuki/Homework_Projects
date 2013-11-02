from pageRank import WebGraph
from pageRank import PageRank
import sys

def q2(path):
    """docstring for q2"""
    graph = WebGraph(path)
    graph.parse()
    graph.statistic()
    ranker = PageRank(graph)
    ranker.rank("q2")
    sorted_ranks = ranker.sort(ranker.ranks)
    sorted_inlink = ranker.sort(ranker.graph.inlinkDict)
    print ""
    print "Top 50 pages sorted by rank"
    ranker.printTopRankInfo(sorted_ranks[:50])
    print ""
    print "Top 50 pages sorted by inlink:"
    ranker.printTopRankInfo(sorted_inlink[:50])


if __name__ == '__main__':
    f = sys.argv[1]
    q2(f)
