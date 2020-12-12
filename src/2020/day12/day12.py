from math import cos, radians, sin
from operator import mul
from typing import SupportsFloat
import common as com

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

class waterVessel(object):
    def __init__(self):
        self.NORTH = 0
        self.EAST = 90
        self.SOUTH = 180
        self.WEST = 270
        self.heading = self.EAST
    
    def turn(self, degrees:int):
        while degrees < 0:
            degrees += 360
        while degrees >= 360:
            degrees -= 360
        self.heading += degrees
        self.heading %= 360

    def setPoint(self, point):
        self.point = point

    def _performTasksForHeadings(self, north, east, south, west):
        if self.heading == self.NORTH:
            if callable(north):
                return north()
            return north
        elif self.heading == self.EAST:
            if callable(east):
                return east()
            return east
        elif self.heading == self.SOUTH:
            if callable(south):
                return south()
            return south
        elif self.heading == self.WEST:
            if callable(west):
                return west()
            return west

    def moveNorth(self, spaces):
        vector = com.util.vector_math(mul, com.CartesianGrid.UP, [spaces, spaces])
        self.point.move(*vector)

    def moveEast(self, spaces):
        vector = com.util.vector_math(mul, com.CartesianGrid.RIGHT, [spaces, spaces])
        self.point.move(*vector)

    def moveSouth(self, spaces):
        vector = com.util.vector_math(mul, com.CartesianGrid.DOWN, [spaces, spaces])
        self.point.move(*vector)

    def moveWest(self, spaces):
        vector = com.util.vector_math(mul, com.CartesianGrid.LEFT, [spaces, spaces])
        self.point.move(*vector)

    def moveForward(self, spaces: int):
        tasks = (
            lambda: self.moveNorth(spaces),
            lambda: self.moveEast(spaces),
            lambda: self.moveSouth(spaces),
            lambda: self.moveWest(spaces)
        )
        self._performTasksForHeadings(*tasks)

    def moveBackward(self, spaces: int):
        tasks = (
            lambda: self.moveSouth(spaces),
            lambda: self.moveWest(spaces),
            lambda: self.moveNorth(spaces),
            lambda: self.moveEast(spaces)
        )
        self._performTasksForHeadings(*tasks)

    def moveLeft(self, spaces: int):
        tasks = (
            lambda: self.moveWest(spaces),
            lambda: self.moveNorth(spaces),
            lambda: self.moveEast(spaces),
            lambda: self.moveSouth(spaces),
        )
        self._performTasksForHeadings(*tasks)

    def moveRight(self, spaces: int):
        tasks = (
            lambda: self.moveEast(spaces),
            lambda: self.moveSouth(spaces),
            lambda: self.moveWest(spaces),
            lambda: self.moveNorth(spaces),
        )
        self._performTasksForHeadings(*tasks)
    
    def __str__(self):
        return self._performTasksForHeadings('^', '>', 'v', '<')
            

def Part1(lines):
    grid = com.CartesianGrid()
    myShip = waterVessel()
    shipPoint = com.Point(0,0,myShip)
    grid.addPoint(shipPoint)
    myShip.setPoint(shipPoint)
    for line in lines:
        command = line[0]
        units = int(line[1:].strip())
        if command == 'N':
            myShip.moveNorth(units)
        elif command == 'E':
            myShip.moveEast(units)
        elif command == 'S':
            myShip.moveSouth(units)
        elif command == 'W':
            myShip.moveWest(units)
        elif command == 'L':
            # turning left should be the same as moving negative degrees
            myShip.turn(-units)
        elif command == 'R':
            myShip.turn(units)
        elif command == 'F':
            myShip.moveForward(units)
    return shipPoint.ManhattenDistance(com.Point(0,0,None))

def rotateWaypoint(refPoint: com.Point, angleDegs:SupportsFloat, point: com.Point):
    # flip the angle so that it rotates clockwise instead of ccw
    angleDegs *= -1
    sine = sin(radians(angleDegs))
    cosine = cos(radians(angleDegs))

    # translate point back to refPoint
    point.move(-refPoint.x, -refPoint.y)

    # rotate point
    newX = point.x * cosine - point.y * sine
    newY = point.x * sine + point.y * cosine

    # translate point back
    point.moveTo(int(round(newX + refPoint.x)), int(round(newY + refPoint.y)))

def Part2(lines):
    grid = com.CartesianGrid()
    myShip = waterVessel()
    shipPoint = com.Point(0,0,myShip)
    grid.addPoint(shipPoint)
    myShip.setPoint(shipPoint)
    waypoint = waterVessel()
    waypointPoint = com.Point(10,1,waypoint)
    grid.addPoint(waypointPoint)
    waypoint.setPoint(waypointPoint)
    origin = com.Point(0,0, None)
    grid.addPoint(origin)
    for line in lines:
        command = line[0]
        units = int(line[1:].strip())
        if command == 'N':
            waypoint.moveNorth(units)
        elif command == 'E':
            waypoint.moveEast(units)
        elif command == 'S':
            waypoint.moveSouth(units)
        elif command == 'W':
            waypoint.moveWest(units)
        elif command == 'L':
            # turning left should be the same as moving negative degrees
            rotateWaypoint(origin, -units, waypointPoint)
        elif command == 'R':
            rotateWaypoint(origin, units, waypointPoint)
        elif command == 'F':
            print('ship ' + str(shipPoint.x) + ', ' + str(shipPoint.y))
            print('waypoint ' + str(waypointPoint.x) + ', ' + str(waypointPoint.y))
            scaledVector = com.util.vector_math(mul, [waypointPoint.x, waypointPoint.y], [units, units])
            print('scaledVector ' + str(scaledVector[0]) + ', ' + str(scaledVector[1]))
            shipPoint.move(*scaledVector)
            # don't actually need to move the waypoint as it's always relative to the ship
            print('movedShip ' + str(shipPoint.x) + ', ' + str(shipPoint.y))
    return shipPoint.ManhattenDistance(com.Point(0,0,None))

if test:
    lines = com.readFile("test.txt")
else:
    #print(puzzle.input_data)
    #lines = com.readFile("input.txt")
    lines = puzzle.input_data.splitlines()

if part1:
    part1Answer = Part1(lines)
    if part1Answer is None:
        print("Returned None for part1")
    elif test:
        print("Part1 test result: " + str(part1Answer))
    else:
        puzzle.answer_a = part1Answer
            

if part2:
    part2Answer = Part2(lines)
    if part2Answer is None:
        print("Returned None for part2")
    elif test:
        print("Part2 test result: " + str(part2Answer))
    else:
        puzzle.answer_b = part2Answer