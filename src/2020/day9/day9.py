import common as com
import queue
import itertools
from typing import List

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def is_valid(considerables: List[int], target: int):
	return any(a + b == target for a, b in itertools.combinations(considerables, 2))

def find_rule_breaker(numbers: List[int], preamble_length: int):
	return next(
		number
		for i, number in itertools.islice(enumerate(numbers), preamble_length, None)
		if not is_valid(numbers[i - preamble_length:i], number)
	)


def doit(data, preamble_length: int):
    numbers = list(map(int, data))
    found = find_rule_breaker(numbers, preamble_length)

    for i in range(len(numbers)):
        for j in range(i + 2, len(numbers)):
            considering = numbers[i:j]
            total = sum(considering)
            if total < found:
                continue
            elif total > found:
                break

            return sum(sorted(considering)[::len(considering) - 1])

def Part1(lines, preambleLength):
    slider = queue.Queue(preambleLength)
    for line in lines:
        nextNum = int(line.strip())
        if not slider.full():
            slider.put(nextNum)
            continue
        foundNum = False
        for num1 in list(slider.queue):
            for num2 in list(slider.queue)[1:]:
                if num1 + num2 == nextNum:
                    foundNum = True
                    break
            if foundNum:
                break
        if not foundNum:
            return nextNum
        slider.get_nowait()
        slider.put(nextNum)

    return None

def Part2(lines, preambleLength):
    invalidNum = 127
    counters = list()
    validIndices = list()
    currentIndex = 0
    found = list()
    for line in lines[preambleLength:]:
        validIndices.append(currentIndex)
        currentIndex += 1
        counters.append(list())
        number = int(line.strip())
        for index in list(validIndices):
            counters[index].append(number)
            newSum = sum(counters[index])
            if newSum == invalidNum:
                #found.append(min(counters[index]) + max(counters[index]))
                found.append(index)
                validIndices.remove(index)
            if newSum > invalidNum:
                validIndices.remove(index)

    for idx in found:
        print(counters[idx])
        print(sum(counters[idx]))
    return None

if test:
    lines = com.readFile("test.txt")
else:
    print(puzzle.input_data)
    #lines = com.readFile("input.txt")
    lines = puzzle.input_data.splitlines()

value = doit(lines, 25)

if test:
    preambleLength = 5
else:
    preambleLength = 25
if part1:
    part1Answer = Part1(lines, preambleLength)
    if part1Answer is None:
        print("Returned None for part1")
    elif test:
        print("Part1 test result: " + str(part1Answer))
    else:
        puzzle.answer_a = part1Answer
            

if part2:
    part2Answer = Part2(lines, preambleLength)
    if part2Answer is None:
        print("Returned None for part2")
    elif test:
        print("Part2 test result: " + str(part2Answer))
    else:
        puzzle.answer_b = part2Answer