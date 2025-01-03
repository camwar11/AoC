import math
from operator import add, sub
from typing import List
import common.utilityfunctions as util

class Point(object):
    def __init__(self, x, y, data):
        self.x = x
        self.y = y
        self.data = data
    
    def __str__(self):
        return str(self.data)
    
    def __add__(self, other):
        if isinstance(other, Point):
            other = [other.x, other.y]
        return util.vector_math(add, [self.x, self.y], other)

    def __sub__(self, other):
        if isinstance(other, Point):
            other = [other.x, other.y]
        return util.vector_math(sub, [self.x, self.y], other)

    def key(self):
        return (self.x, self.y)
    
    def setGrid(self, grid):
        self.grid = grid
    
    def ManhattenDistance(self, otherPoint):
        return CartesianGrid.ManhattenDistance(self.x, otherPoint.x, self.y, otherPoint.y)
    
    def AngleBetweenPoints(self, otherPoint):
        return CartesianGrid.Angle(self.x, otherPoint.x, self.y, otherPoint.y)

    def move(self, xDiff, yDiff):
        if self.grid is None:
            raise AttributeError("point is not part of a grid")
        self.grid.movePoint(self, xDiff, yDiff)
    
    def moveTo(self, newX, newY):
        if self.grid is None:
            raise AttributeError("point is not part of a grid")
        self.grid.movePointTo(self, newX, newY)

    def getAdjacentPoints(self, includeDiagonals = False, includeMissing = False, includeDirection = False):
        return self.grid.getAdjacentPoints(self.x, self.y, includeDiagonals, includeMissing, includeDirection)
    
    def getAdjacentPoint(self, direction, includeMissing = False):
        newX, newY = self + direction
        newPoint = self.grid.getPoint(newX, newY)
        if newPoint:
            return newPoint
        elif includeMissing:
            newPoint = Point(newX, newY, None)
            newPoint.setGrid(self.grid)
        return newPoint


def defaultCellOutputStr(cell):
        return str(cell)

class CartesianGrid(object):
    UP = [0, 1]
    RIGHT = [1, 0]
    DOWN = [0, -1]
    LEFT = [-1, 0]

    UP_LEFT = [-1, 1]
    UP_RIGHT = [1, 1]
    DOWN_LEFT = [-1, -1]
    DOWN_RIGHT = [1, -1]

    directions = {
        '^': UP,
        '>': RIGHT,
        'v': DOWN,
        '<': LEFT
    }

    turn_clock = {
        '^': '>',
        '>': 'v',
        'v': '<',
        '<': '^'
    }
    turn_counterclock = {
        '^': '<',
        '>': '^',
        'v': '>',
        '<': 'v'
    }
    turn_180 = {
        '^': 'v',
        '>': '<',
        'v': '^',
        '<': '>'
    }

    def __init__(self, emptyCellOutput = '.', cellOutputStrFcn = defaultCellOutputStr, flipOutput = False):
        self.grid = {}
        self.emptyCellOutput = emptyCellOutput
        self.cellOutputStrFcn = cellOutputStrFcn
        self.flipOutput = flipOutput

    def copy(self):
        new = CartesianGrid(self.emptyCellOutput, self.cellOutputStrFcn, self.flipOutput)
        for point in self.getAllPoints():
            new.addPoint(Point(point.x, point.y, point.data))
        return new
    
    def addPoint(self, point):
        xAxis = self.grid.get(point.x)
        if xAxis is None:
            self.grid[point.x] = {}
            xAxis = self.grid.get(point.x)
        
        xAxis[point.y] = point
        point.setGrid(self)
        return point
    
    def removePoint(self, point):
        xAxis = self.grid.get(point.x)
        if point.y in xAxis:
            del xAxis[point.y]
        if len(self.grid.get(point.x)) == 0:
            del self.grid[point.x]

    def movePoint(self, point, xDiff, yDiff):
        xAxis = self.grid.get(point.x)
        del xAxis[point.y]
        if len(self.grid.get(point.x)) == 0:
            del self.grid[point.x]
        point.x += xDiff
        point.y += yDiff
        self.addPoint(point)
    
    def movePointTo(self, point, newX, newY):
        xAxis = self.grid.get(point.x)
        del xAxis[point.y]
        if len(self.grid.get(point.x)) == 0:
            del self.grid[point.x]
        point.x = newX
        point.y = newY
        self.addPoint(point)
    
    def movePointViaCoords(self, oldX, oldY, xDiff, yDiff):
        self.movePoint(self.getPoint(oldX, oldY), xDiff, yDiff)
    
    def getPoint(self, x, y):
        xAxis = self.grid.get(x)
        if xAxis is not None:
            return xAxis.get(y)
        return None

    def getAdjacentPoints(self, x, y, includeDiagonals = False, includeMissing = False, includeDirection = False):
        points = list()
        point = self.getPoint(x, y)
        if not point:
            return points

        if includeDiagonals:
            directions = CartesianGrid.AllDirections()
        else:
            directions = CartesianGrid.CardinalDirections()

        for direction in directions:
            newPoint = point.getAdjacentPoint(direction, includeMissing)
            if newPoint:
                if includeDirection:
                    points.append((newPoint, direction))
                else:
                    points.append(newPoint)
        return points
    
    def getAllPoints(self, lowYFirst = False) -> List[Point]:
        minX = None
        maxX = None
        minY = None
        maxY = None
        allPoints = []
        for x in self.grid.keys():
            if minX is None or x < minX:
                minX = x
            if maxX is None or x > maxX:
                maxX = x
            for y in self.grid[x].keys():
                if minY is None or y < minY:
                    minY = y
                if maxY is None or y > maxY:
                    maxY = y
        
        yRange = range(maxY, minY -1, -1)
        if lowYFirst:
            yRange = range(minY, maxY + 1)

        for y in yRange:
            for x in range(minX, maxX + 1):
                yAxis = self.grid.get(x)
                if yAxis is not None:
                    value = yAxis.get(y)
                    if value is not None:
                        allPoints.append(value)
        return allPoints

    def getBounds(self) -> (int, int, int, int):
        minX = None
        maxX = None
        minY = None
        maxY = None
        for x in self.grid.keys():
            if minX is None or x < minX:
                minX = x
            if maxX is None or x > maxX:
                maxX = x
            for y in self.grid[x].keys():
                if minY is None or y < minY:
                    minY = y
                if maxY is None or y > maxY:
                    maxY = y
        return minX, maxX, minY, maxY

    def __str__(self):
        string = ''
        minX, maxX, minY, maxY = self.getBounds()
        yRange = range(maxY, minY - 1, -1)
        if self.flipOutput:
            yRange = range(minY, maxY + 1, 1)
        for y in yRange:
            for x in range(minX, maxX + 1):
                yAxis = self.grid.get(x)
                if yAxis is None:
                    string = string + self.emptyCellOutput
                else:
                    value = yAxis.get(y)
                    if value is None:
                        string = string + self.emptyCellOutput
                    else:
                        string = string + self.cellOutputStrFcn(value)
            string = string + '\n'
        return string
    
    def moveAllPoints(self, xDiff: int, yDiff: int):
        for point in self.getAllPoints():
            self.movePoint(point, xDiff, yDiff)
    
    @staticmethod
    def ManhattenDistance(x1, x2, y1, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    @staticmethod
    def Angle(x1, x2, y1, y2):
        y = (y2 - y1)
        x = (x2 - x1)
        return math.atan2(y, x)

    @staticmethod
    def CardinalDirections() -> list:
        return [CartesianGrid.UP, CartesianGrid.RIGHT, CartesianGrid.DOWN, CartesianGrid.LEFT]
    
    @staticmethod
    def DiagonalDirections() -> list:
        return [CartesianGrid.UP_LEFT, CartesianGrid.UP_RIGHT, CartesianGrid.DOWN_LEFT, CartesianGrid.DOWN_RIGHT]

    @staticmethod
    def AllDirections() -> list:
        return [CartesianGrid.UP_LEFT, CartesianGrid.UP, CartesianGrid.UP_RIGHT, CartesianGrid.LEFT, CartesianGrid.RIGHT, CartesianGrid.DOWN_LEFT, CartesianGrid.DOWN, CartesianGrid.DOWN_RIGHT]

def parse_to_grid(lines: List[str], grid: CartesianGrid, conversionFcn = None, flip = False):
    y = 0
    for line in lines:
        x = 0
        line = line.strip()
        for char in line:
            if conversionFcn:
                point = Point(x, y, conversionFcn(char))
            else:
                point = Point(x, y, char)
            grid.addPoint(point)
            x += 1
        y += 1
def parse_raw_to_grid(raw_input: str, conversionFcn = None, flip = True):
    lines = raw_input.splitlines()
    grid = CartesianGrid()
    if flip:
        lines.reverse()
    parse_to_grid(lines, grid, conversionFcn, flip)
    return grid