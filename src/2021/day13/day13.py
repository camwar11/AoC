from typing import List, Set
import common as com
from common.cartesianGrid import CartesianGrid

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def foldGrid(grid: CartesianGrid, axis, line):
    pointsToRemove = list()
    for point in grid.getAllPoints(True):
        if axis == 'y' and point.y > line:
            # fold up by finding the distance from the line and changing the y coord to an
            # equal distance above the line
            diff = point.y - line
            if grid.getPoint(point.x, line - diff):
                # remove this point because another one already exists
                pointsToRemove.append(point)
            else:
                grid.movePointTo(point, point.x, line - diff)
        
        if axis == 'x' and point.x > line:
            # fold left by finding the distance from the line and changing the x coord to an
            # equal distance left of the line
            diff = point.x - line
            if grid.getPoint(line - diff, point.y):
                # remove this point because another one already exists
                pointsToRemove.append(point)
            else:
                grid.movePointTo(point, line - diff, point.y)
        
    for point in pointsToRemove:
        grid.removePoint(point)


def doOrigami(lines: List[str], isPart1):
    parseFolds = False
    folds = list()
    grid = com.CartesianGrid(flipOutput=True)
    for line in lines:
        if line.strip() == "":
            parseFolds = True
            continue
        if parseFolds:
            axis, num = line.strip().split(' ')[2].split('=')
            folds.append((axis, int(num)))
        else:
            x, y = line.strip().split(',')
            point = com.Point(int(x), int(y), '#')
            grid.addPoint(point)
    
    for axis, lineNum in folds:
        foldGrid(grid, axis, lineNum)
        # part 1 is just one fold
        if isPart1:
            break

    if part1:
        return len(grid.getAllPoints())
    else:
        # Easier to just print out the grid and read it to submit
        print(grid)
        return None


def Part1(lines: List[str]):
    return doOrigami(lines, True)


def Part2(lines):        
    return doOrigami(lines, False)



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