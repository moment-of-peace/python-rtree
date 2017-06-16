'''
rtreeNN.py
Arguements: -d <datasetFile>, -q <queryFile>, -b <Bvalue>
Author: Yi Liu
Best First algorithm to solve nearest neighbor queries
'''

# standard libraries
import time
import getopt
import sys
# private libraries
import rtreeBuilder
import Rtree
import scanNN

# the nearest distance
global distance
# the nearest neighbors
global results

# the nearest distance from a query point to a node
def nDis(node, query):
    dis = 0
    # component on x axis
    if query[0] < node.range[0]:
        dis += (node.range[0]-query[0])**2
    elif query[0] > node.range[1]:
        dis += (query[0]-node.range[1])**2
    # component on y axis
    if query[1] < node.range[2]:
        dis += (node.range[2]-query[1])**2
    elif query[1] > node.range[3]:
        dis += (query[1]-node.range[3])**2
    # if the query point is inside of the node, return 0
    return dis

# in a leaf, find all points which have the least distance from the query point
def getNN(leaf, query):
    global distance
    global results
    
    for point in leaf.childList:
        newDis = (point.x-query[0])**2 + (point.y-query[1])**2
        if newDis < distance:
            distance = newDis
            results.clear()
            results.append(point)
        elif newDis == distance:
            results.append(point)

# answer a NN query using "Best First" algorithm
def bestFirst(tupleList, query):
    global distance

    if isinstance(tupleList[0][1], Rtree.Branch):
        node = tupleList[0][1]
        # remove the first element in the tuple list
        del tupleList[0]
        # add all children of the first node to the tuple list
        for child in node.childList:
            tupleList.append((nDis(child, query), child))
        # sort the tuple list by distance
        tupleList = sorted(tupleList, key=lambda t:t[0])
    elif isinstance(tupleList[0][1], Rtree.Leaf):
        node = tupleList[0][1]
        # remove the first element in the tuple list
        del tupleList[0]
        getNN(node, query)
        
    # in this case, the NN has been found
    if distance < tupleList[0][0]:
        return
    # implement Best First algorithm resursively
    bestFirst(tupleList, query)

# answer all the queries using "Best First" algorithm with a given r-tree
def answerNnQueries(root, queries):
    global distance
    global results
    
    resultFile = 'resultNN.txt'
    # the start time
    timeStart = time.time()
    f = open(resultFile, 'wt')
    for query in queries:
        # initialize global variables
        distance = float('inf')
        results = []
        # answer query
        bestFirst([(0, root)], query)
        for result in results:
            f.write(str(result.ident) + ' ')
        f.write('\r\n')
    # the end time
    timeEnd = time.time()
    f.close()
    i = len(queries)
    print('NN Queries finished. Average time: ' + str((timeEnd-timeStart)/i))

def main():
    datasetFile = 'dataset.txt'
    queryFile = 'queriesNN.txt'
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
    # answer NN queries
    queries = scanNN.readNn(queryFile)
    answerNnQueries(root, queries)
    
if __name__ == '__main__':
    main()
