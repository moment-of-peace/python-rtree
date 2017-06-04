'''
datasetBuilder.py
Arguements: -s <size>, -r <rangeLimit>, -o <outputName>
Author: Yi Liu
Build a data set
format:
 size
 id_1 x_1 y_1
 ......
 id_m x_m y_m
 ......
'''
import sys
import getopt
import random

# write coordinates of a rtreePoint
def writePoint(f, rangeLimit):
    x = round(random.uniform(-rangeLimit, rangeLimit),2)
    y = round(random.uniform(-rangeLimit, rangeLimit),2)
    f.write(str(x) + ' ' + str(y) + '\r\n')

# build data set
def buildDataSet(fileName, size, rangeLimit):
    f = open(fileName, 'wt')
    f.write(str(size) + '\r\n') # first line
    # remained lines
    for i in range(1, size+1):
        f.write(str(i) + ' ')
        writePoint(f, rangeLimit)

    f.close()
    print('Size: ', size, '. Range: ', -rangeLimit, ':', rangeLimit)

def main():
    fileName = 'dataset.txt'
    size = 10000 
    rangeLimit = 500
    
    # parse arguements
    options,args = getopt.getopt(sys.argv[1:],"s:r:o:")
    for opt, para in options:
        if opt == '-s':
            size = int(para)
        if opt == '-r':
            rangeLimit = int(para)
        if opt == '-o':
            fileName = para
    
    # build data set
    buildDataSet(fileName, size, rangeLimit)
    
if __name__ == '__main__':
    main()
