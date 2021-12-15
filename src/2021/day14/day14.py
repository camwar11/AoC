from typing import List, Set
import common as com
from common.cartesianGrid import CartesianGrid
from common.utilityfunctions import increment_dict

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def RunPolymers(lines: List[str], steps: int):
    template = None
    pairRules = dict()
    counts = dict()

    for line in lines:
        if template == None:
            template = line.strip()
            continue
        if line.strip() == '':
            continue
        pair, insertion = line.strip().split('->')
        pairRules[pair.strip()] = insertion.strip()
    
    pairs = dict()
    previous = None
    for char in template:
        increment_dict(counts, char, 1)
        if previous == None:
            previous = char
            continue
        pair = previous + char
        increment_dict(pairs, pair, 1)
        previous = char

    for step in range(steps):
        newPairs = dict()
        for pair in pairs:
            count = 1
            if pair in pairs:
                count = pairs[pair]
            
            insertion = pairRules[pair]
            increment_dict(counts, insertion, count)

            
            newPair1 = pair[0] + insertion
            increment_dict(newPairs, newPair1, count)
            
            newPair2 = insertion + pair[1]
            increment_dict(newPairs, newPair2, count)
        pairs = newPairs
        #print(pairs)
        print('Length after ' + str(step + 1) + ' ' + str(1 + sum([pairs[x] for x in pairs])))
    
    minimum = 9999999999999999999
    maximum = -1
    least = None
    most = None
    for char in counts:
        count = counts[char]
        if count < minimum:
            minimum = count
            least = char
        elif count > maximum:
            maximum = count
            most = char
    
    return maximum - minimum

def Part1(lines: List[str]):
    return RunPolymers(lines, 10)
def Part2(lines):        
    return RunPolymers(lines, 40)

if test:
    lines = com.readFile("test.txt")
else:
    #print(puzzle.input_data)
    #lines = com.readFile("input.txt")
    lines = puzzle.input_data.splitlines()

if part1:
    part1Answer = Part1(lines)
    if part1Answer is None:
        print("Returned None for part1")
    elif test:
        print("Part1 test result: \n" + str(part1Answer))
    else:
        puzzle.answer_a = part1Answer
            

if part2:
    part2Answer = Part2(lines)
    if part2Answer is None:
        print("Returned None for part2")
    elif test:
        print("Part2 test result: \n" + str(part2Answer))
    else:
        puzzle.answer_b = part2Answer