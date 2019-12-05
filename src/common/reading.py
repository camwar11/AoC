def readFile(file):
    with open(file) as openFile:
        contents = list()
        for line in openFile.readlines():
            if line[0] != '#':
                contents.append(line)
    return contents