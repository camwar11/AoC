import common as com

test = False
part1 = True
part2 = False

def newValue(point: com.Point, grid: com.CartesianGrid):
    directions = [grid.UP, grid.DOWN, grid.LEFT, grid.RIGHT]
    adjacent = 0
    for direction in directions:
        check = grid.getPoint(*(point + direction))
        if check is not None and check.data == '#':
            adjacent += 1    
    if point.data == '#':
        if adjacent != 1:
            return '.'
        return '#'
    else:
        if adjacent == 1 or adjacent == 2:
            return '#'
        return '.'

def Part1(lines):
    x = 0
    y = 4
    grid = com.CartesianGrid()
    for line in lines:
        for char in line.strip():
            point = com.Point(x, y, char)
            grid.addPoint(point)
            x += 1
        y -= 1
        x = 0
    
    minute = 1
    states = {}
    while True:
        changes = []
        for point in grid.getAllPoints():
            if newValue(point, grid) != point.data:
                changes.append(point)
        for change in changes:
            if change.data == '#':
                change.data = '.'
            else:
                change.data = '#'
        print(minute, '\n', grid, sep='')
        state = tuple(i.data for i in grid.getAllPoints())
        foundState = states.get(state)
        if foundState is not None:
            break
        states[state] = True
        minute += 1
    biodiversity = 0
    powerOfTwo = 1
    for point in grid.getAllPoints():
        if point.data == '#':
            biodiversity += powerOfTwo
        powerOfTwo *= 2
    print(biodiversity)

def Part2(lines):
    pass

file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file, '!')

if part1:
    Part1(lines)

if part2:
    Part2(lines)