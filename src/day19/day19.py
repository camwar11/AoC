import common as com

test = False
part1 = False
part2 = True

x = 0
y = 600
maximum = 0
first = True
affected = 0
stop = False

def inputFcn():
    global x, y, first, affected, stop
    if first:
        if x >= 50:
            x = 0
            y += 1
        temp = x
        x += 1
        first = False
        return temp
    else:
        first = True
        if y >= 50:
            print(affected)
            stop = True
        else:
            return y
def outputFcn(value):
    global affected
    if value == 1:
        affected += 1

def Part1(lines):
    global stop, y
    y = 0
    intCode = com.intCode(lines[0], printOutput=False, needsInputCallback=inputFcn, hasOutputCallback=outputFcn)
    while not stop:
        intCode.RunIntCodeComputer()

affectedThenNot = False
wasAffected = False
rows = []
inCommon = []

def numberInCommon(pair1, pair2):
    pair2Length = pair2[1] - pair2[0] + 1
    after = pair2[1] - pair1[1]
    return pair2Length - after

def inputFcn2():
    global x, y, affectedThenNot, first, affected, stop, rows, inCommon, maximum
    if first:
        if affectedThenNot:
            thisMinMax = [rows[-1][0], rows[-1][-1]]
            maximum = thisMinMax[1]
            badIndices = []
            inCommonIdx = 0
            badCount = 0
            for value in inCommon:
                incommonNum = numberInCommon(value, thisMinMax)
                if  incommonNum < 100:
                    badIndices.append(inCommonIdx)
                    badCount += 1
                #print(value, thisMinMax, incommonNum)
                inCommonIdx += 1
            
            badIndices.reverse()
            for bad in badIndices:
                inCommon.pop(bad)
            inCommon.append(thisMinMax)

            if inCommonIdx - badCount + 1 >= 100:
                stop = True
                print(thisMinMax[0] * 10000 + (y - 99), x, y) 


            if bool(rows[-1]):
                x = rows[-1][0] - 5
                if x < 0:
                    x = 0
            else:
                x = 0
            y += 1
            rows.append([])
        temp = x
        x += 1
        first = False
        return temp
    else:
        first = True
        # if bool(rows) and len(rows[-1]) > 100:
        #     start = rows[-1][0]
        #     done = True
        #     for rowIdx in range(-2, -101, -1):
        #         if start < rows[rowIdx][0] or start > rows[rowIdx][-1]:
        #             done = False
        #             break
        #     if done:
        #         print(rows[-1][0] * 1000 + y)  
        #         stop = True
        #         return
        return y
def outputFcn2(value):
    global affected, x, y, affectedThenNot, wasAffected, rows, maximum
    affectedThenNot = False
    if value == 1:
        affected += 1
        if not bool(rows):
            rows.append([])
        rows[-1].append(x-1)
        if wasAffected and x < maximum:
            x = maximum
        wasAffected = True
    else:
        if wasAffected:
            wasAffected = False
            affectedThenNot = True
        else:
            if (not bool(rows) or not bool(rows[-1])) and x > 10000:
                affectedThenNot = True

def Part2(lines):
    global stop
    intCode = com.intCode(lines[0], printOutput=False, needsInputCallback=inputFcn2, hasOutputCallback=outputFcn2)
    while not stop:
        intCode.RunIntCodeComputer()

file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file)

if part1:
    Part1(lines)

if part2:
    Part2(lines)