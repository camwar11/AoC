import common as com
import math

test = False
part1 = False
part2 = True

class Asteroid(com.Point):
    def __init__(self, x, y):
        com.Point.__init__(self, x, y, {})
    
    def addAsteroidIfInView(self, asteroid):
        angle = self.AngleBetweenPoints(asteroid)
        distance = self.ManhattenDistance(asteroid)
        currentAsteroidOnAngle = self.data.get(angle)
        if currentAsteroidOnAngle is None:
            self.data[angle] = [(distance, asteroid)]
        else:
            self.data[angle].append((distance, asteroid))

        backwardsAngle = asteroid.AngleBetweenPoints(self)
        otherAsteroidsData = asteroid.data.get(backwardsAngle)
        if otherAsteroidsData is None:
            asteroid.data[backwardsAngle] = [(distance, self)]
        else:
            asteroid.data[backwardsAngle].append((distance, self))


def Part1(lines):
    asteroids = []
    y = 0
    x = 0
    for line in lines:
        for char in line:
            if char == '#':
                asteroid = Asteroid(x, y)
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
    return bestAsteroid
    
def byFirstItem(value):
    return value[0]

def Part2(lines):
    bestAsteroid = Part1(lines)
    sortedRadians = sorted(bestAsteroid.data.keys())
    count = 0
    firstTime = True
    twoHundredthAsteroid = None
    while twoHundredthAsteroid is None:
        for radian in sortedRadians:
            if firstTime:
                bestAsteroid.data[radian] = sorted(bestAsteroid.data[radian], reverse = True, key = byFirstItem)
                if radian < -math.pi / 2:
                    continue
            asteroidsAtAngle = bestAsteroid.data.get(radian)
            if asteroidsAtAngle is None or bool(asteroidsAtAngle) == False:
                continue
            lastBlastedAsteroid = asteroidsAtAngle.pop()
            if lastBlastedAsteroid[1].x == 12 and lastBlastedAsteroid[1].y == 13:
                test = 5
            print('Blasting asteroid at', lastBlastedAsteroid[1].x, ',', lastBlastedAsteroid[1].y)
            count += 1
            if count == 200:
                twoHundredthAsteroid = lastBlastedAsteroid[1]
                break
        firstTime = False
    print('200th asteroid is at ', twoHundredthAsteroid.x, ', ', twoHundredthAsteroid.y, ' = ', twoHundredthAsteroid.x * 100 + twoHundredthAsteroid.y)


file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file, '!')

if part1:
    Part1(lines)

if part2:
    Part2(lines)