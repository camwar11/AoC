import common as com

test = False
part1 = True
part2 = False

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