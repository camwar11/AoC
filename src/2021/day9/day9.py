from math import prod
from typing import Set
import common as com

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def getLowPoints(grid):
    lowPoints = list()
    for point in grid.getAllPoints():
        adjacentPoints = grid.getAdjacentPoints(point.x, point.y)
        isLowPoint = True
        for adjacentPoint in adjacentPoints:
            if point.data >= adjacentPoint.data:
                isLowPoint = False
                break
        if isLowPoint:
            lowPoints.append(point)
    return lowPoints

def makeCaveGrid(lines):
    grid = com.CartesianGrid(flipOutput=True)
    y = 0
    for line in lines:
        x = 0
        for char in line.strip():
            point = com.Point(x, y, int(char))
            grid.addPoint(point)
            x += 1
        y += 1
    return grid

def Part1(lines: list):
    grid = makeCaveGrid(lines)

    lowPoints = getLowPoints(grid)
    
    return sum([x.data + 1 for x in lowPoints])

def findBasin(grid: com.CartesianGrid, point: com.Point, basin: Set[com.Point]):
    if point.data == 9 or point in basin:
        return

    basin.add(point)

    adjacents = grid.getAdjacentPoints(point.x, point.y)
    for adjacent in adjacents:
        findBasin(grid, adjacent, basin)
    
    return

def Part2(lines):        
    grid = makeCaveGrid(lines)
    lowPoints = getLowPoints(grid)
    basins = list()

    for lowPoint in lowPoints:
        basin = set()
        findBasin(grid, lowPoint, basin)
        basins.append(basin)

    biggest = sorted(map(lambda x: len(x), basins))[-3:]
    return prod(biggest)

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