#!/usr/bin/env python3

def display(data):
    result = []
    for i in range(0, len(data)-1, 40):
        result.append(data[i:i+40])
    return result

if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as f:
        for x in display(f.read()):
            print(x)
