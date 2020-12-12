import common as com

test = False
part1 = True
part2 = False
puzzle = com.PuzzleWithTests()

def getOccupiedSeatCount(grid: com.CartesianGrid, point: com.Point):
    count = 0
    for x in range(point.x - 1, point.x + 2):
        for y in range(point.y - 1, point.y +2):
            if point.x == x and point.y == y:
                continue
            adjPoint = grid.getPoint(x, y)
            if adjPoint is not None and adjPoint.data == '#':
                count += 1
    return count

def getOldAndNewSeat(grid: com.CartesianGrid, x, y):
    point:com.Point = grid.getPoint(x, y)
    if point.data == 'L' and getOccupiedSeatCount(grid, point) == 0:
        return point.data, '#'
    elif point.data == '#' and getOccupiedSeatCount(grid, point) >= 4:
        return point.data, 'L'
    return point.data, point.data
    


def Part1(lines):
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
                oldSeat, newSeat = getOldAndNewSeat(grid, x, y)
                newPoint = com.Point(x, y, newSeat)
                hadChange |= oldSeat != newSeat
                newGrid.addPoint(newPoint)
        grid = newGrid
        if not hadChange:
            break
        print('------------------------------------')
        print('')
        print(grid)
        loops += 1

    count = 0
    for point in grid.getAllPoints():
        if point.data == '#':
            count += 1
    return count

def Part2(lines):
    return None

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