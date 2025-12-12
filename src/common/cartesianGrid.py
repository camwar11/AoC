import math
from operator import add, sub
from typing import Callable, List
import common.utilityfunctions as util

class Point(object):
    def __init__(self, x, y, data):
        self.x = x
        self.y = y
        self.data = data
        self.grid: CartesianGrid | None = None
    
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
    
    def setGrid(self, grid: 'CartesianGrid'):
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

    def getAdjacentPoints(self, includeDiagonals = False, includeMissing = False, includeDirection = False, createIfOverBounds = False):
        return self.grid.getAdjacentPoints(self.x, self.y, includeDiagonals, includeMissing, includeDirection, createIfOverBounds)
    
    def getAdjacentPoint(self, direction, includeMissing = False, createIfOverBounds = False):
        newX, newY = self + direction
        newPoint = self.grid.getPoint(newX, newY)
        if newPoint:
            return newPoint
        elif includeMissing and (createIfOverBounds or self.grid.isInBounds(newX, newY)):
            newPoint = Point(newX, newY, None)
            self.grid.addPoint(newPoint)
        return newPoint
    
    def is_in_polygon(self, edge_finder: Callable[['Point'], bool], vertex_finder: Callable[['Point'], bool]):
        # Ray-casting algorithm to determine if point is in a polygon
        # Could be optimized by picking the closeset edge, but this is fine for now
        minX, maxX, minY, maxY = self.grid.getBounds()
        idx = 0

        # Bail if we know we're already on an edge or vertex
        if vertex_finder(self) or edge_finder(self):
            return True
        
        directions = CartesianGrid.CardinalDirections()
        prev_direction = directions[-1]
        for direction in directions:
            coord = (self.x, self.y)
            # Count the number of times we cross an edge
            crossings = 0
            while minX <= coord[0] <= maxX and minY <= coord[1] <= maxY:
                # Need to test a point and a perpendicular point so get rid of riding
                # on any line / vertex
                test_point = self.grid.getPoint(coord[0], coord[1])
                perp_point = self.grid.getPoint(coord[0] + prev_direction[0], coord[1] + prev_direction[1])
                if test_point is None or perp_point is None:
                    coord = (coord[0] + direction[0], coord[1] + direction[1])
                    continue
                
                if (vertex_finder(test_point) or edge_finder(test_point)) and (vertex_finder(perp_point) or edge_finder(perp_point)):
                    crossings += 1
                coord = (coord[0] + direction[0], coord[1] + direction[1])
            
            if crossings % 2 == 1:
                return True
            idx += 1
        
        return False

def defaultCellOutputStr(cell):
    if cell.data is None:
        return str(cell.grid.emptyCellOutput)
    else:
        return str(cell)

class CartesianGrid(object):
    UP = (0, 1)
    RIGHT = (1, 0)
    DOWN = (0, -1)
    LEFT = (-1, 0)

    UP_LEFT = (-1, 1)
    UP_RIGHT = (1, 1)
    DOWN_LEFT = (-1, -1)
    DOWN_RIGHT = (1, -1)

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

    def __init__(self, emptyCellOutput = '.', cellOutputStrFcn:Callable[[Point], str] = defaultCellOutputStr, flipOutput = False):
        self.grid: dict[int, dict[int, Point]] = {}
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
            xAxis = {}
            self.grid[point.x] = xAxis
        
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
        return point
    
    def movePointTo(self, point, newX, newY):
        xAxis = self.grid.get(point.x)
        del xAxis[point.y]
        if len(self.grid.get(point.x)) == 0:
            del self.grid[point.x]
        point.x = newX
        point.y = newY
        self.addPoint(point)
        return point
    
    def movePointViaCoords(self, oldX, oldY, xDiff, yDiff):
        self.movePoint(self.getPoint(oldX, oldY), xDiff, yDiff)
    
    def getPoint(self, x, y) -> Point | None:
        xAxis = self.grid.get(x)
        if xAxis is not None:
            return xAxis.get(y)
        return None
    
    def isInBounds(self, x, y):
        minX, maxX, minY, maxY = self.getBounds()
        return minX <= x <= maxX and minY <= y <= maxY

    def getAdjacentPoints(self, x, y, includeDiagonals = False, includeMissing = False, includeDirection = False, createIfOverBounds = False) -> List[Point] | List[tuple[Point, tuple[int, int]]]:
        points = list()
        point = self.getPoint(x, y)
        if not point:
            if includeMissing and (createIfOverBounds or self.isInBounds(x, y)):
                point = Point(x, y, None)
                self.addPoint(point)
            else:
                return points

        if includeDiagonals:
            directions = CartesianGrid.AllDirections()
        else:
            directions = CartesianGrid.CardinalDirections()

        for direction in directions:
            newPoint = point.getAdjacentPoint(direction, includeMissing, createIfOverBounds)
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

    def getBounds(self) -> tuple[int, int, int, int]:
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
    def CardinalDirections() -> list[tuple[int, int]]:
        return [CartesianGrid.UP, CartesianGrid.RIGHT, CartesianGrid.DOWN, CartesianGrid.LEFT]
    
    @staticmethod
    def DiagonalDirections() -> list[tuple[int, int]]:
        return [CartesianGrid.UP_LEFT, CartesianGrid.UP_RIGHT, CartesianGrid.DOWN_LEFT, CartesianGrid.DOWN_RIGHT]

    @staticmethod
    def AllDirections() -> list[tuple[int, int]]:
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
def parse_raw_to_grid(raw_input: str, conversionFcn = None, flip = True) -> CartesianGrid:
    lines = raw_input.splitlines()
    grid = CartesianGrid()
    if flip:
        lines.reverse()
    parse_to_grid(lines, grid, conversionFcn, flip)
    return grid

def compress_points(data: list[tuple[int, int]]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    xs: set[int] = set()
    ys: set[int] = set()
    for point in data:
        xs.add(point[0])
        ys.add(point[1])
    x_sorted = sorted(xs)
    y_sorted = sorted(ys)
    new_points: list[tuple[tuple[int, int], tuple[int, int]]] = []

    for point in data:
        new_x = x_sorted.index(point[0])
        new_y = y_sorted.index(point[1])
        new_points.append(((new_x, new_y), (point[0], point[1])))

    return new_points