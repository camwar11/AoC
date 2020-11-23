import common as com
from collections import deque

test = False
part1 = True
part2 = False
puzzle = com.PuzzleWithTests()

impossible = 999999999999999

def edgeWeightFcn(ownedKeys):
    def edgeWeight(source, dest, edge):
        global impossible
        if isinstance(source, int) or isinstance(dest, int):
            return edge
        #if source != '@' and source == source.upper():
        #    if not source.lower() in ownedKeys:
        #        return impossible
        #if dest != '@' and dest == dest.upper():
        #    if not dest.lower() in ownedKeys:
        #        return impossible
        return edge
    return edgeWeight



def isDoor(value):
    return value != '@' and value != value.lower()

def isKey(value):
    return value != '@' and value == value.lower()

def findShortest(graph: com.Graph, currentNode, ownedKeys: set, allKeys: set, currentSteps: int):
    pathQueue = deque()
    alreadyHit = {}
    alreadyHit[(currentNode, frozenset(ownedKeys))] = currentSteps
    keysInOrder = list()
    pathQueue.append((currentSteps,currentNode, ownedKeys, keysInOrder))
    allKeysHash = frozenset(allKeys).__hash__()
    shortestSoFar = impossible
    shortestPath = None
    while pathQueue:
        currentSteps, currentNode, ownedKeys, keysInOrder = pathQueue.popleft()
        ownedKeys = ownedKeys.copy()
        keysInOrder = keysInOrder.copy()
        if isKey(currentNode):
            ownedKeys.add(currentNode)
            keysInOrder.extend(currentNode)

        currentOwnedKeys = frozenset(ownedKeys)
        if allKeysHash == currentOwnedKeys.__hash__():
            if shortestSoFar >= currentSteps:
                shortestSoFar = currentSteps
                shortestPath = keysInOrder
                continue
            else:
                continue

        for weight, edge in graph.direct_connected_weights_and_edges(currentNode):
            newSteps = currentSteps + weight
            if isDoor(edge) and edge.lower() not in ownedKeys:
                continue
            if alreadyHit.get((edge, currentOwnedKeys)):
                if alreadyHit.get((edge, currentOwnedKeys)) < newSteps:
                    continue
            alreadyHit[(edge, currentOwnedKeys)] = newSteps
            pathQueue.append((newSteps, edge, ownedKeys, keysInOrder))
    return shortestSoFar, shortestPath


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
    
    answer, path = findShortest(graph, '@', ownedKeys, remainingKeys, 0)
    print(answer)
    print(path)
    return answer

def Part2(lines):
    pass

if test:
    lines = com.readFile("test.txt", "!")
else:
    #print(puzzle.input_data)
    lines = puzzle.input_data.splitlines()

if part1:
    part1Answer = Part1(lines)
    if part1Answer is None:
        print("Returned None for part1")
    elif test:
        print("Part1 test result: " + str(part1Answer))
    else:
        puzzle.answer_a = part1Answer
            

if part2:
    part2Answer = Part2(lines)
    if part2Answer is None:
        print("Returned None for part2")
    elif test:
        print("Part2 test result: " + str(part2Answer))
    else:
        puzzle.answer_b = part2Answer