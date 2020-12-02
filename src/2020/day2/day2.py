import common as com

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def isValidPassword(line:str, part1:bool):
    policy, password = line.split(':')
    password = password.strip()
    interval, letter = policy.split(' ')
    minimum, maximum = interval.split('-')
    minimum = int(minimum)
    maximum = int(maximum)
    if part1:
        difference = password.__len__() - password.replace(letter, '').__len__()
        if minimum <= difference <= maximum:
            print(password + " was valid according to: " + policy)
            return True
        return False
    else:
        if (password[minimum-1] == letter) ^ (password[maximum-1] == letter):
            return True
        return False

def Part1(lines):
    total = 0
    for line in lines:
        if isValidPassword(line, True):
            total += 1
    return total

def Part2(lines):
    total = 0
    for line in lines:
        if isValidPassword(line, False):
            total += 1
    return total

if test:
    lines = com.readFile("test.txt")
else:
    print(puzzle.input_data)
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