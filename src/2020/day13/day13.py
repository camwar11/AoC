import common as com

test = False
part1 = True
part2 = False
puzzle = com.PuzzleWithTests()

def Part1(lines):
    timestamp = int(lines[0])
    busses = list()
    for bus in lines[1].split(','):
        if bus.strip() == 'x':
            continue
        busses.append(int(bus))
    
    bestBus = 0
    bestWait = 99999999999999999999
    for bus in busses:
        wait = bus - (timestamp % bus)
        if wait < bestWait:
            bestWait = wait
            bestBus = bus
    return bestBus * bestWait

def Part2(lines):
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