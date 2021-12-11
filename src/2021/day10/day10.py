from math import prod
from typing import Set
import common as com
from common.advanced_math import median

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

startingAndPointsByEnding = {
    ')': ('(', 3),
    ']': ('[', 57),
    '}': ('{', 1197),
    '>': ('<', 25137)
}

autoCompletePointsByEnding = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

endingsByStarting = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

def findSyntaxErrorValue(line: str) -> int:
    stack = list()
    for char in line.strip():
        if char not in startingAndPointsByEnding:
            stack.append(char)
        else:
            starting, points = startingAndPointsByEnding[char]
            previousStarter = stack.pop()
            if starting != previousStarter:
                return points
    return 0

def findAutoCompleteStringAndScore(line: str) -> str:
    stack = list()
    autoComplete = ''
    for char in line.strip():
        if char not in startingAndPointsByEnding:
            stack.append(char)
        else:
            starting, points = startingAndPointsByEnding[char]
            previousStarter = stack.pop()

            if starting != previousStarter:
                # invalid line
                return None, None
    
    score = 0
    stack.reverse()
    for char in stack:
        ending = endingsByStarting[char]
        autoComplete += ending
        score *= 5
        score += autoCompletePointsByEnding[ending]

    return autoComplete, score


def Part1(lines: list):
    total = 0
    for line in lines:
        total += findSyntaxErrorValue(line)
    return total

def Part2(lines):        
    scores = list()
    for line in lines:
        autoComplete, score = findAutoCompleteStringAndScore(line)
        if autoComplete:
            scores.append(score)
    return int(median(scores, True))

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