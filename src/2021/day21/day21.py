from __future__ import annotations
import functools
from typing import List, Optional, Set, Tuple, Union
import common as com
import copy

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

# Total counts of each roll added together
quantumRollCounts = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1
}

def deterministic_die(prev):
    next = prev + 1
    if next == 101:
        next = 1
    return next

def move_and_score(playerNum: int, rollTotal: int, positions: List[int], scores:List[int]):
    currentLocation = positions[playerNum]
    # Subtract 1 from the position so we can use mod 10, then add 1 back at the end
    currentLocation -= 1
    currentLocation += rollTotal
    currentLocation = (currentLocation % 10) + 1
    scores[playerNum] += currentLocation
    positions[playerNum] = currentLocation

def Part1(lines: List[str]):
    playerPositions = list()
    playerScores = list()
    for line in lines:
        position = int(line.split(' ')[-1].strip())
        playerPositions.append(position)
        playerScores.append(0)

    numDieRolls = 3
    dieRoll = 0
    playerNum = 0
    numberOfRollsSoFar = 0
    while(True):
        rollTotal = 0
        for rollNum in range(numDieRolls):
            dieRoll = deterministic_die(dieRoll)
            rollTotal += dieRoll
        numberOfRollsSoFar += numDieRolls
        move_and_score(playerNum, rollTotal, playerPositions, playerScores)
        if playerScores[playerNum] >= 1000:
            losingScore = playerScores[(playerNum + 1) % 2]
            break
        playerNum = (playerNum + 1) % 2
    return losingScore * numberOfRollsSoFar

@functools.lru_cache(None)
def playQuantumGame(playerNum: int, turnRollTotal: int, positions: Tuple[int, int], scores: Tuple[int, int]):
    global quantumRollCounts
    positionsList = list(positions)
    scoresList = list(scores)
    # Subtract 1 from the position so we can use mod 10, then add 1 back at the end
    position = positionsList[playerNum]
    position -= 1
    position += turnRollTotal
    position = (position % 10) + 1
    positionsList[playerNum] = position
    scoresList[playerNum] += position
    winner = list()
    winner.append(0)
    winner.append(0)
    if scoresList[playerNum] >= 21:
        winner[playerNum] += 1
        return tuple(winner)
    else:
        playerNum = (playerNum + 1) % 2
        for roll in quantumRollCounts:
            count = quantumRollCounts[roll]
            childWinners = playQuantumGame(playerNum, roll, tuple(positionsList), tuple(scoresList))
            winner[0] += childWinners[0] * count
            winner[1] += childWinners[1] * count
        return tuple(winner)

def Part2(lines):
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