import math
from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com
from typing import Callable

RUN_EXAMPLES = True
day, year = get_day_and_year()
puzzle = Puzzle(year, day)
def symbol_func(symbol: str) -> Callable[[int, int], int]:
    if symbol == '+':
        return sum
    elif symbol == '*':
        return math.prod
    else:
        raise ValueError(f"Unknown symbol: {symbol}")

def input_parser_1(input_data: str) -> tuple[list[Callable[[int, int], int]], list[list[int]]]:
    lines = input_data.splitlines()
    lines.reverse()
    symbols = list(map(symbol_func, lines[0].split()))
    return symbols, [list(map(int, x.split())) for x in lines[1:]]

def input_parser_2(input_data: str) -> tuple[list[Callable[[int, int], int]], list[str]]:
    lines = input_data.splitlines()
    lines.reverse()
    symbols = list(map(symbol_func, lines[0].split()))
    symbols.reverse()
    numbers: list[str] = []
    for line in lines[1:]:
        for i, char in enumerate(reversed(line)):
            if len(numbers) <= i:
                numbers.append('')
            # backward since we are reversing the lines
            numbers[i] = char + numbers[i]
    return symbols, numbers

def part_1(data: tuple[list[Callable[[int, int], int]], list[list[int]]]) -> str | None:
    symbols, numbers = data

    values = []
    for number_list in numbers:
        for i, number in enumerate(number_list):
            if len(values) <= i:
                values.append(number)
                continue
            values[i] = symbols[i]([values[i], number])

    return str(sum(values))

def part_2(data: tuple[list[Callable[[int, int], int]], list[str]]) -> str | None:
    symbols, numbers = data
    current_values = []
    results = []
    current_symbol_index = 0
    for i, number_str in enumerate(numbers):
        stripped = number_str.strip()
        last = i == len(numbers) - 1
        if last:
            current_values.append(int(stripped))
        if stripped == '' or last:
            results.append(symbols[current_symbol_index](current_values))
            current_values.clear()
            current_symbol_index += 1
            continue
        current_values.append(int(stripped))
    return str(sum(results))

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