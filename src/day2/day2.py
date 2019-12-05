import common as com

test = False
part1 = False
part2 = True

registers = []

HALTED = -1

def sumIntCode(index):
    value = registers[registers[index]] + registers[registers[index+1]]
    registers[registers[index+2]] = value
    return 4

def multiply(index):
    value = registers[registers[index]] * registers[registers[index+1]]
    registers[registers[index+2]] = value
    return 4

def halt(index):
    return HALTED

instructions = {
    1: sumIntCode,
    2: multiply,
    99: halt
}

def RunIntCodeComputer(line, noun, verb, debug):
    global registers
    registers = [int(i) for i in line.split(',')]
    if noun:
        registers[1] = noun
    if verb:
        registers[2] = verb

    jump = 4
    index = 0
    while True:
        instruction = instructions.get(registers[index])
        if instruction is None:
            raise Exception("invalid instruction " + str(registers[index]))
        result = instruction(index+1)
        if result is HALTED:
            if debug:
                print(registers)
            return registers[0]
        index = index + jump

def Part1(lines):
    noun = None
    verb = None
    if not test:
        noun = 12
        verb = 2
    print(str(RunIntCodeComputer(lines[0], noun, verb, True)))
        

def Part2(lines):
    neededResult = 19690720
    for noun in range(0, 100):
        for verb in range(0, 100):
            result = RunIntCodeComputer(lines[0], noun, verb, False)
            if result == neededResult:
                print(str(100 * noun + verb))
                return
    print("No answer")

file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file)

if part1:
    Part1(lines)

if part2:
    Part2(lines)