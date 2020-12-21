import common as com
from math import factorial

test = True
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def Part1(lines):
    minVoltageGap = 1
    maxVoltageGap = 3
    voltages = list()
    for line in lines:
        voltages.append(int(line.strip()))
    
    sortedAdapters = sorted(voltages)
    threeGaps = 0
    oneGaps = 0
    prev = 0
    for adapter in sortedAdapters:
        diff = adapter - prev
        if diff == 3:
            threeGaps += 1
        elif diff == 1:
            oneGaps +=1
        prev = adapter
    return oneGaps * (threeGaps+1)

def runTest(numbersInARow: int):
    for i in range(1, numbersInARow-2):
        for j in range(1, numbersInARow-2):


def getCombinations(oneDiffssInARow: int):
    # 1
    # 12
    # 123
    # 1_3
    # 1234
    # 1_34
    # 1__4
    # 12_4
    # 12345
    # 1_345
    # 1__45
    # 12_45
    # 12__5
    # 123_5
    # 123456
    # 1_3456
    # 1__456
    # 12_456
    # 12__56
    # 123_56
    # 123__6
    # 1234_6
    # 1234567
    # 1_34567
    # 1__4567
    # 12_4567
    # 12__567
    # 123_567
    # 123__67
    # 1234_67
    # 1234__7
    # 12345_7


    frontAndBackConstant = 2
    allThere = 1
    combinationsWithoutSingleNumber = 2
    numbersInThisChain = oneDiffssInARow + 1 # add one because there is one more number than diffs
    if(numbersInThisChain < 3):
        return 1
    return ((numbersInThisChain - frontAndBackConstant) * combinationsWithoutSingleNumber) + allThere

def Part2(lines):
    minVoltageGap = 1
    maxVoltageGap = 3
    voltages = list()
    for line in lines:
        voltages.append(int(line.strip()))
    
    sortedAdapters = sorted(voltages)
    threeGaps = 0
    oneGaps = 0
    prev = 0
    diffs = list()
    for adapter in sortedAdapters:
        diff = adapter - prev
        diffs.append(diff)
        prev = adapter
    total = 1
    onesInARow = 0
    for diff in diffs:
        if diff == 1:
            onesInARow += 1
        else:
            if onesInARow != 0:
                total *= getCombinations(onesInARow)
                onesInARow = 0
    return total

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
        print("Part1 test result: " + str(part1Answer))
    else:
        puzzle.answer_a = part1Answer
            

if part2:
    part2Answer = Part2(lines)
    if part2Answer is None:
        print("Returned None for part2")
    elif test:
        print("Part2 test result: " + str(part2Answer))
    else:
        puzzle.answer_b = part2Answer