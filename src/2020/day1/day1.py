import common as com

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def Part1(lines):
    values = list()
    for line in lines:
        new_value = int(line)
        for value in values:
            if new_value + value == 2020:
                return new_value * value
        values.append(new_value)
    return None

def Part2(lines):
    values = list()
    for line in lines:
        new_value = int(line)
        for value in values:
            for value2 in values:
                if new_value + value + value2 == 2020:
                    return new_value * value * value2
        values.append(new_value)
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