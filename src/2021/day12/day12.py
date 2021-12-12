from typing import List, Set
import common as com

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def isBigCave(name: str):
    return name.isupper()

def depthFirstSearch(graph: com.Graph, currentNode: str, endNode: str, visited: Set[str], currentPath: List[str], allPaths:list):
    if currentNode in visited:
        return
    if not isBigCave(currentNode):
        visited.add(currentNode)
    currentPath.append(currentNode)
    if currentNode == endNode:
        allPaths.append(currentPath)
        return
    edges = graph.direct_connected_weights_and_edges(currentNode)
    for node in edges:
        if node not in visited:
            depthFirstSearch(graph, node, endNode, set(visited), list(currentPath), allPaths)

def canVisit(node: str, visited: Set[str], visitedTwice: Set[str], markVisited = False):
    if isBigCave(node):
        return True
    if node == 'start':
        if node in visited:
            return False
        if markVisited:
            visited.add(node)
        return True
    if node in visited:
        if len(visitedTwice) > 0:
            return False
        if markVisited:
            visitedTwice.add(node)
        return True
    if markVisited:
        visited.add(node)
    return True
    
def depthFirstSearchAllowRevisited(graph: com.Graph, currentNode: str, endNode: str, visited: Set[str], visitedTwice: Set[str], currentPath: List[str], allPaths:list):
    if not canVisit(currentNode, visited, visitedTwice, True):
        return

    currentPath.append(currentNode)

    if currentNode == endNode:
        allPaths.append(currentPath)
        return
    edges = graph.direct_connected_weights_and_edges(currentNode)
    for node in edges:
        if canVisit(node, visited, visitedTwice):
            depthFirstSearchAllowRevisited(graph, node, endNode, set(visited), set(visitedTwice), list(currentPath), allPaths)

def Part1(lines: List[str]):
    graph = com.Graph(False)
    pathStart = None
    pathEnd = None
    allPaths = list()
    for line in lines:
        startNodeName, endNodeName = line.strip().split('-')
        startNode = startNodeName
        endNode = endNodeName

        graph.add_node(startNode)
        if startNode == 'start':
            pathStart = startNode

        graph.add_node(endNode)
        if endNode == 'end':
            pathEnd = endNode
        graph.add_edge(startNode, endNode, None)
    
    depthFirstSearch(graph, pathStart, pathEnd, set(), list(), allPaths)
    
    return len(allPaths)

def Part2(lines):        
    graph = com.Graph(False)
    pathStart = None
    pathEnd = None
    allPaths = list()
    for line in lines:
        startNodeName, endNodeName = line.strip().split('-')
        startNode = startNodeName
        endNode = endNodeName

        graph.add_node(startNode)
        if startNode == 'start':
            pathStart = startNode

        graph.add_node(endNode)
        if endNode == 'end':
            pathEnd = endNode
        graph.add_edge(startNode, endNode, None)
    
    depthFirstSearchAllowRevisited(graph, pathStart, pathEnd, set(), set(), list(), allPaths)
    
    return len(allPaths)


if test:
    lines = com.readFile("test.txt")
else:
    #print(puzzle.input_data)
    #lines = com.readFile("input.txt")
    lines = puzzle.input_data.splitlines()

if part1:
    part1Answer = Part1(lines)
    if part1Answer is None:
        print("Returned None for part1")
    elif test:
        print("Part1 test result: \n" + str(part1Answer))
    else:
        puzzle.answer_a = part1Answer
            

if part2:
    part2Answer = Part2(lines)
    if part2Answer is None:
        print("Returned None for part2")
    elif test:
        print("Part2 test result: \n" + str(part2Answer))
    else:
        puzzle.answer_b = part2Answer