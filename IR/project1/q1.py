from pageRank import WebGraph
from pageRank import PageRank
import sys

def q1(path):
    """docstring for q1"""
    graph = WebGraph(path)
    graph.parse()
    graph.statistic()
    ranker = PageRank(graph)
    ranker.rank("q1")



if __name__ == '__main__':
    f = sys.argv[1]
    q1(f)
