import re
from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com

RUN_EXAMPLES = True
day, year = get_day_and_year()
puzzle = Puzzle(year, day)

def input_parser_1(input_data: str) -> list[str]:
    return input_data.splitlines()
    # return com.parse_raw_to_grid(input_data)

def input_parser_2(input_data: str) -> list[str]:
    return input_parser_1(input_data)

def part_1(data: list[str]) -> str | None:
    patterns = []
    for i in range(9, 0, -1):
        for j in range(9, 0, -1):
            patterns.append((re.compile(rf'.*{i}.*{j}.*'), (i, j)))

    joltage = 0
    for bank in data:
        for pattern, (first, last) in patterns:
            if pattern.match(bank):
                joltage += int(str(first) + str(last))
                break

    return joltage

def part_2(data: list[str]) -> str | None:
    digits = 12
    joltage = 0
    for bank in data:
        bank_len = len(bank)
        current = []
        i = 0
        for battery in bank:
            left = bank_len - i
            i += 1
            bat_val = int(battery)
            if len(current) == 0:
                current = [bat_val]
                continue
            for current_idx, current_val in enumerate(current):
                needed = digits - current_idx
                if needed > left:
                    # Not enough digits left to complete
                    continue
                if current_val < bat_val:
                    current = current[:current_idx]
                    break
            if len(current) < digits:
                current.append(bat_val)
        value = int(''.join([str(x) for x in current]))
        joltage += value
    return joltage

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