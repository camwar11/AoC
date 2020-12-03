import common as com

test = False
part1 = True
part2 = True
puzzle = com.PuzzleWithTests()

def countTrees(lines, xStep, yStep):
    x = y = 0
    newLines = list()
    for line in lines:
        newLines.append(line.strip())
    xLength = newLines[0].__len__()
    yLength = newLines.__len__()
    treesFound = 0
    while True:
        x = (x + xStep) % xLength
        y = y + yStep
        if y >= yLength:
            break
        possibleTree = newLines[y][x]
        if possibleTree == "#":
            treesFound += 1
    return treesFound

def Part1(lines):
    return countTrees(lines, 3, 1)

def Part2(lines):
    return countTrees(lines, 1, 1) * countTrees(lines, 3, 1) * countTrees(lines, 5, 1) * countTrees(lines, 7, 1) * countTrees(lines, 1, 2)

if test:
    lines = com.readFile("test.txt", "!")
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