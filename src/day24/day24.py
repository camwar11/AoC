import common as com

test = True
part1 = True
part2 = False

def Part1(lines):
    for line in lines:
        for char in line:
            pass
        pass

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