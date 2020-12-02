import common as com

def Part1(lines):
    grid = com.CartesianGrid()
    centralPort = com.Point(0, 0, -1)
    lineId = 0
    smallestDistance = 99999999999
    for line in lines:
        x = 0
        y = 0
        for split in line.split(','):
            direction = split[0]
            length = int(split[1:])
            xDelta = 0
            yDelta = 0
            if direction == 'U':
                yDelta = length
            elif direction == 'D':
                yDelta = -length
            elif direction == 'R':
                xDelta = length
            elif direction == 'L':
                xDelta = -length
            if xDelta:
                newX = x + xDelta
                for xRange in range(min(x, newX), max(x, newX), 1):
                    point = com.Point(xRange, y, lineId)
                    existingPoint = grid.getPoint(xRange, y)
                    if existingPoint and point.data != existingPoint.data:
                        distance = centralPort.ManhattenDistance(point)
                        if distance > 0 and distance < smallestDistance:
                            smallestDistance = distance
                            closestPoint = point
                    grid.addPoint(point)
                x = newX

            if yDelta:
                newY = y + yDelta
                for yRange in range(min(y, newY), max(y, newY), 1):
                    point = com.Point(x, yRange, lineId)
                    existingPoint = grid.getPoint(x, yRange)
                    if existingPoint and point.data != existingPoint.data:
                        distance = centralPort.ManhattenDistance(point)
                        if distance > 0 and distance < smallestDistance:
                            smallestDistance = distance
                            closestPoint = point
                    grid.addPoint(point)
                y = newY

        lineId = lineId + 1
    print('smallest = '+ str(smallestDistance) + ': ' + str(closestPoint.x) + ', ' + str(closestPoint.y))

def Part2(lines):
    grid = com.CartesianGrid()
    #centralPort = com.Point(0, 0, {-1 : 999999})
    lineId = 0
    smallestDistance = 99999999999
    for line in lines:
        x = 0
        y = 0
        steps = 0
        for split in line.split(','):
            direction = split[0]
            length = int(split[1:])
            xDelta = 0
            yDelta = 0
            if direction == 'U':
                yDelta = length
            elif direction == 'D':
                yDelta = -length
            elif direction == 'R':
                xDelta = length
            elif direction == 'L':
                xDelta = -length
            if xDelta:
                newX = x + xDelta
                rangeX = None
                if xDelta > 0:
                    rangeX = range(x, newX, 1)
                else:
                    rangeX = range(x, newX, -1)

                for xRange in rangeX:
                    if(xRange != 0 or y != 0):
                        steps = steps + 1
                    point = com.Point(xRange, y, {lineId: steps})
                    existingPoint = grid.getPoint(xRange, y)
                    if (xRange != 0 or y != 0) and existingPoint and existingPoint.data.get(lineId) is None:
                        distance = existingPoint.data[0] + steps
                        if distance > 0 and distance < smallestDistance:
                            smallestDistance = distance
                            closestPoint = point
                    grid.addPoint(point)
                x = newX

            if yDelta:
                newY = y + yDelta
                rangeY = None
                if yDelta > 0:
                    rangeY = range(y, newY, 1)
                else:
                    rangeY = range(y, newY, -1)

                for yRange in rangeY:
                    if(x != 0 or yRange != 0):
                        steps = steps + 1
                    point = com.Point(x, yRange, {lineId: steps})
                    existingPoint = grid.getPoint(x, yRange)
                    if (x != 0 or yRange != 0) and existingPoint and existingPoint.data.get(lineId) is None:
                        distance = existingPoint.data[0] + steps
                        if distance > 0 and distance < smallestDistance:
                            smallestDistance = distance
                            closestPoint = point
                    grid.addPoint(point)
                y = newY

        lineId = lineId + 1
    #print(grid)
    print('smallest = '+ str(smallestDistance) + ': ' + str(closestPoint.x) + ', ' + str(closestPoint.y))


test = False
part1 = False
part2 = True

file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file)

if part1:
    Part1(lines)

if part2:
    Part2(lines)