from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com

runExamples = True
day, year = get_day_and_year()
puzzle = Puzzle(year, day)

def inputParser1(input_data):
    grid = com.CartesianGrid()
    lines = input_data.splitlines()
    lines.reverse()
    com.parse_to_grid(lines, grid)
    return grid

def inputParser2(input_data):
    return inputParser1(input_data)

def Part1(data):
    guard=None
    for point in data.getAllPoints():
        if point.data == '^':
            guard = point
            break
    minX, maxX, minY, maxY = data.getBounds()
    while minX <= guard.x <= maxX and minY <= guard.y <= maxY:
        guard = moveGuard(guard, data)[0]
        #print()
        #print(data)
    
    return len([x for x in data.getAllPoints() if x.data == 'X'])

def moveGuard(guard, grid):
    directions = {
        '^': com.CartesianGrid.UP,
        '>': com.CartesianGrid.RIGHT,
        'v': com.CartesianGrid.DOWN,
        '<': com.CartesianGrid.LEFT
    }
    turns = ['^', '>', 'v', '<', '^']
    facing = guard.data
    direction = directions[facing]
    newPoint = guard.getAdjacentPoint(direction, True)
    while newPoint.data == '#':
        facing = turns[turns.index(facing) + 1]
        direction = directions[facing]
        newPoint = guard.getAdjacentPoint(direction, True)
    guard.data = 'X'
    newPointOldValue = newPoint.data
    newPoint.data = facing
    return newPoint, newPointOldValue

def Part2(data):
    guard=None
    for point in data.getAllPoints():
        if point.data == '^':
            guard = point
            break
    minX, maxX, minY, maxY = data.getBounds()

    total = 0
    for point in data.getAllPoints():
        copy = data.copy()
        point_copy = copy.getPoint(point.x, point.y)
        if(point_copy.data == '^' or point_copy.data == '#'):
            continue
        guard_copy = copy.getPoint(guard.x, guard.y)
        point_copy.data = '#'
        last_open = 0
        steps_to_be_a_loop = 200
        while (minX <= guard_copy.x <= maxX and minY <= guard_copy.y <= maxY) and last_open < steps_to_be_a_loop:
            guard_copy, last = moveGuard(guard_copy, data)
            if last == "." or None:
                last_open = 0
            else:
                last_open += 1
            #print()
            #print(data)
        if last_open == steps_to_be_a_loop:
            total += 1
    
    return total

if runExamples:
    part1ExamplePassed = False
    part2ExamplePassed = False
    for i, example in enumerate(puzzle.examples):
        part1Answer = str(Part1(inputParser1(example.input_data)))
        if part1Answer != example.answer_a:
            print(f"Incorrect: part1 example {i}. Extra={example.extra};Input=\n{example.input_data}\nExpect: {example.answer_a}\nActual: {part1Answer}")
            part1ExamplePassed = False
            break
        
        print("Part 1 Example Passed")
        part1ExamplePassed = True
        part2Answer = str(Part2(inputParser2(example.input_data)))
        if part2Answer != "6":
            print(f"Incorrect: part2 example {i}. Extra={example.extra};Input=\n{example.input_data}\nExpect: {"6"}\nActual: {part2Answer}")
            part2ExamplePassed = False
            break
        print("Part 2 Example Passed")
        part2ExamplePassed = True
else:
    part1ExamplePassed = True
    part2ExamplePassed = True

if part1ExamplePassed:
    puzzle.answer_a = Part1(inputParser1(puzzle.input_data))

if part2ExamplePassed:
    puzzle.answer_b = Part2(inputParser2(puzzle.input_data))