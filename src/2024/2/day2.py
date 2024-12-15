from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com

runExamples = True
day, year = get_day_and_year()
puzzle = Puzzle(year, day)

def inputParser1(input_data):
    return [list(map(int, x.split(' '))) for x in input_data.splitlines()]

def inputParser2(input_data):
    return inputParser1(input_data)

def Part1(data):
    safe = 0
    for report in data:
        prev = None
        inc = None
        reportSafe = True
        for level in report:
            if prev == None:
                prev = level
                continue
            diff = prev - level
            prev = level
            if(diff == 0 or abs(diff) > 3):
                reportSafe = False
                break
            isInc = diff < 0
            if(inc == None):
                inc = isInc
            else:
                if inc != isInc:
                    reportSafe = False
                    break
        if reportSafe:
            safe += 1
    return safe

def isReportSafe(report, removeIdx = None):
    prev = None
    inc = None
    reportSafe = True
    for i, level in enumerate(report):
        if i == removeIdx:
            continue
        if prev == None:
            prev = level
            continue
        diff = prev - level
        if(diff == 0 or abs(diff) > 3):
            reportSafe = False
            break
        isInc = diff < 0
        if(inc == None):
            inc = isInc
        else:
            if inc != isInc:
                reportSafe = False
                break
        prev = level
    return reportSafe


def Part2(data):
    safe = 0
    for report in data:
        reportSafe = isReportSafe(report)
        if not reportSafe:
            for i in range(report.__len__()):
                reportSafe = isReportSafe(report, i)
                if(reportSafe):
                    break
        if reportSafe:
            safe += 1
    return safe

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
        if part2Answer != example.answer_b:
            print(f"Incorrect: part2 example {i}. Extra={example.extra};Input=\n{example.input_data}\nExpect: {example.answer_b}\nActual: {part2Answer}")
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