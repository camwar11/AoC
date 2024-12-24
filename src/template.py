from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com

runExamples = True
day, year = get_day_and_year()
puzzle = Puzzle(year, day)

def inputParser1(input_data):
    return input_data.splitlines()
    # return com.parse_raw_to_grid(input_data)

def inputParser2(input_data):
    return inputParser1(input_data)

def Part1(data):
    return None

def Part2(data):
    return None

if runExamples:
    part1ExamplePassed = True
    part2ExamplePassed = True

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
        part1Answer = str(Part1(inputParser1(example[0])))
        if part1Answer != example[1]:
            print(f"Incorrect: part1 example {i}. Extra={example[3]};Input=\n{example[0]}\nExpect: {example[1]}\nActual: {part1Answer}")
            part1ExamplePassed = False
            continue
        
        print("Part 1 Example Passed")
        part1ExamplePassed &= True
        part2Answer = str(Part2(inputParser2(example[0])))
        if part2Answer != example[2]:
            print(f"Incorrect: part2 example {i}. Extra={example[3]};Input=\n{example[0]}\nExpect: {example[2]}\nActual: {part2Answer}")
            part2ExamplePassed = False
            continue
        print("Part 2 Example Passed")
        part2ExamplePassed &= True
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