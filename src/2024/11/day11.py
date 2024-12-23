from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com

runExamples = True
day, year = get_day_and_year()
puzzle = Puzzle(year, day)

def inputParser1(input_data):
    return [int(x) for x in input_data.split(" ")]

def inputParser2(input_data):
    return inputParser1(input_data)

def addToCounts(counts, num, count):
    counts.setdefault(num, 0)
    counts[num] += count

def changeStone(counts):
    for val, count in [x for x in counts.items()]:
        counts[val] -= count
        if val == 0:
            addToCounts(counts, 1, count)
        else:
            stone_str = str(val)
            length = len(stone_str)
            if length % 2 == 0:
                addToCounts(counts, int(stone_str[0:int(length/2)]), count)
                addToCounts(counts, int(stone_str[int(length/2):]), count)
            else:
                addToCounts(counts, val * 2024, count)
        
def runBlinks(data, num):
    counts = dict()
    for val in data:
        addToCounts(counts, val, 1)
    for i in range(num):
        changeStone(counts)

    return sum(counts.values())

def Part1(data):
    return runBlinks(data, 25)

def Part2(data):
    return runBlinks(data, 75)

if runExamples:
    part1ExamplePassed = False
    part2ExamplePassed = False

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
            "125 17",
            example.answer_a,
            example.answer_b,
            example.extra
        ])

    for i, example in enumerate(examples):
        part1Answer = str(Part1(inputParser1(example[0])))
        if part1Answer != example[1]:
            print(f"Incorrect: part1 example {i}. Extra={example[3]};Input=\n{example[0]}\nExpect: {example[1]}\nActual: {part1Answer}")
            part1ExamplePassed = False
            break
        
        print("Part 1 Example Passed")
        part1ExamplePassed = True
        #part2Answer = str(Part2(inputParser2(example[0])))
        #if part2Answer != example[2]:
        #    print(f"Incorrect: part2 example {i}. Extra={example[3]};Input=\n{example[0]}\nExpect: {example[2]}\nActual: {part2Answer}")
        #    part2ExamplePassed = False
        #    break
        #print("Part 2 Example Passed")
        part2ExamplePassed = True
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