import common as com

test = False
part1 = False
part2 = True

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

def makeBlankGrid():
    grid = com.CartesianGrid()
    for y in range(5):
        for x in range(5):
            point = com.Point(x, y, '.')
            grid.addPoint(point)
            x += 1
        y += 1
        x = 0
    return grid

grids = {}
def getGridAtLevel(gridLevel: int):
    global grids
    existing = grids.get(gridLevel)
    after_existing = grids.get(gridLevel + 1)
    before_existing = grids.get(gridLevel - 1)
    
    if after_existing is None:
        grids[gridLevel+1] = makeBlankGrid()
    if before_existing is None:
        grids[gridLevel-1] = makeBlankGrid()
    if existing is not None:
        return existing
    existing = makeBlankGrid()
    grids[gridLevel] = existing
    return existing

def getPoints(point: com.Point, grid: com.CartesianGrid, gridLevel: int, direction):
    global grids

    check = grid.getPoint(*(point + direction))
    if check is None:
        outside = getGridAtLevel(gridLevel - 1)
        bottom = [2, 1]
        top = [2, 3]
        leftSide = [1, 2]
        rightSide = [3, 2]
        pointToGet = {}
        pointToGet[tuple(grid.UP)] = top
        pointToGet[tuple(grid.DOWN)] = bottom
        pointToGet[tuple(grid.LEFT)] = leftSide
        pointToGet[tuple(grid.RIGHT)] = rightSide
        return [outside.getPoint(*pointToGet[tuple(direction)])]
    elif check.x == 2 and check.y == 2:
        inside = getGridAtLevel(gridLevel + 1)
        bottom = [[x, 0] for x in range(5)]
        top = [[x, 4] for x in range(5)]
        leftSide = [[0, y] for y in range(5)]
        rightSide = [[4, y] for y in range(5)]
        sliceToGet = {}
        sliceToGet[tuple(grid.UP)] = bottom
        sliceToGet[tuple(grid.DOWN)] = top
        sliceToGet[tuple(grid.LEFT)] = rightSide
        sliceToGet[tuple(grid.RIGHT)] = leftSide
        return [inside.getPoint(*sidePoint) for sidePoint in sliceToGet[tuple(direction)]]
    else:
        return [check]


def newValue2(point: com.Point, grid: com.CartesianGrid, gridLevel: int):
    global grids
    directions = [grid.UP, grid.DOWN, grid.LEFT, grid.RIGHT]
    adjacent = 0
    for direction in directions:
        for check in getPoints(point, grid, gridLevel, direction):
            if check.data == '#':
                adjacent += 1    
    if point.data == '#':
        if adjacent != 1:
            return '.'
        return '#'
    else:
        if adjacent == 1 or adjacent == 2:
            return '#'
        return '.'

def Part2(lines):
    global grids
    x = 0
    y = 4
    base_grid = getGridAtLevel(0)
    for line in lines:
        for char in line.strip():
            point = com.Point(x, y, char)
            base_grid.addPoint(point)
            x += 1
        y -= 1
        x = 0
    
    for minute in range(1, 201):
        changes = []
        for gridLvl in [key for key in grids.keys()]:
            if abs(gridLvl) > minute:
                continue
            for point in grids[gridLvl].getAllPoints():
                if point.x == 2 and point.y == 2:
                    continue
                if newValue2(point, grids[gridLvl], gridLvl) != point.data:
                    changes.append(point)
        for change in changes:
            if change.data == '#':
                change.data = '.'
            else:
                change.data = '#'
        print('minute=', minute)
        #keys = sorted([key for key in grids.keys()])
        #for grid in keys:
        #    print('grid', grid)
        #    print(grids[grid])
        minute += 1
    bugs = 0
    for grid in grids:
        for point in grids[grid].getAllPoints():
            if point.data == '#':
                bugs += 1
    print(bugs)

file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file, '!')

if part1:
    Part1(lines)

if part2:
    Part2(lines)