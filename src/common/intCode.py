class intCode(object):
    def __init__(self, initialMemory, printOutput = True, presetInputs = None, needsInputCallback = None, hasOutputCallback = None):
        self.initialMemory = [int(i) for i in initialMemory.split(',')]
        self.initialMemory.extend([0 for i in range(40)])
        self.instructions = {
            1: self.sumIntCode,
            2: self.multiply,
            3: self.input,
            4: self.output,
            5: self.jumpIfTrue,
            6: self.jumpIfFalse,
            7: self.lessThan,
            8: self.equals,
            9: self.adjustRelativeBase,
            99: self.halt
        }
        self.CONTINUING = -3
        self.PAUSED = -2
        self.HALTED = -1
        
        self.POSITION = 0
        self.IMMEDIATE = 1
        self.RELATIVE = 2
        
        self.paramModes = [0, 0, 0, 0]
        self.instructionPointer = 0
        self.presetInputs = presetInputs
        self.printOutput = printOutput
        self.needsInputCallback = needsInputCallback
        self.hasOutputCallback = hasOutputCallback
        self.paused = False
        self.relativeBase = 0

    def sumIntCode(self):
        value = self.resolveParameterValue(0) + self.resolveParameterValue(1)
        self.setMemoryValue(2, value)
        return 4

    def multiply(self):
        value = self.resolveParameterValue(0) * self.resolveParameterValue(1)
        self.setMemoryValue(2, value)
        return 4

    def setPresetInputs(self, values):
        self.presetInputs = values

    def input(self):
        if self.needsInputCallback:
            inputValue = self.needsInputCallback()
        else:
            if self.presetInputs is None:
                inputValue = int(input('Enter input: '))
            else:
                inputValue = self.presetInputs[self.inputIndex]
                self.inputIndex = self.inputIndex + 1

        self.setMemoryValue(0, inputValue)
        return 2

    def output(self):
        self.outputValue = self.resolveParameterValue(0)
        if self.hasOutputCallback:
            self.hasOutputCallback(self.outputValue)
        if self.printOutput:
            print(self.outputValue)
        return 2
    
    def jumpIfTrue(self):
        first = self.resolveParameterValue(0)
        if first != 0:
            self.instructionPointer = self.resolveParameterValue(1)
            return 0
        return 3
    
    def jumpIfFalse(self):
        first = self.resolveParameterValue(0)
        if first == 0:
            self.instructionPointer = self.resolveParameterValue(1)
            return 0
        return 3

    def lessThan(self):
        first = self.resolveParameterValue(0)
        second = self.resolveParameterValue(1)
        value = 0
        if first < second:
            value = 1
        self.setMemoryValue(2, value)
        return 4

    def equals(self):
        first = self.resolveParameterValue(0)
        second = self.resolveParameterValue(1)
        value = 0
        if first == second:
            value = 1
        self.setMemoryValue(2, value)
        return 4
    
    def adjustRelativeBase(self):
        self.relativeBase += self.resolveParameterValue(0)
        return 2

    def setMemoryValue(self, index, value):
        abs_index = self.resolveParameterAbsoluteIndex(index)
        self.checkAndExtendMemory(abs_index)
        self.registers[abs_index] = value

    def checkAndExtendMemory(self, abs_index):
        numRegisters = len(self.registers)
        while abs_index >= numRegisters:
            self.registers.extend([0 for i in range(numRegisters)])
            numRegisters *= 2

    def resolveParameterValue(self, paramIndex):
        index = self.resolveParameterAbsoluteIndex(paramIndex)
        self.checkAndExtendMemory(index)
        return self.registers[index]
        

    def resolveParameterAbsoluteIndex(self, paramIndex):
        mode = self.paramModes[paramIndex]
        paramAbsoluteIndex = self.instructionPointer + paramIndex + 1
        self.checkAndExtendMemory(paramAbsoluteIndex)
        if mode == self.IMMEDIATE:
            return paramAbsoluteIndex
        elif mode == self.POSITION:
            index = paramAbsoluteIndex
        elif mode == self.RELATIVE:
            return self.relativeBase + self.registers[paramAbsoluteIndex]
        else:
            raise Exception("Invalid mode " + str(mode))
        
        self.checkAndExtendMemory(index)
        return self.registers[index]

    def halt(self):
        return self.HALTED

    def RunIntCodeComputer(self, noun = None, verb = None, debug = False, reset = True):
        self.Initialize(noun, verb, debug, reset)
        return self.Run(debug)

    def Initialize(self, noun = None, verb = None, debug = False, reset = True):
        if reset or not self.registers:
            self.registers = self.initialMemory.copy()
        self.inputIndex = 0
        if noun:
            self.registers[1] = noun
        if verb:
            self.registers[2] = verb

        self.instructionPointer = 0
        self.relativeBase = 0

    def pause(self):
        self.paused = True
    def unpause(self):
        self.paused = False
        self.Run()
    
    def Run(self, debug = False):
        self.paused = False
        while not self.paused:
            result = self.RunOneInstruction(debug)
            if result != self.CONTINUING:
                return result
        return self.PAUSED
    
    def RunOneInstruction(self, debug = False):
        rawInstruction = str(self.registers[self.instructionPointer])
        instruction = self.instructions.get(int(rawInstruction[-2:]))
        self.paramModes = [0, 0, 0, 0]
        index = 0
        for i in rawInstruction[-3::-1]:
            self.paramModes[index] = int(i)
            index = index + 1

        if instruction is None:
            raise Exception("invalid instruction " + str(self.registers[self.instructionPointer]))
        result = instruction()
        if result is self.HALTED:
            if debug:
                print(self.registers)
            return self.registers[0]
        self.instructionPointer = self.instructionPointer + result
        return self.CONTINUING