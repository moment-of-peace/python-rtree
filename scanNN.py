'''
scanNN.py
Arguements: -d <datasetFile>, -q <queryFile>
Author: Yi Liu
Scan method for a set of nearest neighbor queries
'''
# standard libraries
import sys
import time
import getopt
# private libraries
import scanRange

# read all queries
def readNn(queryFile):
    fileHandle = open(queryFile, 'rt')
    queries = []
    nextLine = fileHandle.readline()
    
    while nextLine != '':
        queries.append(scanRange.getQuery(nextLine))
        nextLine = fileHandle.readline()
    
    fileHandle.close()
    return queries

# the distance between point and query
def getDis(point, query):
    return (point[1]-query[0])**2 + (point[2]-query[1])**2

# answer all queries using scanning method
def scanNNQueries(points, queries):
    # the output file
    resultFile = 'resultNN-scan.txt'
    f = open(resultFile, 'wt')
    # start time
    timeStart = time.time()
    # answer each query
    for query in queries:
        distance = getDis(points[0], query)
        results = [points[0]]
        # scan each point
        for j in range(1, len(points)):
            newDis = getDis(points[j], query)
            if newDis < distance:
                results.clear()
                results.append(points[j])
                distance = newDis
            elif newDis == distance:
                results.append(points[j])
        # write results
        for result in results:
            f.write(str(result[0]) + ' ')
            
        f.write('\r\n')
    
    f.close()
    # end time
    timeEnd = time.time()
    i = len(queries)
    print('Scan NN queries finished. Average time: ' + str((timeEnd-timeStart)/i))

def main():
    datasetFile = 'dataset.txt'
    queryFile = 'queriesNN.txt'
    
    # parse arguements
    options,args = getopt.getopt(sys.argv[1:],"d:q:")
    for opt, para in options:
        if opt == '-d':
            datasetFile = para
        if opt == '-q':
            queryFile = para
    
    # scan the data-set and answer range queries
    points = scanRange.readPoints(datasetFile)
    queries = readNn(queryFile)
    scanNNQueries(points, queries)

if __name__ == '__main__':
    main()
