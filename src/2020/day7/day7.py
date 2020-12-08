import common as com
import re

test = False
part1 = True
part2 = False
puzzle = com.PuzzleWithTests()

def getBagType(predicate: str):
    return predicate[:predicate.find(' bags')]

def Part1(lines, startingBag):
    bagGraph = com.Graph()
    bagGraph.add_node(startingBag)
    for line in lines:
        bagType, contains = line.split('contain')
        bagType = getBagType(bagType)
        if 'no other bags' not in contains:
            bagGraph.add_node(bagType)
            insideBags = contains.split(',')
            for insideBag in insideBags:
                number, insideBagType = re.findall('(\d+) (.*? .*?) bag', insideBag)[0]
                bagGraph.add_node(insideBagType)
                bagGraph.add_edge(insideBagType, bagType, int(number))
    #print(bagGraph)
    foundNodes = set()
    nodesToWalk = list()
    nodesToWalk.append(startingBag)

    while nodesToWalk:
        newNodes = list(nodesToWalk)
        nodesToWalk.clear()
        for node in newNodes:
            if node != startingBag:
                foundNodes.add(node)
            for edge in bagGraph.direct_connected_weights_and_edges(node):
                if edge not in foundNodes:
                    nodesToWalk.append(edge)

    return foundNodes.__len__()

def Part2(lines):
    return None

if test:
    lines = com.readFile("test.txt")
else:
    #print(puzzle.input_data)
    #lines = com.readFile("input.txt")
    lines = puzzle.input_data.splitlines()

if part1:
    part1Answer = Part1(lines, 'shiny gold')
    if part1Answer is None:
        print("Returned None for part1")
    elif test:
        print("Part1 test result: " + str(part1Answer))
    else:
        puzzle.answer_a = part1Answer
            

if part2:
    part2Answer = Part2(lines)
    if part2Answer is None:
        print("Returned None for part2")
    elif test:
        print("Part2 test result: " + str(part2Answer))
    else:
        puzzle.answer_b = part2Answer