from typing import List, Set
import common as com
from common.buoyancyInterchangeTransmissionSystem import BITSPacket

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def total_version_nums(packet: BITSPacket) -> int:
    value = packet.version
    for child in packet.subPackets:
        value += total_version_nums(child)
    return value

def Part1(lines: List[str]):
    total = 0
    for line in lines:
        packet, _ = BITSPacket.parse(line.strip(), True)
        total += total_version_nums(packet)

    return total

def Part2(lines):
    for line in lines:
        packet, _ = BITSPacket.parse(line.strip(), True)

    return packet.decodedData

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