import math
from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com

RUN_EXAMPLES = True
day, year = get_day_and_year()
puzzle = Puzzle(year, day)

def input_parser_1(input_data: str) -> list[int]:
    return [int(line.replace("L", "-").replace("R", "")) for line in input_data.splitlines() if line]
    # return com.parse_raw_to_grid(input_data)

def input_parser_2(input_data: str) -> list[int]:
    return input_parser_1(input_data)

def part_1(data: list[int]) -> str | None:
    position = 50
    mod = 100
    count = 0
    for move in data:
        position += move
        position %= mod
        if position == 0:
            count += 1
    return str(count)

def part_2(data: list[int]) -> str | None:
    position = 50
    mod = 100
    count = 0
    for move in data:
        prev = position
        extra_rotations = math.floor(abs(move) / mod)
        remove = extra_rotations * mod
        if move < 0:
            remove = -remove
        leftovers = move - (remove )

        position += leftovers
        new_pos = position % mod

        if new_pos == 0:
            count += 1
        elif new_pos != position and prev != 0:
            count += 1
        position = new_pos
        count += extra_rotations
    return str(count)

if RUN_EXAMPLES:
    part1_example_passed = True
    part2_example_passed = True

    examples = [
        # Add custom examples here
        [
           "R149\nL175",
           "0",
           "2",
           "extra"
        ],
        [
           "R1000\nL50\nL1\nR2\nL1\nR200\nL1\nR200\nR2\nL150",
           "3",
           "21",
           "extra"
        ]
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