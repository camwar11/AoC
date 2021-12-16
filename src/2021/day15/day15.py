from typing import List, Set
import common as com
from common.cartesianGrid import CartesianGrid, Point, parse_to_grid
from common.graph import Graph

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def edgeWeightFcn(start: Point, end: Point):
    return end.data

def dupeGrid(grid: CartesianGrid):
    currentPoints = grid.getAllPoints(True)
    maxX = max([point.x for point in currentPoints]) + 1
    maxY = max([point.x for point in currentPoints]) + 1

    for xDupe in range(1,5):
        for point in currentPoints:
            newData = point.data + xDupe
            if newData >= 10:
                newData = (newData % 10) + 1
            newPoint = Point((xDupe * maxX) + point.x, point.y, newData)
            grid.addPoint(newPoint)
    
    currentPoints = grid.getAllPoints(True)
    for yDupe in range(1,5):
        for point in currentPoints:
            newData = point.data + yDupe
            if newData >= 10:
                newData = (newData % 10) + 1
            newPoint = Point(point.x, (yDupe * maxY) + point.y, newData)
            grid.addPoint(newPoint)


def Part1(lines: List[str]):
    grid = CartesianGrid(flipOutput=True)
    parse_to_grid(lines, grid, lambda x: int(x))
    
    graph = Graph.parse_from_grid(grid, edgeWeightFinder= edgeWeightFcn)

    allPoints = grid.getAllPoints(True)
    start = allPoints[0]
    end = allPoints[-1]
    path, distance = graph.dijsktra(start, end)
    return distance

def Part2(lines):
    grid = CartesianGrid(flipOutput=True)
    parse_to_grid(lines, grid, lambda x: int(x))

    dupeGrid(grid)

    print(grid)

    
    graph = Graph.parse_from_grid(grid, edgeWeightFinder= edgeWeightFcn)


    allPoints = grid.getAllPoints(True)
    start = allPoints[0]
    end = allPoints[-1]
    path, distance = graph.dijsktra(start, end)
    return distance

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