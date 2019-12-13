import common as com

test = False
part1 = False
part2 = True

def Part1(lines):
    x = None
    y = None
    tid = None
    grid = com.CartesianGrid(' ')
    numBlocks = 0

    def outputCallback(output):
        nonlocal x, y, tid, grid, numBlocks
        if x is None:
            x = output
        elif y is None:
            y = output
        elif tid is None:
            tid = output
            point = com.Point(x, y, tid)
            if tid == 2:
                numBlocks += 1
            grid.addPoint(point)
            x = None
            y = None
            tid = None


    compy = com.intCode(lines[0], printOutput=False, hasOutputCallback=outputCallback)
    compy.RunIntCodeComputer()
    print(numBlocks)

def cellStr(cell):
    if cell.data == 0:
        return ' '
    elif cell.data == 1:
        return 'X'
    elif cell.data == 2:
        return '^'
    elif cell.data == 3:
        return '_'
    elif cell.data == 4:
        return '.'

def Part2(lines):
    x = None
    y = None
    tid = None
    grid = com.CartesianGrid(' ', cellOutputStrFcn=cellStr)
    score = 0

    ball = None
    paddle = None

    def inputCallback():
        nonlocal grid, ball, paddle
        #print(grid)
        if ball.x == paddle.x:
            return 0
        elif ball.x < paddle.x:
            return -1
        else:
            return 1

    def outputCallback(output):
        nonlocal x, y, tid, grid, score, ball, paddle
        if x is None:
            x = output
        elif y is None:
            y = output
        elif tid is None:
            tid = output
            point = com.Point(x, y, tid)
            if tid > 4 and x == -1 and y == 0:
                score = tid
            else:
                if tid == 4:
                    ball = point
                elif tid == 3:
                    paddle = point
                grid.addPoint(point)
            x = None
            y = None
            tid = None


    compy = com.intCode(lines[0], printOutput=False, hasOutputCallback=outputCallback, needsInputCallback=inputCallback)
    compy.initialMemory[0] = 2
    compy.RunIntCodeComputer()
    print(score)

file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file)

if part1:
    Part1(lines)

if part2:
    Part2(lines)