import math
from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com

RUN_EXAMPLES = True
day, year = get_day_and_year()
puzzle = Puzzle(year, day)

def input_parser_1(input_data: str) -> list[list[int]]:
    return [list(map(int, x.split(','))) for x in input_data.splitlines()]
    # return com.parse_raw_to_grid(input_data)

def input_parser_2(input_data: str) -> list[list[int]]:
    return input_parser_1(input_data)

def distance(p1: list[int], p2: list[int]) -> int:
    """Calculate the Euclidean distance between points in N dimensions."""
    return sum((a - b) ** 2 for a, b in zip(p1, p2)) ** 0.5

def part_1(data: list[list[int]], num_connections: int) -> str | None:
    adjacencies: list[(int, tuple[int, int])] = []

    for i, first in enumerate(data):
        for j, second in enumerate(data):
            if i >= j:
                continue
            adjacencies.append((distance(first, second), (i, j)))
        adjacencies.sort()
            
    circuits: list[set[int]] = []
    box_to_circuit: dict[int, int] = {}

    for connection in range(num_connections):
        _, (first, second) = adjacencies[connection]
        existing_first_circuit_idx = box_to_circuit.get(first)
        existing_second_circuit_idx = box_to_circuit.get(second)
        index_to_use = None
        if existing_first_circuit_idx is None and existing_second_circuit_idx is None:
            index_to_use = len(circuits)
            circuits.append(set())
        elif existing_first_circuit_idx is not None and existing_second_circuit_idx is not None:
            if existing_first_circuit_idx == existing_second_circuit_idx:
                continue
            first_circuit = circuits[existing_first_circuit_idx]
            second_circuit = circuits[existing_second_circuit_idx]
            if len(first_circuit) < len(second_circuit):
                first_circuit, second_circuit = second_circuit, first_circuit
                existing_first_circuit_idx, existing_second_circuit_idx = existing_second_circuit_idx, existing_first_circuit_idx
            index_to_use = existing_first_circuit_idx
            for box in second_circuit:
                first_circuit.add(box)
                box_to_circuit[box] = index_to_use
            circuits[existing_second_circuit_idx] = set()
            continue
        elif existing_first_circuit_idx is not None:
            index_to_use = existing_first_circuit_idx
        elif existing_second_circuit_idx is not None:
            index_to_use = existing_second_circuit_idx
        
        circuit = circuits[index_to_use]
        circuit.add(first)
        circuit.add(second)
        box_to_circuit[first] = index_to_use
        box_to_circuit[second] = index_to_use

    counts = list(map(len, circuits))
    counts.sort()

    return math.prod(counts[-3:])

def part_2(data: list[list[int]]) -> str | None:
    adjacencies: list[(int, tuple[int, int])] = []

    for i, first in enumerate(data):
        for j, second in enumerate(data):
            if i >= j:
                continue
            adjacencies.append((distance(first, second), (i, j)))
        adjacencies.sort()
            
    circuits: list[set[int]] = []
    box_to_circuit: dict[int, int] = {}

    for _, (first, second) in adjacencies:
        existing_first_circuit_idx = box_to_circuit.get(first)
        existing_second_circuit_idx = box_to_circuit.get(second)
        index_to_use = None
        if existing_first_circuit_idx is None and existing_second_circuit_idx is None:
            index_to_use = len(circuits)
            circuits.append(set())
        elif existing_first_circuit_idx is not None and existing_second_circuit_idx is not None:
            if existing_first_circuit_idx == existing_second_circuit_idx:
                continue
            first_circuit = circuits[existing_first_circuit_idx]
            second_circuit = circuits[existing_second_circuit_idx]
            if len(first_circuit) < len(second_circuit):
                first_circuit, second_circuit = second_circuit, first_circuit
                existing_first_circuit_idx, existing_second_circuit_idx = existing_second_circuit_idx, existing_first_circuit_idx
            index_to_use = existing_first_circuit_idx
            for box in second_circuit:
                first_circuit.add(box)
                box_to_circuit[box] = index_to_use
            circuits[existing_second_circuit_idx] = set()
            if len(first_circuit) == len(data):
                return str(data[first][0] * data[second][0])
            continue
        elif existing_first_circuit_idx is not None:
            index_to_use = existing_first_circuit_idx
        elif existing_second_circuit_idx is not None:
            index_to_use = existing_second_circuit_idx
        
        circuit = circuits[index_to_use]
        circuit.add(first)
        circuit.add(second)
        if len(circuit) == len(data):
            return str(data[first][0] * data[second][0])
        box_to_circuit[first] = index_to_use
        box_to_circuit[second] = index_to_use
    return None

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
        part1Answer = str(part_1(input_parser_1(example[0]), 10))
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
    #part1Answer = part_1(input_parser_1(puzzle.input_data), 1000)
    if part1Answer is not None:
        print(f"Submitting part 1 answer of {part1Answer}")
    puzzle.answer_a = part1Answer

if part2_example_passed:
    part2Answer = part_2(input_parser_2(puzzle.input_data))
    if part2Answer is not None:
        print(f"Submitting part 2 answer of {part2Answer}")
        puzzle.answer_b = part2Answer