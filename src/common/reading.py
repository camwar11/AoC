def readFile(file, commentMarker = '#'):
    with open(file) as openFile:
        contents = list()
        for line in openFile.readlines():
            if line[0] != commentMarker:
                contents.append(line)
    return contents
    
def parseXYZCoords(line):
    return [int(i.split('=')[1].strip('>\n')) for i in line.split(',')]