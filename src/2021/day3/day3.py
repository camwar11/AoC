from logging import fatal
import common as com

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def Part1(lines):
    zeroes = list()
    ones = list()
    first = True
    for line in lines:
        i = 0
        for char in line.strip():
            if first:
                zeroes.append(0)
                ones.append(0)
            if char == '0':
                zeroes[i] += 1
            elif char == '1':
                ones[i] += 1
            i += 1
        first = False
    
    gamma = ''
    epsilon = ''
    for i in range(len(zeroes)):
        if zeroes[i] > ones[i]:
            gamma += '0'
            epsilon += '1'
        else:
            gamma += '1'
            epsilon += '0'
    
    return int(gamma, 2) * int(epsilon, 2)

def filterSet(values: set, index, mostCommon):
    zeroes = set()
    ones = set()
    for value in values:
        if value[index] == '0':
            zeroes.add(value)
        else:
            ones.add(value)
    if mostCommon:
        if len(zeroes) > len(ones):
            toRemove = zeroes
        else:
            toRemove = ones
    else:
        if len(zeroes) > len(ones):
            toRemove = ones
        else:
            toRemove = zeroes
            
    for remove in toRemove:
            values.remove(remove)

def Part2(lines):
    mostCommon = set([x.strip() for x in lines])
    leastCommon = set(mostCommon)

    for i in range(len(next(iter(mostCommon)))):
        if len(mostCommon) > 1:
            filterSet(mostCommon, i, True)
        if len(leastCommon) > 1:
            filterSet(leastCommon, i, False)
    
    return int(next(iter(mostCommon)), 2) * int(next(iter(leastCommon)), 2)





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