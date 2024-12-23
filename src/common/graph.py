from typing import Callable, Any, Tuple
from heapq import *

from common.cartesianGrid import CartesianGrid

class Graph(object):
    EDGE = 0
    NODE = 1
    def __init__(self, directed = True, edgeWeightFcn= None):
        self.__graph = {}
        self.directed = directed
        self.edgeWeightFcn = edgeWeightFcn
    
    def __str__(self):
        return self.__graph.__str__()

    def __contains__(self, node):
        return self.get_node(node) is not None
    
    def add_node(self, node):
        if node not in self:
            self.__graph[node] = {}
    
    def get_node(self, node):
        return self.__graph.get(node)

    def get_all_nodes(self):
        return self.__graph.keys()

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
            addReverse = not self.directed
        self.__add_edge_impl(source, destination, edgeInfo, addReverse)

    def direct_connected_weights_and_edges(self, source):
        edges = self.__graph.get(source)
        if self.edgeWeightFcn is None:
            return edges
        return map(lambda edge: (self.edgeWeightFcn(source, edge, edges[edge]), edge), edges)

    def dijsktra(self, start, end) -> Tuple[list, int]:
        # shortest paths is a dict of nodes
        # whose value is a tuple of (previous node, weight)
        shortest_paths = {start: (None, 0)}
        current_node = start
        visited = set()
        
        while current_node != end:
            visited.add(current_node)
            destinations = self.direct_connected_weights_and_edges(current_node)
            weight_to_current_node = shortest_paths[current_node][1]

            for next_node in destinations:
                weight = destinations[next_node] + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)
            
            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return None
            # next node is the destination with the lowest weight
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
        
        # Work back through destinations in shortest path
        path = []
        while current_node is not None:
            path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
        # Reverse path
        path = path[::-1]
        return path, shortest_paths[end][1]


    @staticmethod
    def parse_from_grid(grid: CartesianGrid, directed = True, edgeWeightFinder = None, includeDiagonals = False):
        graph = Graph(directed)
        for point in grid.getAllPoints():
            graph.add_node(point)
            for adjacent in grid.getAdjacentPoints(point.x, point.y, includeDiagonals):
                graph.add_node(adjacent)
                edgeWeight = 1
                if edgeWeightFinder:
                    edgeWeight = edgeWeightFinder(point, adjacent)
                if edgeWeight is not None:
                    graph.add_edge(point, adjacent, edgeWeight, not(directed))
        
        return graph