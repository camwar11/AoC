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
            self.__graph[node] = []

    def remove_node(self, node, reattachEnds = True):
        connected = self.__graph.get(node)
        for otherNode in connected:
            otherNodesConnections = self.__graph.get(otherNode[self.NODE])
            index = 0
            for otherNodeConnection in otherNodesConnections:
                if otherNodeConnection[self.NODE] == node:
                    break
                index += 1
            removedConnection = otherNodesConnections.pop(index)
            if reattachEnds:
                for reattachNode in connected:
                    if reattachNode == otherNode:
                        continue
                    self.add_edge(otherNode[self.NODE], reattachNode[self.NODE], otherNode[self.EDGE] + reattachNode[self.EDGE], False )
        self.__graph.pop(node)

    def __add_edge_impl(self, source, destination, edgeInfo, addReverse):
        existing = self.__graph.get(source)
        if existing is None:
            existing = []
            self.__graph[source] = existing
        edge = (edgeInfo, destination)
        existing.append(edge)
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
        return map(lambda edge: (self.edgeWeightFcn(source, edge[self.NODE], edge[self.EDGE]), edge[self.NODE]), edges)