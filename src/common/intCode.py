class intCode(object):
    def __init__(self, initialMemory):
        self.initialMemory = [int(i) for i in initialMemory.split(',')]
        self.instructions = {
            1: self.sumIntCode,
            2: self.multiply,
            3: self.input,
            4: self.output,
            99: self.halt
        }
        self.HALTED = -1
        self.IMMEDIATE = 1
        self.POSITION = 0
        self.paramModes = [0, 0, 0, 0]
        self.instructionPointer = 0

    def sumIntCode(self, start_index):
        value = self.resolveParameter(start_index) + self.resolveParameter(start_index+1)
        self.registers[self.registers[start_index+2]] = value
        return 4

    def multiply(self, start_index):
        value = self.resolveParameter(start_index) * self.resolveParameter(start_index+1)
        self.registers[self.registers[start_index+2]] = value
        return 4

    def input(self, start_index):
        self.registers[self.registers[start_index]] = int(input('Enter input: '))
        return 2

    def output(self, start_index):
        print(self.resolveParameter(start_index))
        return 2
    
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

    def RunIntCodeComputer(self, noun, verb, debug):
        self.registers = self.initialMemory.copy()
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