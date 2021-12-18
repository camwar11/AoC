class tree(object):
    def __init__(self):
        self.root = None
        self._allNodes = set()
        self._leafNodes = set()

    def addNode(self, parent, node):
        self._allNodes.add(node)
        if self.root is None:
            self.root = node
        if not parent is None:
            parent.addChild(node)
        self._leafNodes.discard(node.parent)
        self._leafNodes.add(node)
    
    def removeNode(self, node):
        self._allNodes.discard(node)
        if node == self.root:
            self.root = None
        if node in self._leafNodes:
            self._leafNodes.remove(node)
            self._leafNodes.add(node.parent)
        
        if not node.parent is None:
            node.parent.removeChild(node)

    def replaceNode(self, oldNode, newNode):
        self._allNodes.discard(oldNode)
        if oldNode == self.root:
            self.root = newNode
        if oldNode in self._leafNodes:
            self._leafNodes.remove(oldNode)
            self._leafNodes.add(newNode)
        
        if oldNode.parent is not None:
            oldNode.parent.replaceChild(oldNode, newNode)
    
    def breadthFirstTraverse(self, callback, backwards = False):
        self._breadthFirstTraverseImpl(callback, self.root, 0, backwards)

    def _breadthFirstTraverseImpl(self, callback, currentNode, level, backwards = False):
        callback(currentNode, level)
        children = currentNode.children
        if backwards:
            children = reversed(children)
        for child in children:
            self._breadthFirstTraverseImpl(callback, child, level + 1, backwards)

    def breadthFirstIterate(self, startNode = None, backwards = False):
        if not startNode:
            startNode = self.root
        yield from self._breadthFirstTraverseImpl(startNode, 0, backwards)

    def _breadthFirstIterateImpl(self, currentNode, level, backwards = False):
        yield currentNode, level
        
        children = currentNode.children
        if backwards:
            children = reversed(children)
        for child in children:
            yield from self._breadthFirstIterateImpl(child, level + 1, backwards)

    def depthFirstTraverse(self, callback, backwards = False):
        self._depthFirstTraverseImpl(callback, self.root, 0, backwards)

    def _depthFirstTraverseImpl(self, callback, currentNode, level, backwards = False):
        children = currentNode.children
        
        if backwards:
            children = reversed(children)
        for child in children:
            self._depthFirstTraverseImpl(callback, child, level + 1, backwards)
        
        callback(currentNode, level)

    def depthFirstIterate(self, startNode = None, backwards = False):
        if not startNode:
            startNode = self.root
        yield from self._depthFirstIterateImpl(startNode, 0, backwards)

    def _depthFirstIterateImpl(self, currentNode, level, backwards = False):
        children = currentNode.children
        
        if backwards:
            children = reversed(children)
        for child in children:
            yield from self._depthFirstIterateImpl(child, level + 1, backwards)

        yield currentNode, level

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
        self.parent = None
    
    def addChild(self, child):
        self.children.append(child)
        child.parent = self

    def removeChild(self, child):
        self.children.remove(child)
        child.parent = None

    def replaceChild(self, oldChild, newChild):
        index = self.children.index(oldChild)
        self.children.pop(index)
        self.children.insert(index, newChild)
        oldChild.parent = None
        newChild.parent = self

    def getAncestors(self, orderTopToBottom = True):
        ancestors = []
        currentNode = self
        while currentNode.parent is not None:
            ancestors.append(currentNode.parent)
            currentNode = currentNode.parent

        if orderTopToBottom:
            ancestors.reverse()
        return ancestors
        