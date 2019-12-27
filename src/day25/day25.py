import common as com
from operator import add
from copy import deepcopy
from collections import deque
from itertools import combinations
import math

test = False
part1 = True
part2 = False

drop = 'drop '
take = 'take '
north = 'north'
south = 'south'
east = 'east'
west = 'west'
inventory = 'inv'

def toAsciiInts(string):
    return [ord(i) for i in string]

def printCell(cell):
    return cell.data[0]

grid = com.CartesianGrid(''.rjust(30), printCell)
compys = []
pickUpItems = True
def inputCallback(gridIdx):
    global compys, grid, north, south, east, west
    inputIdx = 0
    inputValue = None
    compy = compys[gridIdx]
    def internalCallback():
        nonlocal inputValue, inputIdx, compy
        if inputValue is None:
            if compy[3]:
                realInput = compy[3].pop()
            else:
                realInput = input()
                while realInput == 'print':
                    print(grid)
                    realInput = input()
            if realInput.startswith(take):
                ownedItems.add(realInput.replace(take, ''))
            move = False
            if realInput == north:
                compy[1] = com.vector_math(add, compy[1], grid.UP)
                move = True
            elif realInput == south:
                compy[1] = com.vector_math(add, compy[1], grid.DOWN)
                move = True
            elif realInput == west:
                compy[1] = com.vector_math(add, compy[1], grid.LEFT)
                move = True
            elif realInput == east:
                compy[1] = com.vector_math(add, compy[1], grid.RIGHT)
                move = True
            if move:
                point = com.Point(*compy[1], None)
                grid.addPoint(point)

            inputValue = toAsciiInts(realInput + '\n')
            inputIdx = 0

        valueToReturn = inputValue[inputIdx]
        inputIdx += 1
        if inputIdx == len(inputValue):
            inputValue = None
        return valueToReturn 
    return internalCallback

badItems = set()
badItems.add('infinite loop')
badItems.add('giant electromagnet')
ownedItems = set()
droppedItems = set()
allGoodItems = set()
invalidMin = None
invalidMax = None
currentlyCheckingWeights = False
lastChecked = None
def outputCallback(outputIdx):
        global compys
        compy = compys[outputIdx]

        def internalCallback(output):
            global drop, take, north, south, east, west, inventory, grid, badItems, ownedItems, pickUpItems, currentlyCheckingWeights, invalidMin, invalidMax, allGoodItems, droppedItems
            nonlocal outputIdx, compy
            value = chr(output)
            outputBuffer = compy[2]
            outputBuffer.append(value)
            items = None
            if value == '?':
                asStr = ''.join(outputBuffer)
                if not asStr.endswith('Command?'):
                    return
                split = asStr.strip().split('\n\n')
                name = None
                for splitVal in split:
                    if splitVal.startswith('=='):
                        name = (str(compy[1][0]) + ',' + str(compy[1][1]) + ': ' + ''.join(list(splitVal.split('\n')[0])[3:-3])).rjust(30)
                    elif splitVal.startswith('Doors here lead'):
                        directions = [i.strip('- ') for i in splitVal.strip().split('\n')[1:]]
                    elif splitVal.startswith('Items here'):
                        items = [i.strip('- ') for i in splitVal.strip().split('\n')[1:]]

                if name:
                    cell = grid.getPoint(*compy[1])
                    cell.data = (name, directions, items)
                    outputBuffer.clear()
                    if 'Security Checkpoint' in name:
                        pickUpItems = False
            
            if not pickUpItems and not currentlyCheckingWeights:
                allGoodItems = set(ownedItems)
                invalidMin = 1
                invalidMax = len(allGoodItems)
                currentlyCheckingWeights = True

            if currentlyCheckingWeights and not compy[3]:
                halfway = 4#math.ceil((invalidMax + invalidMin) / 2)
                allAdditions = []
                for combo in combinations(allGoodItems, halfway):
                    thingsToAdd = []
                    for item in list(ownedItems):
                        if item not in combo:
                            thingsToAdd.append(drop + item)
                            ownedItems.remove(item)

                    for item in combo:
                        if item not in ownedItems:
                            thingsToAdd.append(take + item)
                            ownedItems.add(item)
                    thingsToAdd.append('inv')
                    thingsToAdd.append(south)
                    thingsToAdd.reverse()
                    allAdditions.append(thingsToAdd)
                
                for addition in allAdditions[::-1]:
                    for thingToAdd in addition:
                        compy[3].append(thingToAdd)


            
            if items and pickUpItems:
                for item in [i for i in items if not i in badItems]:
                    itemCompy = deepcopy(compy[0])
                    inputValue = toAsciiInts(take + item + '\n')
                    inputIdx = 0
                    needsToContinue = True
                    def itemInput():
                        nonlocal inputValue, inputIdx, needsToContinue
                        if inputValue is None:
                            needsToContinue = False
                            return 10
                        valueToReturn = inputValue[inputIdx]
                        inputIdx += 1
                        if inputIdx == len(inputValue):
                            inputValue = None
                        return valueToReturn
                    itemCompy.needsInputCallback = itemInput
                    def itemOutput(output):
                        value = chr(output)
                        print(value, end='')
                    itemCompy.hasOutputCallback = itemOutput
                    
                    bad = False
                    while needsToContinue:
                        result = itemCompy.RunOneInstruction()
                        if result != itemCompy.CONTINUING:
                            badItems.add(item)
                            bad = True
                            break
                    if not bad:
                        compy[3].append(take + item)
            print(value, end='')
        return internalCallback

keepRunning = True
def Part1(lines):
    global compys, grid, keepRunning
    compys.append([None, [0,0], [], deque()])
    origin = com.Point(0, 0, None)
    grid.addPoint(origin)
    intCode = com.intCode(lines[0], False, hasOutputCallback=outputCallback(0),needsInputCallback=inputCallback(0))
    compys[0][0] = intCode
    while keepRunning:
        intCode.RunIntCodeComputer()

def Part2(lines):
    pass

file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file)

if part1:
    Part1(lines)

if part2:
    Part2(lines)