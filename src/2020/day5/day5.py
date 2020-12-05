import common as com

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def halfRange(letter:str, start: int, end: int):
    upper = letter == 'B' or letter == 'R'
    middle = ((end - start + 1) / 2) + start
    if upper:
        return middle, end 
    else:
        return start, middle - 1
        

def getId(boardingPass: str):
    frontOrBack = boardingPass[:7]
    sides = boardingPass[7:10]
    rowMin = 0
    rowMax = 127
    for row in frontOrBack:
        rowMin, rowMax = halfRange(row, rowMin, rowMax)
    colMin = 0
    colMax = 7
    for col in sides:
        colMin, colMax = halfRange(col, colMin, colMax)
    
    print(str(rowMin) + ', ' + str(colMin))
    return int((rowMin * 8) + colMin)
    

def Part1(lines):
    highestId = 0
    for line in lines:
        iD = getId(line)
        if iD > highestId:
            highestId = iD
    return highestId

def Part2(lines):
    ids = list()
    for line in lines:
        iD = getId(line)
        ids.append(iD)
    prev = 0
    for sortedID in sorted(ids):
        print(sortedID)
        if prev != 0 and (sortedID - prev) > 1:
            return sortedID - 1
        prev = sortedID
    return 0

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