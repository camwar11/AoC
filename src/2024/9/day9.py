from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com
from collections import deque
from heapq import heappush, heappop

runExamples = True
day, year = get_day_and_year()
puzzle = Puzzle(year, day)

def inputParser1(input_data):
    return input_data

def inputParser2(input_data):
    return inputParser1(input_data)

FREE_SPACE = -1
def parse_files(line):
    files = deque()
    file_id = 0
    full_idx = 0
    for i, size in enumerate([int(x) for x in line]):
        if i % 2 == 0:
            files.append([file_id, size, full_idx])
            file_id += 1
        else:
            if size == 0:
                continue
            files.append([FREE_SPACE, size, full_idx])
        full_idx += size
    return files

def calc_checksum(file_id: int, start: int, size: int):
    multiple = sum([x for x in range(start, start + size)])

    checksum = file_id * multiple
    #print(f"id: {file_id}; start: {start}; size: {size}; checksum: {checksum}")
    return checksum

def Part1(data):
    files = parse_files(data)

    checksum = 0
    file_index = 0
    i = 0
    count = len(files)
    for file_id, size, _ in [x for x in files]:
        if i == count:
            break
        if file_id == FREE_SPACE:
            while size > 0:
                file_to_move = files[-1]
                if file_to_move[0] == FREE_SPACE:
                    files.pop()
                    count -= 1
                    continue
                filled = file_to_move[1]
                size -= filled
                if size < 0:
                    leftover = size * -1
                    filled -= leftover
                    file_to_move[1] = leftover
                else:
                    files.pop()
                    count -= 1
                checksum += calc_checksum(file_to_move[0], file_index, filled)
                file_index += filled
        else:
            checksum += calc_checksum(file_id, file_index, size)
            file_index += size
        i += 1
    return checksum

def moveFile(free_space, file_to_move):
    file_id, size, index = file_to_move
    earliest = index
    free_space_size = 0
    for cand_size in range(size, 10):
        if cand_size not in free_space or len(free_space[cand_size]) == 0:
            continue
        free_idx = free_space[cand_size][0]
        if free_idx < earliest:
            earliest = free_idx
            free_space_size = cand_size

    if earliest == index:
        return

    file_to_move[2] = earliest
    
    free_indices = free_space[free_space_size]
    heappop(free_indices)
    remainder = free_space_size - size
    if remainder != 0:
        free_vals = free_space.setdefault(remainder, [])
        heappush(free_vals, earliest+size)

def Part2(data):
    all_files = parse_files(data)
    data_files = deque()
    free_space = dict()
    max_free_space = 0
    for file in [x for x in all_files]:
        file_id, size, index = file
        if file_id == FREE_SPACE:
            if size > max_free_space:
                max_free_space = size
            free_vals = free_space.setdefault(size, [])
            heappush(free_vals, index)
        else:
            data_files.append(file)
    
    final_files = []
    while data_files:
        file_to_move = data_files.pop()
        file_id, size, index = file_to_move
        moveFile(free_space, file_to_move)
        heappush(final_files, (file_to_move[2], file_to_move[0], file_to_move[1]))

    checksum = 0
    while final_files:
        file_index, file_id, size = heappop(final_files)
        checksum += calc_checksum(file_id, file_index, size)

    return checksum

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
        if part2Answer != "2858":
            print(f"Incorrect: part2 example {i}. Extra={example.extra};Input=\n{example.input_data}\nExpect: {"2858"}\nActual: {part2Answer}")
            part2ExamplePassed = False
            break
        print("Part 2 Example Passed")
        part2ExamplePassed = True
else:
    part1ExamplePassed = True
    part2ExamplePassed = True

if part1ExamplePassed:
    #puzzle.answer_a = Part1(inputParser1(puzzle.input_data))
    pass

if part2ExamplePassed:
    puzzle.answer_b = Part2(inputParser2(puzzle.input_data))