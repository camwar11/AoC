from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com
import functools

RUN_EXAMPLES = True
day, year = get_day_and_year()
puzzle = Puzzle(year, day)
START = 'S'
BEAM = '|'
SPLITTER = '^'

def input_parser_1(input_data: str) -> com.CartesianGrid:
    return com.parse_raw_to_grid(input_data)

def input_parser_2(input_data: str) -> com.CartesianGrid:
    return input_parser_1(input_data)

def part_1(data: com.CartesianGrid) -> str | None:
    splits = 0
    for point in data.getAllPoints():
        below = point.getAdjacentPoint(com.CartesianGrid.DOWN)
        if below is None:
            continue
        if point.data == START:
            below.data = BEAM
        if point.data == BEAM:
            if below.data == SPLITTER:
                splits += 1
                below.getAdjacentPoint(com.CartesianGrid.LEFT).data = BEAM
                below.getAdjacentPoint(com.CartesianGrid.RIGHT).data = BEAM
            else:
                below.data = BEAM
    return str(splits)

@functools.lru_cache(maxsize=None)
def walk_timelines(start: com.Point) -> int:
    timelines = 0
    down = start.getAdjacentPoint(com.CartesianGrid.DOWN)
    if down is None:
        #TODO: maybe not?
        return 1
    if down.data == SPLITTER:
        left = down.getAdjacentPoint(com.CartesianGrid.LEFT)
        right = down.getAdjacentPoint(com.CartesianGrid.RIGHT)
        timelines += walk_timelines(left)
        timelines += walk_timelines(right)
    else:
        timelines += walk_timelines(down)
    return timelines


def part_2(data: com.CartesianGrid) -> str | None:
    for point in data.getAllPoints():
        if point.data == START:
            start = point
            break
    return str(walk_timelines(start))

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
        part1Answer = str(part_1(input_parser_1(example[0])))
        if part1Answer != example[1]:
            print(f"Incorrect: part1 example {i}. Extra={example[3]};Input=\n{example[0]}\nExpect: {example[1]}\nActual: {part1Answer}")
            part1_example_passed = False
            part2_example_passed = False
            continue
        
        print("Part 1 Example Passed")
        part1_example_passed &= True
        part2Answer = str(part_2(input_parser_2(example[0])))
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