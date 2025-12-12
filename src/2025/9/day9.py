from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com

RUN_EXAMPLES = True
day, year = get_day_and_year()
puzzle = Puzzle(year, day)

EDGE = '#'
INTERNAL = 'X'

def input_parser_1(input_data: str) -> list[tuple[int, int]]:
    return [tuple(map(int, x.split(','))) for x in input_data.splitlines()]
    # return com.parse_raw_to_grid(input_data)

def input_parser_2(input_data: str) -> list[tuple[int, int]]:
    return input_parser_1(input_data)

def area(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    width = abs(p2[0] - p1[0]) + 1
    height = abs(p2[1] - p1[1]) + 1
    return width * height

def part_1(data: list[tuple[int, int]]) -> str | None:
    areas: list[(int, tuple[int, int])] = []

    for i, first in enumerate(data):
        for j, second in enumerate(data):
            if i >= j:
                continue
            areas.append((area(first, second), (i, j)))
        areas.sort(reverse=True)
    
    return str(areas[0][0])

def is_edge(point: com.Point) -> bool:
    return point.data is not None and point.data[0] == EDGE

def is_internal(point: com.Point) -> bool:
    return point.data is not None and point.data[0] == INTERNAL

def is_area_colored(p1: tuple[int, int], p2: tuple[int, int], colored: com.CartesianGrid) -> bool:
    for x in range(min(p1[0], p2[0]), max(p1[0], p2[0]) + 1):
        for y in range(min(p1[1], p2[1]), max(p1[1], p2[1]) + 1):
            point = colored.getPoint(x, y)
            if point is None or point.data is None:
                return False

            if not is_edge(point) and not is_internal(point):
                return False
    return True

def color_area(first_internal_point: com.Point):
    visited = set()
    visited.add(first_internal_point)
    queue = [first_internal_point]
    while len(queue) > 0:
        first_internal_point = queue.pop(0)
        if not is_edge(first_internal_point) and not is_internal(first_internal_point):
            first_internal_point.data = INTERNAL
        else:
            continue
        for adjacent in first_internal_point.getAdjacentPoints(includeMissing=True):
            if adjacent not in visited:
                visited.add(adjacent)
                queue.append(adjacent)

def part_2(data: list[tuple[int, int]]) -> str | None:
    grid = com.CartesianGrid(flipOutput=True, cellOutputStrFcn=lambda p: p.data[0] if p.data is not None else '.')

    compressed = com.compress_points(data)

    prev_point = compressed[-1]
    for point, original_point in compressed:
        prev, _ = prev_point
        grid.addPoint(com.Point(point[0], point[1], (EDGE, original_point)))
        if point[0] == prev[0]:
            for y in range(min(point[1], prev[1]), max(point[1], prev[1]) + 1):
                if grid.getPoint(point[0], y) is None:
                    grid.addPoint(com.Point(point[0], y, (EDGE, original_point)))
        elif point[1] == prev[1]:
            for x in range(min(point[0], prev[0]), max(point[0], prev[0]) + 1):
                if grid.getPoint(x, point[1]) is None:
                    grid.addPoint(com.Point(x, point[1], (EDGE, original_point)))
        prev_point = (point, original_point)

    first_internal_point = None
    for point, original_point in compressed:
        start = grid.getPoint(point[0], point[1])
        for adjacent in start.getAdjacentPoints(includeDiagonals=True, includeMissing=True):
            if (adjacent.data and adjacent.data[0] == EDGE) or not adjacent.is_in_polygon(is_edge, is_edge):
                continue
            else:
                first_internal_point = adjacent
                break
        if first_internal_point is not None:
            break
    
    color_area(first_internal_point)

    areas: list[(int, com.Point)] = []

    for i, first in enumerate(compressed):
        for j, second in enumerate(compressed):
            if i >= j:
                continue
            areas.append((area(first[1], second[1]), (first[0], second[0])))
        areas.sort(reverse=True)    
    
    for area_size, (p1, p2) in areas:
        if is_area_colored(p1, p2, grid):
            print(grid)
            return str(area_size)

    return None

if RUN_EXAMPLES:
    part1_example_passed = True
    part2_example_passed = True

    examples = [
        # Add custom examples here
        #[
        #    "input_data",
        #    "answer_a",
        #    "answer_b",
        #    "extra"
        #]
    ]
    for example in puzzle.examples:
        examples.append([
            example.input_data,
            example.answer_a,
            example.answer_b,
            example.extra
        ])

    for i, example in enumerate(examples):
        example[1] = '50'  # expected answer for part 1
        part1Answer = str(part_1(input_parser_1(example[0])))
        if part1Answer != example[1]:
            print(f"Incorrect: part1 example {i}. Extra={example[3]};Input=\n{example[0]}\nExpect: {example[1]}\nActual: {part1Answer}")
            part1_example_passed = False
            part2_example_passed = False
            continue
        
        print("Part 1 Example Passed")
        part1_example_passed &= True
        part2Answer = str(part_2(input_parser_2(example[0])))
        example[2] = '24'  # expected answer for part 2
        if part2Answer != example[2]:
            print(f"Incorrect: part2 example {i}. Extra={example[3]};Input=\n{example[0]}\nExpect: {example[2]}\nActual: {part2Answer}")
            part2_example_passed = False
            continue
        print("Part 2 Example Passed")
        part2_example_passed &= True
else:
    part1_example_passed = True
    part2_example_passed = True

if part1_example_passed:
    part1Answer = part_1(input_parser_1(puzzle.input_data))
    if part1Answer is not None:
        print(f"Submitting part 1 answer of {part1Answer}")
    puzzle.answer_a = part1Answer

if part2_example_passed:
    part2Answer = part_2(input_parser_2(puzzle.input_data))
    if part2Answer is not None:
        print(f"Submitting part 2 answer of {part2Answer}")
        puzzle.answer_b = part2Answer