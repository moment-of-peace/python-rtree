'''
nnGenerator.py
Arguements: -s <size>, -r <rangeLimit>, -o <outputFile>
Author: Yi Liu
Build a set of 100 (default size) range queries
Format:
 x_1 y_1
 ......
 x_m y_m
 ......
'''
# standard libraries
import sys
import getopt
# private libraries
import datasetBuilder

def main():
    fileName = 'queriesNN.txt'
    size = 100
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

    f = open(fileName, 'wt')
    for i in range(1, size+1):
        datasetBuilder.writePoint(f, rangeLimit)
    
    f.close()
    print('Finished')

if __name__ == '__main__':
    main()
