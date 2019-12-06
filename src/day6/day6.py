import common as com

test = False
part1 = False
part2 = True

numOrbits = 0
numOfTransfers = 0
santaNode = None
youNode = None

def orbitCounter(node, level):
    global numOrbits
    numOrbits = numOrbits + level

def addToTree(tree, parent, currentNodeKey, createdNodes, allOrbits):
    global santaNode
    global youNode
    currentNode = com.tree_node(currentNodeKey)
    if currentNodeKey == 'SAN':
        santaNode = currentNode
    elif currentNodeKey == 'YOU':
        youNode = currentNode
    createdNodes[currentNodeKey] = currentNode
    tree.addNode(parent, currentNode)
    for childKey in allOrbits.get(currentNodeKey):
        addToTree(tree, currentNode, childKey, createdNodes, allOrbits)

def unorderedAddToTree(tree, lines):
    allOrbits = {}
    possibleRoots = set()
    for line in lines:
        split = line.split(')')
        first = split[0].strip()
        second = split[1].strip()
        firstNode = allOrbits.get(first)
        secondNode = allOrbits.get(second)
        if secondNode is None:
            secondNode = []
            allOrbits[second] = secondNode
        else:
            possibleRoots.remove(second)
        if firstNode is None:
            firstNode = [second]
            allOrbits[first] = firstNode
            possibleRoots.add(first)
        else:
            firstNode.append(second)

    if not bool(possibleRoots):
        print("Bad list")
        return
    root = possibleRoots.pop()
    createdNodes = {}
    addToTree(tree, None, root, createdNodes, allOrbits)

def Part1(lines):
    global numOrbits
    numOrbits = 0
    tree = com.tree()
    unorderedAddToTree(tree, lines)
    tree.breadthFirstTraverse(orbitCounter)
    print('Orbits= ' + str(numOrbits))

def Part2(lines):
    global santaNode
    global youNode
    tree = com.tree()
    unorderedAddToTree(tree, lines)
    # knock off 2 because we don't need to count YOU and SAN
    print('Number of transfers= ' + str(tree.distance(santaNode, youNode) - 2))

file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file)

if part1:
    Part1(lines)

if part2:
    Part2(lines)