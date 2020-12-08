import common as com
import re

test = False
part1 = True
part2 = True
puzzle = com.PuzzleWithTests()

def getBagType(predicate: str):
    return predicate[:predicate.find(' bags')]

def walkBagNodes(foundNodes, bagGraph, currentNode, multiplier):
    count = multiplier
    edgesAndWeights = bagGraph.direct_connected_weights_and_edges(currentNode)
    for edge in edgesAndWeights:
        foundNodes.add(edge)
        insideBagCount = edgesAndWeights[edge]
        count += walkBagNodes(foundNodes, bagGraph, edge, insideBagCount * multiplier)
    return count


def CountBags(lines, startingBag, part1):
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
                if part1:
                    bagGraph.add_edge(insideBagType, bagType, 1)
                else:
                    bagGraph.add_edge(bagType, insideBagType, int(number))
    foundNodes = set()
    total = walkBagNodes(foundNodes, bagGraph, startingBag, 1)
    if part1:
        return foundNodes.__len__()
    else:
        return total - 1

def Part1(lines, startingBag):
    return CountBags(lines, startingBag, True)

def Part2(lines, startingBag):
    return CountBags(lines, startingBag, False)

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
    part2Answer = Part2(lines, 'shiny gold')
    if part2Answer is None:
        print("Returned None for part2")
    elif test:
        print("Part2 test result: " + str(part2Answer))
    else:
        puzzle.answer_b = part2Answer