def readFile(file, commentMarker = '#'):
    with open(file) as openFile:
        contents = list()
        for line in openFile.readlines():
            if line[0] != commentMarker:
                contents.append(line)
    return contents