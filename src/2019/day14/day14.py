import common as com
import math

test = False
part1 = False
part2 = True

def runReaction(element, desiredTotalAmount, reactions, elementUsage, leftovers):
    currentAmount = leftovers.get(element)
    if currentAmount is not None:
        if currentAmount >= desiredTotalAmount:
            return
    else:
        currentAmount = 0
    reaction = reactions.get(element)
    reactionProduces = reaction[0]
    reactionNeeds = reaction[1]
    neededAmount = desiredTotalAmount - currentAmount
    neededTimesToRun = math.ceil(neededAmount / reactionProduces)
    for inputAmountAndElement in reactionNeeds:
        neededInputAmount = inputAmountAndElement[0] * neededTimesToRun
        runReaction(inputAmountAndElement[1], neededInputAmount, reactions, elementUsage, leftovers)
        leftovers[inputAmountAndElement[1]] -= neededInputAmount
        used = elementUsage.get(inputAmountAndElement[1])
        if used is None:
            elementUsage[inputAmountAndElement[1]] = 0
        elementUsage[inputAmountAndElement[1]] += neededInputAmount
    
    leftover = leftovers.get(element)
    if leftover is None:
        leftovers[element] = 0
    leftovers[element] += reactionProduces * neededTimesToRun
        

def Part1(lines):
    reactions = {}
    for line in lines:
        inRxn, outRxn = line.strip().split('=>')
        outputAmount, outputElement = outRxn.strip().split(' ')
        outputAmount = int(outputAmount)
        inputs = []
        for rxn in inRxn.split(','):
            amount, element = rxn.strip().split(' ')
            amount = int(amount)
            inputs.append((amount, element))
        reactions[outputElement] = (outputAmount, inputs)
    elementUsage = {}
    leftoverElements = {}
    leftoverElements['ORE'] = 9999999999999999999999999999

    runReaction('FUEL', 1, reactions, elementUsage, leftoverElements)   
    print(elementUsage) 

def Part2(lines):
    reactions = {}
    for line in lines:
        inRxn, outRxn = line.strip().split('=>')
        outputAmount, outputElement = outRxn.strip().split(' ')
        outputAmount = int(outputAmount)
        inputs = []
        for rxn in inRxn.split(','):
            amount, element = rxn.strip().split(' ')
            amount = int(amount)
            inputs.append((amount, element))
        reactions[outputElement] = (outputAmount, inputs)

    fuelLow = 0
    fuelHigh = 10000000
    target = 1000000000000
    def runSearch(value):
        elementUsage = {}
        leftoverElements = {}
        leftoverElements['ORE'] = 999999999999999999999999999999
        runReaction('FUEL', value, reactions, elementUsage, leftoverElements)   
        usage = int(elementUsage['ORE'])
        return usage
    
    def targetValueIsHigher(value):
        nonlocal target
        return value < target
    
    def targetValueIsLower(value):
        nonlocal target
        return value > target

    result = com.binary_search(fuelLow, fuelHigh, runSearch, targetValueIsHigher, targetValueIsLower )

    print(result)

file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file)

if part1:
    Part1(lines)

if part2:
    Part2(lines)