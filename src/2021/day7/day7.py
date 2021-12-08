from typing import ByteString
import common as com
from common.tree import tree

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def getSumDifferences(nums: list[int], subtrahend):
    diffs = list(map(lambda x: abs(x - subtrahend), nums))
    return sum(diffs)

def getPart2FuelUsage(nums: list[int], subtrahend):
    diffs = list(map(lambda x: int(com.sumSeries(abs(x - subtrahend))), nums))
    return sum(diffs)

def minimizeDifferences(nums: list[int], differenceSelector):
    minimum = 99999999999999999999
    low = nums[0]
    high = nums[len(nums) - 1]
    while(low < high):
        currentTest = (low + high) // 2
        result = differenceSelector(nums, currentTest)
        minimum = min(result, minimum)

        if differenceSelector(nums, currentTest + 1) < result:
            low = currentTest + 1
        elif differenceSelector(nums, currentTest - 1) < result:
            high = currentTest - 1
        else:
            minimum = min(differenceSelector(nums, currentTest), minimum)
            break
    
    if low == high:
            minimum = min(differenceSelector(nums, low), minimum)
    return minimum

def Part1(lines: list):
    numbers = sorted([int(x) for x in lines.pop().split(',')])
    return minimizeDifferences(numbers, getSumDifferences)

def Part2(lines):        
    numbers = sorted([int(x) for x in lines.pop().split(',')])
    return minimizeDifferences(numbers, getPart2FuelUsage)

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