# python_rtree
Implement rtree range queries and nearest neighbour queries, and compare with sequentially scanning

Author: Yi Liu

***************************** R-tree files **********************************

Rtree.py
    Contains classes representing point, leaf node and branch node of R-tree

rtreeBuilder.py
    Build a R-tree from a given data-set file

rtreeRange.py
    Answer a set of range queries using R-tree. 
    Output file is 'resultRange.txt'

rtreeNN.py
    Answer a set of NN queries using R-tree. 
    Output file is 'resultNN.txt'

rtreeQuries.py
    Implement: sequential-scanning, building r-tree,range queries (using scanning and r-tree 
    respectively), and NN queries (using scanning and "Best First" respectively) all together


********************* Sequential-scanning methods for queries ************************

scanRange.py
    Answer a set of range queries using scanning method. 
    Output file is 'resultRange-scan.txt'

scanNN.py
    Answer a set of NN queries using scanning method.
    Output file is 'resultNN-scan.txt'


********************************** Generators *****************************************

datasetBuilder.py
    Build a dataset. Default size and range are 10000 and +-500
    Default output file is 'dataset.txt'
    
generateRange.py
    Generate a set of range queries. Default size and range are 100 and +-500
    Default output file is 'queriesRange.txt'
    
generateNN.py
    Generate a set of NN queries. Default size and range are 100 and +-500
    Default output file is 'queriesNN.txt'
