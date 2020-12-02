import common as com

test = False
part1 = True
part2 = False

def Part1(lines):
    compy = com.intCode(lines[0])
    compy.RunIntCodeComputer(debug=False)

def Part2(lines):
    pass

file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file)

if part1:
    Part1(lines)

if part2:
    Part2(lines)