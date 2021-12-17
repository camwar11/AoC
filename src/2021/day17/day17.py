from typing import List, Optional, Set, Tuple
import common as com

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

grid = com.CartesianGrid()

def in_target(xMin: int, xMax:int, yMin: int, yMax:int, point: com.Point):
    return point.x >= xMin and point.x <= xMax and point.y >= yMin and point.y <= yMax

def shoot_probe(xMin: int, xMax:int, yMin: int, yMax:int, xVelocity: int, yVelocity: int, currentMaxHeight: Optional[int]):
    "Returns None if the probe misses the target or doesn't go over the current max height, else max height"
    global grid
    position = com.Point(0, 0, None)
    grid.addPoint(position)
    previousHeight = 0
    maxHeight = 0

    # Bail if we overshot in the X direction
    while(position.x <= xMax):
        if in_target(xMin, xMax, yMin, yMax, position):
            if not currentMaxHeight:
                # Part2 just needs to know if we hit the target
                return True
            if maxHeight > currentMaxHeight:
                return maxHeight
            return None
        
        position.move(xVelocity, yVelocity)
        maxHeight = max(maxHeight, position.y)

        if previousHeight > position.y:
            if currentMaxHeight and maxHeight < currentMaxHeight:
                # Bail if we didn't reach high enough
                return None
            elif position.y < yMin:
                # Bail if we overshot in the Y direction
                return None
        
        previousHeight = position.y
        yVelocity -= 1
        if xVelocity > 0:
            xVelocity -= 1
        elif xVelocity < 0:
            xVelocity += 1
    
    return None

def Part1(lines: List[str]):
    maxHeight = 0
    line = lines[0].strip()
    _, _, xRaw, yRaw = line.split(' ')
    xRaw = xRaw.split('=')[1][0:-1] # take off the comma
    yRaw = yRaw.split('=')[1]
    xMin, xMax = xRaw.split('..')
    yMin, yMax = yRaw.split('..')

    xMin = int(xMin)
    xMax = int(xMax)
    yMin = int(yMin)
    yMax = int(yMax)

    for y in range(1, 500):
        for x in range(1, 500):
            height = shoot_probe(xMin, xMax, yMin, yMax, x, y, maxHeight)
            if height:
                maxHeight = max(height, maxHeight)
        

    return maxHeight

def Part2(lines):
    count = 0
    line = lines[0].strip()
    _, _, xRaw, yRaw = line.split(' ')
    xRaw = xRaw.split('=')[1][0:-1] # take off the comma
    yRaw = yRaw.split('=')[1]
    xMin, xMax = xRaw.split('..')
    yMin, yMax = yRaw.split('..')

    xMin = int(xMin)
    xMax = int(xMax)
    yMin = int(yMin)
    yMax = int(yMax)

    # Brute force it
    for y in range(-200, 500):
        for x in range(1, 500):
            height = shoot_probe(xMin, xMax, yMin, yMax, x, y, None)
            if height:
                count += 1
        

    return count

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