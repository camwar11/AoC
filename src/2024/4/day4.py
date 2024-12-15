from aocd.get import get_day_and_year
from aocd.models import Puzzle
import common as com

runExamples = False
day, year = get_day_and_year()
puzzle = Puzzle(year, day)

def inputParser1(input_data):
    grid = com.CartesianGrid()
    com.parse_to_grid(input_data.splitlines(), grid)
    return grid

def inputParser2(input_data):
    return inputParser1(input_data)

def searchForWord(word: str, point: com.Point, direction = None):
    first_char = word[0]
    if point is None or point.data != first_char:
        return 0
    if word.__len__() == 1:
        return 1
    remaining_chars = word[1:]
    total = 0
    if direction is None:
        for direction in com.CartesianGrid.AllDirections():
            total += searchForWord(word, point, direction)
    else:
        newPoint = point.getAdjacentPoint(direction)
        total += searchForWord(remaining_chars, newPoint, direction)
    return total
    

def Part1(data: com.CartesianGrid):
    word = "XMAS"
    total = 0
    for point in data.getAllPoints():
        total += searchForWord(word, point)
    return total

def searchForXmas(point: com.Point):
    if point is None or point.data != "A":
        return 0
    
    up_left = point.getAdjacentPoint(com.CartesianGrid.UP_LEFT, True).data
    up_right = point.getAdjacentPoint(com.CartesianGrid.UP_RIGHT, True).data
    down_left = point.getAdjacentPoint(com.CartesianGrid.DOWN_LEFT, True).data
    down_right = point.getAdjacentPoint(com.CartesianGrid.DOWN_RIGHT, True).data

    one = ["M", "S"]
    two = ["M", "S"]

    if (up_left == "M" and down_right == "S") or (up_left == "S" and down_right == "M"):
        if (up_right == "M" and down_left == "S") or (up_right == "S" and down_left == "M"):
            return 1
    return 0

def Part2(data):
    total = 0
    for point in data.getAllPoints():
        total += searchForXmas(point)
    return total

if runExamples:
    part1ExamplePassed = False
    part2ExamplePassed = False
    for i, example in enumerate(puzzle.examples):
        example1 ="""MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
        part1Answer = str(Part1(inputParser1(example1)))
        if part1Answer != "18":
            print(f"Incorrect: part1 example {i}. Extra={example.extra};Input=\n{example1}\nExpect: {"18"}\nActual: {part1Answer}")
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