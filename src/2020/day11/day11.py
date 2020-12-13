import common as com

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def getOccupiedSeatCountPart1(grid: com.CartesianGrid, point: com.Point):
    count = 0
    for x in range(point.x - 1, point.x + 2):
        for y in range(point.y - 1, point.y +2):
            if point.x == x and point.y == y:
                continue
            adjPoint = grid.getPoint(x, y)
            if adjPoint is not None and adjPoint.data == '#':
                count += 1
    return count

def getOccupiedSeatCountPart2(grid: com.CartesianGrid, point: com.Point):
    count = 0
    upLeft = [-1, 1]
    upRight = [1, 1]
    downLeft = [-1, -1]
    downRight = [1, -1]
    
    directions = (
        upLeft,
        com.CartesianGrid.UP,
        upRight,
        com.CartesianGrid.RIGHT,
        downRight,
        com.CartesianGrid.DOWN,
        downLeft,
        com.CartesianGrid.LEFT
    )

    for direction in directions:
        adjPoint = point
        while adjPoint is not None:
            adjPoint = grid.getPoint(*(adjPoint + direction))
            if adjPoint is None:
                break
            if adjPoint.data == '#':
                count += 1
                break
            if adjPoint.data == 'L':
                break
    return count

def getOldAndNewSeatPart1(grid: com.CartesianGrid, x, y):
    point:com.Point = grid.getPoint(x, y)
    if point.data == 'L' and getOccupiedSeatCountPart1(grid, point) == 0:
        return point.data, '#'
    elif point.data == '#' and getOccupiedSeatCountPart1(grid, point) >= 4:
        return point.data, 'L'
    return point.data, point.data

def getOldAndNewSeatPart2(grid: com.CartesianGrid, x, y):
    point:com.Point = grid.getPoint(x, y)
    if point.data == 'L' and getOccupiedSeatCountPart2(grid, point) == 0:
        return point.data, '#'
    elif point.data == '#' and getOccupiedSeatCountPart2(grid, point) >= 5:
        return point.data, 'L'
    return point.data, point.data
    
def runSimulation(lines, getOldAndNewSeatFcn):
    grid = com.CartesianGrid(' ')
    x = 0
    y = 0
    for line in lines:
        for char in line.strip():
            point = com.Point(x, y, char)
            grid.addPoint(point)
            x += 1
        x = 0
        y -= 1
    
    loops = 0
    while True:
        newGrid = com.CartesianGrid(' ')
        hadChange = False
        for y in range(0, -1*len(lines), -1):
            for x in range(len(lines[0].strip())):
                oldSeat, newSeat = getOldAndNewSeatFcn(grid, x, y)
                newPoint = com.Point(x, y, newSeat)
                hadChange |= oldSeat != newSeat
                newGrid.addPoint(newPoint)
        grid = newGrid
        if not hadChange:
            break
        loops += 1

    count = 0
    for point in grid.getAllPoints():
        if point.data == '#':
            count += 1
    return count

def Part1(lines):
    return runSimulation(lines, getOldAndNewSeatPart1)

def Part2(lines):
    return runSimulation(lines, getOldAndNewSeatPart2)


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