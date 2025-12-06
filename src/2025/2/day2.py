from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com

RUN_EXAMPLES = True
day, year = get_day_and_year()
puzzle = Puzzle(year, day)

def input_parser_1(input_data: str) -> list[(int, int)]:
    return [tuple(map(int, ranges.split('-'))) for ranges in input_data.split(',')]

def input_parser_2(input_data: str) -> list[str]:
    return input_parser_1(input_data)

def is_invalid(id: str) -> bool:
    length = len(id)
    return id[:length//2] == id[length//2:]

def is_invalid2(id: str) -> bool:
    length = len(id)
    for count in range(1, int((length / 2) + 1)):
        if length % count != 0:
            continue
        repetitions = length // count
        if id[:count] * repetitions == id:
            return True
    return False
        
def part_1(data: list[(int, int)]) -> str | None:
    invalid = []
    for start, end in data:
        for num in range(start, end + 1):
            if is_invalid(str(num)):
                invalid.append(num)
            
    return str(sum(invalid))

def part_2(data: list[(int, int)]) -> str | None:
    invalid = []
    for start, end in data:
        for num in range(start, end + 1):
            if is_invalid2(str(num)):
                invalid.append(num)
            
    return str(sum(invalid))

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