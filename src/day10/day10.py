import common as com

test = False
part1 = True
part2 = False

class Asteroid(com.Point):
    def __init__(self, x, y):
        com.Point.__init__(self, x, y, {})
    
    def addAsteroidIfInView(self, asteroid):
        if self.x == 4 and self.y == 4:
            test = 4
        slope = self.SlopeBetweenPoints(asteroid)
        if self.x > asteroid.x:
            direction = 1
        elif self.x == asteroid.x:
            direction = 0
        else:
            direction = -1
        distance = self.ManhattenDistance(asteroid)
        if slope == 0:
            if self.x < asteroid.x:
                slope = 0.00000000000000000000000000000000000000001
            else:
                slope = -0.00000000000000000000000000000000000000001
        key = (direction, slope)
        currentAsteroidOnSlope = self.data.get(key)
        if currentAsteroidOnSlope is None or currentAsteroidOnSlope[0] > distance:
            self.data[key] = (distance, asteroid)
            asteroid.data[(direction, -slope)] = (distance, self)

def Part1(lines):
    asteroids = []
    y = 0
    x = 0
    for line in lines:
        for char in line:
            if char == '#':
                asteroid = Asteroid(x, y)
                if x == 0 and y == 2:
                    test = 1
                for oldAsteroid in asteroids:
                    asteroid.addAsteroidIfInView(oldAsteroid)
                asteroids.append(asteroid)
            x += 1
        y += 1
        x = 0
    largest = 0
    bestAsteroid = None
    for asteroid in asteroids:
        asteroidsInView = len(asteroid.data)
        if asteroidsInView > largest:
            largest = asteroidsInView
            bestAsteroid = asteroid
    
    print('Best Asteroid is at ' + str(bestAsteroid.x) + ', ' + str(bestAsteroid.y) + ' with count ' + str(largest))

def Part2(lines):
    pass

file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file, '!')

if part1:
    Part1(lines)

if part2:
    Part2(lines)