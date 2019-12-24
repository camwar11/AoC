import common as com
from functools import reduce
from operator import add, mul
from itertools import cycle, repeat

test = False
part1 = False
part2 = True

def getOnes(a):
    result = int(str(a)[-1])
    return result

def Part1(lines):
    inputs = [int(i) for i in lines[0].strip()]
    basePattern = [0, 1, 0, -1]
    inputsLen = len(inputs)
    
    for phase in range(100):
        output = []
        index = 0
        for num in inputs:
            pattern = []
            patternIndex = 0
            for pat in cycle(basePattern):
                for i in range(index+1):
                    pattern.append(pat)
                    patternIndex += 1
                if patternIndex > inputsLen:
                    break
            newValue = reduce(add, map(mul, inputs, pattern[1:]))
            newValueOnes = getOnes(newValue)
            output.append(newValueOnes)
            index += 1
        print('Phase', phase, output)
        inputs = output

def Part2(lines):
    inputs = [int(i) for i in lines[0].strip()]
    offset = inputs[:7]
    offset = int(''.join(map(str, offset)))
    inputsLen = len(inputs)
    multiplier = 10000
    end = offset + 8
    basePattern = [0, 1, 0, -1]
    inputs *= multiplier
    inputs = inputs[offset:]
    
    for phase in range(100):
        output = []
        index = 0
        for num in inputs:
            pattern = []
            patternIndex = offset
            first = True
            for pat in cycle(basePattern):
                if first == True:
                    first = False
                    continue
                for i in range(index+1):
                    pattern.append(pat)
                    patternIndex += 1
                if patternIndex > inputsLen:
                    break
            newValue = reduce(add, map(mul, inputs, pattern))
            multiplied = newValue * multiplier
            newValueOnes = getOnes(newValue)
            output.append(newValueOnes)
            index += 1
        #print('Phase', phase, output)
        inputs = output
    print('Output', ''.join(map(str, output[0:8])))

file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file)

if part1:
    Part1(lines)

if part2:
    Part2(lines)