import common as com
from itertools import combinations
from functools import reduce
import operator

test = False
part1 = True
part2 = False

def Part1(lines):
    moons = []
    for line in lines:
        values = [int(i.split('=')[1].strip('>\n')) for i in line.split(',')]
        moons.append([values, [0, 0 ,0]])
    
    for i in range(1000):
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
        
        # apply velocity
        for moon in moons:
            moon[0] = list(map(operator.add, moon[0], moon[1]))
            #print(moon)
    
    # calc total energy
    total = 0
    for moon in moons:
        potential = reduce(operator.add, [abs(i) for i in moon[0]])
        kinetic = reduce(operator.add, [abs(i) for i in moon[1]])
        subTotal = potential * kinetic
        total += subTotal
    print('total energy=', total)

        

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