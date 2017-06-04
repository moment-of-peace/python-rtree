'''
rtreeBuilder.py
Arguements: -d <datasetFile>, -b <Bvalue>
Author: Yi Liu
Build a r-tree from a given data set
'''

# standard libraries
import getopt
import sys
# private libraries
import Rtree
import scanRange

global root
global Bvalue

def handleOverFlow(node):
    global root
    global Bvalue
    
    # split node into two new nodes
    nodes = node.split()
    # if root node is overflow, new root need to build
    if node.paren == None:
        root = Rtree.Branch(Bvalue, node.level + 1, nodes[0])
        root.addChild(nodes[0])
        root.addChild(nodes[1])
        root.childList[0].paren = root
        root.childList[1].paren = root
    else:
        # update the parent node
        parent = node.paren
        parent.childList.remove(node)
        parent.childList += nodes
        # check whether parent node is overflow
        if parent.isOverFlow():
            handleOverFlow(parent)

# insert a point to a node
def insert(node, point):    
    # if the node is a leaf, add this point
    if  isinstance(node, Rtree.Leaf):
        node.addChild(point)
        if node.isOverFlow():
            handleOverFlow(node)

    # if the node is a branch, choose a child to add this point
    elif isinstance(node, Rtree.Branch):
        node.update(point)
        childNode = node.chooseChild(point)
        insert(childNode, point)

    else:
        pass

def buildRtree(dataSetName, *B):
    global root
    global Bvalue
    
    Bvalue = 25
    if len(B) == 1 and B[0] != None:
        Bvalue = B[0]
        
    f = open(dataSetName, 'rt')
    nextLine = f.readline()
    # size of date set
    size = int(nextLine.strip('\n'))
    # read the first point and build a root
    nextLine = f.readline()
    point = Rtree.Point(scanRange.getPoint(nextLine))
    root = Rtree.Leaf(Bvalue, 1, point)
    root.addChild(point)
    
    # add the remained points
    nextLine = f.readline()
    while nextLine != '':
        point = Rtree.Point(scanRange.getPoint(nextLine))
        insert(root, point)
        nextLine = f.readline()

    f.close()
    print('R-tree has been built. B is:', Bvalue,'Highest level is:',root.level)
    return root

# check all nodes and points in a r-tree
def checkRtree(rtree):    
    checkBranch(rtree)
    print('Finished checking R-tree')

# check the correctness of a leaf node in r-tree
def checkLeaf(leaf):    
    # check whether a point is inside of a leaf
    def insideLeaf(x, y, parent):
        if x<parent[0] or x>parent[1] or y<parent[2] or y>parent[3]:
            return False
        else:
            return True
    
    # general check
    checkNode(leaf)
    # check whether each child point is inside of leaf's range
    for point in leaf.childList:
        if not insideLeaf(point.x, point.y, leaf.range):
            print('point(', point.x, point.y, 'is not in leaf range:', leaf.range)

# check the correctness of a branch node in r-tree
def checkBranch(branch):    
    # check whether a branch is inside of another branch
    def insideBranch(child, parent):
        if child[0]<parent[0] or child[1]>parent[1] or child[2]<parent[2] or child[3]>parent[3]:
            return False
        else:
            return True
    
    # general check
    checkNode(branch)
    # check whether child's range is inside of this node's range
    for child in branch.childList:
        if not insideBranch(child.range, branch.range):
            print('child range:', child.range, 'is not in node range:', branch.range)
        # check this child
        if isinstance(child, Rtree.Branch):
            # if child is still a branch node, check recursively
            checkBranch(child)
        elif isinstance(child, Rtree.Leaf):
            # if child is a leaf node
            checkLeaf(child)

# general check for both branch and leaf node
def checkNode(node):
    global Bvalue
    
    length = len(node.childList)
    # check whether is empty
    if length == 0:
        print('empty node. node level:', node.level, 'node range:', node.range)
    # check whether overflow
    if length > Bvalue:
        print('overflow. node level:', node.level, 'node range:', node.range)
        
    # check whether the centre is really in the centre of the node's range
    r = node.range
    if (r[0]+r[1])/2 != node.centre[0] or (r[2]+r[3])/2 != node.centre[1]:
        print('wrong centre. node level:', node.level, 'node range:', node.range)
    if r[0]>r[1] or r[2]>r[3]:
        print('wrong range. node level:', node.level, 'node range:', node.range)

def main():
    global root

    datasetFile = 'dataset.txt'
    Bvalue = None
    
    # parse arguments
    options,args = getopt.getopt(sys.argv[1:],"d:b:")
    for opt, para in options:
        if opt == '-d':
            datasetFile = para
        if opt == '-b':
            Bvalue = int(para)
    
    # build r-tree from a given data-set
    buildRtree(datasetFile, Bvalue)
    # check the correctness of r-tree
    checkRtree(root)

if __name__ == "__main__":
    main()
