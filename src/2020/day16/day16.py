from typing import Set
import common as com

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def readTicket(line:str):
    ticket = list()
    for field in line.split(','):
        number = int(field)
        ticket.append(number)
    return ticket

def Part1(lines):
    rules = dict()
    section = 0
    myTicket = None
    tickets = list()
    for line in lines:
        if line.strip() == '':
            continue
        if 'your ticket' in line:
            section += 1
            continue
        elif 'nearby tickets' in line:
            section += 1
            continue
        elif section == 0:
            field, numbers = line.split(':')
            range1, range2 = numbers.split('or')
            range1Bot, range1Top = range1.split('-')
            range2Bot, range2Top = range2.split('-')
            rules[field] = ((int(range1Bot), int(range1Top)), (int(range2Bot), int(range2Top)))
            continue
        elif section == 1:
            myTicket = readTicket(line)
        elif section == 2:
            tickets.append(readTicket(line))

    rate = 0

    for ticket in tickets:
        for field in ticket:
            passedRule = False
            for rule in rules:
                for set in rules[rule]:
                    if set[0] <= field <= set[1]:
                        passedRule = True
                        break
                if passedRule:
                    break
            if not passedRule:
                    rate += field

    return rate

def Part2(lines):
    rules = dict()
    section = 0
    myTicket = None
    tickets = list()
    for line in lines:
        if line.strip() == '':
            continue
        if 'your ticket' in line:
            section += 1
            continue
        elif 'nearby tickets' in line:
            section += 1
            continue
        elif section == 0:
            field, numbers = line.split(':')
            range1, range2 = numbers.split('or')
            range1Bot, range1Top = range1.split('-')
            range2Bot, range2Top = range2.split('-')
            rules[field] = ((int(range1Bot), int(range1Top)), (int(range2Bot), int(range2Top)))
            continue
        elif section == 1:
            myTicket = readTicket(line)
        elif section == 2:
            tickets.append(readTicket(line))


    goodTickets = list()
    for ticket in tickets:
        ticketIsGood = True
        for field in ticket:
            passedRule = False
            for rule in rules:
                for ruleSet in rules[rule]:
                    if ruleSet[0] <= field <= ruleSet[1]:
                        passedRule = True
                        break
                if passedRule:
                    break
            if not passedRule:
                ticketIsGood = False
        if ticketIsGood:
            goodTickets.append(ticket)

    ruleToFieldsIdx = dict()
    for rule in rules:
        goodFields = set()
        for field in range(len(tickets[0])):
            goodFields.add(field)

        for ticket in goodTickets:
            idx = 0
            for field in ticket:
                if idx not in goodFields:
                    idx += 1
                    continue
                isGood = False
                for ruleSet in rules[rule]:
                    if ruleSet[0] <= field <= ruleSet[1]:
                        isGood = True
                if not isGood:
                    goodFields.remove(idx)
                idx += 1
        ruleToFieldsIdx[rule] = goodFields

    ruleToFieldIdx = dict()

    idxToRemove = -1
    while True:
        for rule in ruleToFieldsIdx:
            if idxToRemove == -1:
                length = len(ruleToFieldsIdx[rule])
                if length == 1:
                    idxToRemove = ruleToFieldsIdx[rule].pop()
                    ruleToFieldIdx[rule] = idxToRemove
                    break
            else:
                ruleToFieldsIdx[rule].remove(idxToRemove)
        if idxToRemove == -1:
            break
        idxToRemove = -1

    count = 1
    for rule in ruleToFieldIdx:
        if rule.startswith('departure'):
            count *= myTicket[ruleToFieldIdx[rule]]


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