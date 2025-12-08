from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com

RUN_EXAMPLES = True
day, year = get_day_and_year()
puzzle = Puzzle(year, day)

def input_parser_1(input_data: str) -> tuple[list[tuple[int, int]], list[int]]:
    data = input_data.splitlines()
    ranges: list[tuple[int, int]] = []
    ingredients: list[int] = []
    is_ranges = True
    for line in data:
        if line == "":
            is_ranges = False
            continue
        if is_ranges:
            split_range = line.split('-')
            ranges.append((int(split_range[0]), int(split_range[1])))
        else:
            ingredients.append(int(line))
    return ranges, ingredients
    # return com.parse_raw_to_grid(input_data)

def input_parser_2(input_data: str) -> tuple[list[tuple[int, int]], list[int]]:
    return input_parser_1(input_data)

def part_1(data: tuple[list[tuple[int, int]], list[int]]) -> str | None:
    ranges, ingredients = data
    fresh = 0
    for ingredient in ingredients:
        for start, end in ranges:
            if start <= ingredient <= end:
                fresh += 1
                break

    return str(fresh)

def part_2_old(data: tuple[list[tuple[int, int]], list[int]]) -> str | None:
    ranges, _ = data
    ranges.sort()
    prev_end = 0
    fresh_ids = 0
    for i, (start, end) in enumerate(ranges):
        if end <= prev_end:
            continue
        new_start = max(start, prev_end)
        diff = end - new_start
        if diff > 0:
            # Need to count inclusive
            if new_start == start and start != prev_end:
                diff += 1
        fresh_ids += diff
        prev_end = end

    return str(fresh_ids)

def part_2(data: tuple[list[tuple[int, int]], list[int]]) -> str | None:
    ranges, _ = data
    ranges.sort()
    prev_end = 0
    fresh_ids = 0
    for i, (start, end) in enumerate(ranges):
        if end <= prev_end:
            continue
        new_start = max(start, prev_end)
        diff = end - new_start
        # Need to count inclusive
        if new_start == start and start != prev_end:
            diff += 1
        fresh_ids += diff
        prev_end = end

    return str(fresh_ids)

if RUN_EXAMPLES:
    part1_example_passed = True
    part2_example_passed = True

    examples = [
        # Add custom examples here
        [
           "1-10\n2-11\n2-11\n3-11\n3-14\n15-19\n20-20\n21-21\n\n7",
           "1",
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
        else:
            print("Part 1 Example Passed")
            part1_example_passed &= True
        part2Answer = str(part_2(input_parser_2(example[0])))
        if part2Answer != example[2]:
            print(f"Incorrect: part2 example {i}. Extra={example[3]};Input=\n{example[0]}\nExpect: {example[2]}\nActual: {part2Answer}")
            part2_example_passed = False
        else:
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