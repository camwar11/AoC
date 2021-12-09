import common as com

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def getSegmentsPerNumber():
    uniqueSegmentsPerNumber = dict()
    uniqueSegmentsPerNumber[2] = {1}
    uniqueSegmentsPerNumber[3] = {7}
    uniqueSegmentsPerNumber[4] = {4}
    uniqueSegmentsPerNumber[5] = {2, 3, 5}
    uniqueSegmentsPerNumber[6] = {0, 6, 9}
    uniqueSegmentsPerNumber[7] = {8}
    return uniqueSegmentsPerNumber

def getBasicDigit(signal: str, uniqueSegmentsPerNumber: dict):
    segments = len(signal)
    if segments in uniqueSegmentsPerNumber:
        numbers = uniqueSegmentsPerNumber[segments]
        if len(numbers) == 1:
            return list(numbers)[0]
    return None

def hasCommonSegments(signal, testNumber, segmentPerNumber, numCommonSegments):
    if testNumber in segmentPerNumber:
        testSegment = segmentPerNumber[testNumber]
        if len([x for x in testSegment if x in signal]) == numCommonSegments:
            return True
        return False
    return None

def getDigits(signals: list):
    uniqueSegmentsPerNumber = getSegmentsPerNumber()
    actualNumberPerSegments = dict()
    segmentPerNumber = dict()

    while len(actualNumberPerSegments) < 10:
        for signal in [x for x in signals if not x in actualNumberPerSegments]:
            basic = getBasicDigit(signal, uniqueSegmentsPerNumber)
            if basic != None:
                actualNumberPerSegments[signal] = basic
                segmentPerNumber[basic] = signal
                continue
            if len(signal) == 5:
                foundNumber = None
                if hasCommonSegments(signal, 1, segmentPerNumber, 2):
                    # 3 is the only 5 length digit with both one segments in it
                    foundNumber = 3
                elif hasCommonSegments(signal, 6, segmentPerNumber, 5):
                    # 5 is the only 5 length digit with 5 six segments in it
                    foundNumber = 5
                
                if foundNumber:
                    actualNumberPerSegments[signal] = foundNumber
                    segmentPerNumber[foundNumber] = signal
                    uniqueSegmentsPerNumber[5].remove(foundNumber)
                continue
            if len(signal) == 6:
                foundNumber = None
                isSix = hasCommonSegments(signal, 1, segmentPerNumber, 2)
                if isSix != None and not isSix:
                    # 6 is the only 6 length digit without both one segments in it
                    foundNumber = 6
                elif hasCommonSegments(signal, 3, segmentPerNumber, 5):
                    # 9 is the only 6 length digit with all of 3 in it
                    foundNumber = 9
                
                if foundNumber:
                    actualNumberPerSegments[signal] = foundNumber
                    segmentPerNumber[foundNumber] = signal
                    uniqueSegmentsPerNumber[6].remove(foundNumber)
                continue

    
    return actualNumberPerSegments

def Part1(lines: list):
    count = 0
    for line in lines:
        pattern, output = line.split('|')
        for digit in [x.strip() for x in output.split(' ')]:
            if getBasicDigit(digit, getSegmentsPerNumber()):
                count += 1
    return count

def Part2(lines):        
    count = 0
    for line in lines:
        outputDigits = ''
        pattern, output = line.split('|')
        digits = getDigits([''.join(sorted(x.strip())) for x in pattern.split(' ')])
        for outputVal in [''.join(sorted(x.strip())) for x in output.strip().split(' ')]:
            outputDigits += str(digits[outputVal])
        count += int(outputDigits)

    return count

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
        print("Part1 test result: \n" + str(part1Answer))
    else:
        puzzle.answer_a = part1Answer
            

if part2:
    part2Answer = Part2(lines)
    if part2Answer is None:
        print("Returned None for part2")
    elif test:
        print("Part2 test result: \n" + str(part2Answer))
    else:
        puzzle.answer_b = part2Answer