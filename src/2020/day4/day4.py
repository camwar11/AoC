import common as com

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def validateByr(value: str):
    year = int(value)
    if 1920 <= year <= 2002:
        return True
    return False

def validateIyr(value: str):
    year = int(value)
    if 2010 <= year <= 2020:
        return True
    return False

def validateEyr(value: str):
    year = int(value)
    if 2020 <= year <= 2030:
        return True
    return False

def validateHgt(value: str):
    cm = True
    if value.endswith('in'):
        cm = False
    elif not value.endswith('cm'):
        return False
    height = int(value[:-2])
    if cm and (150 <= height <= 193):
        return True
    elif (not cm) and (59 <= height <= 76):
        return True        
    return False

def validateHcl(value: str):
    if not value.startswith('#'):
        return False
    if value.__len__() != 7:
        return False
    for char in value[1:]:
        if (not char.isdigit()) and char != 'a' and char != 'b' and char != 'c' and char != 'd' and char != 'e' and char != 'f':
            return False
    return True

def validateEcl(value: str):
    count = 0
    for color in 'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth':
        if value.find(color) >= 0:
            count += 1
    return count == 1

def validatePid(value: str):
    if value.__len__() != 9 or not value.isnumeric():
        return False
    return True

def isValidPassport(passport, part1 = True):
    req = dict()
    req['byr:'] = validateByr
    req['iyr:'] = validateIyr
    req['eyr:'] = validateEyr
    req['hgt:'] = validateHgt
    req['hcl:'] = validateHcl
    req['ecl:'] = validateEcl
    req['pid:'] = validatePid
    valid = True

    for field in req:
        index = passport.find(field)
        if index < 0:
            return False
        elif part1 is False:
            endIndex = passport.find(' ', index)
            value = passport[index + field.__len__() : endIndex]
            if(req[field](value) == False):
                return False


    return True
    


def Part1(lines):
    passport = ''
    validPassports = 0
    for line in lines:
        if line.strip() == '':
            if isValidPassport(passport):
                validPassports +=1
            passport = ''
        else:
            passport += line
    if isValidPassport(passport):
            validPassports +=1
    return validPassports

def Part2(lines):
    passport = ''
    validPassports = 0
    for line in lines:
        if line.strip() == '':
            if isValidPassport(passport, False):
                validPassports +=1
            passport = ''
        else:
            passport += line + ' '
    if isValidPassport(passport, False):
            validPassports +=1
    return validPassports

if test:
    lines = com.readFile("test.txt")
else:
    print(puzzle.input_data)
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