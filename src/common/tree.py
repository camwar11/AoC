class tree(object):
    def __init__(self):
        self.root = None
        self._allNodes = set()
        self._leafNodes = set()

    def addNode(self, parent, node):
        node.parent = parent
        self._allNodes.add(node)
        if self.root is None:
            self.root = node
        if not parent is None:
            parent.addChild(node)
        self._leafNodes.discard(node.parent)
        self._leafNodes.add(node)
    
    def removeNode(self, node):
        self._allNodes.remove(node)
        if node == self.root:
            self.root = None
        if node in self._leafNodes:
            self._leafNodes.remove(node)
            self._leafNodes.add(node.parent)
        
        if not node.parent is None:
            node.parent.removeChild(node)
    
    def breadthFirstTraverse(self, callback):
        self._breadthFirstTraverseImpl(callback, self.root, 0)

    def _breadthFirstTraverseImpl(self, callback, currentNode, level):
        callback(currentNode, level)
        for child in currentNode.children:
            self._breadthFirstTraverseImpl(callback, child, level + 1)
    
    def distance(self, node1, node2):
        node1Ancestors = node1.getAncestors()
        node2Ancestors = node2.getAncestors()
        index = 0
        while True:
            if len(node1Ancestors) <= index or len(node2Ancestors) <= index:
                break
            node1Ancestor = node1Ancestors[index]
            node2Ancestor = node2Ancestors[index]
            if node1Ancestor != node2Ancestor:
                break
            index = index + 1
        
        lastCommonAncestorIndex = index - 1
        distanceToNode1FromAncestor = len(node1Ancestors[lastCommonAncestorIndex : ])
        distanceToNode2FromAncestor = len(node2Ancestors[lastCommonAncestorIndex : ])
        return distanceToNode1FromAncestor + distanceToNode2FromAncestor
                


class tree_node(object):
    def __init__(self, data):
        self.data = data
        self.children = []
    
    def addChild(self, child):
        self.children.append(child)

    def removeChild(self, child):
        self.children.remove(child)

    def getAncestors(self):
        ancestors = []
        currentNode = self
        while currentNode.parent is not None:
            ancestors.append(currentNode.parent)
            currentNode = currentNode.parent

        ancestors.reverse()
        return ancestors
        