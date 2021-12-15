def divide_chunks(list, length): 
    # looping till length l 
    for i in range(0, len(list), length):  
        yield list[i:i + length]

def binary_search(low, high, closureToRun, targetValueIsHigher, targetValueIsLower):
    while(low < high):
        currentTest = (low + high) // 2
        result = closureToRun(currentTest)
        if targetValueIsHigher(result):
            low = currentTest + 1
        elif targetValueIsLower(result):
            high = currentTest - 1
    return low

def vector_math(operator, first, second):
    result = []
    firstLen = len(first)
    secondLen = len(second)
    maxLen = max(firstLen, secondLen)
    for index in range(maxLen):
        if index >= firstLen:
            result.append(second[index])
        elif index >= secondLen:
            result.append(first[index])
        else:
            result.append(operator(first[index], second[index])) 
    return result

def increment_dict(dictionary: dict, key, increment: int):
    count = 0
    if key in dictionary:
        count = dictionary[key]
    count += increment
    dictionary[key] = count