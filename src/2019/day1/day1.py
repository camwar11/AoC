import common as com
import math

def Part1(lines):
    print(sum([neededFuelAmount(int(i)) for i in lines]))

def Part2(lines):
    print(sum([neededFuelAmountIncludingFuel(int(i)) for i in lines]))

def neededFuelAmount(moduleMass):
    return math.floor(moduleMass / 3) - 2

def neededFuelAmountIncludingFuel(mass):
    if mass is 0:
        return 0

    fuel = max(0, neededFuelAmount(mass))
    return fuel + neededFuelAmountIncludingFuel(fuel)

test = False
part1 = False
part2 = True

file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file)

if part1:
    Part1(lines)

if part2:
    Part2(lines)