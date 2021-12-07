import common as com
from common.cartesianGrid import CartesianGrid
from common.cartesianGrid import Point

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def SimFish(lines: list, numDays: int):
    timers = [int(x) for x in lines.pop(0).split(',')]
    daysTilSpawn = [0 for x in range(9)]
    for timer in timers:
        daysTilSpawn[timer] += 1
    for day in range(numDays):
        spawned = daysTilSpawn.pop(0)
        # The new fish are set to 8
        daysTilSpawn.append(spawned)
        # The initial fish get set to 6
        daysTilSpawn[6] += spawned

        #print(daysTilSpawn)
    
    return sum(daysTilSpawn)

def Part1(lines: list):
    return SimFish(lines, 80)

def Part2(lines):        
    return SimFish(lines, 256)

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