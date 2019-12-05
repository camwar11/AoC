class intCode(object):
    def __init__(self, initialMemory):
        self.initialMemory = [int(i) for i in initialMemory.split(',')]
        self.instructions = {
            1: self.sumIntCode,
            2: self.multiply,
            99: self.halt
        }
        self.HALTED = -1

    def sumIntCode(self, start_index):
        value = self.registers[self.registers[start_index]] + self.registers[self.registers[start_index+1]]
        self.registers[self.registers[start_index+2]] = value
        return 4

    def multiply(self, start_index):
        value = self.registers[self.registers[start_index]] * self.registers[self.registers[start_index+1]]
        self.registers[self.registers[start_index+2]] = value
        return 4

    def halt(self, start_index):
        return self.HALTED

    def RunIntCodeComputer(self, noun, verb, debug):
        self.registers = self.initialMemory.copy()
        if noun:
            self.registers[1] = noun
        if verb:
            self.registers[2] = verb

        jump = 4
        index = 0
        while True:
            instruction = self.instructions.get(self.registers[index])
            if instruction is None:
                raise Exception("invalid instruction " + str(self.registers[index]))
            result = instruction(index+1)
            if result is self.HALTED:
                if debug:
                    print(self.registers)
                return self.registers[0]
            index = index + jump