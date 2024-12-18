from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com
from collections import deque

runExamples = False
day, year = get_day_and_year()
puzzle = Puzzle(year, day)

def inputParser1(input_data):
    grid = com.CartesianGrid()
    lines = input_data.splitlines()
    lines.reverse()
    com.parse_to_grid(lines, grid)
    return grid

def inputParser2(input_data):
    return inputParser1(input_data)

INFINITE = 99999999999

def run_maze(maze, point, end, direction):
    visited = dict()
    to_visit = {
        point: [(direction, 0)]
    }

    while len(to_visit) > 0:
        point, dirs_and_scores = to_visit.popitem()

        for direction, score in dirs_and_scores:
            #print(f"{direction} x:{point.x} y: {point.y} val: {point.data} score: {score}")
            if point in visited and direction in visited[point]:
                point_dir_min = visited[point][direction]
            else:
                visited.setdefault(point, dict())
                point_dir_min = INFINITE

            if score >= point_dir_min or point.data == '#':
                continue

            visited[point][direction] = score

            turns = [
                (com.CartesianGrid.turn_clock[direction], 1000), 
                (com.CartesianGrid.turn_counterclock[direction], 1000), 
                (com.CartesianGrid.turn_180[direction], 2000), 
            ]
            for dir_to_go, weight in turns:
                dir_score = to_visit.setdefault(point, [])
                dir_score.append((dir_to_go, score + weight))

            forward = point.getAdjacentPoint(com.CartesianGrid.directions[direction])
            dir_score = to_visit.setdefault(forward, [])
            dir_score.append((direction, score + 1))
    
    return min(visited[end].values())

def run_maze2(maze, point, end, direction):
    visited_score = dict()
    visited_path = dict()
    to_visit = deque([(point, direction, 0, [])])

    debug = {
        (11, 5, '>'),
        (12, 5, '>'),
        (13, 5, '^'),
        (13, 6, '^'),
        (13, 7, '>'),
        (14, 7, '>'),
        (15, 7, '^'),
        (15, 8, '^'),
        (15, 9, '^'),
        (15, 10, '^'),
    }
    while to_visit:
        point, direction, score, path = to_visit.popleft()
        if point.x == 15 and point.y == 10:
            pass

        #print(f"{direction} x:{point.x} y: {point.y} val: {point.data} score: {score}")
        if point in visited_score and direction in visited_score[point]:
            point_dir_min = visited_score[point][direction]
        else:
            visited_score.setdefault(point, dict())
            visited_path.setdefault(point, dict())
            point_dir_min = INFINITE

        if score > point_dir_min or point.data == '#':
            continue

        if (point.x, point.y, direction) in debug:
            pass

        new_path = path.copy()
        new_path.append(point)

        if score == point_dir_min:
            paths = visited_path[point].setdefault(direction, [])
            paths.append(new_path)
            continue

        visited_path[point][direction] = new_path
        visited_score[point][direction] = score

        turns = [
            (com.CartesianGrid.turn_clock[direction], 1000), 
            (com.CartesianGrid.turn_counterclock[direction], 1000), 
            (com.CartesianGrid.turn_180[direction], 2000), 
        ]
        for dir_to_go, weight in turns:
            to_visit.append((point, dir_to_go, score + weight, path))

        forward = point.getAdjacentPoint(com.CartesianGrid.directions[direction])
        to_visit.append((forward, direction, score + 1, new_path))
    
    min_keys = []
    min_value = None
    value: dict = visited_score[end]

    for key, val in value.items():
        if min_value is None or val < min_value:
            min_keys = [key]
            min_value = val
            continue
        if val == min_value:
            min_keys.append(key)

    nodes = set()
    for key in min_keys:
        path = visited_path[end][key]
        for node in path:
            try:
                iter(node)
                for sub in node:
                    try:
                        iter(sub)
                        for subsub in sub:
                            subsub.data = "O"
                            nodes.add(subsub)
                    except TypeError:
                        sub.data = "O"
                        nodes.add(sub)
            except TypeError:
                node.data = "O"
                nodes.add(node)
    
            
    #print(maze)
    return len(nodes)

def Part1(data):
    start = None
    end = None
    for point in data.getAllPoints():
        if point.data == 'S':
            start = point
        if point.data == 'E':
            end = point
    return run_maze(data, start, end, '>')

def Part2(data):
    start = None
    end = None
    for point in data.getAllPoints():
        if point.data == 'S':
            start = point
        if point.data == 'E':
            end = point
    return run_maze2(data, start, end, '>')

if runExamples:
    part1ExamplePassed = False
    part2ExamplePassed = False
    for i, example in enumerate(puzzle.examples):
        input_data = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""
        part1Answer = str(Part1(inputParser1(input_data)))
        if part1Answer != "11048":
            print(f"Incorrect: part1 example {i}. Extra={example.extra};Input=\n{input_data}\nExpect: {11048}\nActual: {part1Answer}")
            part1ExamplePassed = False
            break
        
        print("Part 1 Example Passed")
        part1ExamplePassed = True
        part2Answer = str(Part2(inputParser2(input_data)))
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