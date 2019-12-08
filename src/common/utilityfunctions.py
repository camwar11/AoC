def divide_chunks(list, length): 
    # looping till length l 
    for i in range(0, len(list), length):  
        yield list[i:i + length] 