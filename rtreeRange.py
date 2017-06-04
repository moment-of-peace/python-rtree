'''
rtreeRange.py
Arguements: -d <datasetFile>, -q <queryFile>, -b <Bvalue>
Author: Yi Liu
Algorithm to solve range queries
'''

# standard libraries
import time
import getopt
import sys
# private libraries
import rtreeBuilder
import Rtree
import scanRange

# range-query algorithm
def rangeQuery(node, queryRange):
    result = 0
    if isinstance(node, Rtree.Leaf):
        # report all covered points in this leaf
        result = searchLeaf(node, queryRange)
    else:
        # search all children which are intersected recursively
        for child in node.childList:
            if isIntersect(child.range, queryRange):
                result += rangeQuery(child, queryRange)
    
    return result

# retrieve all points covered by a rectangle in a leaf
def searchLeaf(leaf, ranges):
    # number of points covered by the query range
    result = 0
    for point in leaf.childList:
        if point.x<ranges[0] or point.x>ranges[1] or point.y<ranges[2] or point.y>ranges[3]:
            pass
        else:
            result += 1
        
    return result

# determine whether two rectangles are intersected
def isIntersect(range1, range2):
    if range1[0]>range2[1] or range1[1]<range2[0] or range1[2]>range2[3] or range1[3]<range2[2]:
        return False
    else:
        return True

# answer all queries using range-query algorithm with a given r-tree
def answerRangeQueries(root, queries):
    resultFile = 'resultRange.txt'
    # start time
    timeStart = time.time()
    f = open(resultFile, 'wt')
    for query in queries:
        result = rangeQuery(root, query)
        f.write(str(result) + '\r\n')
    # the end time
    timeEnd = time.time()
    f.close()
    i = len(queries)
    print('Range Queries finished. Average time: ' + str((timeEnd-timeStart)/i))


def main():
    datasetFile = 'dataset.txt'
    queryFile = 'queriesRange.txt'
    Bvalue = None
    
    # parse arguments
    options,args = getopt.getopt(sys.argv[1:],"d:q:b:")
    for opt, para in options:
        if opt == '-d':
            datasetFile = para
        if opt == '-q':
            queryFile = para
        if opt == '-b':
            Bvalue = int(para)
    
    # build r-tree
    root = rtreeBuilder.buildRtree(datasetFile, Bvalue)
    rtreeBuilder.checkRtree(root)
    # answer range queries
    queries = scanRange.readRanges(queryFile)
    answerRangeQueries(root, queries)

if __name__ == '__main__':
    main()
