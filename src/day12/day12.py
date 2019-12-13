import common as com
from itertools import combinations
from functools import reduce
import operator
import math

test = False
part1 = False
part2 = True

def readMoons(lines):
    moons = []
    for line in lines:
        values = [int(i.split('=')[1].strip('>\n')) for i in line.split(',')]
        moons.append([values, [0, 0 ,0]])
    return moons

def applyGravity(moons):
    # apply gravity
    for moon1, moon2 in combinations(moons, 2):
        moon1Pos, moon1Vel = moon1
        moon2Pos, moon2Vel = moon2
        for axis in range(3):
            oneChange = 0
            twoChange = 0
            if moon1Pos[axis] > moon2Pos[axis]:
                oneChange = -1
                twoChange = 1
            elif moon1Pos[axis] < moon2Pos[axis]:
                oneChange = 1
                twoChange = -1
            moon1Vel[axis] += oneChange
            moon2Vel[axis] += twoChange

def applyVelocity(moons):
    # apply velocity
    for moon in moons:
        moon[0] = list(map(operator.add, moon[0], moon[1]))
        #print(moon)

def totalEnergy(moons):
    # calc total energy
    total = 0
    for moon in moons:
        potential = reduce(operator.add, [abs(i) for i in moon[0]])
        kinetic = reduce(operator.add, [abs(i) for i in moon[1]])
        subTotal = potential * kinetic
        total += subTotal
    print('total energy=', total)
    return total

def Part1(lines):
    moons = readMoons(lines)
    
    for i in range(1000):
        applyGravity(moons)
        applyVelocity(moons)
    
    totalEnergy(moons)    

def toTuple(moon, axis):
    axisValues = [pos_vel[axis] for pos_vel in moon]
    return tuple(axisValues)

def Part2(lines):
    moons = readMoons(lines)
    
    previousStates = [{} for axis in range(3)]
    foundRepeat = [False for axis in range(3)]

    i = 1
    while True:
        applyGravity(moons)
        applyVelocity(moons)
        moonIdx = 0

        for axis in range(3):
            if 0 == reduce(operator.add, [abs(vel[axis]) for vel in [moon[1] for moon in moons]]):
                foundRepeat[axis] = i
        i += 1
        if reduce(lambda x, y : bool(x) and bool(y), foundRepeat):
            break
    lcm = com.lcm(foundRepeat) 
    print('Took ', lcm, ' iterations or maybe ', lcm * 2) # not sure why I have to multiply by 2 sometimes but it works on the tests
    

file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file)

if part1:
    Part1(lines)

if part2:
    Part2(lines)