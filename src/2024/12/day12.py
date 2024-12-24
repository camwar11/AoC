from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com

runExamples = True
day, year = get_day_and_year()
puzzle = Puzzle(year, day)

def inputParser1(input_data):
    return com.parse_raw_to_grid(input_data)

def inputParser2(input_data):
    return inputParser1(input_data)

def get_region(plot, used, plant, region):
    if plot in used or plot.data != plant:
        return 0
    region.append(plot)
    used.add(plot)
    perimeter = 0
    for adj in plot.getAdjacentPoints(includeMissing=True):
        if adj.data == plant:
            perimeter += get_region(adj, used, plant, region)
        else:
            perimeter += 1
    return perimeter

def get_sides(plot, plant):
    left = plot.getAdjacentPoint(com.CartesianGrid.LEFT, True)
    up = plot.getAdjacentPoint(com.CartesianGrid.UP, True)
    right = plot.getAdjacentPoint(com.CartesianGrid.RIGHT, True)
    down = plot.getAdjacentPoint(com.CartesianGrid.DOWN, True)

    return [
        left.data != plant,
        up.data != plant,
        right.data != plant,
        down.data != plant
    ]

def set_direction_for_connected(used, plot, plant, counted, direction, cartDirs, value):
    if plot in counted or used[plot][direction] == value or plot.data != plant:
        return
    used[plot][direction] = value
    counted.add(plot)
    for cartDir in cartDirs:
        adj = plot.getAdjacentPoint(cartDir)
        if adj is None:
            continue
        set_direction_for_connected(used, adj, plant, counted, direction, cartDirs, value)

def find_sides(used, region):
    sides = 0
    cartDirs = [
        [com.CartesianGrid.UP, com.CartesianGrid.DOWN],
        [com.CartesianGrid.LEFT, com.CartesianGrid.RIGHT],
        [com.CartesianGrid.UP, com.CartesianGrid.DOWN],
        [com.CartesianGrid.LEFT, com.CartesianGrid.RIGHT]
    ]
    for direction in range(4):
        counted = set()
        for plot in region:
            if plot in counted or not used[plot][direction]:
                continue
            sides += 1
            set_direction_for_connected(used, plot, plot.data, counted, direction, cartDirs[direction], False)
    return sides

def get_region2(plot, used, plant, region):
    if plot in used or plot.data != plant:
        return
    region.append(plot)
    total_sides = 0

    new_sides = get_sides(plot, plant)
    used[plot] = new_sides

    for adj, new_dir in plot.getAdjacentPoints(includeMissing=True, includeDirection=True):
        if adj.data == plant:
            get_region2(adj, used, plant, region)

def Part1(data):
    used = set()
    regions = []
    sizes = []
    for plot in data.getAllPoints():
        region = []
        sizes.append((get_region(plot, used, plot.data, region), len(region)))
        regions.append(region)
    return sum([x * y for x, y in sizes])

def Part2(data):
    used = dict()
    regions = []
    sizes = []
    for plot in data.getAllPoints():
        region = []
        get_region2(plot, used, plot.data, region)
        if len(region) > 0:
            regions.append(region)
    
    for region in regions:
        counted = set()
        sides = find_sides(used, region)
        sizes.append((len(region), sides))
    return sum([x * y for x, y in sizes])

if runExamples:
    part1ExamplePassed = False
    part2ExamplePassed = False

    examples = [
        # Add custom examples here
        [
            """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO""",
            "772",
            "436",
            "extra"
        ],
        [
            """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE""",
            "1930",
            "1206",
            "extra"
        ],
    ]
    for example in puzzle.examples:
        examples.append([
            example.input_data,
            "140",
            "80",
            example.extra
        ])

    for i, example in enumerate(examples):
        part1Answer = str(Part1(inputParser1(example[0])))
        if part1Answer != example[1]:
            print(f"Incorrect: part1 example {i}. Extra={example[3]};Input=\n{example[0]}\nExpect: {example[1]}\nActual: {part1Answer}")
            part1ExamplePassed = False
            continue
        
        print("Part 1 Example Passed")
        part1ExamplePassed = True
        part2Answer = str(Part2(inputParser2(example[0])))
        if part2Answer != example[2]:
            print(f"Incorrect: part2 example {i}. Extra={example[3]};Input=\n{example[0]}\nExpect: {example[2]}\nActual: {part2Answer}")
            part2ExamplePassed = False
            continue
        print("Part 2 Example Passed")
        part2ExamplePassed = True
else:
    part1ExamplePassed = True
    part2ExamplePassed = True

if part1ExamplePassed:
    part1Answer = Part1(inputParser1(puzzle.input_data))
    print(f"Submitting part 1 answer of {part1Answer}")
    puzzle.answer_a = part1Answer

if part2ExamplePassed:
    part2Answer = Part2(inputParser2(puzzle.input_data))
    print(f"Submitting part 2 answer of {part2Answer}")
    puzzle.answer_b = part2Answer