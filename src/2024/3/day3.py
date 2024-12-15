from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com
import re

runExamples = True
day, year = get_day_and_year()
puzzle = Puzzle(year, day)

def inputParser1(input_data):
    return input_data

def inputParser2(input_data):
    return inputParser1(input_data)

def Part1(data):
    matches = re.findall("mul\((\d{1,3}),(\d{1,3})\)", data)
    total = 0
    for pair in matches:
        total += int(pair[0]) * int(pair[1]) 
    return total

def Part2(data):
    data = "do()" + data
    dont_split =  re.split("don't\(\)", data)
    total = 0
    for value in dont_split:
        do_split = re.split("do\(\)", value)
        if do_split.__len__() == 1:
            continue
        for enabled in do_split[1:]:
            matches = re.findall("mul\((\d{1,3}),(\d{1,3})\)", enabled)
            for pair in matches:
                total += int(pair[0]) * int(pair[1]) 
    return total

if runExamples:
    part1ExamplePassed = False
    part2ExamplePassed = False
    for i, example in enumerate(puzzle.examples):
        part1Answer = str(Part1(inputParser1(example.input_data)))
        if part1Answer != "161":
            print(f"Incorrect: part1 example {i}. Extra={example.extra};Input=\n{example.input_data}\nExpect: {161}\nActual: {part1Answer}")
            part1ExamplePassed = False
            break
        
        print("Part 1 Example Passed")
        part1ExamplePassed = True
        part2Answer = str(Part2(inputParser2("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))")))
        if part2Answer != "48":
            print(f"Incorrect: part2 example {i}. Extra={example.extra};Input=\n{example.input_data}\nExpect: {"48"}\nActual: {part2Answer}")
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