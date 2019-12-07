class intCode(object):
    def __init__(self, initialMemory, printOutput = True, presetInputs = None):
        self.initialMemory = [int(i) for i in initialMemory.split(',')]
        self.instructions = {
            1: self.sumIntCode,
            2: self.multiply,
            3: self.input,
            4: self.output,
            5: self.jumpIfTrue,
            6: self.jumpIfFalse,
            7: self.lessThan,
            8: self.equals,
            99: self.halt
        }
        self.HALTED = -1
        self.IMMEDIATE = 1
        self.POSITION = 0
        self.paramModes = [0, 0, 0, 0]
        self.instructionPointer = 0
        self.presetInputs = presetInputs
        self.printOutput = printOutput

    def sumIntCode(self, start_index):
        value = self.resolveParameter(start_index) + self.resolveParameter(start_index+1)
        self.registers[self.registers[start_index+2]] = value
        return 4

    def multiply(self, start_index):
        value = self.resolveParameter(start_index) * self.resolveParameter(start_index+1)
        self.registers[self.registers[start_index+2]] = value
        return 4

    def setPresetInputs(self, values):
        self.presetInputs = values

    def input(self, start_index):
        if self.presetInputs is None:
            inputValue = int(input('Enter input: '))
        else:
            inputValue = self.presetInputs[self.inputIndex]
            self.inputIndex = self.inputIndex + 1

        self.registers[self.registers[start_index]] = inputValue
        return 2

    def output(self, start_index):
        self.outputValue = self.resolveParameter(start_index)
        if self.printOutput:
            print(self.outputValue)
        return 2
    
    def jumpIfTrue(self, start_index):
        first = self.resolveParameter(start_index)
        if first != 0:
            self.instructionPointer = self.resolveParameter(start_index+1)
            return 0
        return 3
    
    def jumpIfFalse(self, start_index):
        first = self.resolveParameter(start_index)
        if first == 0:
            self.instructionPointer = self.resolveParameter(start_index+1)
            return 0
        return 3

    def lessThan(self, start_index):
        first = self.resolveParameter(start_index)
        second = self.resolveParameter(start_index + 1)
        value = 0
        if first < second:
            value = 1
        self.registers[self.registers[start_index + 2]] = value
        return 4

    def equals(self, start_index):
        first = self.resolveParameter(start_index)
        second = self.resolveParameter(start_index + 1)
        value = 0
        if first == second:
            value = 1
        self.registers[self.registers[start_index + 2]] = value
        return 4

    def resolveParameter(self, paramIndex):
        offset = paramIndex - self.instructionPointer - 1
        mode = self.paramModes[offset]
        if mode == self.IMMEDIATE:
            return self.registers[paramIndex]
        if mode == self.POSITION:
            return self.registers[self.registers[paramIndex]]
        
        raise Exception("Invalid mode " + str(mode))

    def halt(self, start_index):
        return self.HALTED

    def RunIntCodeComputer(self, noun = None, verb = None, debug = False):
        self.registers = self.initialMemory.copy()
        self.inputIndex = 0
        if noun:
            self.registers[1] = noun
        if verb:
            self.registers[2] = verb

        self.instructionPointer = 0
        while True:
            rawInstruction = str(self.registers[self.instructionPointer])
            instruction = self.instructions.get(int(rawInstruction[-2:]))
            self.paramModes = [0, 0, 0, 0]
            index = 0
            for i in rawInstruction[-3::-1]:
                self.paramModes[index] = int(i)
                index = index + 1

            if instruction is None:
                raise Exception("invalid instruction " + str(self.registers[self.instructionPointer]))
            result = instruction(self.instructionPointer+1)
            if result is self.HALTED:
                if debug:
                    print(self.registers)
                return self.registers[0]
            self.instructionPointer = self.instructionPointer + result