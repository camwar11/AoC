from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com
import math
from functools import cmp_to_key

runExamples = True
day, year = get_day_and_year()
puzzle = Puzzle(year, day)

def inputParser1(input_data):
    rules = []
    updates = []
    inRulesSection = True
    for line in input_data.splitlines():
        if line.isspace() or line.__len__() == 0:
            inRulesSection = False
            continue
        if inRulesSection:
            rules.append([int(x) for x in line.split('|')])
        else:
            updates.append([int(x) for x in line.split(',')])
    return (rules, updates)

def inputParser2(input_data):
    return inputParser1(input_data)

def Part1(data):
    rules = data[0]
    updates = data[1]

    rule_dict = {}
    for rule in rules:
        if rule[1] not in rule_dict:
            rule_dict[rule[1]] = set()
        rule_dict[rule[1]].add(rule[0])
    
    total = 0
    for update in updates:
        bad = set()
        success = True
        for value in update:
            if value in bad:
                success = False
                break
            if value in rule_dict:
                bad = bad.union(rule_dict[value])
        if success:
            mid = math.floor(len(update)/2)
            total += update[mid]
    return total

def Part2(data):
    rules = data[0]
    updates = data[1]

    rule_dict = {}
    for rule in rules:
        if rule[1] not in rule_dict:
            rule_dict[rule[1]] = set()
        rule_dict[rule[1]].add(rule[0])
    
    total = 0
    for update in updates:
        bad = set()
        success = True
        for value in update:
            if value in bad:
                success = False
                break
            if value in rule_dict:
                bad = bad.union(rule_dict[value])
        if not success:
            update = sorted(update, key=cmp_to_key(lambda x, y: compare(x, y, rule_dict)))
            mid = math.floor(len(update)/2)
            total += update[mid]
    return total

def compare(x, y, rule_dict):
    if x in rule_dict and y in rule_dict[x]:
        return 1
    if y in rule_dict and x in rule_dict[y]:
        return -1
    return 0

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
        if part2Answer != "123":
            print(f"Incorrect: part2 example {i}. Extra={example.extra};Input=\n{example.input_data}\nExpect: {"123"}\nActual: {part2Answer}")
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