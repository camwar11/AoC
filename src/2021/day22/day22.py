from __future__ import annotations
from typing import List, Optional, Set, Tuple, Union
import common as com

test = True
part1 = True
part2 = False
puzzle = com.PuzzleWithTests()

class Cuboid(object):
    def __init__(self, on: bool, x1:int, x2:int, y1:int, y2:int, z1:int, z2:int) -> None:
        super().__init__()
        self.on = on
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2
    
    def volume(self):
        length = abs(self.x2 - self.x1)
        width = abs(self.y2 - self.y1)
        height = abs(self.z2 - self.z1)
        return length * width * height

    def overlaps(self, other: Cuboid):
        if self.x1 <= other.x1 and self.x2 < self.x1:
            return False
        if self.y1 <= other.y1 and self.y2 < self.y1:
            return False
        if self.z1 <= other.z1 and self.z2 < self.z1:
            return False


def Part1(lines: List[str]):
    for line in lines:
        position = int(line.split(' ')[-1].strip())
        playerPositions.append(position)
        playerScores.append(0)

    return None

def Part2(lines: List[str]):
    playerPositions = list()
    playerScores = list()
    winners = list()
    for line in lines:
        position = int(line.split(' ')[-1].strip())
        playerPositions.append(position)
        playerScores.append(0)
        winners.append(0)

    playerNum = 0
    for roll in quantumRollCounts:
        count = quantumRollCounts[roll]
        childWinners = playQuantumGame(playerNum, roll, tuple(playerPositions), tuple(playerScores))
        winners[0] += childWinners[0] * count
        winners[1] += childWinners[1] * count
    return max(winners)

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