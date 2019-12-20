from typing import Callable, Any

class Graph(object):
    EDGE = 0
    NODE = 1
    def __init__(self, directed = True, edgeWeightFcn= None):
        self.__graph = {}
        self.directed = directed
        self.edgeWeightFcn = edgeWeightFcn
    
    def add_node(self, node):
        existing = self.__graph.get(node)
        if existing is None:
            self.__graph[node] = {}

    def remove_node(self, node, reattachEnds = True):
        connected = self.__graph.get(node)
        for otherNode in connected:
            otherNodesConnections = self.__graph.get(otherNode)
            if node in otherNodesConnections:
                otherNodesConnections.pop(node)
            if reattachEnds:
                for reattachNode in connected:
                    if reattachNode == otherNode:
                        continue
                    self.add_edge(otherNode, reattachNode, connected[otherNode] + connected[reattachNode], False )
        self.__graph.pop(node)

    def __add_edge_impl(self, source, destination, edgeInfo, addReverse):
        existing = self.__graph.get(source)
        if existing is None:
            existing = {}
            self.__graph[source] = existing
        existingEdge = existing.get(destination)
        if existingEdge is not None:
            test = 0
        if existingEdge is None or (self.edgeWeightFcn is not None and self.edgeWeightFcn(source, destination, existingEdge) > self.edgeWeightFcn(source, destination, edgeInfo)) or (self.edgeWeightFcn is None and existingEdge > edgeInfo):
            existing[destination] = edgeInfo
        if addReverse:
            self.__add_edge_impl(destination, source, edgeInfo, False)
    
    def add_edge(self, source, destination, edgeInfo, addReverse = None):
        if addReverse is None:
            addRevers = not self.directed
        self.__add_edge_impl(source, destination, edgeInfo, addReverse)

    def direct_connected_weights_and_edges(self, source):
        edges = self.__graph.get(source)
        if self.edgeWeightFcn is None:
            return edges
        return map(lambda edge: (self.edgeWeightFcn(source, edge, edges[edge]), edge), edges)