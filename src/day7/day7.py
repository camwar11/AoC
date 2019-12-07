import common as com

test = False
part1 = True
part2 = False

def Part1(lines):
    line = lines[0]
    amps = [com.intCode(line, printOutput=False) for i in range(5)]
    maxOutput = 0
    # probably a way better way to do this
    for a in range(5):
        for b in range(5):
            if b == a:
                continue
            for c in range(5):
                if c == a or c == b:
                    continue
                for d in range(5):
                    if d == a or d == b or d == c:
                        continue
                    for e in range(5):
                        if e == a or e == b or e == c or e == d:
                            continue
                        amps[0].setPresetInputs([a, 0])
                        amps[0].RunIntCodeComputer()
                        amps[1].setPresetInputs([b, amps[0].outputValue])
                        amps[1].RunIntCodeComputer()
                        amps[2].setPresetInputs([c, amps[1].outputValue])
                        amps[2].RunIntCodeComputer()
                        amps[3].setPresetInputs([d, amps[2].outputValue])
                        amps[3].RunIntCodeComputer()
                        amps[4].setPresetInputs([e, amps[3].outputValue])
                        amps[4].RunIntCodeComputer()
                        if maxOutput < amps[4].outputValue:
                            maxOutput = amps[4].outputValue
    print(maxOutput)


def Part2(lines):
    pass

file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file)

if part1:
    Part1(lines)

if part2:
    Part2(lines)