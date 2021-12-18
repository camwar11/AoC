from __future__ import annotations
from typing import List, Optional, Set, Tuple, Union
import common as com
from common.tree import tree, tree_node
import math
import copy

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def explode(tree: com.tree, node: tree_node, levelOfNesting: int):
    if not(levelOfNesting == 4 and len(node.children) == 2):
        return False

    nextLeftNode = get_next_node(tree, node, True)
    nextRightNode = get_next_node(tree, node, False)

    if nextLeftNode:
        nextLeftNode.data += node.children[0].data
    
    if nextRightNode:
        nextRightNode.data += node.children[1].data

    node.children.clear()
    node.data = 0
    return True

def split(tree: com.tree, node: tree_node):
    if not(node.data and node.data >= 10):
        return False

    value = node.data / 2
    node.addChild(tree_node(int(math.floor(value))))
    node.addChild(tree_node(int(math.ceil(value))))
    node.data = None
    return True

def get_next_node(tree: com.tree, node: tree_node, left = True):
    for ancestor in node.getAncestors(False):
        returnNext = False
        for search, _ in tree.depthFirstIterate(ancestor, left):
            if search == node:
                returnNext = True
                continue
            if returnNext and len(search.children) == 0:
                return search
    return None

def parseLine(line: str) -> tree_node:
    parent_node = None
    for char in line:
        if char == '[':
            new_node = tree_node(None)
            if parent_node:
                parent_node.addChild(new_node)
            parent_node = new_node
            continue
        if char.isnumeric():
            parent_node.addChild(tree_node(int(char)))
            continue
        if char == ',':
            continue
        if char == ']':
            if parent_node.parent is None:
                # Finished parsing
                return parent_node
            parent_node = parent_node.parent
    return 'Bad parse'

def findMagnitude(node: tree_node):
    if len(node.children) == 0:
        return node.data
    
    left = findMagnitude(node.children[0]) * 3
    right = findMagnitude(node.children[1]) * 2
    return left + right

def printTree(node: tree_node):
    if len(node.children) == 2:
        print('[', end='')
        printTree(node.children[0])
        print(',', end='')
        printTree(node.children[1])
        print(']', end='')
    else:
        print(str(node.data), end='')
        
def Part1(lines: List[str]):
    snail_tree = tree()
    root = None
    shouldPrint = False

    for line in lines:
        newNode = parseLine(line.strip())
        if shouldPrint:
            print()

        if root is None:
            snail_tree.addNode(None, newNode)
            root = newNode
        else:
            newRoot = tree_node(None)
            snail_tree.replaceNode(root, newRoot)
            snail_tree.addNode(newRoot, root)
            snail_tree.addNode(newRoot, newNode)
            root = newRoot
            needsReduction = True
            while needsReduction:
                anyReduced = False
                for node, level in snail_tree.depthFirstIterate():
                    anyReduced |= explode(snail_tree, node, level)
                    if anyReduced:
                        break
                if not anyReduced:
                    for node, level in snail_tree.depthFirstIterate():
                        anyReduced |= split(snail_tree, node)
                        if anyReduced:
                            break
                needsReduction = anyReduced
                if shouldPrint:
                    printTree(root)
                    print()

    return findMagnitude(root)

def Part2(lines):
    all_nodes = list()
    maxMagnitude = 0

    for line in lines:
        newNode = parseLine(line.strip())
        all_nodes.append(newNode)
    
    for xNode in all_nodes:
        for yNode in all_nodes:
            if xNode == yNode:
                continue
            
            snail_tree = tree()
            root = tree_node(None)
            snail_tree.addNode(None, root)
            snail_tree.addNode(root, copy.deepcopy(xNode))
            snail_tree.addNode(root, copy.deepcopy(yNode))

            needsReduction = True
            while needsReduction:
                anyReduced = False
                for node, level in snail_tree.depthFirstIterate():
                    anyReduced |= explode(snail_tree, node, level)
                    if anyReduced:
                        break
                if not anyReduced:
                    for node, level in snail_tree.depthFirstIterate():
                        anyReduced |= split(snail_tree, node)
                        if anyReduced:
                            break
                needsReduction = anyReduced
            
            maxMagnitude = max(maxMagnitude, findMagnitude(root))

    return maxMagnitude

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