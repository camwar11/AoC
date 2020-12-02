import common as com

test = False
part1 = False
part2 = True

def Part1(lines):
    OPEN = 1
    WALL = 0
    currentPoint = com.Point(0, 0, OPEN)
    nextPoint = None
    north = [0, 1]
    east = [1, 0]
    south = [0, -1]
    west = [-1, 0]
    directions = [east, north, west, south]
    directionInputs = [4, 1, 3, 2]
    facingIdx = 0
    turned = False
    def outputPoint(point):
        nonlocal facingIdx, currentPoint
        if point.data == 0:
            return '#'
        elif point == currentPoint:
            if facingIdx == 0:
                return '>'
            elif facingIdx == 1:
                return '^'
            elif facingIdx == 2:
                return '<'
            elif facingIdx == 3:
                return 'v'
        return '.'
    grid = com.CartesianGrid(' ', outputPoint)
    grid.addPoint(currentPoint)

    def inputHandler():
        nonlocal grid, currentPoint, OPEN, WALL, north, east, south, west, directions, facingIdx, directionInputs, nextPoint, turned
        while True:
            leftIdx = (facingIdx + 1) % 4
            newCoords = currentPoint + directions[leftIdx]
            leftPoint = grid.getPoint(newCoords[0], newCoords[1])
            if leftPoint is None:
                nextPoint = com.Point(newCoords[0], newCoords[1], 99999999)
                grid.addPoint(nextPoint)
                print('left point at ', nextPoint.x, nextPoint.y, ' not visited. Facing', facingIdx)
                turned = True
                return directionInputs[leftIdx]
            elif leftPoint.data >= OPEN:
                nextPoint = leftPoint
                facingIdx = leftIdx
                print('left point at ', nextPoint.x, nextPoint.y, ' is open. Facing', facingIdx)
                return directionInputs[leftIdx]
            
            # go straight
            newCoords = currentPoint + directions[facingIdx]
            forwardPoint = grid.getPoint(newCoords[0], newCoords[1])
            if forwardPoint is None:
                forwardPoint = com.Point(newCoords[0], newCoords[1], 99999999)
                grid.addPoint(forwardPoint)
                print('fwd point at ', nextPoint.x, nextPoint.y, ' is empty. Facing', facingIdx)
            elif forwardPoint.data == WALL:
                facingIdx = (facingIdx - 1) % 4
                print('fwd point at ', nextPoint.x, nextPoint.y, ' is Wall. Facing', facingIdx)
                continue
            else:
                print('fwd point at ', nextPoint.x, nextPoint.y, ' is open. Facing', facingIdx)
            nextPoint = forwardPoint
            return directionInputs[facingIdx]
    
    def outputHandler(output):
        nonlocal grid, currentPoint, OPEN, WALL, nextPoint, turned, facingIdx
        localTurned = turned
        turned = False
        if output == WALL:
            nextPoint.data = output
            print('Ran into wall at', nextPoint.x, nextPoint.y)
        elif output == 2:
            print('Oxygen system at ', nextPoint.x, nextPoint.y, 'with steps', currentPoint.data)
            compy.pause()
            return
        elif output == OPEN:
            steps = currentPoint.data + 1
            if steps < nextPoint.data:
                nextPoint.data = steps
            print('Walked to', nextPoint.x, nextPoint.y, 'with steps', steps)
            print(grid)
            if localTurned:
                facingIdx = (facingIdx + 1) % 4
            currentPoint = nextPoint

    compy = com.intCode(lines[0], False, None, inputHandler, outputHandler)
    compy.RunIntCodeComputer()

def Part2(lines):
    OPEN = 1
    WALL = 0
    currentPoint = com.Point(0, 0, OPEN)
    nextPoint = None
    north = [0, 1]
    east = [1, 0]
    south = [0, -1]
    west = [-1, 0]
    directions = [east, north, west, south]
    directionInputs = [4, 1, 3, 2]
    facingIdx = 0
    turned = False
    maxSteps = 9999999999999
    def outputPoint(point):
        nonlocal facingIdx, currentPoint
        if point.data == 0:
            return '#'
        elif point == currentPoint:
            if facingIdx == 0:
                return '>'
            elif facingIdx == 1:
                return '^'
            elif facingIdx == 2:
                return '<'
            elif facingIdx == 3:
                return 'v'
        return '.'
    grid = com.CartesianGrid(' ', outputPoint)
    grid.addPoint(currentPoint)

    def inputHandler():
        nonlocal grid, currentPoint, OPEN, WALL, north, east, south, west, directions, facingIdx, directionInputs, nextPoint, turned
        while True:
            leftIdx = (facingIdx + 1) % 4
            newCoords = currentPoint + directions[leftIdx]
            leftPoint = grid.getPoint(newCoords[0], newCoords[1])
            if leftPoint is None:
                nextPoint = com.Point(newCoords[0], newCoords[1], 99999999)
                grid.addPoint(nextPoint)
                #print('left point at ', nextPoint.x, nextPoint.y, ' not visited. Facing', facingIdx)
                turned = True
                return directionInputs[leftIdx]
            elif leftPoint.data >= OPEN:
                nextPoint = leftPoint
                facingIdx = leftIdx
                #print('left point at ', nextPoint.x, nextPoint.y, ' is open. Facing', facingIdx)
                return directionInputs[leftIdx]
            
            # go straight
            newCoords = currentPoint + directions[facingIdx]
            forwardPoint = grid.getPoint(newCoords[0], newCoords[1])
            if forwardPoint is None:
                forwardPoint = com.Point(newCoords[0], newCoords[1], 99999999)
                grid.addPoint(forwardPoint)
                #print('fwd point at ', nextPoint.x, nextPoint.y, ' is empty. Facing', facingIdx)
            elif forwardPoint.data == WALL:
                facingIdx = (facingIdx - 1) % 4
                #print('fwd point at ', nextPoint.x, nextPoint.y, ' is Wall. Facing', facingIdx)
                continue
            else:
                pass
                #print('fwd point at ', nextPoint.x, nextPoint.y, ' is open. Facing', facingIdx)
            nextPoint = forwardPoint
            return directionInputs[facingIdx]
    
    def outputHandler(output):
        nonlocal grid, currentPoint, OPEN, WALL, nextPoint, turned, facingIdx, maxSteps
        localTurned = turned
        turned = False
        if output == WALL:
            nextPoint.data = output
            #print('Ran into wall at', nextPoint.x, nextPoint.y)
        elif output == 2:
            print('Oxygen system at ', nextPoint.x, nextPoint.y, 'with steps', currentPoint.data)
            for point in grid.getAllPoints():
                if point.data > WALL:
                    point.data = 9999999999999999999999999
            nextPoint.data = WALL # make it a wall so we don't go back
            currentPoint = nextPoint
            maxSteps = 0
            return
        elif output == OPEN:
            steps = currentPoint.data + 1
            if steps < nextPoint.data:
                nextPoint.data = steps
                if maxSteps < steps:
                    maxSteps = steps
            #print('Walked to', nextPoint.x, nextPoint.y, 'with steps', steps)
            if steps % 20 == 0:
                print(grid)
            if localTurned:
                facingIdx = (facingIdx + 1) % 4
            currentPoint = nextPoint

    compy = com.intCode(lines[0], False, None, inputHandler, outputHandler)
    compy.RunIntCodeComputer()

file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file)

if part1:
    Part1(lines)

if part2:
    Part2(lines)