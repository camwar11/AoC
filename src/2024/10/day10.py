from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com

runExamples = True
day, year = get_day_and_year()
puzzle = Puzzle(year, day)

def edgeWeightFcn1(start, end):
    # Do this backwards to go from 9s down to other
    if start.data - end.data != 1:
        return None
    return 1

def edgeWeightFcn2(start, end):
    if end.data - start.data != 1:
        return None
    return 1

def inputParser1(input_data):
    grid = com.CartesianGrid()
    lines = input_data.splitlines()
    lines.reverse()
    com.parse_to_grid(lines, grid, conversionFcn=int)
    graph = com.Graph.parse_from_grid(grid, edgeWeightFinder=edgeWeightFcn1)
    return graph

def inputParser2(input_data):
    grid = com.CartesianGrid()
    lines = input_data.splitlines()
    lines.reverse()
    com.parse_to_grid(lines, grid, conversionFcn=int)
    graph = com.Graph.parse_from_grid(grid, edgeWeightFinder=edgeWeightFcn2)
    return graph

def walkTrail(scores, graph, current_node, peak):
    score = scores.setdefault(current_node, set())
    score.add(peak)
    for node in graph.direct_connected_weights_and_edges(current_node):
        walkTrail(scores, graph, node, peak)

def Part1(data):
    scores = dict()
    trailheads = set()
    for node in data.get_all_nodes():
        if node.data == 9:
            walkTrail(scores, data, node, node)
        if node.data == 0:
            trailheads.add(node)

    return sum([len(scores[x]) for x in trailheads])

def getRating(graph, current_node):
    if current_node.data == 9:
        return 1
    total = 0
    for node in graph.direct_connected_weights_and_edges(current_node):
        total += getRating(graph, node)
    return total

def Part2(data):
    total = 0
    for node in data.get_all_nodes():
        if node.data == 0:
            total += getRating(data, node)
    return total

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
            """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""",
            example.answer_a,
            "81",
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
        part2Answer = str(Part2(inputParser2(example[0])))
        if part2Answer != example[2]:
            print(f"Incorrect: part2 example {i}. Extra={example[3]};Input=\n{example[0]}\nExpect: {example[2]}\nActual: {part2Answer}")
            part2ExamplePassed = False
            break
        print("Part 2 Example Passed")
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