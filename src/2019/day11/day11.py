import common as com

test = False
part1 = False
part2 = True

def cellStr(cell):
    if cell.data == 0:
        return ' '
    else:
        return 'X'

def runRobot(line, startingColor):
    grid = com.CartesianGrid(' ', cellStr)
    black = 0
    white = 1
    currentPoint = com.Point(0, 0, startingColor)
    grid.addPoint(currentPoint)
    painted = set()
    needsColorOutput = True
    up = [0, 1]
    right = [1, 0]
    down = [0, -1]
    left = [-1, 0]
    directions = [up, right, down, left]
    facingIdx = 0

    def outputCallback(output):
        nonlocal needsColorOutput, currentPoint, painted, directions, facingIdx
        if needsColorOutput:
            currentPoint.data = output
            painted.add(currentPoint)
            needsColorOutput = False
        else:
            if output == 0:
                facingIdx -= 1
            else:
                facingIdx += 1
            
            facingIdx %= 4
            nextX = currentPoint.x + directions[facingIdx][0]
            nextY = currentPoint.y + directions[facingIdx][1]
            currentPoint = grid.getPoint(nextX, nextY)
            if currentPoint is None:
                currentPoint = com.Point(nextX, nextY, 0)
                grid.addPoint(currentPoint)

            needsColorOutput = True

    def inputCallback():
        nonlocal currentPoint
        return currentPoint.data
    
    intcode = com.intCode(lines[0], printOutput=False, needsInputCallback=inputCallback, hasOutputCallback=outputCallback)
    intcode.RunIntCodeComputer()
    return painted, grid

def Part1(lines):
    painted, grid = runRobot(lines[0], 0)
    print('Painted', len(painted))


def Part2(lines):
    painted, grid = runRobot(lines[0], 1)
    print(grid)

file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file)

if part1:
    Part1(lines)

if part2:
    Part2(lines)