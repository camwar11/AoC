import common as com

test = False
part1 = True
part2 = True
puzzle = com.PuzzleWithTests()

def Part1(lines):
    console = com.gameConsole()
    output, haltedNormally = console.runProgram(lines)
    return output

def Part2(lines):
    console = com.gameConsole()
    haltedNormally = False
    idx = 0
    while not haltedNormally:
        newLines = list(lines)
        if lines[idx].startswith('jmp'):
            newLines[idx] = newLines[idx].replace('jmp', 'nop')
        elif lines[idx].startswith('nop'):
            newLines[idx] = newLines[idx].replace('nop', 'jmp')
        else:
            idx += 1
            continue
        output, haltedNormally = console.runProgram(newLines)
        idx += 1
    return output

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