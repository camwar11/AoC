from __future__ import annotations
import functools
from typing import List, Optional, Set, Tuple, Union
import common as com
import copy

test = True
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
def getWinners(playerNum: int, turnRollTotal: int, positions: Tuple[int, int], scores: Tuple[int, int]):
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
    winner[0] = 0
    winner[1] = 0
    while True:
        if scoresList[playerNum] >= 21:
            winner[playerNum] += quantumRollCounts[turnRollTotal]
            return tuple(winner)
        else:
            playerNum = (playerNum + 1) % 2
            for roll in quantumRollCounts:
                count = quantumRollCounts[roll]
                childWinner = getWinners(playerNum, roll, tuple(positionsList), tuple(scoresList))
                winner[0] += childWinner[0]
                winner[1] += childWinner[1] 




def playQuantumGame(playerNum: int, turnRollTotal: int, position0: int, position1: int, scores: List[int], winners: List[int]):
    numDieRolls = 3
    while(True):
        if turnRollNum < 3:
            for dieRoll in range(numDieRolls):
                playQuantumGame(playerNum, turnRollNum + 1, turnRollTotal + dieRoll, copy.copy(positions), copy.copy(scores), winners)
        elif turnRollNum == 3:
            move_and_score(playerNum, turnRollTotal, positions, scores)
            if scores[playerNum] >= 21:
                winners[playerNum] += 1
                return
            playerNum = (playerNum + 1) % 2
            turnRollNum = 1
            turnRollTotal = 0

def Part2(lines):
    playerPositions = list()
    playerScores = list()
    winners = list()
    for line in lines:
        position = int(line.split(' ')[-1].strip())
        playerPositions.append(position)
        playerScores.append(0)
        winners.append(0)

    numDieRolls = 3
    dieRoll = 0
    playerNum = 0
    numberOfRollsSoFar = 0
    playQuantumGame(playerNum, 0, 0, playerPositions, playerScores, winners)
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