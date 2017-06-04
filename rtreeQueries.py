'''
rtreeRange.py
Arguements: -d <datasetFile>, -r <rangeQueryFile>, -n <nnQueryFile>, -b <Bvalue>
Author: Yi Liu
Answer queries using sequentially scanning and r-tree respectively
'''

# standard libraries
import time
import sys
import getopt
# private libraries
import rtreeBuilder
import rtreeRange
import rtreeNN
import scanRange
import scanNN

# scan the data set sequentially and print the time
def scanDataSet(datasetFile):
    points = []
    start = time.time()
    f = open(datasetFile, 'rt')
    nextLine = f.readline() # the first line is the size
    nextLine = f.readline()
    while nextLine != '':
        points.append(scanRange.getPoint(nextLine))
        nextLine = f.readline()
        
    f.close()
    end = time.time()
    print('Scanning time:', str(end-start))
    return points

def main():
    datasetFile = 'dataset.txt'
    rangeFile = 'queriesRange.txt'
    nnFile = 'queriesNN.txt'
    Bvalue = None
    scanFlag = 'n'
    
    # parse arguments
    options,args = getopt.getopt(sys.argv[1:],"d:r:n:b:")
    for opt, para in options:
        if opt == '-d':
            datasetFile = para
        if opt == '-r':
            rangeFile = para
        if opt == '-n':
            nnFile = para
        if opt == '-b':
            Bvalue = int(para)
        
    # scan the data set
    points = scanDataSet(datasetFile)
    
    # build r-tree
    try:
        root = rtreeBuilder.buildRtree(datasetFile, Bvalue)
        rtreeBuilder.checkRtree(root)
    except Exception:
        print('Memory overflow')
    
    # answer range queries
    queries = scanRange.readRanges(rangeFile)
    scanRange.scanRangeQueries(points, queries)
    rtreeRange.answerRangeQueries(root, queries)
    
    # answer NN queries
    queries = scanNN.readNn(nnFile)
    scanNN.scanNNQueries(points, queries)
    rtreeNN.answerNnQueries(root, queries)

if __name__ == '__main__':
    main()
