'''
scanRange.py
Arguements: -d <datasetFile>, -q <queryFile>
Author: Yi Liu
Scan method for a set of range queries
'''

import sys
import time
import getopt

# read a single point from a line of text
def getPoint(nextLine):
    # split the string with whitespace
    content = nextLine.strip('\n').split(' ')
    while content.count('') != 0:
        content.remove('')
    # point id
    ident = int(content[0])
    #point id and coordinates
    x = float(content[1])
    y = float(content[2])
    
    return [ident, x, y]

# read points from data set
def readPoints(datasetFile):
    fileHandle = open(datasetFile, 'rt')
    points = []
    nextLine = fileHandle.readline()
    nextLine = fileHandle.readline()
    
    while nextLine != '':
        points.append(getPoint(nextLine))
        nextLine = fileHandle.readline()
    
    fileHandle.close()
    return points

# read a single query from a line of text
def getQuery(nextLine):
    # split the string with whitespace
    content = nextLine.strip('\n').split(' ')
    while content.count('') != 0:
        content.remove('')
    result = []
    for s in content:
        result.append(float(s))
    
    return result

# sort a single query so that x1<=x1', y1<=y1'
def sortQuery(result):
    if result[0]>result[1]:
        temp = result[0]
        result[0] = result[1]
        result[1] = temp
    if result[2]>result[3]:
        temp = result[2]
        result[2] = result[3]
        result[3] = temp
    return result

# read all range queries
def readRanges(queryFile):
    fileHandle = open(queryFile, 'rt')
    queries = []
    nextLine = fileHandle.readline()
    
    while nextLine != '':
        query = getQuery(nextLine)
        queries.append(sortQuery(query))
        nextLine = fileHandle.readline()
    
    fileHandle.close()
    return queries

# determine whether a point is cover by a query(a rectangular)
def isIntersect(point, query):
    # coordinates of point
    x = point[1]
    y = point[2]
    # range of rectangular
    left = query[0]
    right = query[1]
    top = query[2]
    bottom = query[3]
    
    if((x-left)*(x-right) <= 0 and (y-top)*(y-bottom) <= 0):
        return True
    else:
        return False

# answer all queries using scanning method
def scanRangeQueries(points, queries):
    # the output file
    resultFile = 'resultRange-scan.txt'
    fResult = open(resultFile, 'wt')
    # start time
    timeStart = time.time()
    # answer each query
    for query in queries:
        times = 0
        # scan each point
        for point in points:
            if isIntersect(point, query):
                times += 1
                
        fResult.write(str(times) + '\r\n')
    
    fResult.close()
    # end time
    timeEnd = time.time()
    i = len(queries)
    print('Scan range queries finished. Average time: ' + str((timeEnd-timeStart)/i))

def main():
    datasetFile = 'dataset.txt'
    queryFile = 'queriesRange.txt'
    
    # parse arguements
    options,args = getopt.getopt(sys.argv[1:],"d:q:")
    for opt, para in options:
        if opt == '-d':
            datasetFile = para
        if opt == '-q':
            queryFile = para
    
    # scan the data-set and answer range queries
    queries = readRanges(queryFile)
    points = readPoints(datasetFile)
    scanRangeQueries(points, queries)

if __name__ == '__main__':
    main()
