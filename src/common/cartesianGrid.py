import math

class Point(object):
    def __init__(self, x, y, data):
        self.x = x
        self.y = y
        self.data = data
    
    def __str__(self):
        return str(self.data)
    
    def setGrid(self, grid):
        self.grid = grid
    
    def ManhattenDistance(self, otherPoint):
        return CartesianGrid.ManhattenDistance(self.x, otherPoint.x, self.y, otherPoint.y)
    
    def AngleBetweenPoints(self, otherPoint):
        return CartesianGrid.Angle(self.x, otherPoint.x, self.y, otherPoint.y)

class CartesianGrid(object):
    def __init__(self):
        self.grid = {}
    
    def addPoint(self, point):
        xAxis = self.grid.get(point.x)
        if xAxis is None:
            self.grid[point.x] = {}
            xAxis = self.grid.get(point.x)
        
        xAxis[point.y] = point
        point.setGrid(self)
    
    def getPoint(self, x, y):
        xAxis = self.grid.get(x)
        if xAxis is not None:
            return xAxis.get(y)
        return None

    def __str__(self):
        minX = None
        maxX = None
        minY = None
        maxY = None
        string = ''
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
        
        for y in range(maxY, minY, -1):
            for x in range(minX, maxX):
                yAxis = self.grid.get(x)
                if yAxis is None:
                    string = string + '.'
                else:
                    value = yAxis.get(y)
                    if value is None:
                        string = string + '.'
                    else:
                        string = string + str(value)
            string = string + '\n'
        return string
    
    @staticmethod
    def ManhattenDistance(x1, x2, y1, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    @staticmethod
    def Angle(x1, x2, y1, y2):
        y = (y2 - y1)
        x = (x2 - x1)
        return math.atan2(y, x)
        