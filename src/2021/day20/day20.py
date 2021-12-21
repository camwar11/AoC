from __future__ import annotations
from typing import List, Optional, Set, Tuple, Union
import common as com

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def enhance(picture: com.CartesianGrid, algorithm: str, outsideValue: str):
    newPicture = com.CartesianGrid(flipOutput=True)
    for point in picture.getAllPoints(True):
        lookup = ''
        pointsToCheck = picture.getAdjacentPoints(point.x, point.y, True, True)
        pointsToCheck.append(point)
        pointsToCheck = sorted(pointsToCheck, key= lambda x: (x.y, x.x))
        if len(pointsToCheck) != 9:
            test = 0
        for x in pointsToCheck:
            data = x.data
            if data is None:
                data = outsideValue
            if data == '#':
                lookup += '1'
            else:
                lookup += '0'
        newValue = algorithm[int(lookup, 2)]
        newPicture.addPoint(com.Point(point.x, point.y, newValue))
    return newPicture


        
def Part1(lines: List[str]):
    return runEnhancementCalcs(lines, 2)

def runEnhancementCalcs(lines, numEnhancements):
    enhancementAlgorithm = None
    picture = com.CartesianGrid(flipOutput=True)
    squareSize = 0
    y = 0
    for line in lines:
        stripped = line.strip()
        if stripped == '':
            continue
        if enhancementAlgorithm is None:
            enhancementAlgorithm = stripped
            continue
        x = 0
        for char in stripped:
            point = com.Point(x, y, char)
            picture.addPoint(point)
            x += 1
        y += 1
        squareSize = max(squareSize, y)
    
    print(picture)
    extrasToAdd = 1
    outsideValue = '.'
    for i in range(numEnhancements):
        #print('Before')
        #print(picture)
        picture.moveAllPoints(extrasToAdd, extrasToAdd)
        squareSize += (extrasToAdd * 2)
        for x in range(squareSize):
            for extra in range(extrasToAdd):
                picture.addPoint(com.Point(x, extra, outsideValue))
                picture.addPoint(com.Point(extra, x, outsideValue))
                picture.addPoint(com.Point(squareSize - (extra + 1), x, outsideValue))
                picture.addPoint(com.Point(x, squareSize - (extra + 1), outsideValue))

        #print('After Shift')
        #print(picture)
        picture = enhance(picture, enhancementAlgorithm, outsideValue)
        #print('After Enhance')
        #print(picture)

        outsideValue = enhancementAlgorithm[0]
        if i % 2 != 0 and outsideValue == '#':
            outsideValue = enhancementAlgorithm[-1]

    print(picture)
    total = 0
    for point in picture.getAllPoints():
        if point.data == '#':
            total += 1
    return total

def Part2(lines):
    return runEnhancementCalcs(lines, 50)

if test:
    lines = com.readFile("test.txt", '-')
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