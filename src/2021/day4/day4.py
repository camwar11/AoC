import common as com

test = False
part1 = False
part2 = True
puzzle = com.PuzzleWithTests()

def getScore(board, call, justCalledNum):
    i = 0
    j = 0
    score = 0
    for row in call:
        j = 0
        for col in row:
            if not col:
                score += int(board[i][j])
            j += 1
        i += 1
     
    return score * justCalledNum

def won(board, row, col):
    wins = True
    for i in range(5):
        if not board[i][col]:
            wins = False
            break
        if not wins:
            break
    if wins:
        return True

    for j in range(5):
        if not board[row][j]:
            return False
    return True

def Part1(lines):
    boards = list()
    calledNumbers = list()
    first = True
    board = list()
    marked = list()

    for line in lines:
        if first:
            calledNumbers = line.split(",")
            first = False
            continue
        if line.strip() == "":
            board = list()
            marked = list()
            boards.append([board, marked])
            continue

        boardRow = [x for x in line.strip().split(" ") if x != ""]
        board.append(boardRow)
        markRow = [False, False, False, False, False]
        marked.append(markRow)
    
    for number in calledNumbers:
        for board, call in boards:
            i = 0
            j = 0
            for row in board:
                j = 0
                for col in row:
                    if col == number:
                        call[i][j] = True
                        if(won(call, i, j)):
                            return getScore(board, call, int(number))
                    j += 1
                i += 1
    return None

def Part2(lines):
    boards = list()
    calledNumbers = list()
    first = True
    board = list()
    marked = list()

    for line in lines:
        if first:
            calledNumbers = line.split(",")
            first = False
            continue
        if line.strip() == "":
            board = list()
            marked = list()
            boards.append([board, marked])
            continue

        boardRow = [x for x in line.strip().split(" ") if x != ""]
        board.append(boardRow)
        markRow = [False, False, False, False, False]
        marked.append(markRow)
    
    for number in calledNumbers:
        wonBoards = list()
        boardNum = 0
        for board, call in boards:
            i = 0
            j = 0
            for row in board:
                j = 0
                for col in row:
                    if col == number:
                        call[i][j] = True
                        if(won(call, i, j)):
                            wonBoards.append(boardNum)
                    j += 1
                i += 1
            boardNum += 1
        if len(boards) == 1 and len(wonBoards) == 1:
            return getScore(boards[0][0], boards[0][1], int(number))

        wonBoards.reverse()
        for boardNum in wonBoards:
            boards.pop(boardNum)
        
    return None

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
        print("Part1 test result: " + str(part1Answer))
    else:
        puzzle.answer_a = part1Answer
            

if part2:
    part2Answer = Part2(lines)
    if part2Answer is None:
        print("Returned None for part2")
    elif test:
        print("Part2 test result: " + str(part2Answer))
    else:
        puzzle.answer_b = part2Answer