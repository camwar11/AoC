import common as com

test = False
part1 = False
part2 = True

def Part1(lines):
    grid = com.CartesianGrid()
    currentX = 0
    currentY = 0

    def outputCallback(output):
        nonlocal grid, currentX, currentY
        value = chr(output)        
        if output == 10:
            currentY += 1
            currentX = 0
            print('\n', end='')
        else:
            currentPoint = com.Point(currentX, currentY, value)
            grid.addPoint(currentPoint)
            currentX += 1
            print(value, end='')

    intCode = com.intCode(lines[0], False, hasOutputCallback=outputCallback)
    intCode.RunIntCodeComputer()

    total = 0
    for point in grid.getAllPoints():
        if point.data == '#':
            up = grid.getPoint(point.x, point.y + 1)
            if up is not None and up.data == '#':
                down = grid.getPoint(point.x, point.y - 1)
                if down is not None and down.data == '#':
                    left = grid.getPoint(point.x - 1, point.y)
                    if left is not None and left.data == '#':
                        right = grid.getPoint(point.x + 1, point.y)
                        if right is not None and right.data == '#':
                            total += (point.x * point.y)
    print(total)

def toAsciiInts(string):
    return [ord(i) for i in string]

def Part2(lines):
    grid = com.CartesianGrid()
    currentX = 0
    currentY = 0
    gridFinished = False

    def outputCallback(output):
        nonlocal grid, currentX, currentY, gridFinished
        if not gridFinished:
            if output > 256:
                print(output)
                return
            value = chr(output)        
            if output == 10:
                currentY += 1
                currentX = 0
                print('\n', end='')
            else:
                currentPoint = com.Point(currentX, currentY, value)
                grid.addPoint(currentPoint)
                currentX += 1
                print(value, end='')
        else:
            print(output)
    
    inputNum = 0
    localInputNum = 0
    def inputCallback():
        nonlocal inputNum, gridFinished,localInputNum
        value = None
        #gridFinished = True
        if inputNum == 0: # main
            value = toAsciiInts('A,C,A,C,B,B,C,B,C,A\n')
        elif inputNum == 1: # A
            value = toAsciiInts('R,12,L,8,R,12\n')
        elif inputNum == 2: # B
            value = toAsciiInts('R,8,L,8,R,8,R,4,R,4\n')
        elif inputNum == 3: # C
            value = toAsciiInts('R,8,R,6,R,6,R,8\n')
        elif inputNum == 4: # video
            value = toAsciiInts('n\n')

        character = value[localInputNum]
        if character == 10:
            inputNum += 1
            localInputNum = 0
        else:
            localInputNum += 1
        return character

    stringList = list(lines[0])
    stringList[0] = '2'
    intCode = com.intCode(''.join(stringList), False, needsInputCallback=inputCallback, hasOutputCallback=outputCallback)
    intCode.RunIntCodeComputer()

file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file)

if part1:
    Part1(lines)

if part2:
    Part2(lines)