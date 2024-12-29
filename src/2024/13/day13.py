from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com

runExamples = False
day, year = get_day_and_year()
puzzle = Puzzle(year, day)

PRIZE = "PRIZE"

def parse_operation(val):
    _, op,  parsed = val.partition("+")
    if parsed == "":
        _, op,  parsed = val.partition("=")
    return op, parsed

def inputParser1(input_data):
    configs = []
    current = []
    configs.append(current)
    for line in input_data.splitlines():
        if line == "":
            continue
        if len(current) == 3:
            current = []
            configs.append(current)
    
        label, _,  rest = line.partition(":")
        x, y = [val.strip() for val in rest.split(",")]
        x_op,  x_val = parse_operation(x)
        y_op,  y_val = parse_operation(y)
        current.append(com.Point(int(x_val), int(y_val), label))
    return configs
    # return com.parse_raw_to_grid(input_data)

def inputParser2(input_data):
    return inputParser1(input_data)

INF = 9999999999999
def minForPrize(maximum, a, b, prize):
    min_for_prize = INF
    a_cost = 3
    b_cost = 1
    for i in range(maximum, -1, -1):
        a_tokens = i * a_cost
        a_pos = (i * a.x, i * a.y)
        if (a_pos[0] > prize.x or a_pos[1] > prize.y):
            continue
        for j in range(0, maximum + 1):
            tokens =  a_tokens + j * b_cost
            if tokens > min_for_prize:
                continue
            if ((prize.x, prize.y) == (a_pos[0] + (j * b.x), a_pos[1] + (j * b.y))):
                return tokens
    return min_for_prize

def Part1(data):
    maximum = 100
    total = 0
    for a, b, prize in data:
        min_for_prize = minForPrize(maximum, a, b, prize)
        if min_for_prize != INF:
            total += min_for_prize  

    return total

def smarterMinForPrize(a, b, prize):
    a_cost = 3
    b_cost = 1

    z = a.x
    y = b.x
    x = prize.x

    w = a.y
    v = b.y
    u = prize.y

    # equations are in the form
    # za + yb = x
    # wa + vb = u

    # Solving that system gives
    a = (v*x - u*y)/(v*z - w*y)
    b = (u*z - w*x)/(v*z - w*y)

    if a % 1 != 0 or b % 1 != 0:
        return None

    return a_cost * a + b_cost * b


def Part2(data):
    total = 0
    add = 10000000000000
    for a, b, prize in data:
        prize = com.Point(prize.x + add, prize.y + add, prize.data)
        min_for_prize = smarterMinForPrize(a, b, prize)
        if min_for_prize is not None:
            total += min_for_prize  

    return total

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
            "480",
            [[example.answer_b]],
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