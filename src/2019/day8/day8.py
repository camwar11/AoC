import common as com

test = False
part1 = False
part2 = True

def Part1(lines):
    image = []
    correctLayerDigitCounts = [99999999999999 for i in range(10)]
    layerIdx = 0
    width, height = (int(i) for i in lines[0].split('x'))
    for layer in com.divide_chunks(lines[1], width * height):
        image.append([])
        currentLayerDigitCounts = [0 for i in range(10)]
        for pixel in [int(number) for number in layer.strip()]:
            image[layerIdx].append(pixel)
            currentLayerDigitCounts[pixel] += 1
        if currentLayerDigitCounts[0] < correctLayerDigitCounts[0]:
            correctLayerDigitCounts = currentLayerDigitCounts
        layerIdx += 1
    print(str(correctLayerDigitCounts[1] * correctLayerDigitCounts[2]))

def outputForPixel(pixel):
    if pixel == 0:
        return 'X'
    elif pixel == 1:
        return '-'
    elif pixel == 2:
        return ' '


def Part2(lines):
    width, height = (int(i) for i in lines[0].split('x'))
    renderedImage = [2 for i in range(width*height)]
    for layer in com.divide_chunks(lines[1], width * height):
        pixelIdx = 0
        for pixel in [int(number) for number in layer.strip()]:
            currentRenderedPixel = renderedImage[pixelIdx]
            if currentRenderedPixel == 2:
                renderedImage[pixelIdx] = pixel
            pixelIdx += 1
    for imageLine in com.divide_chunks(renderedImage, width):
        renderedLine = [outputForPixel(pixel) for pixel in imageLine]
        print(*renderedLine, sep='')


file = "input.txt"

if test:
    file = "test.txt"

lines = com.readFile(file)

if part1:
    Part1(lines)

if part2:
    Part2(lines)