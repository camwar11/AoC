from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com
import operator as op

runExamples = True
day, year = get_day_and_year()
puzzle = Puzzle(year, day)

def inputParser1(input_data):
    output = []
    for line in input_data.splitlines():
        total, rest = line.split(":")
        rest = [int(x) for x in rest.split(" ") if x != ""]
        output.append((int(total), rest))
    return output

def inputParser2(input_data):
    return inputParser1(input_data)

def can_calibrate(ops, result, numbers: list, current_value = None):
    if len(numbers) == 0:
        return current_value == result
    
    first = numbers[0]
    if(len(numbers) == 1):
        rest = []
    else:
        rest = numbers[1:]

    if current_value is None:
        return can_calibrate(ops, result, rest, first)
    for op in ops:
        new_value = op(current_value, first)
        if(can_calibrate(ops, result, rest, new_value)):
            return True

def Part1(data):
    ops = [op.add, op.mul]
    total = 0
    for result, numbers in data:
        if(can_calibrate(ops, result, numbers)):
            total += result
    return total

def concat(x, y):
    return int(str(x) + str(y))

def Part2(data):
    ops = [op.add, op.mul, concat]
    total = 0
    for result, numbers in data:
        if(can_calibrate(ops, result, numbers)):
            total += result
    return total

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
        if part2Answer != "11387":
            print(f"Incorrect: part2 example {i}. Extra={example.extra};Input=\n{example.input_data}\nExpect: {"11387"}\nActual: {part2Answer}")
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