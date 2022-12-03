from __future__ import annotations
from typing import List, Optional, Set, Tuple, Union
import common as com
from common.tree import tree, tree_node
import math
import copy

test = True
part1 = True
part2 = False
puzzle = com.PuzzleWithTests()
        
def Part1(lines: List[str]):

    for line in lines:
        a = 0

    return None

def Part2(lines):
    for line in lines:
        a = 0

    return None

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