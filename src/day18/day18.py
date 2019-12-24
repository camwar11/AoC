import common as com
from copy import deepcopy

test = False
part1 = True
part2 = False

impossible = 999999999999999

def edgeWeightFcn(ownedKeys):
    def edgeWeight(source, dest, edge):
        global impossible
        if isinstance(source, int) or isinstance(dest, int):
            return edge
        if source != '@' and source == source.upper():
            if not source.lower() in ownedKeys:
                return impossible
        if dest != '@' and dest == dest.upper():
            if not dest.lower() in ownedKeys:
                return impossible
        return edge
    return edgeWeight

shortestSoFar = impossible

def findShortest(graph: com.Graph, currentNode, ownedKeys: set, remainingKeys: set, currentSteps: int):
    global impossible, shortestSoFar
    if not bool(remainingKeys):
        if currentSteps < shortestSoFar:
            shortestSoFar = currentSteps
        return currentSteps
    else:
        if currentSteps >= shortestSoFar:
            return impossible

    connected = graph.direct_connected_weights_and_edges(currentNode)
    choices = []
    for value in connected:
        if value[0] != impossible:
            choices.append(value)

    graph.remove_node(currentNode, True)
    
    choicesSteps = []
    for choice in choices:
        node = choice[1]
        nodesGraph = deepcopy(graph)
        nodesOwnedKeys = deepcopy(ownedKeys)
        nodesRemainingKeys = deepcopy(remainingKeys)
        nodesGraph.edgeWeightFcn = edgeWeightFcn(nodesOwnedKeys)
        if node.lower() == node:
            nodesOwnedKeys.add(node)
            nodesRemainingKeys.remove(node)            
        
        steps = findShortest(nodesGraph, node, nodesOwnedKeys, nodesRemainingKeys, currentSteps + choice[0])
        choicesSteps.append(steps)
    
    return min(choicesSteps)
 

def connectedInDirection(grid: com.CartesianGrid, point: com.Point, direction, steps: int, previouslyHit: set):
    pointInDirection = grid.getPoint(*(point + direction))
    if pointInDirection is None or pointInDirection in previouslyHit:
        return []
    previouslyHit.add(pointInDirection)
    return [(pointInDirection.data, steps + 1)]

def connectedGridElements(grid: com.CartesianGrid, point: com.Point, steps: int, previouslyHit: set):
    connected = []
    up = connectedInDirection(grid, point, grid.UP, steps, previouslyHit)
    if up is not None:
        connected.extend(up)
    down = connectedInDirection(grid, point, grid.DOWN, steps, previouslyHit)
    if down is not None:
        connected.extend(down)
    left = connectedInDirection(grid, point, grid.LEFT, steps, previouslyHit)
    if left is not None:
        connected.extend(left)
    right = connectedInDirection(grid, point, grid.RIGHT, steps, previouslyHit)
    if right is not None:
        connected.extend(right)
    return connected

def Part1(lines):
    grid = com.CartesianGrid(' ')
    keysAndDoors = {}
    start = None
    KEY = 0
    DOOR = 1
    remainingKeys = set()
    openSpaces = []
    y = 0
    openSpaceIdx = 0
    for line in lines:
        x = 0
        for char in line.strip():
            if char != '#':
                data = char
                if char == '.':
                    data = openSpaceIdx
                    openSpaceIdx += 1
                point = com.Point(x, y, data)
                grid.addPoint(point)
                if char == '@':
                    start = point
                elif char != '.':
                    charToLower = char.lower()
                    existing = keysAndDoors.get(charToLower)
                    if existing is None:
                        existing = [None, None]
                        keysAndDoors[charToLower] = existing
                    if charToLower == char:
                        existing[KEY] = point
                        remainingKeys.add(point.data)
                    else:
                        existing[DOOR] = point
            x += 1
        y += 1
    ownedKeys = set()
    graph = com.Graph(False, edgeWeightFcn(ownedKeys))
    for point in grid.getAllPoints():
        graph.add_node(point.data)
        previouslyHit = set()
        previouslyHit.add(point)
        connected = connectedGridElements(grid, point, 0, previouslyHit)
        for edge in connected:
            graph.add_edge(point.data, edge[0], edge[1], False)

    for openSpace in range(openSpaceIdx):
        graph.remove_node(openSpace)
    
    print(findShortest(graph, '@', ownedKeys, remainingKeys, 0))

def Part2(lines):
    pass

file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file, '!')

if part1:
    Part1(lines)

if part2:
    Part2(lines)