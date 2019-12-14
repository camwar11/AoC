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