import common as com
from functools import reduce
from operator import add, mul
from itertools import cycle

test = False
part1 = True
part2 = False

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
    pass

file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file)

if part1:
    Part1(lines)

if part2:
    Part2(lines)