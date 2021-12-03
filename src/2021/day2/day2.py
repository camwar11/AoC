import common as com

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def Part1(lines):
    point = com.Point(0, 0, None)
    for line in lines:
        direction, amount = line.split(' ')
        amount = int(amount)
        if(direction == 'forward'):
            point.x += amount
        if(direction == 'up'):
            point.y -= amount
        if(direction == 'down'):
            point.y += amount
    return point.x * point.y

def Part2(lines):
    point = com.Point(0, 0, None)
    aim = 0
    for line in lines:
        direction, amount = line.split(' ')
        amount = int(amount)
        if(direction == 'forward'):
            point.x += amount
            point.y += aim * amount
        if(direction == 'up'):
            aim -= amount
        if(direction == 'down'):
            aim += amount
    return point.x * point.y

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