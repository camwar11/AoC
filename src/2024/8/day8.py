from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com

runExamples = True
day, year = get_day_and_year()
puzzle = Puzzle(year, day)

def inputParser1(input_data):
    grid = com.CartesianGrid(flipOutput=True)
    com.parse_to_grid(input_data.splitlines(), grid)
    return grid

def inputParser2(input_data):
    return inputParser1(input_data)

def calc_antinodes(minX, maxX, minY, maxY, point1, point2):
    firstDiffX = point1.x - point2.x
    firstDiffY = point1.y - point2.y

    first = (point1.x + firstDiffX, point1.y + firstDiffY)

    secondDiffX = point2.x - point1.x
    secondDiffY = point2.y - point1.y
    second = (point2.x + secondDiffX, point2.y + secondDiffY)
    in_graph = []

    if(minX <= first[0] <= maxX and minY <= first[1] <= maxY):
        in_graph.append(first)

    if(minX <= second[0] <= maxX and minY <= second[1] <= maxY):
        in_graph.append(second)

    return in_graph

def Part1(data):
    antinodes = set()
    minX, maxX, minY, maxY = data.getBounds()
    points_by_freq = {}
    for point in data.getAllPoints():
        if point.data == '.':
            continue
        if point.data in points_by_freq:
            for other in points_by_freq[point.data]:
                new_antinodes = calc_antinodes(minX, maxX, minY, maxY, point, other)
                for antinode in new_antinodes:
                    antinodes.add(antinode)
            points_by_freq[point.data].append(point)
        else:
            points_by_freq[point.data] = [point]
    return len(antinodes)

def calc_antinodes_p2(minX, maxX, minY, maxY, point1, point2):
    firstDiffX = point1.x - point2.x
    firstDiffY = point1.y - point2.y

    in_graph = []
    x = point1.x
    y = point1.y
    while minX <= x <= maxX and minY <= y <= maxY:
        in_graph.append((x, y))
        x += firstDiffX
        y += firstDiffY

    secondDiffX = point2.x - point1.x
    secondDiffY = point2.y - point1.y
    x = point2.x
    y = point2.y
    while minX <= x <= maxX and minY <= y <= maxY:
        in_graph.append((x, y))
        x += secondDiffX
        y += secondDiffY

    return in_graph

def Part2(data):
    antinodes = set()
    minX, maxX, minY, maxY = data.getBounds()
    points_by_freq = {}
    for point in data.getAllPoints():
        if point.data == '.':
            continue
        if point.data in points_by_freq:
            for other in points_by_freq[point.data]:
                new_antinodes = calc_antinodes_p2(minX, maxX, minY, maxY, point, other)
                for antinode in new_antinodes:
                    antinodes.add(antinode)
            points_by_freq[point.data].append(point)
        else:
            points_by_freq[point.data] = [point]
    return len(antinodes)

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
        if part2Answer != "34":
            print(f"Incorrect: part2 example {i}. Extra={example.extra};Input=\n{example.input_data}\nExpect: {"34"}\nActual: {part2Answer}")
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