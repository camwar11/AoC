import common as com

def Part1(lines):
    lineSplit = lines[0].split('-')
    minimum = int(lineSplit[0])
    maximum = int(lineSplit[1])
    validValues = [i for i in range(minimum, maximum + 1, 1) if isValid(i, False)]
    print(len(validValues))

def Part2(lines):
    lineSplit = lines[0].split('-')
    minimum = int(lineSplit[0])
    maximum = int(lineSplit[1])
    validValues = [i for i in range(minimum, maximum + 1, 1) if isValid(i, True)]
    print(len(validValues))

def isValid(integer, partTwo):
    asStr = str(integer)
    previous = -1
    repeat = False
    repeatNum = 0
    for i in [int(asStr[i]) for i in range(len(asStr))]:
        if i < previous:
            return False
        if i == previous:
            if partTwo:
                repeatNum = repeatNum + 1
            else:
                repeat = True
        else:
            if partTwo and repeatNum is 1:
                repeat = True
            repeatNum = 0
        previous = i
    return repeat or (partTwo and repeatNum is 1)

test = False
part1 = False
part2 = True

file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file)

if part1:
    Part1(lines)

if part2:
    Part2(lines)