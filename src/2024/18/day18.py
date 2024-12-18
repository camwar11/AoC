from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com

runExamples = True
day, year = get_day_and_year()
puzzle = Puzzle(year, day)

SAFE = "."
CORRUPTED = "#"

def inputParser1(input_data, bytes, size):
    grid = com.CartesianGrid(flipOutput=True)

    for x in range(size+1):
        for y in range(size+1):
            grid.addPoint(com.Point(x, y, SAFE))

    for i, line in enumerate(input_data.splitlines()):
        if i == bytes:
            break
        split = [int(x) for x in line.split(",")]
        grid.getPoint(split[0], split[1]).data = CORRUPTED
    return grid

def inputParser2(input_data, bytes, size):
    grid = com.CartesianGrid(emptyCellOutput="#", flipOutput=True)

    for x in range(size+1):
        for y in range(size+1):
            grid.addPoint(com.Point(x, y, SAFE))

    positions = [(int(x[0]), int(x[1])) for x in [line.split(",") for line in input_data.splitlines()]]
    for i, line in enumerate(positions[0:bytes]):
        point = grid.getPoint(line[0], line[1])
        grid.removePoint(point)
    return grid, positions[bytes:]

def edgeWeightFcn(start: com.Point, end: com.Point):
    if start.data == CORRUPTED or end.data == CORRUPTED:
        return 9999999
    return 1

def Part1(data):
    #print(data)
    minX, maxX, minY, maxY = data.getBounds()
    graph = com.Graph.parse_from_grid(data, edgeWeightFinder=edgeWeightFcn)

    start = data.getPoint(minX, minY)
    end = data.getPoint(maxX, maxY)
    path, weight = graph.dijsktra(start, end)
    return weight

def Part2(data):
    grid, bytes = data

    minX, maxX, minY, maxY = grid.getBounds()
    graph = com.Graph.parse_from_grid(grid)

    start = grid.getPoint(minX, minY)
    end = grid.getPoint(maxX, maxY)
    
    shortest = None
    for pos in bytes:
        point = grid.getPoint(pos[0], pos[1])
        graph.remove_node(point, False)
        #print()
        #print(grid)
        if shortest is not None and point not in shortest:
            # don't need to recalculate if we didn't remove a point in the shortest path
            # because it would still exist
            continue

        result = graph.dijsktra(start, end)
        if result is None:
            return f"{pos[0]},{pos[1]}"
        shortest = set(result[0])


    return None

if runExamples:
    part1ExamplePassed = False
    part2ExamplePassed = False
    for i, example in enumerate(puzzle.examples):
        part1Answer = str(Part1(inputParser1(example.input_data, 12, 6)))
        if part1Answer != "22":
            print(f"Incorrect: part1 example {i}. Extra={example.extra};Input=\n{example.input_data}\nExpect: {22}\nActual: {part1Answer}")
            part1ExamplePassed = False
            break
        
        print("Part 1 Example Passed")
        part1ExamplePassed = True
        part2Answer = str(Part2(inputParser2(example.input_data, 12, 6)))
        if part2Answer != "6,1":
            print(f"Incorrect: part2 example {i}. Extra={example.extra};Input=\n{example.input_data}\nExpect: {"6,1"}\nActual: {part2Answer}")
            part2ExamplePassed = False
            break
        print("Part 2 Example Passed")
        part2ExamplePassed = True
else:
    part1ExamplePassed = True
    part2ExamplePassed = True

if part1ExamplePassed:
    puzzle.answer_a = Part1(inputParser1(puzzle.input_data, 1024, 70))

if part2ExamplePassed:
    puzzle.answer_b = Part2(inputParser2(puzzle.input_data, 1024, 70))