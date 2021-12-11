import math
from functools import reduce

def lcm(numbers):
    return reduce(lambda x, y: (x*y)/math.gcd(x,y), numbers, 1)

def median(numbers: list, sort = False):
    sortedNumbers = numbers
    if sort:
        sortedNumbers = sorted(numbers)

    length = len(sortedNumbers)
    if length % 2 == 0:
        value1 = sortedNumbers[int(length / 2) - 1]
        value2 = sortedNumbers[int(length / 2)]
    else:
        value1 = sortedNumbers[int(math.ceil(length / 2) - 1)]
        value2 = value1
    return (value1 + value2)/2

def sumSeries(n: int):
    return (n * (n + 1)) / 2
        