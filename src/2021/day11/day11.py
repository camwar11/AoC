from typing import Set
import common as com
from common.cartesianGrid import Point

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def processFlash(grid: com.CartesianGrid, point: Point, alreadyFlashed: Set[Point]):
    if point in alreadyFlashed:
        return
    alreadyFlashed.add(point)

    for adjacentPoint in grid.getAdjacentPoints(point.x, point.y, True):
        adjacentPoint.data += 1
        if adjacentPoint.data > 9:
            processFlash(grid, adjacentPoint, alreadyFlashed)

def runSim(lines, part1 = True):
    total = 0
    grid = com.CartesianGrid(flipOutput=True)
    numOctopi = 0
    y = 0
    steps = 100
    if not part1:
        steps = 10000000
    for line in lines:
        x = 0
        for char in line.strip():
            point = Point(x, y, int(char))
            grid.addPoint(point)
            numOctopi += 1
            x += 1
        y += 1
    
    for step in range(steps):
        alreadyFlashed = set()
        for point in grid.getAllPoints(lowYFirst=True):
            if point in alreadyFlashed:
                continue
            point.data += 1
            if point.data > 9:
                processFlash(grid, point, alreadyFlashed)
        total += len(alreadyFlashed)
        for point in alreadyFlashed:
            point.data = 0
        if not part1 and len(alreadyFlashed) == numOctopi:
            return step + 1
        alreadyFlashed.clear()
    return total

def Part1(lines: list):
    return runSim(lines)

def Part2(lines):        
    return runSim(lines, False)


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