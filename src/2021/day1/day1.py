import common as com

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def Part1(lines):
    prev = 9999999
    count = 0
    for line in lines:
        new = int(line)
        if new > prev:
            count += 1
        prev = new
    return count

def Part2(lines):
    prev = 9999999
    window = list()
    count = 0
    for line in lines:
        new = int(line)
        window.append(new)
        if len(window) == 3:
            value = sum(window)
            if(value > prev):
                count += 1
            prev = value
            window.pop(0)

        
    return count

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