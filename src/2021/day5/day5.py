import common as com
from common.cartesianGrid import CartesianGrid
from common.cartesianGrid import Point

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def markPoint(grid, x, y):
    point = grid.getPoint(x, y)
    if not point:
        point = grid.addPoint(Point(x, y, 0))
    point.data += 1

def Part1(lines):
    grid = CartesianGrid('0')
    for line in lines:
        first, second = line.strip().split('->')
        firstX, firstY = first.strip().split(',')
        secondX, secondY = second.strip().split(',')
        firstX = int(firstX)
        firstY = int(firstY)
        secondX = int(secondX)
        secondY = int(secondY)
        if not (firstX == secondX or firstY == secondY):
            continue

        if firstX == secondX:
            x = firstX
            for y in range(min(firstY, secondY), max(firstY, secondY) + 1):
                markPoint(grid, x, y)
        
        if firstY == secondY:
            y = firstY
            for x in range(min(firstX, secondX), max(firstX, secondX) + 1):
                markPoint(grid, x, y)

    return len([x for x in grid.getAllPoints() if x.data > 1])

def Part2(lines):        
    grid = CartesianGrid('.', flipOutput=True)
    for line in lines:
        first, second = line.strip().split('->')
        firstX, firstY = first.strip().split(',')
        secondX, secondY = second.strip().split(',')
        firstX = int(firstX)
        firstY = int(firstY)
        secondX = int(secondX)
        secondY = int(secondY)

        if firstX == secondX:
            xValues = [firstX for x in range(1000)]
        elif firstX < secondX:
            xValues = range(firstX, secondX+1, 1)
        else:
            xValues = range(firstX, secondX-1, -1)

        if firstY == secondY:
            yValues = [firstY for x in range(1000)]
        elif firstY < secondY:
            yValues = range(firstY, secondY+1, 1)
        else:
            yValues = range(firstY, secondY-1, -1)

        for x, y in zip(xValues, yValues):
            markPoint(grid, x, y)

    return len([x for x in grid.getAllPoints() if x.data > 1]) #grid.__str__() #

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