import math
from functools import reduce

def lcm(numbers):
    return reduce(lambda x, y: (x*y)/math.gcd(x,y), numbers, 1)