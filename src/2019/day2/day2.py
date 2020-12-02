import common as com

test = False
part1 = False
part2 = True

def Part1(lines):
    noun = None
    verb = None
    if not test:
        noun = 12
        verb = 2
    computer = com.intCode(lines[0])
    print(str(computer.RunIntCodeComputer(noun, verb, True)))
        

def Part2(lines):
    neededResult = 19690720
    computer = com.intCode(lines[0])
    for noun in range(0, 100):
        for verb in range(0, 100):
            result = computer.RunIntCodeComputer(noun, verb, False)
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