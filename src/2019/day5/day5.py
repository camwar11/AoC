import common as com

test = False
part1 = False
part2 = True

def Part1(lines):
    noun = None
    verb = None
    computer = com.intCode(lines[0])
    computer.RunIntCodeComputer(noun, verb, False)
        

def Part2(lines):
    noun = None
    verb = None
    computer = com.intCode(lines[0])
    computer.RunIntCodeComputer(noun, verb, False)

file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file)

if part1:
    Part1(lines)

if part2:
    Part2(lines)