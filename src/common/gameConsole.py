class gameConsole(object):
    def __init__(self):
        self.instructions = {
            'acc': self.acc,
            'jmp': self.jmp,
            'nop': self.nop,
        }
        self._resetCounters()

    def _resetCounters(self):
        self._accumulator = 0
        self._instruction = 0
    
    def acc(self, param: int):
        self._accumulator += param
        self._instruction += 1

    def jmp(self, param: int):
        self._instruction += param

    def nop(self, param: int):
        self._instruction += 1

    def runProgram(self, lines):
        self._program = lines
        programLineCount = lines.__len__()
        self._resetCounters()
        
        ranInstructions = set()
        haltedNormally = False
        while self._instruction not in ranInstructions and not haltedNormally:
            ranInstructions.add(self._instruction)
            instruction, param = self._program[self._instruction].split(' ')
            self.instructions[instruction](int(param))
            if self._instruction >= programLineCount:
                haltedNormally = True
        return self._accumulator, haltedNormally