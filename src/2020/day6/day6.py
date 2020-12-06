import common as com

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def getYessesPart1(group):
    yesses = dict()
    for line in group:
        for char in line:
            yesses[char] = True
    count = 0
    for char in yesses:
        count += 1
    return count

def getYessesPart2(group):
    yesses = dict()
    people = 0
    for line in group:
        people += 1
        for char in line:
            if char in yesses:
                yesses[char] += 1 
            else:
                yesses[char] = 1
    count = 0
    for char in yesses:
        if yesses[char] == people:
            count += 1
    return count


def Part1(lines):
    total = 0
    group = list()
    for line in lines:
        if line.strip() == '':
            total += getYessesPart1(group)
            group.clear()
        else:
            group.append(line.strip())
    total += getYessesPart1(group)
    return total

def Part2(lines):
    total = 0
    group = list()
    for line in lines:
        if line.strip() == '':
            total += getYessesPart2(group)
            group.clear()
        else:
            group.append(line.strip())
    total += getYessesPart2(group)
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